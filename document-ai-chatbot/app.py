import streamlit as st
from config.settings import get_settings
from rag.clients import build_gateway_client
from rag.pipeline import answer_question

st.set_page_config(page_title="Document AI Assistant", page_icon="📚", layout="wide")
settings = get_settings()

@st.cache_resource(show_spinner=False)
def gateway_client(host, token):
    return build_gateway_client(host, token)

st.session_state.setdefault("messages", [])

st.title("📚 Document AI Assistant")
st.caption("Ask questions about your indexed PDF and DOCX documents.")

with st.sidebar:
    st.subheader("Knowledge base")
    st.caption(f"Index: `{settings.vector_search_index}`")
    st.caption(f"Endpoint: `{settings.vector_search_endpoint}`")
    st.caption(f"Embedding: `{settings.embedding_model}`")
    st.caption(f"LLM: `{settings.llm_model}`")
    top_k = st.slider("Retrieved chunks", 1, 10, settings.top_k)
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

try:
    client = gateway_client(settings.databricks_host, settings.databricks_token)
except Exception as exc:
    st.error("Could not initialize Databricks AI Gateway.")
    st.exception(exc)
    st.stop()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander(f"Sources ({len(message['sources'])})"):
                for source in message["sources"]:
                    st.markdown(f"**[{source['citation_number']}] {source.get('document_name') or 'Document'}**")
                    st.caption(f"Page: {source.get('page_number') or 'N/A'} · Chunk: {source.get('chunk_id') or 'N/A'} · Score: {source.get('similarity_score')}")
                    st.markdown(source.get("chunk_text", ""))
                    st.divider()

question = st.chat_input("Ask a question about your documents...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating an answer..."):
            try:
                result = answer_question(question, settings, client, top_k)
                st.markdown(result["answer"])
                if result["sources"]:
                    with st.expander(f"Sources ({len(result['sources'])})", expanded=True):
                        for source in result["sources"]:
                            st.markdown(f"**[{source['citation_number']}] {source.get('document_name') or 'Document'}**")
                            st.caption(f"Page: {source.get('page_number') or 'N/A'} · Chunk: {source.get('chunk_id') or 'N/A'} · Score: {source.get('similarity_score')}")
                            st.markdown(source.get("chunk_text", ""))
                            st.divider()
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"],
                })
            except Exception as exc:
                st.error("Could not process this question.")
                st.exception(exc)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"An error occurred: {exc}",
                    "sources": [],
                })
