from fastapi import APIRouter

from app.services.embeddings import embed_data
from app.services.loaders import loader_data
from app.services.retrievers import retriever_data
from app.services.splitters import splitter_data
from app.services.vectorstores import vectorstore_data

router = APIRouter()


@router.post("/save")
async def loaders():
    loader = loader_data()
    splitter = splitter_data(loader)
    embedding = embed_data()
    vectorstore = vectorstore_data(splitter, embedding)
    return {"vectorstore": vectorstore}


@router.get("/get/{query}")
async def retrievers(query: str):
    embedding = embed_data()
    retriever = retriever_data(query, embedding)
    return {"retriever": retriever}
