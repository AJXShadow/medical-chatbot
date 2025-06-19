from flask import Flask , render_template , jsonify , request
from src.helper import hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chat_models import ChatOllama
from dotenv import load_dotenv, find_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv(find_dotenv())

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

embeddings = hugging_face_embeddings()

index_name = "medical-assistant"

docsearch = PineconeVectorStore.from_existing_index(
    index_name = index_name,
    embedding=embeddings,
)

retrieval = docsearch.as_retriever(
    search_type="similarity", 
    search_kwargs={"k": 5}
)
llm = ChatOllama(model="llama3:8b", temperature=0.7)
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

qna_chain = create_stuff_documents_chain(
    llm , prompt_template
)

rag_chain = create_retrieval_chain(
    retrieval,
    qna_chain
)

# default route
@app.route('/')
def index():
    return render_template('chatbot.html')

@app.route("/get" , methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input" : msg})
    print("response:" , response["answer"])
    return str(response["answer"])
if __name__ == "__main__":
    app.run(host = "0.0.0.0" , port = 8000 , debug = True)

