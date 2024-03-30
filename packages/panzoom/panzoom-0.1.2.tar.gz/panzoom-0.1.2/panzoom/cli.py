import cv2
from PIL import Image
import numpy as np
import argparse
import requests
from io import BytesIO
import random

def download_image(url):
    """
    Download an image from a URL.
    """
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def pan_and_zoom_image(img, output_size, pan_steps, zoom_min, zoom_max):
    """
    Generate frames for panning and zooming effect on the given image with smooth transitions.
    """
    width, height = img.size
    frames = []

    zoom_factor = random.uniform(zoom_min, zoom_max)
    max_left = width - int(width / zoom_factor)
    max_top = height - int(height / zoom_factor)

    start_left = random.randint(0, max(max_left, 1))  # Avoid division by zero
    start_top = random.randint(0, max(max_top, 1))

    pan_step_left = max_left / pan_steps
    pan_step_top = max_top / pan_steps

    for step in range(pan_steps):
        left = start_left + pan_step_left * step
        top = start_top + pan_step_top * step

        left = min(left, max_left)
        top = min(top, max_top)

        crop_width = int(width / zoom_factor)
        crop_height = int(height / zoom_factor)

        right = left + crop_width
        bottom = top + crop_height

        cropped_img = img.crop((left, top, right, bottom))
        resized_img = cropped_img.resize(output_size, Image.Resampling.LANCZOS)

        cv_image = np.array(resized_img)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        frames.append(cv_image)

    return frames

def create_video(image_urls, video_file, fps, output_size, pan_steps, zoom_min, zoom_max):
    """
    Create a video file from a list of image URLs with smooth pan and zoom transitions.
    """
    frame_array = []

    for url in image_urls:
        img = download_image(url)
        frame_array.extend(pan_and_zoom_image(img, output_size, pan_steps, zoom_min, zoom_max))

    height, width, layers = frame_array[0].shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_file, fourcc, fps, (width, height))

    for frame in frame_array:
        out.write(frame)

    out.release()

def main():
    parser = argparse.ArgumentParser(description="Create a pan and zoom video from image URLs.")
    parser.add_argument('urls', type=str, nargs='+', help='Image URLs separated by space')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output video file name')
    parser.add_argument('-s', '--steps', type=int, default=60, help='Number of steps for pan and zoom effect')

    args = parser.parse_args()

    # Pass the steps argument to control the speed of the pan and zoom effect
    create_video(args.urls, args.output, 30, (1080, 1920), args.steps, 1.0, 2.0)

if __name__ == "__main__":
    main()
