import streamlit as st
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.output_parser import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Inject custom CSS to style the title with a blue background and shadow effect
st.markdown("""
    <style>
    .title-container {
        background-color: #007BFF; /* Blue background */
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 30px;
    }

    .title-container h1 {
        font-family: 'Arial', sans-serif;
        font-size: 40px;
        font-weight: bold;
        color: white;
        text-shadow: 
            2px 2px 5px black, /* Black shadow */
            -2px -2px 5px red; /* Red shadow */
        animation: glowing 1.5s infinite;
        display: inline-block;
        padding: 10px 20px;
        margin: 0;
    }

    @keyframes glowing {
        0% { text-shadow: 2px 2px 5px black, -2px -2px 5px red, 0 0 5px yellow; }
        50% { text-shadow: 2px 2px 10px black, -2px -2px 10px red, 0 0 20px yellow; }
        100% { text-shadow: 2px 2px 5px black, -2px -2px 5px red, 0 0 5px yellow; }
    }
    </style>
""", unsafe_allow_html=True)

# Create the title within a styled label-like container
st.markdown("""
    <div class="title-container">
        <h1>Voice Assistant with PDF & Website Interaction 🤖</h1>
    </div>
""", unsafe_allow_html=True)



audio_image_url = "https://www.shutterstock.com/image-vector/voice-recognition-ai-personal-assistant-260nw-1517896490.jpg"
st.image(audio_image_url, width=800)

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url="Add_Qdrant_URL",
    api_key="Add Qdrant_api_key"
)
model_embedding = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Set your Google Gemini API key
api_key = "Google_API_Key"

# st.title("Voice Assistant with PDF & Website Interaction🤖")

# Initialize session state to store conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Sidebar for PDF upload, entering a website URL, and selecting a Gemini model
with st.sidebar:
    st.header("Options")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    website_url = st.text_input("Enter a Company Website URL")
    
    # Dropdown to choose Gemini model
    model_choice = st.selectbox("Select Google Gemini Model", 
                                ["gemini-1", "gemini-1.5", "gemini-1.5-pro", "gemini-1.5-flash"])

# Define collection name
collection_name = "pdf_chatbot"

# Check if collection exists, create if not
try:
    qdrant_client.get_collection(collection_name)
    st.success(f"Collection `{collection_name}` already exists.")
except:
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        force_recreate=True
    )
    st.success(f"Collection `{collection_name}` created.")

# Initialize the text splitter for both PDF and website content
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

# Process PDF content
if uploaded_file:
    pdf_reader = PdfReader(uploaded_file)
    pdf_text = ""
    for page_num in range(len(pdf_reader.pages)):
        pdf_text += pdf_reader.pages[page_num].extract_text()

    # Split PDF text into chunks
    pdf_chunks = text_splitter.split_text(pdf_text)

    # Convert PDF chunks to embeddings and store in Qdrant
    vectors = model_embedding.encode(pdf_chunks)
    points = [{"id": i, "vector": vector, "payload": {"text": chunk}} 
              for i, (vector, chunk) in enumerate(zip(vectors, pdf_chunks))]
    qdrant_client.upsert(collection_name=collection_name, points=points)
    # st.success("PDF content processed and stored in Qdrant.")

# Process website content
if website_url:
    try:
        response = requests.get(website_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        website_text = soup.get_text()

        # Split website content into chunks
        website_chunks = text_splitter.split_text(website_text)

        # Convert website chunks to embeddings and store in Qdrant
        vectors = model_embedding.encode(website_chunks)
        points = [{"id": i, "vector": vector, "payload": {"text": chunk}} 
                  for i, (vector, chunk) in enumerate(zip(vectors, website_chunks))]
        qdrant_client.upsert(collection_name=collection_name, points=points)
        # st.success(f"Website content processed and stored in Qdrant.")
    except Exception as e:
        st.error(f"Failed to scrape the website: {e}")

# Initialize English chat model template
english_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant. Please always respond in English."),
        ("human", "{human_input}"),
    ]
)

# Select and Initialize the AI model based on user choice
st.write(f"Using Gemini Model: {model_choice}")
model = ChatGoogleGenerativeAI(model=model_choice, google_api_key=api_key)

# Speech recognition or text input for query (English only)
text = speech_to_text(language="en", use_container_width=True, just_once=True, key="STT")

# Display previous conversation history
if st.session_state.conversation:
    st.subheader("Conversation History")
    for i, (user_msg, bot_reply) in enumerate(st.session_state.conversation):
        st.write(f"**You:** {user_msg}")
        st.write(f"**Bot:** {bot_reply}")

if text:
    st.subheader("Recognized Text:")
    st.write(text)

    # Embed the query for searching the content in Qdrant
    user_query_embedding = model_embedding.encode([text])[0]
    search_result = qdrant_client.search(
        collection_name=collection_name, query_vector=user_query_embedding, limit=1
    )

    if search_result:
        best_match = search_result[0].payload["text"]
        response_input = f"User Query: {text}\nBest Match from Content: {best_match}"

        # Generate the response using the chatbot model
        chain = english_template | model | StrOutputParser()
        
        with st.spinner("Generating response..."):
            res = chain.invoke({"human_input": response_input})

            st.subheader("Generated Response:")
            st.write(res)

            # Convert the response text to speech using gTTS and play the audio
            tts = gTTS(text=res, lang='en')
            tts.save("response.mp3")
            st.audio("response.mp3")

else:
    st.error("Could not recognize speech. Please speak again.")
