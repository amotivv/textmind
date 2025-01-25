from flask import Flask, request
from query_processor import process_query
from database_manager import add_document, search_documents, delete_document
import requests
from config import TELNYX_API_KEY, TELNYX_FROM, TELNYX_PROFILE_ID
import os
import datetime

app = Flask(__name__)

# Telnyx webhook for SMS processing
@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook to handle incoming SMS messages from Telnyx.
    """
    data = request.json
    user_message = data.get('text')
    user_number = data.get('from')

    # Process the SMS message using the query processor
    response_message = process_query(user_message)

    # Send SMS response back to user
    send_sms(user_number, response_message)

    return {"status": "success"}, 200


def send_sms(receiver, message):
    """
    Sends an SMS message via Telnyx's Messaging API.

    Args:
        receiver (str): The recipient's phone number.
        message (str): The message content to send.
    """
    url = "https://api.telnyx.com/v2/messages"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TELNYX_API_KEY}"
    }
    payload = {
        "from": TELNYX_FROM,
        "to": receiver,
        "text": message,
        "messaging_profile_id": TELNYX_PROFILE_ID
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to send SMS: {response.text}")


# Endpoints for ChromaDB CRUD operations

@app.route('/add_document', methods=['POST'])
def add_route():
    """
    Adds a document to ChromaDB.
    """
    data = request.json
    doc_id = data.get('id')
    content = data.get('content')
    metadata = data.get('metadata', {})

    if not doc_id or not content:
        return {"error": "Both 'id' and 'content' are required."}, 400

    try:
        add_document(doc_id, content, metadata)
        return {"message": f"Document '{doc_id}' added successfully."}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/search_documents', methods=['GET'])
def search_route():
    """
    Searches for documents in ChromaDB using a query string.

    Query Parameters:
        query (str): The user's query string.
        top_k (int, optional): Number of top results to return. Defaults to 3.
        summarize (bool, optional): Whether to summarize the combined results. Defaults to False.
    """
    query = request.args.get('query')
    top_k = int(request.args.get('top_k', 3))  # Allows specifying number of top results
    summarize = request.args.get('summarize', 'false').lower() == 'true'  # Summarize the response if requested

    if not query:
        return {"error": "Query parameter is required."}, 400

    try:
        # Retrieve top document chunks with optional summarization
        results = search_documents(query, top_k=top_k, summarize=summarize)
        return results, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/delete_document', methods=['DELETE'])
def delete_route():
    """
    Deletes a document from ChromaDB by its ID.
    """
    doc_id = request.args.get('id')
    if not doc_id:
        return {"error": "Document ID parameter is required."}, 400

    try:
        delete_document(doc_id)
        return {"message": f"Document '{doc_id}' deleted successfully."}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/upload_markdown', methods=['POST'])
def upload_markdown():
    """
    Uploads a Markdown file, processes its content, and stores it in ChromaDB with metadata.

    Expects the file to be uploaded via a multipart form with the key `file`.
    """
    if 'file' not in request.files:
        return {"error": "No file part in the request."}, 400

    file = request.files['file']
    if file.filename == '':
        return {"error": "No selected file."}, 400

    # Read the content of the uploaded Markdown file
    content = file.read().decode('utf-8')

    # Split the content into chunks (e.g., based on paragraph structure)
    chunks = chunk_markdown_content(content)

    # Upload each chunk to ChromaDB with metadata
    for i, chunk in enumerate(chunks):
        doc_id = f"{file.filename}_chunk_{i+1}"  # Generate unique doc ID for each chunk
        metadata = {
            "source_file": file.filename,
            "chunk_index": i + 1,
            "uploaded_at": datetime.datetime.utcnow().isoformat(),
        }
        add_document(doc_id, chunk, metadata)

    return {"message": f"Markdown file '{file.filename}' uploaded and processed successfully.",
            "chunks_uploaded": len(chunks)}, 200


def chunk_markdown_content(content, chunk_size=500):
    """
    Splits Markdown content into smaller chunks of a specified size.

    Args:
        content (str): The original Markdown content.
        chunk_size (int, optional): Max size of each chunk. Defaults to 500 characters.

    Returns:
        list[str]: A list of chunks.
    """
    lines = content.split("\n\n")  # Split content into paragraphs
    chunks = []
    current_chunk = ""

    for line in lines:
        # Add the current line to the chunk if it fits within the chunk_size
        if len(current_chunk) + len(line) < chunk_size:
            current_chunk += line + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = line

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
