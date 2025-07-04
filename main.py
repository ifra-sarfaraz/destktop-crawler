from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.crawler import crawl_dir
from backend.indexer import build_index, save_index, load_index
from backend.search import search_query
from backend.rag import generate_rag_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str
    use_stemming: bool = False
    method: str = "tfidf"

class CrawlRequest(BaseModel):
    folder_path: str

@app.post("/crawl")
async def crawl(crawl_request: CrawlRequest = Body(...)):
    folder_path = crawl_request.folder_path
    crawl_dir(folder_path)
    index = build_index(folder_path)
    save_index(index, "index.json")
    return {"status": f"Indexed files from {folder_path}"}

@app.post("/search")
async def search(req: SearchRequest):
    index = load_index("index.json")
    results = search_query(req.query, index, req.method, req.use_stemming)
    return {"results": results}

@app.post("/rag")
async def rag(req: SearchRequest):
    index = load_index("index.json")
    docs = search_query(req.query, index, req.method, req.use_stemming)
    if not docs:
        return {"answer": f"No documents found for query '{req.query}'."}
    answer = generate_rag_answer(docs, req.query)
    return {"answer": answer}