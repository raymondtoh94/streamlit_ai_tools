from langchain.chat_models import init_chat_model


def run_llm(selected_provider, selected_model, prompt):
    print("Running LLM with the following parameters:")
    print(f"Provider: {selected_provider}")
    print(f"Model: {selected_model}")

    model = init_chat_model(
        model=selected_model,
        model_provider=selected_provider,
    )

    response = model.invoke(f"{prompt}")
    return response
