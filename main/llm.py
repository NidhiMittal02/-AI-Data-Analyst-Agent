from langchain_core.language_models.llms import LLM
from typing import Optional, List
import requests
import os
from dotenv import load_dotenv
import random

load_dotenv()

key = os.getenv('AI_PIPE_API_KEY')
key1 = os.getenv('AI_PIPE_API_KEY1')
key2 = os.getenv('AI_PIPE_API_KEY2')
key3 = os.getenv('AI_PIPE_API_KEY3')
key4 = os.getenv('AI_PIPE_API_KEY4')
pkey = os.getenv('PERPLEXITY_API_KEY')
gkey = os.getenv('GROK_API_KEY')

keys = {
    "PER":pkey,
    "AI":key,
    "AI1":key1,
    "AI2":key2,
    "AI3":key3,
    "AI4":key4
}

class AIPipeLLM(LLM):
    
    # api_url: str = "https://api.perplexity.ai/chat/completions"
    api_key: Optional[str] = None

    @property
    def _llm_type(self) -> str:
        return "aipipe"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        print(prompt)
        ty = 'AI'
        if random.randint(0,4)!=0:
            ty += str(random.randint(1,4))

        for i in range(6):
            # randomnum = random.randint(0,4)
            if i==5:
                ty = "PER"
            api_url = "https://aipipe.org/openrouter/v1/chat/completions" if ty!="PER" else "https://api.perplexity.ai/chat/completions"
            try:
                headers = {
                    "Authorization": f"Bearer {keys[ty]}",
                    "Content-Type": "application/json"
                }
                payload = {
                    # "model": "sonar-pro",
                    "model": "openai/gpt-4.1" if ty!='PER' else 'sonar-pro',
                    "messages": [{"role": "user", "content": prompt}],
                    # "max_tokens": 1000
                }
                if ty=='PER':
                    payload['max_tokens'] = 1000

                response = requests.post(api_url, headers=headers, json=payload)

                return response.json()['choices'][0]['message']['content']
            except:
                ty = 'AI'
                if random.randint(0,4)!=0:
                    ty += str(random.randint(1,4))

        return None
    
    def invoke(self,prompt,stop=None):
        for i in range(5):
            # randomnum = random.randint(0,4)
            randomnum = 0
            key = keys[randomnum]
            try:
                headers = {
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "sonar-pro",
                    # "model": "openai/gpt-4.1",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 500  
                }

                response = requests.post(self.api_url, headers=headers, json=payload)
                return response.json()['choices'][0]['message']['content']
            except:
                pass
        return None

if __name__=='__main__':
    templlm = AIPipeLLM()
    print(templlm.invoke("What is the capital of India?"))