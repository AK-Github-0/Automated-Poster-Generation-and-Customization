import streamlit as st
import requests
import io
from PIL import Image

API_URL_GENRE = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
API_URL_PROMPT = "https://api-inference.huggingface.co/models/humarin/chatgpt_paraphraser_on_T5_base"

HEADERS = {"Authorization": "Bearer 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"}

def query_genre(payload):
    response = requests.post(API_URL_GENRE, headers=HEADERS, json=payload)
    return response.content

def query_prompt(payload):
    response = requests.post(API_URL_PROMPT, headers=HEADERS, json=payload)
    return response.json()

Geners = {
    'Event' : ["Concert", "Festival", "Movie", "Sports"],
    'Educational' : ["Science Fair", "Educational Workshop"],
    'Health' : ["Health Awareness", "Medical Conference", "Vaccination Awareness"]
}

# Streamlit app
st.title("Automated Poster Generation and Customization Prototype")

# Genre selection
genre_options = ["Event", "Educational", "Health"]
selected_genre = st.selectbox("Select a genre:", genre_options)

# Sub-genre selection based on the selected genre
sub_genre_options = Geners.get(selected_genre, [])
selected_sub_genre = st.selectbox("Select a sub-genre:", sub_genre_options)

# Automatic prompt selection based on the provided prompts
prompts_dict = {
    "Concert": ["Design a vibrant concert poster capturing the essence of the indie music scene. Incorporate a dynamic blend of colors and imagery that resonates with the indie vibe. Include silhouettes or stylized representations of people immersed in the concert experience, conveying the energy and excitement of live music.--no text"],
    "Festival": ["Generate a vibrant festival poster. Blend a kaleidoscope of colors seamlessly, incorporating elements like confetti, candles and other festive props. Capture the lively spirit of the event with dynamic compositions and energetic visuals. --no text"],
    "Sports": ["Design a dynamic sports poster featuring a striking silhouette of a determined runner against a vibrant background, capturing the essence of speed and endurance. Incorporate bold typography to highlight the event details and use energetic colors to evoke a sense of excitement."],
    "Movie": ["Create a movie poster that captures a timeless essence, appealing to a broad audience. Design a visually striking composition with vibrant colors and dynamic elements. Feature a mix of characters engaging in various activities, hinting at the film's diverse themes. Incorporate an enticing tagline that sparks curiosity and a title presented prominently. Use a balanced composition to ensure the poster is visually engaging and conveys a sense of excitement without revealing specific plot details.",
              "Generate an image for a movie poster with a suspicious theme. Use a darker color scheme to create an atmosphere of intrigue and uncertainty. Depict abstract elements that hint at secrecy, such as obscured silhouettes, hidden symbols, or veiled objects. Utilize shades of mysterious grays, and subtle hints of intense color to convey a sense of suspense. Ensure the overall composition sparks curiosity and invites viewers to delve into the enigma behind the movie. --no text"],
    "Science Fair": ["Generate an eye-catching science fair poster featuring a captivating depiction of nucleus, microscopes, and a beaker with vividly colored chemicals. Explore the hidden world of atoms and molecules, showcasing the beauty and complexity of the microcosm through striking visuals. --no text"],
    "Educational Workshop": ["Generate an image depicting a dynamic educational workshop scenario, featuring a business professional engaged in interactive learning with state-of-the-art technology. Emphasize collaboration, innovation, and the integration of cutting-edge tools within the educational environment."],
    "Health Awareness": ["Generate a health awareness background featuring a prominent illustration of a healthy heart or brain. Include relevant props such as pills, a balanced diet, and exercise imagery. Emphasize vibrant colors and use persuasive text to convey the importance of a healthy lifestyle for overall well-being."],
    "Medical Conference": ["Create a captivating medical conference background featuring a prominent display of a DNA helix or a vibrant cell pattern seamlessly integrated across the poster. Emphasize a professional and visually appealing composition to enhance the overall visual impact and convey the theme of cutting-edge advancements in medical research and innovation. --no text"],
    "Vaccination Awareness": ["Capture the joy of a healthy childhood! Design a vibrant vaccination awareness poster featuring playful silhouettes of children laughing and playing, harmoniously juxtaposed with the caring image of a doctor holding a vaccination injection. Encourage community health through the power of preventive care."]
}

selected_prompt = st.selectbox("Select a prompt:", prompts_dict.get(selected_sub_genre, []))

# Feedback for regeneration
regenerate_feedback = st.text_input("Provide feedback for regeneration (optional):")

if st.button("Generate Background"):
    if not selected_prompt:
        st.warning("Please select a prompt.")
    else:
        st.text("Generating background...")
        image_bytes = generate_background(selected_sub_genre, selected_prompt)

        # Display the generated image
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image, caption="Generated Background", use_column_width=True)

if st.button("Regenerate Background"):
    if not selected_prompt:
        st.warning("Please select a prompt.")
    else:
        st.text("Generating background...")
        paraphrased_prompt = paraphrase_prompt(selected_prompt)

        # Provide feedback and use it in the regeneration process
        if regenerate_feedback:
            st.text(f"Feedback received: {regenerate_feedback}")
            paraphrased_prompt = regenerate_feedback

        image_bytes = regenerate_background(selected_sub_genre, paraphrased_prompt)

        # Display the regenerated image
        regenerated_image = Image.open(io.BytesIO(image_bytes))
        st.image(regenerated_image, caption="Regenerated Background", use_column_width=True)

