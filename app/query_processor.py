from llm_client import generate_llm_response
from database_manager import search_documents

def process_query(user_message):
    """
    Processes the user message using the LLM and vector database.
    """
    intent_prompt = f"""The user has asked a question via SMS. Here is their message:
{user_message}

Using plain text, explain what data or intent they are searching for so I can query a database."""
    inferred_query = generate_llm_response(intent_prompt)

    documents, distances = search_documents(inferred_query)

    if not documents:
        response_prompt = f"The user searched for something related to: {user_message}. No matching data found in the database. Respond politely."
    else:
        closest_doc = documents[0]
        response_prompt = f"""The user searched for: {user_message}.
The database retrieved a matching result: {closest_doc}.
Write a response to convey the results, keeping your response less than 160 characters in length and using no special formatting. Plain text only."""
    
    response_message = generate_llm_response(response_prompt)
    return response_message
