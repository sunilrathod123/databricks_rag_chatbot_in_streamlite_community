def create_query_embedding(question, gateway_client, settings):
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")
    response = gateway_client.embeddings.create(
        model=settings.embedding_model,
        input=[question.strip()],
    )
    if not response.data:
        raise RuntimeError("Embedding endpoint returned no vector.")
    vector = [float(value) for value in response.data[0].embedding]
    if len(vector) != settings.vector_dimension:
        raise RuntimeError(
            f"Expected {settings.vector_dimension} dimensions, received {len(vector)}. "
            "Confirm the embedding model matches Notebook 05."
        )
    return vector
