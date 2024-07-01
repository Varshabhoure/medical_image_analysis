import streamlit as st
from pathlib import Path
import google.generativeai as genai

from api_key import api_key

genai.configure(api_key=api_key)

# Set up the model
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_prompt = """
Analysis Summary for the Uploaded Medical Image:

Provide a brief description of the identified disease based on the image.
Suggest appropriate actions to take if a person is confirmed to be infected with this disease.
Outline precautionary measures to prevent the spread and contraction of this disease.
Recommend a proper diet that can aid in overcoming the effects of the identified condition.

add this Disclaimer in last:
This information is generated by an AI system and is not a substitute for professional medical advice. It is crucial to consult with healthcare professionals for accurate diagnosis and treatment.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro-vision-latest",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

st.set_page_config(page_title="VitalImage Analytics", page_icon="robot")

st.image('vb.png', width=150)

st.title("Vital Image Analytics")
st.subheader("An application that can help user to identify medical uses")

uploaded_file = st.file_uploader("Upload the medical images for analysis", type=['jpg', 'jpeg', 'png'])

submit_button = st.button("Generate the Analysis")

if submit_button and uploaded_file is not None:
    image_data = uploaded_file.getvalue()

    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        },
    ]

    prompt_parts = [
        image_parts[0],
        system_prompt,
    ]

    st.image(image_data)
    response = model.generate_content(prompt_parts)
    print(response.candidates)
    try:
         st.markdown(response.text)
    except:
        st.write(response.candidates[0].content.parts[0])