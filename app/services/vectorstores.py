from langchain_community.vectorstores import FAISS

# 저장
def vectorstore_data(splitter, embedding):
    vectorstore = FAISS.from_documents(splitter, embedding=embedding)
    # 로컬에 DB 저장
    vectorstore.save_local("MY_FAISS_INDEX")
    return vectorstore
