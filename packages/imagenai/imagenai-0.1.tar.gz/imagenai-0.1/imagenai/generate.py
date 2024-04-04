import requests
import matplotlib.pyplot as plt
import numpy as np

def imageGenerate(filename, prompt, model_name, api_key):
    """
    Generate an image based on the given prompt using the specified model hosted from the Imagen.AI.

    Parameters:
        filename (str): The name or path of the file where the generated image will be saved.
        prompt (str): The input or prompt that guides the generation process.
        model_name (str): The name or identifier of the machine learning model used for image generation.
        api_key (str): The key that you got from the website

    Returns:
        None
    """
    
    # Check the api key

    response = requests.get(f"http://localhost:8000/api/checkKey/?key={api_key}")
    if response.status_code == 200:
        if model_name.lower() == 'stable diffusion by keras cv':
            print("Using: Stable Diffusion by Keras CV")
            url = "http://localhost:8000/gen/imageApi/"
            data = {'prompt': prompt}
            response = requests.post(url, json=data)
            data = np.array(response.json()['data'], dtype=np.uint8)
            print(data.shape)
            plt.imsave(filename, data)
        elif model_name.lower() == 'imagen api':
            print("Using: Imagen API")
        else:
            print("Invalid Model Name: The provided Model Name wasn't found in our system. Please ensure you have entered the correct model name and try again")
    else:
        print("Invalid API Key: The provided API key is not valid. Please ensure you have entered the correct key and try again.")

