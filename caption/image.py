# import streamlit as st
# from transformers import BlipProcessor, BlipForConditionalGeneration
# from PIL import Image
# import torch

# # Load the processor and model
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
# model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# # Streamlit App
# st.title("Image Captioning App")
# # st.write("Upload an image, and the app will generate a caption describing it!")

# # File uploader
# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

# if uploaded_file is not None:
#     # Load the image
#     raw_image = Image.open(uploaded_file).convert('RGB')
#     st.image(raw_image, caption="Uploaded Image", use_column_width=True)

#     # Preprocess the image
#     inputs = processor(images=raw_image, return_tensors="pt")

#     # Generate caption
#     with st.spinner("Generating caption..."):
#         output = model.generate(**inputs)
#         caption = processor.decode(output[0], skip_special_tokens=True)

#     # Display the caption
#     st.success("Caption generated!")
#     st.write(f"**Generated Caption:** {caption}")


import streamlit as st
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import torch
import random

HASHTAGS = [
    "#Amazing #Photography #Stunning",
    "#InstaGood #PicOfTheDay #Beautiful",
    "#PhotoOfTheDay #Love #Art",
    "#Lifestyle #Mood #Aesthetic"
]

@st.cache_resource
def load_model():
    processor = AutoProcessor.from_pretrained("microsoft/git-base")
    model = AutoModelForCausalLM.from_pretrained("microsoft/git-base")
    return processor, model

processor, model = load_model()

st.title("Social Media Caption Generator")
st.write("Generate engaging captions for your social media posts!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption="Your Image", use_container_width=True)
    
    inputs = processor(images=image, return_tensors="pt")
    
    with st.spinner("Creating your caption..."):
        output = model.generate(
            **inputs,
            max_length=50,
            num_beams=3,
            num_return_sequences=3,
            no_repeat_ngram_size=2
        )
        captions = [processor.decode(o, skip_special_tokens=True) for o in output]
        
        for i, caption in enumerate(captions):
            styled_caption = f"✨ {caption} ✨\n{random.choice(HASHTAGS)}"
            st.text_area(f"Caption Option {i+1}", styled_caption, height=100)

    if st.button("Generate More"):
        st.experimental_rerun()
