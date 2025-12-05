import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", "")
MODEL = os.getenv("MODEL", "claude-3-5-haiku-20241022")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "3600"))
