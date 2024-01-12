"""
Tool conversation prompt templates. Basically copy from FastChat.
"""

import dataclasses
from enum import auto, Enum
from typing import List, Any, Dict
import re


class SeparatorStyle(Enum):
    """Separator styles."""

    ADD_COLON_SINGLE = auto()
    ADD_COLON_TWO = auto()
    ADD_COLON_SPACE_SINGLE = auto()
    NO_COLON_SINGLE = auto()
    ADD_NEW_LINE_SINGLE = auto()
    DOLLY = auto()
    RWKV = auto()
    PHOENIX = auto()
    ONLY_LAST_ASSISTANT = auto()


@dataclasses.dataclass
class Conversation:
    """A class that keeps all conversation history."""

    # The name of this template
    name: str
    # The System prompt
    system: str
    # Two roles
    roles: List[str]
    # All messages
    messages: List[List[str]]
    # Offset of few shot examples
    offset: int
    # Separators
    sep_style: SeparatorStyle
    sep: str
    sep2: str = None
    # Stop criteria (the default one is EOS token)
    stop_str: str = None
    # Stops generation if meeting any token in this list
    stop_token_ids: List[int] = None

    def get_prompt(self) -> str:
        """Get the prompt for generation."""
        if self.sep_style == SeparatorStyle.ONLY_LAST_ASSISTANT:
            seps = [self.sep, self.sep2]
            ret = ""
            for i, (role, message) in enumerate(self.messages):
                if i + 1 == len(self.messages) and message:
                    ret += role + ": " + str(message) + seps[1]
                elif message:
                    ret += role + ": " + str(message) + seps[0]
                else:
                    ret += role + ":"
            return ret
        elif self.sep_style == SeparatorStyle.ADD_COLON_SINGLE:
            ret = self.system + self.sep
            for role, message in self.messages:
                if message:
                    ret += role + ": " + message + self.sep
                else:
                    ret += role + ":"
            return ret
        elif self.sep_style == SeparatorStyle.ADD_COLON_TWO:
            seps = [self.sep, self.sep2]
            ret = self.system + seps[0]
            for i, (role, message) in enumerate(self.messages):
                try:
                    if message:
                        ret += role + ": " + message + seps[i % 2]
                    else:
                        ret += role + ":"
                except:
                    continue
            return ret
        elif self.sep_style == SeparatorStyle.ADD_COLON_SPACE_SINGLE:
            ret = self.system + self.sep
            for role, message in self.messages:
                if message:
                    ret += role + ": " + message + self.sep
                else:
                    ret += role + ": "  # must be end with a space
            return ret
        elif self.sep_style == SeparatorStyle.NO_COLON_SINGLE:
            ret = self.system
            for role, message in self.messages:
                if message:
                    ret += role + message + self.sep
                else:
                    ret += role
            return ret
        elif self.sep_style == SeparatorStyle.ADD_NEW_LINE_SINGLE:
            ret = self.system + self.sep
            for role, message in self.messages:
                if message:
                    ret += role + "\n" + message + self.sep
                else:
                    ret += role + "\n"
            return ret
        elif self.sep_style == SeparatorStyle.DOLLY:
            seps = [self.sep, self.sep2]
            ret = self.system
            for i, (role, message) in enumerate(self.messages):
                if message:
                    ret += role + ":\n" + message + seps[i % 2]
                    if i % 2 == 1:
                        ret += "\n\n"
                else:
                    ret += role + ":\n"
            return ret
        elif self.sep_style == SeparatorStyle.RWKV:
            ret = self.system
            for i, (role, message) in enumerate(self.messages):
                if message:
                    ret += (
                        role
                        + ": "
                        + message.replace("\r\n", "\n").replace("\n\n", "\n")
                    )
                    ret += "\n\n"
                else:
                    ret += role + ":"
            return ret
        elif self.sep_style == SeparatorStyle.PHOENIX:
            ret = self.system
            for role, message in self.messages:
                if message:
                    ret += role + ": " + "<s>" + message + "</s>"
                else:
                    ret += role + ": " + "<s>"
            return ret
        else:
            raise ValueError(f"Invalid style: {self.sep_style}")
    
    def condense_user_input(self,user_input,conv,roles,conversations,tokenizer):
        user_input_token = tokenizer.tokenize(user_input)
        print(len(user_input_token))
        # encodings = tokenizer(user_input)
        # user_input_ids = encodings['input_ids']
        if len(user_input_token) > 8000 :
            # if len(conversations) <= 4 :
            #     user_input_ids = user_input_ids[:8192]
            #     user_input = tokenizer.decode(user_input_ids)  + '\n' + 'Assistant:'
            #     print(len(user_input_ids))
            #     return user_input[3:]
            # else:
            del_idx = 3
            self.messages = []
            while conversations[del_idx]['value'] != '' and del_idx != len(conversations) -1 :
                conversations[del_idx]['value'] = ''
                conversations.pop(del_idx)
                del_idx += 1
            for item in conversations:
                role = roles[item["from"]]
                conv.append_message(role, item["value"])
            conv.append_message(roles["assistant"], None)
            user_input = conv.get_prompt()
        return user_input

    def append_message(self, role: str, message: str):
        """Append a new message."""
        self.messages.append([role, message])

    def to_gradio_chatbot(self):
        """Convert the history to gradio chatbot format"""
        ret = []
        for i, (role, msg) in enumerate(self.messages[self.offset :]):
            if i % 2 == 0:
                ret.append([msg, None])
            else:
                ret[-1][-1] = msg
        return ret

    def to_openai_api_messages(self):
        """Convert the conversation to OpenAI chat completion format."""
        ret = [{"role": "system", "content": self.system}]

        for i, (_, msg) in enumerate(self.messages[self.offset :]):
            if i % 2 == 0:
                ret.append({"role": "user", "content": msg})
            else:
                if msg is not None:
                    ret.append({"role": "assistant", "content": msg})
        return ret

    def copy(self):
        return Conversation(
            name=self.name,
            system=self.system,
            roles=self.roles,
            messages=[[x, y] for x, y in self.messages],
            offset=self.offset,
            sep_style=self.sep_style,
            sep=self.sep,
            sep2=self.sep2,
            stop_str=self.stop_str,
            stop_token_ids=self.stop_token_ids,
        )

    def dict(self):
        return {
            "name": self.name,
            "system": self.system,
            "roles": self.roles,
            "messages": self.messages,
            "offset": self.offset,
        }


# A global registry for all conversation templates
conv_templates: Dict[str, Conversation] = {}


def register_conv_template(template: Conversation, override: bool = False):
    """Register a new conversation template."""
    if not override:
        assert template.name not in conv_templates, f"{template.name} has been registered."
    conv_templates[template.name] = template


def get_conv_template(name: str) -> Conversation:
    """Get a conversation template."""
    return conv_templates[name].copy()


# tool template
register_conv_template(
    Conversation(
        name="tool",
        system="A chat between a curious user and an artificial intelligence assistant who can use external tools and APIs to solve the user's question. "
        "The assistant gives tools and APIs calling processes or final answer to the human's question.",
        roles=("Human", "Assistant"),
        messages=(),
        offset=0,
        sep_style=SeparatorStyle.ADD_COLON_TWO,
        sep=" ",
        sep2="</s>",
    )
)

# tool with openai function template
register_conv_template(
    Conversation(
        name="tool-single-round",
        system="",
        roles=("System", "User", "Function", "Assistant"),
        messages=(),
        offset=0,
        sep_style=SeparatorStyle.ONLY_LAST_ASSISTANT,
        sep="\n",
        sep2="</s>",
    )
)
