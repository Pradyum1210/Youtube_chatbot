from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings



def create_vector_store(transcript):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.create_documents([transcript])

    embeddings = MistralAIEmbeddings(
        model="mistral-embed"
    )

    vector_store = FAISS.from_documents(chunks, embeddings)

    return vector_store