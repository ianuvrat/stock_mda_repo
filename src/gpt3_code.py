import openai
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()
#Environment variables
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

def generate_text(prompt):
  openai.api_key = OPENAI_API_KEY
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.5,
    max_tokens=2400,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )
  text = response["choices"][0]["text"]
  return text

