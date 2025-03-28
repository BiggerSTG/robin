from manim import *

class TextSlideshow(Scene):
    def __init__(self, slides, **kwargs):
        super().__init__(**kwargs)
        self.slides = slides

    def construct(self):
        num_slides = len(self.slides)
        time_per_slide = min(10, 600 / num_slides)  # Auto-adjust time per slide

        for i, slide in enumerate(self.slides):
            # Create slide title with a maximum width to avoid overflow
            slide_title = Text(f"{slide['title']}", font_size=48)
            if slide_title.width > config.frame_width - 1:
                slide_title.scale_to_fit_width(config.frame_width - 1)
            slide_title.to_edge(UP)

            # Create slide content text
            try:
                slide_content = Tex(slide["content"], font_size=36).scale(0.8)
                if slide_content.width > config.frame_width - 1:
                    slide_content.scale_to_fit_width(config.frame_width - 1)
            except Exception as e:
                print("Tex compilation failed for slide content. Using plain text instead:", e)
                slide_content = Text(slide["content"], font_size=36)
                if slide_content.width > config.frame_width - 1:
                    slide_content.scale_to_fit_width(config.frame_width - 1)
            slide_content.next_to(slide_title, DOWN)

            # Animate title and content
            self.play(FadeIn(slide_title), FadeIn(slide_content), run_time=1)

            # Animate mathematical expression if present
            math_expr = None
            if "math" in slide and slide["math"]:
                try:
                    math_expr = MathTex(slide["math"], font_size=40).scale(0.9).next_to(slide_content, DOWN)
                    self.play(Write(math_expr), run_time=2)
                except Exception as e:
                    print("MathTex compilation failed for math expression. Using plain text instead:", e)
                    math_expr = Text(slide["math"], font_size=40).next_to(slide_content, DOWN)
                    self.play(FadeIn(math_expr), run_time=2)

            self.wait(time_per_slide - 2)

            # Fade out slide elements
            self.play(FadeOut(slide_title), FadeOut(slide_content))
            if "math" in slide and slide["math"]:
                self.play(FadeOut(math_expr))

def construct_slideshow(slides):
    with tempconfig({"output_file": "text_slideshow_output"}):
        scene = TextSlideshow(slides)
        scene.render()