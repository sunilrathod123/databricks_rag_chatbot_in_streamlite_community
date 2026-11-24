from dataclasses import dataclass
import os
import streamlit as st

def read_config(name, default=None):
    try:
        value = st.secrets.get(name)
        if value not in (None, ""):
            return value
    except Exception:
        pass
    return os.getenv(name, default)

@dataclass(frozen=True)
class Settings:
    databricks_host: str
    databricks_token: str
    vector_search_index: str
    vector_search_endpoint: str
    embedding_model: str
    llm_model: str
    vector_dimension: int
    top_k: int
    max_context_chars: int
    max_chunk_chars: int
    max_output_tokens: int
    request_timeout_seconds: int

def get_settings():
    host = read_config("DATABRICKS_HOST")
    token = read_config("DATABRICKS_TOKEN")
    index = read_config("VECTOR_SEARCH_INDEX", "uc_nac_dev.gold.document_vector_index")
    endpoint = read_config("VECTOR_SEARCH_ENDPOINT", "retail_ai_search_endpoint")
    missing = [k for k, v in {
        "DATABRICKS_HOST": host,
        "DATABRICKS_TOKEN": token,
        "VECTOR_SEARCH_INDEX": index,
        "VECTOR_SEARCH_ENDPOINT": endpoint,
    }.items() if not v]
    if missing:
        raise RuntimeError("Missing Streamlit secrets: " + ", ".join(missing))
    host = str(host).strip().rstrip("/")
    if not host.startswith("https://"):
        raise ValueError("DATABRICKS_HOST must start with https://")
    return Settings(
        databricks_host=host,
        databricks_token=str(token).strip(),
        vector_search_index=str(index).strip(),
        vector_search_endpoint=str(endpoint).strip(),
        embedding_model=str(read_config("EMBEDDING_MODEL", "system.ai.gte-large-en")),
        llm_model=str(read_config("LLM_MODEL", "system.ai.gpt-oss-120b")),
        vector_dimension=int(read_config("VECTOR_DIMENSION", 1024)),
        top_k=int(read_config("TOP_K", 5)),
        max_context_chars=int(read_config("MAX_CONTEXT_CHARS", 18000)),
        max_chunk_chars=int(read_config("MAX_CHUNK_CHARS", 5000)),
        max_output_tokens=int(read_config("MAX_OUTPUT_TOKENS", 1200)),
        request_timeout_seconds=int(read_config("REQUEST_TIMEOUT_SECONDS", 60)),
    )
