from rag.embedding import create_query_embedding
from rag.retriever import retrieve_chunks
from rag.prompt import build_context
from rag.llm import generate_answer

def answer_question(question, settings, gateway_client, top_k):
    vector = create_query_embedding(question, gateway_client, settings)
    chunks = retrieve_chunks(vector, settings, top_k)
    if not chunks:
        return {
            "answer": "I could not find relevant information in the indexed documents.",
            "sources": [],
            "retrieved_count": 0,
        }
    context, sources = build_context(chunks, settings)
    if not context.strip():
        return {
            "answer": "Retrieved records did not contain readable text.",
            "sources": [],
            "retrieved_count": len(chunks),
        }
    answer = generate_answer(question, context, gateway_client, settings)
    return {"answer": answer, "sources": sources, "retrieved_count": len(chunks)}
