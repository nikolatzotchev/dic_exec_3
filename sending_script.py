import os
import requests
import base64

def encode_images_to_base64(image_folder):
    encoded_images = []
    for filename in os.listdir(image_folder):
        image_path = os.path.join(image_folder, filename)
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            encoded_images.append(encoded_string)
    return encoded_images

def send_images_to_api(encoded_images, api_endpoint):
    payload = {"images": encoded_images}
    response = requests.post(api_endpoint, json=payload)
    return response.text

image_folder = "./object-detection-TEST"
api_endpoint = "http://54.237.85.27:5000/api/detect"
encoded_images = encode_images_to_base64(image_folder)
response_text = send_images_to_api(encoded_images, api_endpoint)

output_file = "response.txt"
with open(output_file, "w") as file:
    file.write(response_text)

print(f"Response written to {output_file} successfully!")