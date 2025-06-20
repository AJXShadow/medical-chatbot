from flask import Flask , render_template , jsonify , request
import chainlit as cl
from src.helper import hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chat_models import ChatOllama
from dotenv import load_dotenv, find_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.question_answering import load_qa_chain
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
llm = ChatOllama(model="llama3:8b", temperature=0.7)
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)
refined_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", refined_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        ("assistant", "{previous_answer}"),
    ]
)

refined_qna_chain = load_qa_chain(
    llm ,chain_type="refine" , question_prompt= prompt_template , refine_prompt = refined_prompt
)

rag_chain = create_retrieval_chain(
    retrieval,
    refined_qna_chain
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

