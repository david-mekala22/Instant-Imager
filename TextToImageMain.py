import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os
import time

os.environ["HUGGINGFACE_API_KEY"] = "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"

# Set page configuration
st.set_page_config(
    page_title="Instant Imager",
    page_icon="🎨",
    layout="wide",  # Change from "centered" to "wide"
    initial_sidebar_state="auto",
)

# Initialize session state to store previously generated prompts and images
if 'history' not in st.session_state:
    st.session_state.history = []

# Inject custom CSS for styling
st.markdown(
    """
    <style>
        /* Background styling */
        .main {
            background: linear-gradient(145deg, #1f1f1f, #2b2b2b); /* Black with grey shine */
            color: #e0e0e0; /* Light grey text */
        }

        /* Title styling */
        .title {
            font-size: 2.5em;
            font-weight: bold;
            color: #FFA500; /* Orange */
            text-align: center;
            position: relative;
        }

        /* Input box styling */
        .stTextInput > div {
            background-color: #2c2c2c; /* Dark grey */
            border: 2px solid #f39c12; /* Orange */
            border-radius: 5px;
            color: #2c2c2c;
            opacity: 10;
            font-family: verdana, 'open sans', sans-serif;
            position: relative;
        }

        /* Button styling */
        .stButton button {
            background-color: #f39c12; /* Orange */
            color: black;
            font-size: 1.2em;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: 0.3s;
        }

        .stButton button:hover {
            background-color: #e67e22; /* Lighter orange */
        }

        /* Generated image placeholder */
        .image-box {
            border: 2px solid #f39c12; /* Orange */
            border-radius: 10px;
            padding: 10px;
            background-color: #2c2c2c; /* Dark grey */
            color: white; /* White text for placeholder message */
            margin-top: 20px;
            text-align: center;
        }
        /* Custom loading animation style */
        .loading-container {
            border: 2px solid gold; /* Gold border */
            border-radius: 15px; /* Rounded corners */
            padding: 20px;
            text-align: center;
            background-color: #2c2c2c; /* Dark background */
            margin-top: 20px;
        }

        .loading-container img {
            border-radius: 10px; /* Optional, if you want to round the corners of the GIF as well */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Styling for background color
pg_bg_color = """
<style>
[data-testid="stAppViewContainer"]{
background-color: #000;
border: 5px solid rgba(255, 255, 255, 0.4);
border-radius: 15px; /* Rounded corners */
background: linear-gradient(to bottom, #000000, #000000); /* Gradient background */
opacity: 0.8;
}
</style>
"""
st.markdown(pg_bg_color, unsafe_allow_html=True)

# Styling for text box
custom_css = """
<style>
textarea {
    background: rgba(255, 255, 255, 0.7); /* Semi-transparent white background */
    border: 2px solid rgba(255, 255, 255, 0.4); /* Soft border with transparency */
    border-radius: 15px; /* Rounded corners */
    box-shadow: 0px 4px 30px rgba(0, 0, 0, 0.1); /* Subtle shadow for floating effect */
    backdrop-filter: blur(10px); /* Glassmorphism blur effect */
    padding: 15px; /* Add padding for better UX */
    font-size: 16px; /* Adjust font size */
    font-family: 'Arial', sans-serif; /* Font style */
    color: #333; /* Text color */
}

textarea:focus {
    outline: none; /* Remove outline on focus */
    border-color: rgba(255, 255, 255, 0.8); /* Highlight border on focus */
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar styling
sidebar_style = """
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #191970, #000000); /* Gradient background */
        padding: 15px;
        border-radius: 15px; /* Rounded corners */
    }

    [data-testid="stSidebar"] h1 {
        color: gold; /* Gold color */
        text-shadow: 0px 4px 10px rgba(255, 215, 0, 0.7); /* Floating effect with shadow */
        border: 2px solid gold; /* Gold border */
        padding: 10px;
        border-radius: 10px; /* Rounded corners */
        text-align: center;
    }
</style>
"""
st.markdown(sidebar_style, unsafe_allow_html=True)

# Sidebar Navbar
st.sidebar.title("Instant Imager")
st.sidebar.markdown(
    """
    <div ></br>
  
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown(
    """
    <div style="
        padding: 10px; /* Padding inside the box */
        text-align: center; /* Center the text */
        border: 2px solid gold; /* Gold border */
        box-shadow: 0px 4px 10px rgba(255, 215, 0, 0.7); /* Floating effect */
        font-size: 16px; /* Font size */
        font-weight: bold; /* Bold text */
    "><h2> .</h2>
       
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <style>
    @keyframes slideFromTop {
        0% {
            transform: translateY(-100%);
            opacity: 0;
        }
        50% {
            transform: translateY(0);
            opacity: 1;
        }
        100% {
            transform: translateY(-100%);
            opacity: 0;
        }
    }
    
    .slide-text {
        background: rgba(255, 215, 0, 0.2); /* Light gold semi-transparent background */
        border: 2px solid gold; /* Gold border */
        border-radius: 15px; /* Rounded corners */
        padding: 10px; /* Padding inside the box */
        text-align: center; /* Center the text */
        box-shadow: 0px 4px 10px rgba(255, 215, 0, 0.7); /* Floating effect */
        font-size: 16px; /* Font size */
        color: gold; /* Gold text color */
        font-weight: bold; /* Bold text */
        animation: slideFromTop 30s infinite; /* Infinite animation every 30 seconds */
    }
    </style>
    <div class="slide-text">
        Where Imagination Turns Into Visualization
    </div></br>
    """,
    unsafe_allow_html=True
)


# styling for horizantal slider
slider_css = """
<style>
@keyframes circular-slide {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

.slider-container {
    overflow: hidden;
    white-space: nowrap;
    position: relative;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.8); /* Semi-transparent black */
    border: 2px solid gold;
    border-radius: 15px;
    padding: 10px 0;
    margin: 20px 0;
    box-shadow: 0px 4px 10px rgba(255, 215, 0, 0.7);
}

.slider-content {
    display: inline-block;
    animation: circular-slide 20s linear infinite;
    font-size: 2em;
    color: gold;
    font-family: Arial, sans-serif;
    text-shadow: 2px 2px 4px #000000; /* Glow effect */
}

.character {
    display: inline-block;
    margin: 0 20px;
}
</style>

<div class="slider-container">
    <div class="slider-content">
        <span class="character">🌟</span>
        <span class="character">🤖</span>
        <span class="character">🦄</span>
        <span class="character">🎨</span>
        <span class="character">🪐</span>
        <span class="character">⚡</span>
        <span class="character">🐶</span>
        <span class="character">🦜</span>
        <span class="character">🧑‍🎤</span>
        <span class="character">🧸</span>
        <span class="character">🐱</span>
        <span class="character">🐦</span>
        <span class="character">🕺</span>
        <span class="character">🌟</span>
        <span class="character">🤖</span>
        <span class="character">🦄</span>
        <span class="character">🎨</span>
        <span class="character">🪐</span>
        <span class="character">⚡</span>
        <span class="character">🐶</span>
        <span class="character">🦜</span>
        <span class="character">🧑‍🎤</span>
        <span class="character">🧸</span>
        <span class="character">🐱</span>
        <span class="character">🐦</span>
        <span class="character">🕺</span>
    </div>
    <div class="slider-content">
        <span class="character">🌟</span>
        <span class="character">🤖</span>
        <span class="character">🦄</span>
        <span class="character">🎨</span>
        <span class="character">🪐</span>
        <span class="character">⚡</span>
        <span class="character">🐶</span>
        <span class="character">🦜</span>
        <span class="character">🧑‍🎤</span>
        <span class="character">🧸</span>
        <span class="character">🐱</span>
        <span class="character">🐦</span>
        <span class="character">🕺</span>
        <span class="character">🌟</span>
        <span class="character">🤖</span>
        <span class="character">🦄</span>
        <span class="character">🎨</span>
        <span class="character">🪐</span>
        <span class="character">⚡</span>
        <span class="character">🐶</span>
        <span class="character">🦜</span>
        <span class="character">🧑‍🎤</span>
        <span class="character">🧸</span>
        <span class="character">🐱</span>
        <span class="character">🐦</span>
        <span class="character">🕺</span>
    </div>
</div>
"""

# Inject the slider into the Streamlit app
st.markdown(slider_css, unsafe_allow_html=True)

# Dropdown for selecting a previous prompt
selected_prompt = st.sidebar.selectbox("Select a previous prompt", options=[""] + [entry[0] for entry in st.session_state.history])

# If a previous prompt is selected, display the corresponding image
if selected_prompt:
    # Find the corresponding image for the selected prompt
    selected_image = next(entry[1] for entry in st.session_state.history if entry[0] == selected_prompt)
    st.image(selected_image, use_container_width=True)

    # Provide a download button for the image
    buffer = BytesIO()
    selected_image.save(buffer, format="PNG")
    buffer.seek(0)
    st.download_button(
        label="Download Image",
        data=buffer,
        file_name="generated_image.png",
        mime="image/png"
    )

#st.sidebar.image("images/log.png", use_container_width=True)

# Text input for the prompt
prompt = st.text_area("Articulate Your Imagination Below", value="")

# Generate button
generate_button = st.button("Generate")

image_placeholder = st.empty()  # Placeholder for the image
st.markdown('</div>', unsafe_allow_html=True)

if generate_button:
    if prompt.strip() == "" or prompt == "":
        st.warning("Please enter a valid prompt to generate an image.")
    else:
        # Show loading animation in the placeholder (keep placeholder size constant)
        with image_placeholder:
            st.markdown("### ⏳ Generating your image, please wait...")
            st.image("https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWwwb2lhbXoxOTd1eTdlb3V4N2RkdDNrYzhsZWh0OTh1anpnOXFxYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tXL4FHPSnVJ0A/giphy.gif", width=400)  # Example loading GIF

        # Simulate time for image generation (this is just for demonstration, replace with actual image generation)
        time.sleep(3)

        with st.spinner("Generating image..."):
            try:
                # Fetch Hugging Face API key from environment variable
                api_key = os.getenv("HUGGINGFACE_API_KEY")
                if not api_key:
                    st.error("Hugging Face API key not found. Please set the HUGGINGFACE_API_KEY environment variable.")
                else:
                    # Define the API endpoint and headers
                    api_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
                    headers = {"Authorization": f"Bearer {api_key}"}

                    # Send a POST request to Hugging Face API
                    response = requests.post(
                        api_url,
                        headers=headers,
                        json={"inputs": prompt},
                        timeout=240,  # Increase timeout if needed
                    )

                    if response.status_code == 200:
                        # Convert the image data from response into an Image object
                        image = Image.open(BytesIO(response.content))

                        # Clear the placeholder and display the image
                        image_placeholder.empty()
                        image_placeholder.image(image, use_container_width=True)

                        # Add the new prompt and image to the history
                        st.session_state.history.append((prompt, image))

                        # Provide a download button for the image
                        buffer = BytesIO()
                        image.save(buffer, format="PNG")
                        buffer.seek(0)
                        st.download_button(
                            label="Download Image",
                            data=buffer,
                            file_name="generated_image.png",
                            mime="image/png"
                        )

                        # Update the sidebar selectbox with the new prompt
                        st.sidebar.selectbox("Select a previous prompt", options=[""] + [entry[0] for entry in st.session_state.history])
                    else:
                        st.error(f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")

            except Exception as e:
                st.error(f"An error occurred: {e}")
