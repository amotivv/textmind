import requests
import json
from config import LLM_API_URL, USE_OPENAI, OPENAI_API_KEY

def generate_llm_response(prompt):
    """
    Generates a concise, SMS-friendly response to the given prompt using OpenAI or the local LLM.

    Args:
        prompt (str): The input prompt to generate a response for.

    Returns:
        str: The cleaned and SMS-friendly generated response text.
    """
    if USE_OPENAI:
        # OpenAI GPT Chat API via HTTP request
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }

        # Refine the prompt to request a concise SMS-friendly summary
        prompt = (
            f"{prompt}\n\nPlease summarize this in plain text suitable for SMS. "
            "The summary must be concise, avoid line breaks, special characters, or formatting, "
            "and fit in 160 characters or less."
        )

        payload = {
            "model": "gpt-4",  # Use "gpt-4" or another model as required
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise HTTP errors

            # Extract and clean the assistant's generated response
            output = response.json()
            summary = output["choices"][0]["message"]["content"].strip()

            # Clean up the summary for SMS
            summary = sanitize_sms_text(summary)

            return summary

        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI GPT Error: {str(e)}")
        except KeyError:
            raise Exception(f"OpenAI GPT Error: Malformed response: {response.text}")

    else:
        # Local LLM API via HTTP requests
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "deepseek-r1:7b",  # Use your local LLM model
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(LLM_API_URL, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            summary = response.json().get("response", "").strip()

            # Clean up the summary for SMS
            summary = sanitize_sms_text(summary)

            return summary

        except requests.exceptions.RequestException as e:
            raise Exception(f"Local LLM Error: {str(e)}")
        except KeyError:
            raise Exception(f"Local LLM Error: Malformed response: {response.text}")


def sanitize_sms_text(summary):
    """
    Prepares a summary for SMS by removing line breaks, special characters,
    and ensuring clean plain text.

    Args:
        summary (str): The summarized text.

    Returns:
        str: Cleaned SMS-friendly text.
    """
    # Remove line breaks and extra spaces
    summary = summary.replace("\n", " ").replace("\r", " ").strip()

    # Remove special characters or unnecessary formatting
    summary = summary.replace("*", "").replace("_", "").replace("—", "-")

    # Replace excessive white spaces with a single space
    summary = " ".join(summary.split())

    return summary
