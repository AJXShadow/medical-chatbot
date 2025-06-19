from src.helper import hugging_face_embeddings , text_split , load_pdf_file
from dotenv import load_dotenv , find_dotenv
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os
from langchain_pinecone import PineconeVectorStore

load_dotenv(find_dotenv())

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

extracted_data = load_pdf_file("e:/vs codes/medical-chatbot/Data")
text_chunks = text_split(extracted_data)
embeddings = hugging_face_embeddings()

pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "medical-assistant"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384, 
        metric="cosine", 
        spec=ServerlessSpec(
            cloud="aws", 
            region="us-east-1"
        )
    )

doc_search = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    index_name=index_name,
)
