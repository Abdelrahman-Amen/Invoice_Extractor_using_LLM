import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure the Google Generative AI library with the API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Instantiate the generative model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to generate a response from the model
def get_response(input, image, prompt):
    # Generate content based on the input, image, and prompt
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to handle image setup for AI processing
def input_image_setup(uploaded_file):
    # Ensure a file has been uploaded
    if uploaded_file is not None:
        # Read the uploaded file as bytes
        bytes_data = uploaded_file.getvalue()

        # Prepare the image in the required format
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Determine the file type (e.g., image/jpeg)
                "data": bytes_data  # The binary content of the image
            }
        ]
        return image_parts
    else:
        # Raise an error if no file is uploaded
        raise FileNotFoundError("No file uploaded")

# Set the Streamlit app page configuration
st.set_page_config(page_title="Gemini Image Extractor")

# Create a header for the application
st.header("Invoice Extractor Application")

# Input field for users to enter a custom prompt
input = st.text_input("Input Prompt: ", key="input")

# Original input prompt provided to the AI model
input_prompt = """
               You are a specialist in analyzing and interpreting invoice data.  
               Your task is to review input images provided as invoices and generate answers based on the content of these images.  
               You will receive queries related to the invoices, and you should respond accurately and concisely.
               """


# File uploader to accept image files
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Variable to store the uploaded image
image = ""
if uploaded_file is not None:
    # Open the uploaded image using PIL
    image = Image.open(uploaded_file)
    # Display the uploaded image on the Streamlit app
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button to trigger the processing of the image and prompt
submit = st.button("Tell me about the image")

if submit:
    # Process the uploaded image for AI model input
    image_data = input_image_setup(uploaded_file)
    # Get the response from the AI model based on the input and image
    response = get_response(input_prompt, image_data, input)
    # Display the AI model's response
    st.subheader("The Response is")
    st.write(response)
