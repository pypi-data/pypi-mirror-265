from typing import Optional, List

from .mock_ai import MockAI

####### ENVIRONMENT VARIABLES ###################
mock_ai = MockAI()

def mock_completion(messages: List, model: Optional[str] = None, **kwargs):
    last_message = messages[-1]
    if isinstance(last_message, dict):
        if "content" in last_message:
            message = last_message.get("content")
        elif "text" in last_message:
            message = last_message.get("text")
        else:
            raise KeyError
    else:
        message = str(last_message)

    return mock_ai.get_completion(message)


def set_config(json_file_path: str):
    mock_ai.set_config(json_file_path)