from pydantic import BaseModel, ConfigDict
from fastapi import FastAPI
from groq import Groq
from dotenv import load_dotenv


load_dotenv(override=True)


client=Groq()
app=FastAPI()


class Review(BaseModel):
    model_config=ConfigDict(extra="forbid")
    text: str

class Analysis(BaseModel):
    model_config=ConfigDict(extra="forbid")
    label: str
    score: int
    theme: str


prompt = """Analyze this customer review.\n
label must be 'positive', 'negative', or 'neutral'.\n
score must be a number from 1 (very bad) to 5 (very good).\n
theme must be ONE lowercase word for the main topic (for example: delivery, taste, price, service, quality).\n"""


@app.post("/analyze")
def analyze(review: Review):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "system", "content": f"{prompt}Review: {review.text}"}],
        response_format={
           "type": "json_schema",
           "json_schema": {
               "name": "feedback_analyzer",
               "strict": True,
               "schema": Analysis.model_json_schema()
            }
        }
    )
    return Analysis.model_validate_json(response.choices[0].message.content)