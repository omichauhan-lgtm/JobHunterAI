import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Setup paths
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("JobHunterAI")

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# App Configurations
DEFAULT_TEMPLATE = os.getenv("DEFAULT_RESUME_TEMPLATE", "backend.tex")
APPLY_THRESHOLD = float(os.getenv("JOB_APPLY_THRESHOLD", "80.0"))

# Database path
DB_PATH = BASE_DIR / "data" / "candidate.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Generate path
GEN_DIR = BASE_DIR / "data" / "generated"
GEN_DIR.mkdir(parents=True, exist_ok=True)

# LLM Providers Setup
OFFLINE_MODE = not (GEMINI_API_KEY or OPENAI_API_KEY)

if OFFLINE_MODE:
    logger.warning("No API keys (GEMINI_API_KEY or OPENAI_API_KEY) found. Running in OFFLINE mode. AI engines will use mock text generators.")
else:
    logger.info(f"Initialized JobHunterAI in ONLINE mode. Gemini client: {'Configured' if GEMINI_API_KEY else 'N/A'}, OpenAI client: {'Configured' if OPENAI_API_KEY else 'N/A'}")

def call_llm(prompt: str, response_schema=None, system_instruction: str = None) -> str:
    """Unified function to call the available LLM (Gemini preferred, OpenAI fallback, Mock if offline)."""
    if OFFLINE_MODE:
        return "MOCK_RESPONSE: The system is running in offline mode. Configure an API key in .env to generate real text."

    # Try Gemini first if key available
    if GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model_name = 'gemini-1.5-flash'
            
            gen_config = {}
            if response_schema:
                gen_config["response_mime_type"] = "application/json"
                gen_config["response_schema"] = response_schema
                
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
            response = model.generate_content(
                prompt,
                generation_config=gen_config if gen_config else None
            )
            return response.text
        except Exception as e:
            logger.error(f"Error calling Gemini: {e}. Falling back...")
            
    # Try OpenAI if Gemini fails or is not available
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            model_name = "gpt-4o-mini"
            
            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})
            messages.append({"role": "user", "content": prompt})
            
            if response_schema:
                # Use structured outputs
                completion = client.beta.chat.completions.parse(
                    model=model_name,
                    messages=messages,
                    response_format=response_schema
                )
                return completion.choices[0].message.content
            else:
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=messages
                )
                return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling OpenAI: {e}")
            
    return "ERROR: All configured LLM API calls failed."

def retrieve_doc(doc_name: str) -> str:
    """RAG-style helper to dynamically retrieve documentation context for prompts."""
    docs_dir = BASE_DIR / "docs"
    target_path = (docs_dir / doc_name).resolve()
    
    # Security check: Prevent directory traversal
    if not str(target_path).startswith(str(docs_dir)):
        logger.error(f"Unauthorized document retrieval attempt: {doc_name}")
        return ""
        
    if not target_path.exists():
        logger.warning(f"Requested documentation not found: {doc_name}")
        return ""
        
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading documentation {doc_name}: {e}")
        return ""

