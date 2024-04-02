from openai import OpenAI


def chatgpt_basic_conversation(api_key: str, prompts: list, model: str = 'gpt-3.5-turbo') -> str:
    """chatgpt最基本的对话

    Args:
        api_key (str): _description_
        prompts (list): e.g [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}]
        model (str, optional): _description_. Defaults to 'gpt-3.5-turbo'.

    Returns:
        str: ChatGPT response
    """
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(model=model, messages=prompts)
    return completion.choices[0].message.content
