from manim import *
from server.agents.tools import MediaTool
import re
import requests
import os
import urllib.parse


class TextSlideshow(Scene):
    def __init__(self, slides, **kwargs):
        super().__init__(**kwargs)
        self.slides = slides
        self.media_tool = MediaTool()


    def construct(self):
        num_slides = len(self.slides)
        time_per_slide = min(10, 600 / num_slides)  # Auto-adjust time per slide
        error_count = 0
        error_free = 0
        url_pattern = re.compile(r'https?://[^\s,:]+')

        for i, slide in enumerate(self.slides):
            # Create slide title with a maximum width to avoid overflow
            print("Data type for slide: ", type(slide))  # Check what type slide is
            print("Slide data:", slide)
            slide_title = Text(f"{slide['title']}", font_size=48)
            if slide_title.width > config.frame_width - 1:
                slide_title.scale_to_fit_width(config.frame_width - 1)
            slide_title.to_edge(UP)

            image_url = None
            if url_pattern.search(slide["content"]):
                image_url = url_pattern.findall(slide["content"])[0]  # Extract first URL
                slide["content"] = url_pattern.sub("", slide["content"]).strip()  # Remove URL from text


            # Create slide content text
            try:
                slide_content = Tex(slide["content"], font_size=36).scale(0.8)
                if slide_content.width > config.frame_width - 1:
                    slide_content.scale_to_fit_width(config.frame_width - 1)
                error_free += 1
                print(error_free)
            except Exception as e:
                print("Tex compilation failed for slide content. Using plain text instead:", e)
                error_count += 1
                print(error_count)
                slide_content = Text(slide["content"], font_size=36)
                if slide_content.width > config.frame_width - 1:
                    slide_content.scale_to_fit_width(config.frame_width - 1)
            slide_content.next_to(slide_title, DOWN)

            # Animate title and content
            self.play(FadeIn(slide_title), FadeIn(slide_content), run_time=1)

            # Add image if a URL is detected
            image_path = download_image(image_url)

            # Load image from local path
            try:
                image_mobject = ImageMobject(image_path).scale(0.5)
                image_mobject.next_to(slide_content, DOWN, buff=0.5)
                self.play(FadeIn(image_mobject), run_time=1)
            except Exception as e:
                print(f"Fucking path {image_path} got bummed: ", e)



            # Animate mathematical expression if present
            math_expr = None
            if "math" in slide and slide["math"]:
                try:
                    math_expr = MathTex(slide["math"], font_size=40).scale(0.9).next_to(slide_content, DOWN)
                    self.play(Write(math_expr), run_time=2)
                    error_free += 1
                    print(error_free)
                except Exception as e:
                    print("MathTex compilation failed for math expression. Using plain text instead:", e)
                    math_expr = Text(slide["math"], font_size=40).next_to(slide_content, DOWN)
                    self.play(FadeIn(math_expr), run_time=2)
                    error_count += 1
                    print(error_count)

            self.wait(time_per_slide - 2)

            # Fade out slide elements
            self.play(FadeOut(slide_title), FadeOut(slide_content))
            if "math" in slide and slide["math"]:
                self.play(FadeOut(math_expr))


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
    with tempconfig({"output_file": "text_slideshow_output"}):
        scene = TextSlideshow(slides)
        scene.render()