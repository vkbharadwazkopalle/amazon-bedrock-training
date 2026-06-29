from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from kb_retrieval import query_managed_kb, query_self_managed_kb

app = FastAPI()


class InferenceRequest(BaseModel):
    prompt: str
    kb_type: str = "managed"  # "managed" or "self_managed"


class InferenceResponse(BaseModel):
    prompt: str
    kb_type: str
    prediction: str


@app.get("/")
async def root():
    return {"message": "FastAPI inference service is running"}


@app.post("/infer", response_model=InferenceResponse)
async def infer(payload: InferenceRequest):
    # Route to the appropriate knowledge base based on kb_type
    try:
        if payload.kb_type == "self_managed":
            prediction = query_self_managed_kb(payload.prompt)
        else:
            prediction = query_managed_kb(payload.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return InferenceResponse(
        prompt=payload.prompt,
        kb_type=payload.kb_type,
        prediction=prediction,
    )


# To run the FastAPI application, use the following command in your terminal:
# uvicorn app:app --reload
