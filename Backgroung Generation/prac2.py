import requests

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content
image_bytes = query({
	"inputs": "Background for an entertainment poster of red colour",
})
# You can access the image with PIL.Image for example
import io
from PIL import Image
import io
import matplotlib.pyplot as plt
image = Image.open(io.BytesIO(image_bytes))
plt.imshow(image)
plt.axis('off')  # Turn off axis labels and ticks
plt.show()