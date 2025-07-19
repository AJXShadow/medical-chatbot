from flask import Flask , render_template , jsonify , request
import chainlit as cl
from src.helper import hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chat_models import ChatOllama
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from src.prompt import *
import os

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
# llm = ChatOllama(model="llama3:8b", temperature=0.7)
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
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
@cl.on_chat_start
async def start():
    chain = rag_chain
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hi, Welcome to Medical Bot. What is your Question?"
    await msg.update()
    cl.user_session.set("chain", chain)
    cl.user_session.set("chat_history", [])


@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")
    chat_history = cl.user_session.get("chat_history")
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True,
        answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    res = await chain.ainvoke({"input" : message.content , "chat_history" : chat_history}, callbacks=[cb])
    answer = res.get("answer", "No answer found")
    chat_history.append(("human" , message.content))
    chat_history.append(("ai" , answer))
    cl.user_session.set("chat_history", chat_history)
    sources = res.get("context", [])
    if sources:
        answer
    else:
        answer += "\nNo sources found"
    await cl.Message(content=answer).send()

