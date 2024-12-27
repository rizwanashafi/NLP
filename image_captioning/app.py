import streamlit as st
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from PIL import Image

# Load the pre-trained model and necessary components
@st.cache_resource
def load_model():
    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    return model, feature_extractor, tokenizer, device

model, feature_extractor, tokenizer, device = load_model()

# Define prediction function
def predict_caption(image):
    if image.mode != "RGB":
        image = image.convert(mode="RGB")
    pixel_values = feature_extractor(images=[image], return_tensors="pt").pixel_values.to(device)
    gen_kwargs = {"max_length": 16, "num_beams": 4}
    output_ids = model.generate(pixel_values, **gen_kwargs)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
    return caption

# Streamlit App Layout
st.title("Image Caption Generator")
st.write("Upload an image to generate its caption using a pre-trained model.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    try:
        # Open the image
        image = Image.open(uploaded_file)

        # Display the uploaded image
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Generate and display the caption
        with st.spinner("Generating caption..."):
            caption = predict_caption(image)
        st.success("Caption generated!")
        st.write(f"**Caption**: {caption}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
