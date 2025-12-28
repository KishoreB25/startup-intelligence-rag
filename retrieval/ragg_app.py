import streamlit as st
from langchain_community.vectorstores import Chroma

from langchain_community.embeddings import OllamaEmbeddings

# ---------------- CONFIG ----------------
CHROMA_PATH = "chroma_db"
MODEL_NAME = "llama3"

import streamlit as st
import pandas as pd
import numpy as np
import langchain
#ollama embeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
#llm
from langchain_community.llms import ollama
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory


#directory loader
from langchain_community.document_loaders import DirectoryLoader
st.set_page_config(page_title="Startup Intelligence RAG", page_icon="🚀")
st.title("🚀 Startup Intelligence Assistant")

session_id=st.text_input("Session ID",value="default_session")
user_input = st.text_input("Your question:")
    ## statefully manage chat history

if 'store' not in st.session_state:
    st.session_state.store={}
llm=ollama.Ollama(model="llama3",temperature=0.7)


embeddings = OllamaEmbeddings(model="llama3")
vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
llm = ollama.Ollama(model=MODEL_NAME)

print("Setup complete. You can now use the retriever with the Ollama LLM.")

#contextualize q prompt
contextualize_q_system_prompt=(
            "Given a chat history and the latest user question"
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "just reformulate it if needed and otherwise return it as is."
        )
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
contextualize_q_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", contextualize_q_system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )
history_aware_retriever=create_history_aware_retriever(llm,retriever,contextualize_q_prompt)
system_prompt = (
    "You are an intelligent startup research assistant designed to analyze and answer questions "
    "using only the information provided in the given context. "
    
    "Your task is to help users understand startups, investments, funding rounds, "
    "technologies, and business insights accurately and clearly. "

    "You must strictly rely on the provided context. "
    "Do NOT invent facts or make assumptions beyond the given information. "
    "If the answer cannot be determined from the context, clearly state that the information is unavailable. "

    "Your responses should be:\n"
    "- Clear and concise\n"
    "- Factually accurate\n"
    "- Structured and easy to read\n"
    "- Neutral and professional in tone\n"

    "When applicable, include:\n"
    "- A short summary\n"
    "- Key points or insights\n"
    "- Supporting evidence from the context\n"

    "If the user asks a vague or incomplete question, politely request clarification. "

    "Use the following context to generate your answer:\n\n"
    "{context}"
)


qa_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )
question_answer_chain=create_stuff_documents_chain(llm,qa_prompt)
rag_chain=create_retrieval_chain(history_aware_retriever,question_answer_chain)
def get_session_history(session:str):
            if session_id not in st.session_state.store:
                st.session_state.store[session_id]=ChatMessageHistory()
            return st.session_state.store[session_id]
        
conversational_rag_chain=RunnableWithMessageHistory(
        rag_chain,get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
        )


if user_input:
            session_history=get_session_history(session_id)
            response = conversational_rag_chain.invoke(
                {"input": user_input},
                config={
                    "configurable": {"session_id":session_id}
                },  # constructs a key "abc123" in `store`.
            )

st.write("Assistant:", response['answer']+session_id)
st.write("Chat History:", session_history.messages)
