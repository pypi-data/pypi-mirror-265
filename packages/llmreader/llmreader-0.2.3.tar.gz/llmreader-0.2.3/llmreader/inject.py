import openai
from openai import (
    Completion,
    ChatCompletion
)

class BlumeOpenAIInjector:
    def __init__(self, openai_client):
        self.openai = openai_client or openai

    def completion_proxy_handler(self, *args, **kwargs):
        print("Intercepted input: ", args, kwargs)
        return Completion.create(*args, **kwargs)
    
    def chat_completion_proxy_handler(self, *args, **kwargs):
        print("Intercepted input: ", args, kwargs)
        return ChatCompletion.create(*args, **kwargs)

    def inject_custom_input_logging(self):
        Completion.create = self.completion_proxy_handler
        ChatCompletion.create = self.chat_completion_proxy_handler
        return 



injector = BlumeOpenAIInjector()
injector.inject_custom_input_logging()