import os

# Telnyx Configuration
TELNYX_API_KEY = os.getenv("TELNYX_API_KEY")
TELNYX_FROM = os.getenv("TELNYX_FROM")
TELNYX_PROFILE_ID = os.getenv("TELNYX_PROFILE_ID")

# Embedding Model Configuration
EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL")

# LLM Configuration
LLM_API_URL = os.getenv("LLM_API_URL")
USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() == "true"  # Flag to use OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI API key if using OpenAI