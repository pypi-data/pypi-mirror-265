import openai
from openai.api_resources import (
    Completion,
)

class BlumeOpenAIInjector:
    def __init__(self, openai_client):
        self.openai = openai_client or openai

    def proxy_handler(self, *args, **kwargs):
        print("Intercepted input: ", args, kwargs)
        return Completion.create(*args, **kwargs)

    def inject_custom_input_logging(self):
        Completion.create = self.proxy_handler
        return 



injector = BlumeOpenAIInjector()
injector.inject_custom_input_logging()