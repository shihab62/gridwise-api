import os
from typing import Optional
from dotenv import load_dotenv

# Load local environment if present
load_dotenv()

PORT: int = int(os.getenv("PORT", "3000"))
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini").lower().strip()
LLM_API_KEY: str = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY", "")
LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-3.6-flash").strip()
LLM_BASE_URL: Optional[str] = os.getenv("LLM_BASE_URL", "").strip() or None
LLM_FALLBACK_MODEL: Optional[str] = os.getenv("LLM_FALLBACK_MODEL", "gemini-3.1-flash-lite").strip() or None
ENABLE_HEURISTIC_FALLBACK: bool = os.getenv("ENABLE_HEURISTIC_FALLBACK", "true").lower() in ("true", "1", "yes")

# Timeout budgets
LLM_PER_CALL_TIMEOUT: float = 5.0
LLM_TOTAL_TIMEOUT_BUDGET: float = 10.0
REQUEST_TIMEOUT_LIMIT: float = 25.0
