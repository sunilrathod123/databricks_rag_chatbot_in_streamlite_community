from rag.prompt import build_messages

def generate_answer(question, context, gateway_client, settings):
    response = gateway_client.chat.completions.create(
        model=settings.llm_model,
        messages=build_messages(question, context),
        temperature=0.1,
        max_tokens=settings.max_output_tokens,
    )
    answer = response.choices[0].message.content
    if isinstance(answer, list):
        answer = "\n".join(
            item.text for item in answer if getattr(item, "text", None)
        )
    if not answer or not str(answer).strip():
        raise RuntimeError("Chat model returned an empty answer.")
    return str(answer).strip()
