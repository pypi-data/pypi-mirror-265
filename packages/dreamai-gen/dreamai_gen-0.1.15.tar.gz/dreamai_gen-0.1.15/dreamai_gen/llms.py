from copy import deepcopy
from enum import Enum

import instructor
import litellm
import tiktoken
from dsp.modules.lm import LM as DSPyLM
from litellm import completion
from openai import OpenAI
from termcolor import colored

from .message import assistant_message
from .utils import retry_attempts

litellm.drop_params = True


class ModelName(str, Enum):
    GPT_3 = "gpt-3.5-turbo"
    GPT_4 = "gpt-4-turbo-preview"
    GEMINI = "gemini/gemini-pro"
    CLAUDE2 = "claude-2.1"
    CLAUDE3 = "claude-3-haiku-20240307"
    MISTRAL = "anyscale/mistralai/Mistral-7B-Instruct-v0.1"
    MIXTRAL = "anyscale/mistralai/Mixtral-8x7B-Instruct-v0.1"


GPT_MODEL = ModelName.GPT_3
GEMINI_MODEL = ModelName.GEMINI


def dspy_prompt(lm: DSPyLM) -> str:
    n = 1
    skip = 0
    provider: str = lm.provider
    last_prompt = None
    printed = []
    n = n + skip
    for x in reversed(lm.history[-100:]):
        prompt = x["prompt"]
        if prompt != last_prompt:
            if provider == "clarifai" or provider == "google":
                printed.append(
                    (
                        prompt,
                        x["response"],
                    ),
                )
            else:
                printed.append(
                    (
                        prompt,
                        x["response"].generations
                        if provider == "cohere"
                        else x["response"]["choices"],
                    ),
                )
        last_prompt = prompt
        if len(printed) >= n:
            break
    history_str = ""
    for idx, (prompt, choices) in enumerate(reversed(printed)):
        if (n - idx - 1) < skip:
            continue
        history_str += prompt
        text = ""
        if provider == "cohere":
            text = choices[0].text
        elif provider == "openai" or provider == "ollama":
            text = " " + lm._get_choice_text(choices[0]).strip()
        elif provider == "clarifai":
            text = choices
        elif provider == "google":
            text = choices[0].parts[0].text
        else:
            text = choices[0]["text"]
        history_str += text
        if len(choices) > 1:
            history_str += f" \t (and {len(choices)-1} other completions)"
    return history_str


def oai_response(response) -> str:
    try:
        return response.choices[0].message.content
    except Exception:
        return response


def ask_litellm(
    messages: list[dict[str, str]],
    model: str = GEMINI_MODEL,
    json_mode: bool | None = None,
) -> tuple:
    try:
        if json_mode is None and "json" in messages[-1]["content"].lower():
            response_format = {"type": "json_object"}
        else:
            response_format = None
        # response_format = {
        #     "type": (
        #         "json_object"
        #         if json_mode is None and "json" in messages[-1]["content"].lower()
        #         else "text"
        #     )
        # }
        answer = oai_response(
            completion(
                messages=deepcopy(messages),
                model=model,
                response_format=response_format,
            )
        )
        messages.append(assistant_message(content=answer))
        return answer, messages
    except Exception as e:
        print(colored(f"\n\n{model} ERROR: {e}\n\n", "red"))
        return None, messages


def count_gpt_tokens(text: str, model: str = GPT_MODEL) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def ask_oai(
    messages: list[dict[str, str]],
    model: str = GPT_MODEL,
    response_model=None,
    temperature: float = 0.3,
    max_tokens: int | None = None,
    patch_mode=instructor.Mode.TOOLS,
    attempts: int = 1,
    api_key: str | None = None,
    base_url: str | None = None,
) -> tuple:
    """Ask OpenAI to generate a response to the given messages."""
    # print(f"\n\nMESSAGES: {messages}\n\n")
    gpt = instructor.patch(OpenAI(api_key=api_key, base_url=base_url), mode=patch_mode)
    try:
        answer = gpt.chat.completions.create(
            messages=deepcopy(messages),
            model=model,
            response_model=response_model,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=retry_attempts(attempts=attempts),
        )
    except Exception as e:
        print(colored(f"\n\n{model} ERROR: {e}\n\n", "red"))
        return None, messages
    if not response_model:
        answer = oai_response(answer)
        messages.append(assistant_message(content=answer))
        return answer, messages
    messages.append(assistant_message(content=answer.model_dump_json()))
    return answer, messages
