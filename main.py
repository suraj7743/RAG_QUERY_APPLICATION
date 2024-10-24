from fastapi import FastAPI
from pydantic import BaseModel
from index.index import create_query_engine

app = FastAPI()

def success_message(msg: str = "Success", body: any = None, status_code: int = 200):
    response = {"msge":msg, status_code:status_code}
    if body:
        response['body']=body
    return response


class QueryRequest(BaseModel):
    field: str
    question: str

class QueryResponse(BaseModel):
    answer: str

@app.post("/query")
async def query_backend(request: QueryRequest):
    query_engine = create_query_engine(field=request.field)
    response = query_engine.query(request.question)
    return success_message(body=response.response)

# Command to run: uvicorn filename:app --reload
