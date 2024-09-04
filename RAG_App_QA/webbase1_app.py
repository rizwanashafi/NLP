import os
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings

# Load environment variables from .env file
# load_dotenv()
google_api_key = os.getenv("AIzaSyDNEJckKCWPexzXCLwYdmEMorqH_UH90As")

# Stylish title with icons and markdown
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)

st.markdown("""
    <div style="
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin: 20px 0;
    ">
        <i class="fas fa-cogs" style="font-size: 24px; margin-right: 10px; color: #FF5733;"></i>
        <i class="fas fa-rocket" style="font-size: 24px; margin-right: 10px; color: #FFBD33;"></i>
        <h1 style="
            background: linear-gradient(45deg, #FF5733, #FFBD33);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
            margin: 0;
            font-size: 36px;
        ">RAG Webbase Application </h1>
        <i class="fas fa-chart-line" style="font-size: 24px; margin-left: 10px; color: #FF5733;"></i>
        <i class="fas fa-globe" style="font-size: 24px; margin-left: 10px; color: #FFBD33;"></i>
    </div>
""", unsafe_allow_html=True)

# ya try use kia but function ni banay koi ap na 
# phly meny just loade kia tha y try: gpt sy lia tha ok let see
# Load documents from the website
try:
    loader = WebBaseLoader("http://www.connectlogistics.pk/")
    docs = loader.load()
except Exception as e:
    st.error(f"Error loading documents: {e}")
    st.stop()

# Split the documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = text_splitter.split_documents(docs)

# Create a vector store for document retrieval using HuggingFace embeddings
vectorstore = FAISS.from_documents(documents=docs, embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))

# Set up the retriever and language model
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3, max_tokens=400, google_api_key=google_api_key)

# System prompt for the language model
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if query := st.chat_input("What is your question?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)

    # Generate a response using the RAG chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt_template)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        with st.spinner("Thinking..."):
            try:
                result = rag_chain.invoke({"input": query})
                full_response = result['answer']
            except Exception as e:
                full_response = f"Error: {e}"

        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})


