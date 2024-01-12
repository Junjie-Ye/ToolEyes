#!/usr/bin/env python
# coding=utf-8
import sys  # NOQA: E402
sys.path.append('/workspace/ToolEyes')  # NOQA: E402
from Code.Inference.utils import SimpleChatIO, generate_stream, react_parser
from Code.model.model_adapter import get_conversation_template
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)
from typing import Optional
import re
import torch
from peft import PeftModel
from typing import Optional, List
from termcolor import colored
import time
import openai
import gpt3_tokenizer


def compress_prompt(prompt, tokenizer, mode="completion"):
    if mode == 'completion':
        prompt_encode = tokenizer.encode(prompt)
        print(f"prompt tokens: {len(prompt_encode)}")
        function_pattern = re.compile("Function:.*?Assistant:", re.DOTALL)
        while len(prompt_encode) > 6800:
            funtion_content = function_pattern.search(
                prompt).group().replace("Assistant:", "")
            prompt = prompt.replace(funtion_content, "")
            prompt_encode = tokenizer.encode(prompt)
        
        print(f"compressed prompt tokens: {len(prompt_encode)}")

    elif mode == "chat":
        count = 0
        function_idx = []
        for i, item in enumerate(prompt):
            count += len(tokenizer.encode(item["content"]))
            if item["role"] == "function":
                function_idx.append(i)
        print(f"prompt tokens: {count}")
        times = 0
        while count > 6800:
            count -= len(tokenizer.encode(prompt[function_idx[0]-times]["content"]))
            prompt.pop(function_idx[0]-times)
            function_idx.pop(0)
            times += 1

        print(f"compressed prompt tokens: {count}")

    return prompt


class ToolLoRA:
    def __init__(
        self,
        base_name_or_path: str,
        model_name_or_path: str,
        template: str = "tool-single-round",
        device: str = "cuda",
        cpu_offloading: bool = False,
        load_8bit: bool = False,
        max_sequence_length: int = 8192
    ) -> None:
        super().__init__()
        self.model_name = model_name_or_path
        self.template = template
        self.max_sequence_length = max_sequence_length
        self.tokenizer = AutoTokenizer.from_pretrained(
            base_name_or_path, use_fast=False, model_max_length=self.max_sequence_length, padding_side="right")
        model = AutoModelForCausalLM.from_pretrained(
            base_name_or_path,
            load_in_8bit=load_8bit,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.model = PeftModel.from_pretrained(
            model,
            model_name_or_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.tokenizer.pad_token = self.tokenizer.unk_token

        self.use_gpu = (True if device == "cuda" else False)
        # if (device == "cuda" and not cpu_offloading) or device == "mps":
        #     self.model.to(device)
        self.chatio = SimpleChatIO()

    def prediction(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        gen_params = {
            "model": "",
            "prompt": prompt,
            "temperature": 0.3,
            "top_p": 0.5,
            "max_new_tokens": 1024,
            "stop": "</s>",
            "stop_token_ids": None,
            "echo": False
        }
        output_stream = generate_stream(
            self.model, self.tokenizer, gen_params, "cuda", self.max_sequence_length, force_generate=True)
        outputs = self.chatio.return_output(output_stream)
        prediction = outputs.strip()
        return prediction

    def add_message(self, message):
        self.conversation_history.append(message)

    def change_messages(self, messages):
        self.conversation_history = messages

    def display_conversation(self, detailed=False):
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "function": "magenta",
        }
        print("before_print"+"*"*50)
        for message in self.conversation_history:
            print_obj = f"{message['from']}: {message['value']} "
            if "function_call" in message.keys():
                print_obj = print_obj + \
                    f"function_call: {message['function_call']}"
            print_obj += ""
            print(
                colored(
                    print_obj,
                    role_to_color[message["from"]],
                )
            )
        print("end_print"+"*"*50)

    def parse(self, process_id, method):
        conv = get_conversation_template(self.template)
        if self.template == "tool":
            roles = {"human": conv.roles[0], "gpt": conv.roles[1]}
        elif self.template == "tool-single-round" or self.template == "tool-multi-rounds":
            roles = {"system": conv.roles[0], "user": conv.roles[1],
                     "function": conv.roles[2], "assistant": conv.roles[3]}

        self.time = time.time()
        conversation_history = self.conversation_history
        # prompt = ''
        for message in conversation_history:
            conv.append_message(roles[message['from']], message['value'])
            # role = roles[message['from']]
            # content = message['value']
            # prompt += f"{role}: {content}\n"
        # prompt += "Assistant:"
        conv.append_message(roles['assistant'], None)
        prompt = conv.get_prompt()
        prompt = compress_prompt(prompt, self.tokenizer)
        # print(prompt)
        predictions = self.prediction(prompt)
        print(f"Assistant:{predictions}")

        decoded_token_len = len(self.tokenizer.encode(predictions))
        if process_id == 0:
            print(
                f"[process({process_id})]prediction tokens: {decoded_token_len}")

        # react format prediction
        if method == 'tool':
            thought, action, action_input = react_parser(predictions)
            predictions = thought + action + action_input
            message = {
                "role": "assistant",
                "content": thought.replace("Thought: ", "").strip(),
                "function_call": {
                    "name": action.replace("Action: ", "").strip(),
                    "arguments": action_input.replace("Action Input: ", "").strip()
                }
            }
            return predictions, message
        elif method == 'general':
            return predictions


class Tool:
    def __init__(
        self,
        model_name_or_path: str,
        template: str = "tool-single-round",
        device: str = "cuda",
        cpu_offloading: bool = False,
        max_sequence_length: int = 8192
    ) -> None:
        super().__init__()
        self.model_name = model_name_or_path
        self.template = template
        self.max_sequence_length = max_sequence_length
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name_or_path, use_fast=False, model_max_length=self.max_sequence_length)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name_or_path,
            device_map="auto",torch_dtype=torch.float16
        )
        self.tokenizer.pad_token = self.tokenizer.unk_token
        self.use_gpu = (True if device == "cuda" else False)
        self.chatio = SimpleChatIO()

    def prediction(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        with torch.no_grad():
            gen_params = {
                "model": "",
                "prompt": prompt,
                "temperature": 0.3,
                "top_p": 0.5,
                "max_new_tokens": 1024,
                "stop": "</s>",
                "stop_token_ids": None,
                "echo": False
            }
            output_stream = generate_stream(
                self.model, self.tokenizer, gen_params, "cuda", self.max_sequence_length, force_generate=True)
            outputs = self.chatio.return_output(output_stream)
            prediction = outputs.strip()
        return prediction

    def add_message(self, message):
        self.conversation_history.append(message)

    def change_messages(self, messages):
        self.conversation_history = messages

    def display_conversation(self, detailed=False):
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "function": "magenta",
        }
        print("before_print"+"*"*50)
        for message in self.conversation_history:
            print_obj = f"{message['from']}: {message['value']} "
            if "function_call" in message.keys():
                print_obj = print_obj + \
                    f"function_call: {message['function_call']}"
            print_obj += ""
            print(
                colored(
                    print_obj,
                    role_to_color[message["from"]],
                )
            )
        print("end_print"+"*"*50)

    def parse(self, process_id, method):
        conv = get_conversation_template(self.template)
        if self.template == "tool":
            roles = {"human": conv.roles[0], "gpt": conv.roles[1]}
        elif self.template == "tool-single-round" or self.template == "tool-multi-rounds":
            roles = {"system": conv.roles[0], "user": conv.roles[1],
                     "function": conv.roles[2], "assistant": conv.roles[3]}

        self.time = time.time()
        conversation_history = self.conversation_history
        # prompt = ''
        for message in conversation_history:
            conv.append_message(roles[message['from']], message['value'])
            # role = roles[message['from']]
            # content = message['value']
            # prompt += f"{role}: {content}\n"
        # prompt += "Assistant:"
        conv.append_message(roles['assistant'], None)
        prompt = conv.get_prompt()
        prompt = compress_prompt(prompt, self.tokenizer)
        # print(prompt)
        predictions = self.prediction(prompt)
        print(f"Assistant:{predictions}")

        decoded_token_len = len(self.tokenizer.encode(predictions))
        if process_id == 0:
            print(
                f"[process({process_id})]prediction tokens: {decoded_token_len}")

        # react format prediction
        if method == 'tool':
            thought, action, action_input = react_parser(predictions)
            predictions = thought + action + action_input
            message = {
                "role": "assistant",
                "content": thought.replace("Thought: ", "").strip(),
                "function_call": {
                    "name": action.replace("Action: ", "").strip(),
                    "arguments": action_input.replace("Action Input: ", "").strip()
                }
            }
            return predictions, message
        elif method == 'general':
            return predictions


class ChatGPT:
    def __init__(
        self,
        api_key=None,
        orgnization=None,
        url=None,
        mode="chat",
        model=None,
        template: str = "tool-single-round",
    ) -> None:
        super().__init__()
        assert api_key is not None or url is not None, "The api_key or url for call openai models must be provided at least one."
        if api_key is not None:
            self.call_way = "api_key"
            openai.api_key = api_key
            if orgnization is not None:
                openai.organization = orgnization
        else:
            self.call_way = "url"
            self.url = url

        self.tokenizer = gpt3_tokenizer
        
        self.mode = mode
        self.model = model
        self.template = template

    def prediction(self, prompt: str, stop: Optional[List[str]] = None, functions=None) -> str:
        if self.call_way == 'api_key':
            error_times = 0
            if self.mode == "chat":
                while error_times < 20:
                    try:
                        x = openai.ChatCompletion.create(
                            model=self.model,
                            messages=prompt,
                            temperature=0.3,
                            top_p=0.5,
                            max_tokens=1024,
                            stop=stop
                        )

                        return x.choices[0].message.content
                    except openai.error.InvalidRequestError as e:
                        print(e, flush=True)
                        return "Thought: \nAction: finish\nAction Input: {\"Answer\": \"I can not handle the task due to too long context.\"}"
                    except Exception as e:
                        print(e, '    ', prompt, flush=True)
                        error_times += 1
                        time.sleep(5)
            elif self.mode == "completion":
                while error_times < 20:
                    try:
                        x = openai.Completion.create(
                            model=self.model,
                            prompt=prompt,
                            temperature=0.3,
                            top_p=0.5,
                            max_tokens=1024,
                            stop=stop
                        )
                        
                        return x.choices[0].text
                    except openai.error.InvalidRequestError as e:
                        print(e, flush=True)
                        return "Thought: \nAction: finish\nAction Input: {\"Answer\": \"I can not handle the task due to too long context.\"}"
                    except Exception as e:
                        print(e, '    ', prompt, flush=True)
                        error_times += 1
                        time.sleep(5)
            elif self.mode == "function_call":
                while error_times < 20:
                    try:
                        x = openai.ChatCompletion.create(
                            model=self.model,
                            messages=prompt,
                            temperature=0.3,
                            top_p=0.5,
                            max_tokens=1024,
                            stop=stop,
                            functions=functions,
                            function_call='auto'
                        )
                        message = x.choices[0].message
                        if message.content is None:
                            thought_message = ''
                        if message.get("function_call"):
                            action = message['function_call']['name']
                            action_input = message['function_call']['arguments'].replace(
                                '\n  ', '').replace('\n', '')
                        else:
                            action = ''
                            action_input = "{}"

                        return f"Thought: {thought_message}\nAction: {action}\nAction Input: {action_input}"
                    except openai.error.InvalidRequestError as e:
                        print(e, flush=True)
                        return "Thought: \nAction: finish\nAction Input: {\"Answer\": \"I can not handle the task due to too long context.\"}"
                    except Exception as e:
                        print(e, '    ', prompt, flush=True)
                        error_times += 1
                        time.sleep(5)
            return "Thought: \nAction: finish\nAction Input: {\"Answer\": \"I can not handle the task due to some technique issues, please try again latter.\"}"

        elif self.call_way == 'url':
            pass


    def add_message(self, message):
        self.conversation_history.append(message)

    def change_messages(self, messages):
        self.conversation_history = messages
    
    def display_conversation(self, detailed=False):
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "function": "magenta",
        }
        print("before_print"+"*"*50)
        for message in self.conversation_history:
            print_obj = f"{message['from']}: {message['value']} "
            if "function_call" in message.keys():
                print_obj = print_obj + \
                    f"function_call: {message['function_call']}"
            print_obj += ""
            print(
                colored(
                    print_obj,
                    role_to_color[message["from"]],
                )
            )
        print("end_print"+"*"*50)

    def parse(self, process_id, method):
        conv = get_conversation_template(self.template)
        if self.template == "tool":
            roles = {"human": conv.roles[0], "gpt": conv.roles[1]}
        elif self.template == "tool-single-round" or self.template == "tool-multi-rounds":
            roles = {"system": conv.roles[0], "user": conv.roles[1],
                     "function": conv.roles[2], "assistant": conv.roles[3]}

        self.time = time.time()
        conversation_history = self.conversation_history

        if self.mode == "completion":
            for message in conversation_history:
                conv.append_message(roles[message['from']], message['value'])
            conv.append_message(roles['assistant'], None)
            prompt = conv.get_prompt()
            prompt = compress_prompt(prompt, self.tokenizer)
        # print(prompt)
        elif self.mode == "chat":
            prompt = []
            for i, message in enumerate(conversation_history):
                if message["from"] != "function":
                    prompt.append({"role": message["from"], "content": message["value"]})
                else:
                    _, action, _ = react_parser(conversation_history[i-1]["value"])
                    prompt.append({"role": message["from"], "content": message["value"], "name": action.replace("Action: ", "").strip()})
            prompt = compress_prompt(prompt, self.tokenizer, mode="chat")
        predictions = self.prediction(prompt)
        print(f"Assistant: {predictions}")

        decoded_token_len = len(self.tokenizer.encode(predictions))
        if process_id == 0:
            print(
                f"[process({process_id})]prediction tokens: {decoded_token_len}")

        # react format prediction
        if method == 'tool':
            thought, action, action_input = react_parser(predictions)
            predictions = thought + action + action_input
            message = {
                "role": "assistant",
                "content": thought.replace("Thought: ", "").strip(),
                "function_call": {
                    "name": action.replace("Action: ", "").strip(),
                    "arguments": action_input.replace("Action Input: ", "").strip()
                }
            }
            return predictions, message
        elif method == 'general':
            return predictions
        
