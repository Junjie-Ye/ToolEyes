import sys  # NOQA: E402
sys.path.append('/workspace/ToolEyes/Tool_Library')  # NOQA: E402
sys.path.append('/workspace/ToolEyes')  # NOQA: E402

from Code.utils import (
    replace_llama_with_condense
)
from Code.Inference.models import ToolLoRA, Tool, ChatGPT
from termcolor import colored
import re
import os
import json


class pipeline_runner:
    def __init__(self, args, add_retrieval=False, process_id=0, server=False):
        self.args = args
        self.add_retrieval = add_retrieval
        self.process_id = process_id
        self.server = server
        self.method = args.method
        self.backbone_model = self.get_backbone_model()
        if not self.server:
            self.task_list = self.generate_task_list()
        else:
            self.task_list = []

    def get_backbone_model(self):
        args = self.args
        if args.backbone_model == "tool":
            # ratio = 4 means the sequence length is expanded by 4, remember to change the model_max_length to 8192 (2048 * ratio) for ratio = 4
            ratio = int(args.max_sequence_length /
                        args.max_source_sequence_length)
            replace_llama_with_condense(ratio=ratio)
            if args.lora:
                backbone_model = ToolLoRA(
                    base_name_or_path=args.model_path, model_name_or_path=args.lora_path, max_sequence_length=args.max_sequence_length)
            else:
                backbone_model = Tool(
                    model_name_or_path=args.model_path, max_sequence_length=args.max_sequence_length)
        elif args.backbone_model == 'chatgpt':
            backbone_model = ChatGPT(
                api_key=args.api_key, orgnization=args.orgnization, url=args.url, mode=args.mode, model=args.openai_model)
        else:
            backbone_model = args.backbone_model
        return backbone_model

    def get_retriever(self):
        if False:
            return ToolRetriever(corpus_tsv_path=self.args.corpus_tsv_path, model_path=self.args.retrieval_model_path)

    def generate_task_list(self):
        args = self.args
        query_dir = args.input_query_file

        with open(query_dir, 'r', encoding='utf8') as f:
            task_list = json.load(f)
        return task_list

    def method_converter(self, backbone_model, method, conversations, process_id, history_sample=0):
        model = backbone_model
        messages = []
        history_sample = history_sample if history_sample <= len(
            conversations) else len(conversations)
        messages += conversations[:history_sample + 1]
        if method == 'tool':
            finish = False
            turn = 0
            while not finish:
                turn += 1
                print('-' * 30 + 'Turn ' + str(turn) + '-' * 30)
                model.change_messages(messages)
                model.display_conversation()
                try:
                    result, parse_result = model.parse(
                        process_id, method=method)
                except Exception as e:
                    print(f'exit with error: {e}')
                    finish = True
                    messages.append(
                        {"from": "assistant",
                         "value": "Thought: During execution, an error occurs.\nAction: finish\nAction Input: {\"answer\": \"I cannot handle the task.\"}"})
                    continue
                try:
                    messages.append({"from": "assistant", "value": result})
                    if self.args.max_turn >= 0:
                        observation: dict = self.post_process_response(
                            parse_result)
                        if observation.get('format', None) is not None:
                            messages.append(
                                {"from": "user", "value": observation['format']})
                        elif observation.get('error', None) is not None:
                            messages.append(
                                {"from": "function", "value": observation['error']})
                        elif observation.get('human', None) is not None:
                            answer = input()
                            messages.append(
                                {"from": "user", "value": answer})
                        elif observation.get('final', None) is not None:
                            if observation.get('add_format', False) is True:
                                messages[-1]["value"] += '"}'
                            finish = True
                        elif observation.get("observation", None) is not None:
                            function_result = observation['observation']
                            messages.append(
                                {"from": "function", "value": function_result})
                        if turn > self.args.max_turn and not finish:
                            messages.append(
                                {"from": "assistant", "value": "Thought: I cannot solve this task due to trying too many times.\nAction: finish\nAction Input: {\"answer\": \"I cannot handle the task.\"}"})
                            finish = True
                    else:
                        finish = True
                except Exception as e:
                    if turn > self.args.max_turn and not finish:
                        messages.append(
                            {"from": "assistant", "value": "Thought: I cannot solve this task due to trying too many times.\nAction: finish\nAction Input: {\"answer\": \"I cannot handle the task.\"}"})
                        finish = True

        elif method == 'general':
            finish = False
            turn = 0
            while not finish:
                turn += 1
                print('-' * 30 + 'Turn ' + str(turn) + '-' * 30)
                model.change_messages(messages)
                model.display_conversation()
                try:
                    result = model.parse(process_id, method=method)
                    messages.append({"from": "assistant", "value": result})
                except Exception as e:
                    print(f'exit with error: {e}')
                    finish = True
                    messages.append(
                        {"from": "assistant",
                         "value": "Thought: During execution, an error occurs.\nAction: finish\nAction Input: {\"answer\": \"I cannot handle the task.\"}"})
                    continue

                answer = input()
                messages.append(
                    {"from": "user", "value": answer})

                if answer == 'clear':
                    messages.clear()
                    messages.append({"from": "user", "value": "Hello!"})
                elif answer == 'quit' or turn > self.args.max_turn:
                    finish = True

        return messages.copy()

    def run_single_task(self, retriever=None, process_id=0, server=None, history_sample=0, id=None, conversations=None, path=None, **kwargs):
        output_file_path = self.args.output_answer_file
        split = output_file_path.split('/')
        os.makedirs('/'.join(split[:-1]), exist_ok=True)

        self.path = path
        result = self.method_converter(
            backbone_model=self.backbone_model,
            method=self.method,
            conversations=conversations,
            process_id=process_id,
            history_sample=history_sample
        )
        with open(output_file_path, "a", encoding='utf8') as writer:
            writer.write(json.dumps(
                {"id": id, "conversations": result, "path": path, **kwargs}, ensure_ascii=False) + '\n')

    def run(self):
        task_list = self.task_list
        print(f"total tasks: {len(task_list)}")
        output_file_path = self.args.output_answer_file
        if os.path.exists(output_file_path):
            new_task_list = []
            queries = []
            with open(output_file_path, 'r', encoding='utf8') as f:
                for line in f.readlines():
                    if line != '\n':
                        queries.append(json.loads(line)["id"])
            for task in task_list:
                query_id = task["id"]
                if query_id not in queries:
                    new_task_list.append(task)
            task_list = new_task_list

        print(f"undo tasks: {len(task_list)}")
        if self.add_retrieval:
            retriever = self.get_retriever()
        else:
            retriever = None
        for k, task in enumerate(task_list):
            print(
                f"process[{self.process_id}] doing task {k}/{len(task_list)}: {task['path']}---{task['id']}")
            self.run_single_task(
                retriever=retriever, process_id=self.process_id, history_sample=self.args.history_sample, **task)

    def post_process_response(self, parse_result):
        action = parse_result["function_call"]["name"]
        action_input = parse_result["function_call"]["arguments"]
        add_format = False
        if action.lower() == 'finish' and action_input[-2:] != '"}':
            action_input += '"}'
            add_format = True
        if action.lower() == 'finish':
            return {"final": action_input, "add_format": add_format}
        try:
            action_input = eval(action_input)
        except Exception as e:
            return {"format": "Your output format does not match the specified format, please revise your answer to follow the desired format.\n\nDesired format:\nThought: <The thought>\nAction: <The tool you take to>\nAction Input: <The parameters for the tool, you should provide a dict similar to {parameter_1: value_1, parameter_2: value 2} to call action.>"}
        # for item in ["apikey", "APIKEY", "APIkey", "api_key", "apiKey"]:
        #     if item in action_input:
        #         del action_input[item]

        if action.lower() == 'ask_to_user':
            return {"human": action_input}
        try:
            exec(
                f"""from {'.'.join(self.path.split('/')[-2:])}.tool import {action}""")
            result = eval(action)(**action_input)
            result = json.dumps(result, ensure_ascii=False)
            if len(self.backbone_model.tokenizer.encode(result)) > self.args.max_observation_length:
                result = self.backbone_model.tokenizer.decode(
                    self.backbone_model.tokenizer.encode(result)[1:self.args.max_observation_length])
            return {"observation": result, 'action': action}
        except Exception as e:
            return {"error": str(e), "action": action}
