from manim import *

class TextSlideshow(Scene):
    def construct(self):
        # Large text input with LaTeX formatting
        slides = [
            {
                "title": "Introduction",
                "content": r"""
                    Welcome to this mathematical presentation! 
                    In this slide, we explore a famous equation:
                """,
                "math": r"E = mc^2"
            },
            {
                "title": "Probability Basics",
                "content": r"""
                    In probability theory, we often deal with:
                """,
                "math": r"P(A \cup B) = P(A) + P(B) - P(A \cap B)"
            },
            {
                "title": "Conclusion",
                "content": r"""
                    This concludes our brief introduction to LaTeX-rendered slides!
                """,
                "math": None
            }
        ]

        num_slides = len(slides)
        time_per_slide = min(10, 600 / num_slides)  # Auto-adjust time per slide

        for i, slide in enumerate(slides):
            # Create slide title
            slide_title = Text(f"Slide {i + 1}: {slide['title']}", font_size=48).to_edge(UP)
            
            # Slide content text
            slide_content = Tex(slide["content"], font_size=36).scale(0.8).next_to(slide_title, DOWN)

            # Animate title and content
            self.play(FadeIn(slide_title), FadeIn(slide_content), run_time=1)

            # Animate mathematical expression if present
            if slide["math"]:
                math_expr = MathTex(slide["math"], font_size=40).scale(0.9).next_to(slide_content, DOWN)
                self.play(Write(math_expr), run_time=2)

            self.wait(time_per_slide - 2)  # Display slide for calculated time

            # Fade out slide elements
            self.play(FadeOut(slide_title), FadeOut(slide_content))
            if slide["math"]:
                self.play(FadeOut(math_expr))

