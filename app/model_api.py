from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import uvicorn

app = FastAPI()
model = pipeline("sentiment-analysis", model="blanchefort/rubert-base-cased-sentiment")

class TextRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(request: TextRequest):
    result = model(request.text)[0]
    return {
        "label": result["label"],
        "score": result["score"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)