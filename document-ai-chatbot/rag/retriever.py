import requests

def retrieve_chunks(query_vector, settings, top_k):
    url = (
        f"{settings.databricks_host}/api/2.0/vector-search/indexes/"
        f"{settings.vector_search_index}/query"
    )
    headers = {
        "Authorization": f"Bearer {settings.databricks_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "query_vector": query_vector,
        "num_results": int(top_k),
        "columns": [
            "chunk_id", "document_id", "document_name", "file_hash",
            "chunk_index", "chunk_type", "page_number", "section_title",
            "chunk_text", "source_path",
        ],
    }
    response = requests.post(
        url, headers=headers, json=payload,
        timeout=settings.request_timeout_seconds,
    )
    if not response.ok:
        raise RuntimeError(
            f"Vector Search query failed (HTTP {response.status_code}): "
            f"{response.text[:3000]}"
        )
    body = response.json()
    names = [c["name"] for c in body.get("manifest", {}).get("columns", [])]
    rows = body.get("result", {}).get("data_array", [])
    output = []
    for row in rows:
        item = dict(zip(names, row))
        score = row[-1] if len(row) > len(names) else item.get("score")
        item["similarity_score"] = float(score) if score is not None else None
        output.append(item)
    return output
