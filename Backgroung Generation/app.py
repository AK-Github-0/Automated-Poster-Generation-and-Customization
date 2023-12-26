import streamlit as st
import requests
import io
from PIL import Image
import openai

class BackgroundGenerator:
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        self.headers = {"Authorization": "Bearer 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"}
        openai.api_key = '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'
        self.genre_options = ["Event", "Educational", "Health"]

    def query(self, payload):
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.content

    def modify_prompt(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        modified_prompt = response['choices'][0]['text'].strip()
        return modified_prompt

    def generate_background(self, genre, prompt):
        payload = {"inputs": f"{prompt} for the background of poster of {genre} genre --no text
                   "}
        return self.query(payload)

    def regenerate_background(self, genre, feedback, prompt):
        payload = {"inputs": f"{prompt} and {feedback} for the background of poster of {genre} genre"}
        return self.query(payload)

    def run(self):
        st.title("Automated Poster Generation and Customization Prototype")

        selected_genre = st.selectbox("Select a genre:", self.genre_options)
        subgenres = {
            'Event': ["Concert", "Festival", "Movie", "Sports"],
            'Educational': ["Science Fair", "Academic Conference", "Educational Workshop"],
            'Health': ["Health Awareness", "Medical Conference", "Vaccination Campaign"]
        }
        selected_subgenre = st.selectbox(f"Select a subgenre of {selected_genre}:", subgenres[selected_genre])

        prompts_dict = {
    "Concert": "Design a vibrant concert poster capturing the essence of the indie music scene. Incorporate a dynamic blend of colors and imagery that resonates with the indie vibe. Include silhouettes or stylized representations of people immersed in the concert experience, conveying the energy and excitement of live music.--no text",
    "Festival": "Generate a vibrant festival poster. Blend a kaleidoscope of colors seamlessly, incorporating elements like confetti, candles and other festive props. Capture the lively spirit of the event with dynamic compositions and energetic visuals. --no text",
    "Sports": "Design a dynamic sports poster featuring a striking silhouette of a determined runner against a vibrant background, capturing the essence of speed and endurance. Incorporate bold typography to highlight the event details and use energetic colors to evoke a sense of excitement.",
    "Movie": "Generate an image for a movie poster with a suspicious theme. Use a darker color scheme to create an atmosphere of intrigue and uncertainty. Depict abstract elements that hint at secrecy, such as obscured silhouettes, hidden symbols, or veiled objects. Utilize shades of mysterious grays, and subtle hints of intense color to convey a sense of suspense. Ensure the overall composition sparks curiosity and invites viewers to delve into the enigma behind the movie. --no text",
    "Science Fair": "Generate an eye-catching science fair poster featuring a captivating depiction of nucleus, microscopes, and a beaker with vividly colored chemicals. Explore the hidden world of atoms and molecules, showcasing the beauty and complexity of the microcosm through striking visuals. --no text",
    "Educational Workshop": "Generate an image depicting a dynamic educational workshop scenario, featuring a business professional engaged in interactive learning with state-of-the-art technology. Emphasize collaboration, innovation, and the integration of cutting-edge tools within the educational environment.",
    "Health Awareness": "Generate a health awareness background featuring a prominent illustration of a healthy heart or brain. Include relevant props such as pills, a balanced diet, and exercise imagery. Emphasize vibrant colors and use persuasive text to convey the importance of a healthy lifestyle for overall well-being.",
    "Medical Conference": "Create a captivating medical conference background featuring a prominent display of a DNA helix or a vibrant cell pattern seamlessly integrated across the poster. Emphasize a professional and visually appealing composition to enhance the overall visual impact and convey the theme of cutting-edge advancements in medical research and innovation. --no text",
    "Vaccination Campaign": "Capture the joy of a healthy childhood! Design a vibrant vaccination awareness poster featuring playful silhouettes of children laughing and playing, harmoniously juxtaposed with the caring image of a doctor holding a vaccination injection. Encourage community health through the power of preventive care.",
    "Academic Conference" : "Explore the fusion of cutting-edge technology and academic poster presentation by designing a visually engaging poster that incorporates an LCD screen. Showcase the latest advancements in your field using dynamic symbols and interactive elements on the screen, creating an immersive experience for conference attendees. Highlight how this innovative format enhances the dissemination of research findings and facilitates a deeper understanding of complex concepts --no text"
}

        original_prompt = prompts_dict[selected_subgenre]
        modified_prompt = self.modify_prompt(original_prompt)
        prompt = modified_prompt

        if st.button("Generate Background"):
            st.text("Generating background...")
            image_bytes = self.generate_background(selected_genre, self.modify_prompt(prompt))
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption="Generated Background", use_column_width=True)

        if st.button("Regenerate Background"):
            prompt = self.modify_prompt(prompt)
            feedback = st.text_input("Please write feedback for the background:")
            st.text("Regenerating background...")
            image_bytes = self.regenerate_background(selected_genre, feedback, prompt)
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption="Regenerated Background", use_column_width=True)

if __name__ == "__main__":
    generator = BackgroundGenerator()
    generator.run()
