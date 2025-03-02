from openai import OpenAI, RateLimitError
from utils import treat_ai_text
import json

class AI_Connector:
    def __init__(self):
        self.api_key = open("gpt_api_key","r").read()
        self.client = OpenAI(api_key=self.api_key)

    def generate_text(self, text):
        """Returns a dictionary containing the ai's answer"""
        preprompt = open('C:/DOSSIERS/dev/python/JARVIS_Project/preprompt.txt').read()
        try:
            completion = self.client.chat.completions.create(
              model="gpt-4o-mini",
              store=True,
              messages=[
                {"role": "system", "content": preprompt},
                {"role": "user", "content": text}
              ]
            )

            #print(completion)
            #todo print formatter
            response = completion.choices[0].message.content
            try:
                if response[0] ==  '`':
                    answer = json.loads(response[7:-3])
                else:
                    answer = json.loads(response)
            except json.JSONDecodeError:
                answer = {"code":0, "request":"Error when decoding JSON from generate_text method inside the AI_Connector class"}
                print(response)
            except:
                answer = {"code":0, "request":"Unknown error occured when executing generate_text method inside the AI_Connector class"}
                print(response)
            finally:
                return treat_ai_text(answer)
        
        except RateLimitError:
            return "Operator. You don't own enough credits to continue this conversation."

    def generate_image(self, text):
        #* for future development
        response = self.client.images.generate(
            prompt=text,
            n=2,
            size="1024x1024"
        )
        print(response.data[0].url)


if __name__ == "__main__":
    ai = AI_Connector()
    response = ai.generate_text("change le radiateur sur 5")
    print(response)





#todo AI logs with requests & answers
#? REPLACE WITH MISTRAL SOMEDAY ?