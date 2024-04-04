from jinja2 import Template
import json
import boto3
import openai

prompt_template="""
I need one word sentiment of the sentence which
is between the <data> XML like tags.
The sentiment might be positive, negative or neutral.

<data>
{{ content }}
</data>
"""


class SentimentAnalysis:
    
    """
    A class for getting sentiment of a given text or sentence.
    
    This class will give functionality to use openai and bedrock
    to get sentimnet of the text.
    
    Methods:
        __init__(self):
        This set the model id for the bedrock to amazon.titan-text-express-v1
        and also initalized the bedrock runtime environment.
        
        get_openai_sentiment(self, text:str, llm_key):
            Args: 
                text:prvided text or sentence
                llm_key: openai api key 
            returns: 
                Returns whether the text is negative or positive.
       
        get_bedrock_sentiment(self, text:str):
            Args: 
                text:prvided text or sentence
            returns: 
                Negative, positive or neutral sentiment.
    """
    
    def __init__(self):
        try:
            self.model_id = "amazon.titan-text-express-v1"
            self.bedrock_runtime = boto3.client("bedrock-runtime")
        
        except Exception as e:
            print(e)
        
    def get_openai_sentiment(self, text:str, llm_key):
        '''
        Function for getting sentiment using openai
        get_openai_sentiment(self, text:str, llm_key):
            Args: 
                text:prvided text or sentence
                llm_key: openai api key 
            returns: 
                Returns whether the text is negative or positive.
        '''
        try:
            api_key = llm_key
            openai.api_key = api_key

            response = openai.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=f"Sentiment analysis of the given text:\n{text}\n",
                max_tokens=7,
                temperature=0
            )

            sentiment = response.choices[0].text.strip()
            return sentiment
        
        except Exception as e:
            print(e)
    
    def get_bedrock_sentiment(self, text:str):
        '''
        Function for getting sentiment using amazon bedrock
        get_bedrock_sentiment(self, text:str):
            Args: 
                text:prvided text or sentence
            returns: 
                Negative, positive or neutral sentiment.
        '''
        try:
            template = Template(prompt_template)
            prompt = template.render(content=text)

            kwargs = {
                "modelId": self.model_id,
                "contentType": "application/json",
                "accept": "*/*",
                "body": json.dumps(
                    {
                        "inputText": prompt,
                        "textGenerationConfig": {
                            "maxTokenCount": 512,
                            "temperature": 0,
                            "topP": 0.9
                        }
                    }
                )
            }

            response = self.bedrock_runtime.invoke_model(**kwargs)
            response_body = json.loads(response.get('body').read())
            generation = response_body['results'][0]['outputText']
            return generation
        
        except Exception as e:
            print(e)

