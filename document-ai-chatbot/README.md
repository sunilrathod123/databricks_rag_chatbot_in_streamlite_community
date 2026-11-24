# Document AI Chatbot

Streamlit Community Cloud frontend for your Databricks RAG pipeline.

## Files to customize

All workspace-specific values are entered in Streamlit Community Cloud → App → Settings → Secrets. See `.streamlit/secrets.toml.example`.

Required secrets:

```toml
DATABRICKS_HOST = "https://YOUR-WORKSPACE.cloud.databricks.com"
DATABRICKS_TOKEN = "YOUR_WORKSPACE_PERSONAL_ACCESS_TOKEN"
VECTOR_SEARCH_ENDPOINT = "retail_ai_search_endpoint"
VECTOR_SEARCH_INDEX = "uc_nac_dev.gold.document_vector_index"
EMBEDDING_MODEL = "system.ai.gte-large-en"
LLM_MODEL = "system.ai.gpt-oss-120b"
VECTOR_DIMENSION = 1024
TOP_K = 5
```

## Deploy

1. Upload/push this folder to GitHub.
2. In Streamlit Community Cloud, create an app from the repository.
3. Set the entry point to `app.py`.
4. Open App settings → Secrets and paste the TOML above, replacing placeholders with your real values.
5. Deploy.

## Local run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

For local use, create `.streamlit/secrets.toml` with the same TOML keys.

## Databricks permissions and compatibility

The PAT owner must be allowed to:
- Query the Vector Search index and its endpoint.
- Use the configured embedding model through AI Gateway.
- Use the configured chat model through AI Gateway.

The index must expose the columns requested in `rag/retriever.py`. If your index uses different column names, update that list to match the actual index source table.

The app uses the Vector Search REST query endpoint with `query_vector` and uses the Databricks OpenAI client for Unity Gateway model calls. Verify that PAT-based access to both model endpoints is enabled in your workspace.

A workspace PAT is tied to its owner and is less suitable for a shared production service than a service principal. Do not commit the PAT to GitHub or paste it into chat. Streamlit session history is temporary and is not persisted to Delta.
