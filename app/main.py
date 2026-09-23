from contextlib import asynccontextmanager
import os
from app.indexer import search_moss
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.files import read_project_files
from app.router import choose_model
from app.llm import generate_local_answer
from app.gemini import generate_gemini_answer
from app.privacy import prepare_cloud_context


load_dotenv()


# --------------------------------------------------
# Application lifespan
# --------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("NOVA: Running without Moss during development.")
    yield


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="Local AI Developer Copilot",
    version="0.1.0",
    lifespan=lifespan,
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://nova-frontend-qf6r.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Models
# --------------------------------------------------

class FileResponse(BaseModel):
    count: int
    files: list[dict]


# --------------------------------------------------
# Root
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "name": "Local AI Developer Copilot",
        "status": "running",
    }


# --------------------------------------------------
# Health
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "gemini_configured": bool(
            os.getenv("GEMINI_API_KEY")
        ),
    }


# --------------------------------------------------
# Files
# --------------------------------------------------

@app.get("/files", response_model=FileResponse)
def files():

    documents = read_project_files(
        "data/sample-project"
    )

    return FileResponse(
        count=len(documents),
        files=documents,
    )

@app.get("/chat")
async def chat(query: str):

    model = choose_model(query)

    # -------------------------
    # MOSS RETRIEVAL
    # -------------------------

    retrieval_method = "moss"

    try:
        moss_result = await search_moss(query)

        retrieved_docs = moss_result.docs

        context_parts = []

        for doc in retrieved_docs:
            context_parts.append(
                f"File: {doc.metadata.get('path', 'unknown')}\n"
                f"{doc.text}"
            )

        context = "\n\n".join(context_parts)

        retrieval_latency = moss_result.time_taken_ms

    except Exception as e:

        print("========== MOSS ERROR ==========")
        print(f"Error: {e}")
        print("================================")

        retrieval_method = "local-fallback"

        documents = read_project_files(
            "data/sample-project"
        )

        context = "\n\n".join(
            f"File: {doc['path']}\n{doc['content']}"
            for doc in documents
        )

        retrieval_latency = None

    # -------------------------
    # LOCAL QWEN
    # -------------------------

    if model == "local":

        answer = await generate_local_answer(
            query,
            context,
        )

        return {
            "query": query,
            "model": "qwen",
            "retrieval": retrieval_method,
            "retrieval_latency_ms": retrieval_latency,
            "answer": answer,
        }

    # -------------------------
    # PRIVACY GATEWAY
    # -------------------------

    safe_context = prepare_cloud_context(
        context
    )

    # -------------------------
    # GEMINI / SMALL CLOUD
    # -------------------------

    answer = await generate_gemini_answer(
        query,
        safe_context,
    )

    return {
        "query": query,
        "model": "gemini",
        "retrieval": retrieval_method,
        "retrieval_latency_ms": retrieval_latency,
        "privacy_gateway": "enabled",
        "answer": answer,
    }