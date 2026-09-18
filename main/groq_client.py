from groq import Groq as Grok
import os
from dotenv import load_dotenv

load_dotenv()

class Groq:
    models: list = ["openai/gpt-oss-120b","openai/gpt-oss-20b"]
    @staticmethod
    def run(content: str):

        LAPI = ["GROK_API_KEY","GROK_API_KEY1","GROK_API_KEY2"]
        messages = [
            {
                "role": "user",
                "content": f"{content}\n\n\nFor the questions requiring to return an image in base64, just return 'empty' nothing else\n\n\nYou must view the data and perform proper data cleaning, to make sure the answer is accurate\n\n\nOnly give exact answer do not try to modify it."+"\n\n\nFor any problem required a base64 image, you must return 'empty' as string, and must not return the actual base64 image. This is important. All the numeric answers must be in proper integer/float format."
            }
        ]   

        for model in Groq.models:
            for j in range(3):
                try:
                    client = Grok(api_key=os.getenv(LAPI[j]))
                    
                    completion = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=1,
                        max_completion_tokens=8192,
                        top_p=1,
                        reasoning_effort="high" if model != "deepseek-r1-distill-llama-70b" else None,
                        stream=True,
                        stop=None,
                        tools=[{"type": "code_interpreter"}] if model != "deepseek-r1-distill-llama-70b" else None
                    )

                    ans = ""
                    for chunk in completion:
                        delta_content = chunk.choices[0].delta.content
                        if delta_content:
                            ans += delta_content
                    
                    if ans.strip():
                        print("Grok Executed Succesfully.")
                        return ans
                    
                except Exception as e:
                    print(f"Error with model {model}: {e}")
                    continue  

        return None


if __name__ == '__main__':
    question = open('test_cases/test_question.txt', 'r').read()
    print(Groq.run(question))