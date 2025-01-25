import requests
import json
from config import EMBEDDING_API_URL

import time

def generate_embedding(document, retries=3, backoff=2):
    """
    Sends a document to the embedding endpoint and retrieves its vector embedding.
    Retries on transient failures.

    Args:
        document (str): The document to embed.
        retries (int): Number of retry attempts if an error occurs.
        backoff (int): Backoff time (seconds) between retries.

    Returns:
        list: The embedding vector for the document.
    """
    headers = {"Content-Type": "application/json"}
    payload = {"model": "mxbai-embed-large", "prompt": document}

    for attempt in range(retries):
        try:
            response = requests.post(EMBEDDING_API_URL, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            embedding = response.json().get("embedding")
            if not embedding:
                raise Exception("No embedding found in the embedding API response.")
            return embedding
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(backoff)
            else:
                raise Exception(f"Embedding endpoint error (after {retries} attempts): {str(e)}")
