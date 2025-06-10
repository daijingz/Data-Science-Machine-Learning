import os
import json
from PIL import Image
from diffusers import StableDiffusionControlNetImg2ImgPipeline, ControlNetModel
import torch

# Compatible start loading the resource
# My local machine has some problems with the cuda, so I use cpu to compute
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load ControlNet and Stable Diffusion model
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-canny", torch_dtype=torch.float32
).to(device)

# Initialize the pipeline with ControlNet
pipeline_img2img = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4", controlnet=controlnet, torch_dtype=torch.float32
).to(device)

# Collect image 1 and image 2, and resize them to 256, 512 bits.
# This aims to make the image adapt for combination in the next part
def load_and_process_image(image_path):
    image = Image.open(image_path).convert("RGB").resize((256, 512))
    return image

# Main body to generate movie poster images
def generate_image(prompt, negative_prompt, character_1_prompt, character_1_negative_prompt, character_1_image_path,
                   character_2_prompt, character_2_negative_prompt, character_2_image_path):
    # Load both characters' images
    character_1_image = load_and_process_image(character_1_image_path)
    character_2_image = load_and_process_image(character_2_image_path)

    # Horizontally combines two images
    merged_image = Image.new('RGB', (character_1_image.width + character_2_image.width, character_1_image.height))
    merged_image.paste(character_1_image, (0, 0))
    merged_image.paste(character_2_image, (character_1_image.width, 0))

    # Use ControlNet to generate the final image from the merged image
    result = pipeline_img2img(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=merged_image,
        control_image=merged_image,  # Use the merged image as the control image
        strength=0.9,
        guidance_scale=8.5,
        num_inference_steps=22
    )

    # Resize the output image to 1024 * 1024 bits.
    poster_image = result.images[0]
    poster_image = poster_image.resize((1024, 1024), Image.LANCZOS)

    return poster_image

# Update result.json, the generation requirement file
def update_result_json(result_data, save_dir):
    result_json_path = os.path.join(save_dir, 'result.json')

    # Read and load the result.json if there is a result.json file.
    if os.path.exists(result_json_path):
        with open(result_json_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    #
    existing_data.extend(result_data)
    with open(result_json_path, 'w', encoding='utf-8') as f_out:
        json.dump(existing_data, f_out, sort_keys=True, indent=4, ensure_ascii=False)

'''
Main body of execution
1. Read requirements from result.json and generate images
2. Update result.json
3. Store images in a sub-repository "images"
'''
if __name__ == '__main__':

    save_dir = './results'
    benchmark_file_path = './benchmark.json'

    os.makedirs(save_dir, exist_ok=True)
    result_data = []

    with open(benchmark_file_path, 'r', encoding='utf-8') as f:
        benchmark_json = json.load(f)

    for key, value in benchmark_json.items():
        prompt = value['prompt']
        negative_prompt = value['negative_prompt']
        characters = value['characters']

        character_1 = characters[0]
        character_2 = characters[1]

        image = generate_image(
            prompt=prompt,
            negative_prompt=negative_prompt,
            character_1_prompt=character_1['prompt'],
            character_1_negative_prompt=character_1['negative_prompt'],
            character_1_image_path=character_1['image_path'],
            character_2_prompt=character_2['prompt'],
            character_2_negative_prompt=character_2['negative_prompt'],
            character_2_image_path=character_2['image_path']
        )

        save_image_path = os.path.join(save_dir, f'{key}_result.png')
        image.save(save_image_path)

        result_data.append({
            'generated_image': os.path.abspath(save_image_path),
            'character_image_path_list': [character_1['image_path'], character_2['image_path']],
            'caption': prompt
        })

    update_result_json(result_data, save_dir)

    print(f"Images saved in {save_dir} and result.json updated.")