import chromadb
from embedding_client import generate_embedding
from llm_client import generate_llm_response

# Initialize ChromaDB Persistent Client
chroma_client = chromadb.PersistentClient(path="/app/chroma_data")  # Persistent storage at /app/chroma_data

# Check if the collection exists and create/load as needed
collection_name = "documents"
collections = chroma_client.list_collections()  # Now returns a list of collection names directly
if collection_name not in collections:
    # Collection does not exist, create it
    collection = chroma_client.create_collection(name=collection_name)
else:
    # Collection exists, load it
    collection = chroma_client.get_collection(name=collection_name)


def add_document(doc_id, content, metadata=None):
    """
    Adds a new document and its embedding to the vector database.

    Args:
        doc_id (str): The unique identifier for the document.
        content (str): The textual content of the document.
        metadata (dict, optional): Metadata about the document (e.g., source file, chunk index).
    """
    metadata = metadata or {}

    # Generate embedding for the document content
    embedding = generate_embedding(content)

    # Add the document, metadata, and embedding to the collection
    collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[doc_id],
        embeddings=[embedding]
    )


def search_documents(query, top_k=5, summarize=False, distance_threshold=150.0):
    """
    Queries the vector database for the most relevant document chunks.

    Args:
        query (str): The user's query.
        top_k (int): The number of most relevant results to retrieve.
        summarize (bool): Whether to summarize the combined chunks using the LLM.
        distance_threshold (float): Maximum acceptable distance for relevance (e.g., ≤150.0).

    Returns:
        dict: A dictionary containing results with documents, distances, metadata, and optionally a summary.
    """
    # Generate embedding for the query
    query_embedding = generate_embedding(query)

    # Query ChromaDB for top-k results
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    # Extract results
    documents = results.get('documents', [[]])[0]
    distances = results.get('distances', [[]])[0]
    metadata = results.get('metadatas', [[]])[0]

    # Filter results based on distance threshold
    filtered_results = [
        (doc, dist, meta)
        for doc, dist, meta in zip(documents, distances, metadata)
        if dist <= distance_threshold
    ]
    if not filtered_results:
        return {
            "combined_response": "",
            "documents": [],
            "distances": [],
            "metadata": [],
            "summary": None
        }

    # Separate filtered results back into documents, distances, and metadata
    documents, distances, metadata = zip(*filtered_results)

    # Combine the retrieved document chunks into a single response
    combined_response = "\n".join(documents)

    # Optionally summarize the combined response using an LLM
    if summarize:
        prompt = f"""
        The following text is an excerpt from multiple documents related to the query:
        '{query}'
        Please summarize this information in a concise and user-friendly way:
        {combined_response}
        """
        summary = generate_llm_response(prompt)
        return {"summary": summary, "documents": documents, "distances": distances, "metadata": metadata}

    # Return the combined response along with metadata
    return {
        "combined_response": combined_response,
        "documents": documents,
        "distances": distances,
        "metadata": metadata
    }


def delete_document(doc_id):
    """
    Deletes a document from the vector database.

    Args:
        doc_id (str): The unique identifier of the document.
    """
    collection.delete(ids=[doc_id])
