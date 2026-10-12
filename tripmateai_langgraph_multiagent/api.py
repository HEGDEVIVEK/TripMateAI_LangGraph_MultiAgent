from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from tripmateai_langgraph_multiagent.graph_execute import run_tripMate_agent
from tripmateai_langgraph_multiagent.chat_history import get_saved_all_chats_postgres, get_saved_chat_with_thread_id, get_saved_all_chats_mongodb

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["GET","POST"],
    allow_headers=["Content-Type"],
)


class ChatRequest(BaseModel):
    user_query: str = Field(min_length=1)
    thread_id: str = Field(min_length=1)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    result = run_tripMate_agent(
        user_query=request.user_query,
        thread_id=request.thread_id,
    )

    return {
        "thread_id": result["thread_id"],
        "messages": result["messages"],
    }

@app.get("/all-chat-history")
def all_chat_history():
    return get_saved_all_chats_mongodb()

@app.get("/chat-history-threadid/{thread_id}")
def chat_history_threadid(thread_id:str):
    return get_saved_chat_with_thread_id(thread_id=thread_id)