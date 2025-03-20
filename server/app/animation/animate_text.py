from manim import *

class TextSlideshow(Scene):
    def construct(self, text_body, max_duration=600):  # Max video duration = 10 mins
        slides = self.split_into_slides(text_body)  # Split text into slides
        num_slides = len(slides)
        time_per_slide = min(10, max_duration / num_slides)  # Auto-adjust duration

        for i, slide_text in enumerate(slides):
            # Create slide title (e.g., "Slide 1")
            slide_title = Text(f"Slide {i + 1}", font_size=48).to_edge(UP)
            
            # Render LaTeX-compatible text body
            slide_content = Tex(slide_text, font_size=36).scale(0.8).next_to(slide_title, DOWN)

            # Animate slide appearance
            self.play(FadeIn(slide_title), FadeIn(slide_content), run_time=1)
            self.wait(time_per_slide - 2)  # Display slide for calculated time
            self.play(FadeOut(slide_title), FadeOut(slide_content), run_time=1)

    def split_into_slides(self, text, max_chars=500):
        """Splits large text into slide-sized chunks."""
        words = text.split()
        slides, current_slide = [], ""

        for word in words:
            if len(current_slide) + len(word) + 1 > max_chars:
                slides.append(current_slide)
                current_slide = ""
            current_slide += word + " "

        if current_slide:
            slides.append(current_slide)
        
        return slides

if __name__ == "__main__":
    text_input = r"""
    This is a large block of text with LaTeX formatting, such as $E=mc^2$. 
    It will be split into multiple slides dynamically. Escape sequences like \\ and 
    special functions will be compiled properly before rendering.

    \textbf{This is bold text}, and here is some \textit{italicized text}.
    """

    scene = TextSlideshow()
    scene.construct(text_input)
