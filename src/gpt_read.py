import openai
import os

def summarize_paper_in_url(url):
    OpenAI_api_key = os.environ["OPENAI_API_KEY"]

    client = openai.OpenAI(api_key=OpenAI_api_key)

    return "Result message"