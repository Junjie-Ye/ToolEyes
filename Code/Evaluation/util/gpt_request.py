import requests
import time
import openai
import json
from gpt3_tokenizer import count_tokens


def make_request(api_key=None, organization=None, url=None, **kwargs):
    def request_to_gpt(call_way):
        error_times = 0
        while error_times < 20:
            print(error_times, end='   ', flush=True)
            if call_way == 'api_key':
                try:
                    x = openai.ChatCompletion.create(**kwargs)
                    return x
                except openai.error.InvalidRequestError as e:
                    print(e, flush=True)
                    return {"choices": [{"message": {"role": "assistant", "content": "Too long context."}}, {"finish_reason": "length"}]}
                except Exception as e:
                    print(e, '    ', kwargs["messages"], flush=True)
                    error_times += 1
                    time.sleep(5)

        return {"choices": [{"message": {"role": "assistant", "content": "Try too many times to answer the query."}}, {"finish_reason": "times"}]}

    assert api_key is not None or url is not None, "The api_key or url for call openai models must be provided at least one."
    assert "messages" in kwargs.keys(), "The messages to call the model must be provided."

    count = 0
    for item in kwargs['messages']:
        if item["content"] is not None:
            count += count_tokens(item['content'])
    if count > 120000:
        return {"choices": [{"message": {"role": "assistant", "content": "Too long context."}}, {"finish_reason": "length"}]}

    if api_key is not None:
        openai.api_key = api_key
        if organization is not None:
            openai.organization = organization
        return request_to_gpt("api_key")
def make_request_completion(api_key=None, organization=None, url=None, **kwargs):
    def request_to_gpt(call_way):
        error_times = 0
        while error_times < 20:
            print(error_times, end='   ', flush=True)
            if call_way == 'api_key':
                try:
                    x = openai.Completion.create(**kwargs)
                    return {"choices": [{"message": {"role": "assistant", "content": x["choices"][0]["text"]}}, {"finish_reason": x["choices"][0]["finish_reason"]}]}
                    return x
                except openai.error.InvalidRequestError as e:
                    print(e, flush=True)
                    return {"choices": [{"message": {"role": "assistant", "content": "Too long context."}}, {"finish_reason": "length"}]}
                except Exception as e:
                    print(e, '    ', kwargs["prompt"], flush=True)
                    error_times += 1
                    time.sleep(5)

        return {"choices": [{"message": {"role": "assistant", "content": "Try too many times to answer the query."}}, {"finish_reason": "times"}]}

    assert api_key is not None or url is not None, "The api_key or url for call openai models must be provided at least one."
    assert "prompt" in kwargs.keys(), "The prompt to call the model must be provided."

    count = 0
    count += count_tokens(kwargs['prompt'])
    if count > 3000:
        return {"choices": [{"message": {"role": "assistant", "content": "Too long context."}}, {"finish_reason": "length"}]}

    if api_key is not None:
        openai.api_key = api_key
        if organization is not None:
            openai.organization = organization
        return request_to_gpt("api_key")
