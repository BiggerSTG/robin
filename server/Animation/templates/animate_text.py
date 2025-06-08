from manim import *
from server.agents.tools import MediaTool
import re
import requests
import os
import urllib.parse
from mutagen.mp3 import MP3

audio_dir = "./media/audio"

class TextSlideshow(Scene):
    def __init__(self, slides, audio_buffer=1.5, **kwargs):
        super().__init__(**kwargs)
        self.slides = slides
        self.media_tool = MediaTool()
        self.audio_buffer = audio_buffer

    def construct(self):
        num_slides = len(self.slides)
        time_per_slide = min(10, 600 / num_slides)  # Auto-adjust time per slide

        for i, slide in enumerate(self.slides):
            print("Data type for slide: ", type(slide))
            print("Slide data:", slide)

            # --- Title Setup ---
            slide_title = Text(slide['title'], font_size=48)
            slide_title.scale_to_fit_width(config.frame_width - 1)
            slide_title.to_edge(UP)

            # --- Content Setup ---
            try:
                slide_content = MarkupText(slide["content"], font_size=36)
                slide_content.scale_to_fit_width(config.frame_width - 1)
            except Exception as e:
                print("MarkupText failed, using plain Text:", e)
                slide_content = Text(slide["content"], font_size=36)
                slide_content.scale_to_fit_width(config.frame_width - 1)

            slide_content.next_to(slide_title, DOWN)

            # --- Animate Text In ---
            self.play(Write(slide_title), Write(slide_content), run_time=1.2)

            # --- Math Expression ---
            math_expr = None
            if "math" in slide and slide["math"]:
                try:
                    math_expr = MathTex(slide["math"], font_size=40).scale(0.9).next_to(slide_content, DOWN, buff=0.5)
                    self.play(Write(math_expr), run_time=2)
                except Exception as e:
                    print("MathTex failed, fallback:", e)
                    math_expr = Text(slide["math"], font_size=40).next_to(slide_content, DOWN, buff=0.5)
                    self.play(FadeIn(math_expr), run_time=2)

            # --- Image Handling ---
            image_mobject = None
            if "image" in slide and slide["image"]:
                image_url = slide["image"]
                image_path = download_image(image_url)
                try:
                    image_mobject = ImageMobject(image_path).scale(0.5)
                    image_mobject.next_to(math_expr or slide_content, DOWN, buff=0.5)
                    self.play(FadeIn(image_mobject, shift=UP, scale=0.9), run_time=1)
                except Exception as e:
                    print(f"Image failed to render: {image_path} | Error: {e}")
            
            # --- Generate audio narration for the slide ---
            audio_file = os.path.join(audio_dir, f"slide_{i + 1}_audio.mp3")
            wait_duration = time_per_slide - 2 # fallback if no audio

            if os.path.exists(audio_file):
                try:
                    audio = MP3(audio_file)
                    audio_duration = audio.info.length
                    wait_duration = audio_duration + self.audio_buffer
                    self.add_sound(audio_file, gain=-10)
                except Exception as e:
                    print(f"Failed to get duration or play audio {audio_file}: {e}")
            else:
                print(f"Audio file {audio_file} does not exist, skipping audio playback.")

            # --- Wait Duration ---
            self.wait(wait_duration)

            # --- Exit Everything Together ---
            fade_outs = [slide_title, slide_content]
            if image_mobject:
                fade_outs.append(image_mobject)
            if math_expr:
                fade_outs.append(math_expr)

            self.play(LaggedStart(*[FadeOut(mob) for mob in fade_outs], lag_ratio=0.1, run_time=1))
            self.clear()

 # image download
def download_image(image_url):
    try:
        # Define local image path
        image_filename = os.path.basename(urllib.parse.urlparse(image_url).path)
        image_path = os.path.join("images", image_filename)

        # Create temp_images directory if it doesn't exist
        os.makedirs("images", exist_ok=True)

        # Download the image if not already downloaded
        if not os.path.exists(image_path):
            print("Image Url: ", image_url)
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(image_path, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)

            else:
                raise Exception(f"Failed to download image, status code: {response.status_code}")

        return image_path
    except Exception as e:
        print("Failed to load image:", e)

def construct_slideshow(slides):
    with tempconfig({"output_file": "new_video", "disable_caching": True}):
        scene = TextSlideshow(slides)
        scene.render()