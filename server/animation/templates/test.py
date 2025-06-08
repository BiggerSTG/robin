from manim import *
from google.cloud import texttospeech
import os
from dotenv import load_dotenv
from mutagen.mp3 import MP3

load_dotenv()

config.media_dir = "./media"  # Explicit media directory
config.quality = "low_quality"  # For faster testing
config.format = "mp4"  # Direct video format

# Set up Google Text-to-Speech client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_TTS")

# Initialize client
client = texttospeech.TextToSpeechClient()

def get_audio_duration(filename: str) -> float:
    audio = MP3(filename)
    return audio.info.length

def speak_and_wait(text: str, filename: str):
    # Get absolute path using current config
    media_dir = config.media_dir
    audio_dir = os.path.join(media_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    print(f"Audio directory: {audio_dir}")
    full_path = os.path.join(audio_dir, filename)

    if not os.path.exists(filename):
        text_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Chirp3-HD-Aoede",
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.0
        )
        response = client.synthesize_speech(
            input=text_input,
            voice=voice,
            audio_config=audio_config
        )
        with open(full_path, "wb") as out:
            out.write(response.audio_content)

    duration = MP3(full_path).info.length
    # scene.add_sound(full_path, gain=-10)  # -10dB gain for better mixing
    # scene.wait(duration + 0.5)  # Increased buffer

class AnimatedArray(VGroup):
    def __init__(self, values, box_color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.values = values
        self.boxes = VGroup(*[Square().scale(0.75) for _ in values])
        self.texts = VGroup(*[Text(str(val), font_size=32) for val in values])
        for box, text in zip(self.boxes, self.texts):
            text.move_to(box.get_center())
        self.arr = VGroup(*[VGroup(b, t) for b, t in zip(self.boxes, self.texts)])
        self.arr.arrange(RIGHT, buff=0.2)
        self.add(self.arr)

    def highlight(self, indices, color=YELLOW):
        return [self.arr[i][0].animate.set_color(color) for i in indices]

    def swap(self, i, j):
        return [
            self.arr[i].animate.move_to(self.arr[j].get_center()),
            self.arr[j].animate.move_to(self.arr[i].get_center())
        ]

class SelectionSortScene(Scene):
    def construct(self):
        values = [5, 2, 9, 1, 6]
        arr = AnimatedArray(values)
        arr.move_to(ORIGIN)
        self.add(arr)
        self.wait(1)

        n = len(values)
        for i in range(n):
            min_idx = i
            speak_and_wait(self, f"Selecting index {i} as the current minimum.", f"audio_step_{i}_select.mp3")
            self.play(*arr.highlight([i], color=GREEN))

            for j in range(i + 1, n):
                speak_and_wait(self, f"Comparing element at index {j} with current minimum.", f"audio_step_{i}_{j}_compare.mp3")
                self.play(*arr.highlight([j], color=YELLOW))
                if values[j] < values[min_idx]:
                    min_idx = j
                self.wait(0.5)
                self.play(arr.arr[j][0].animate.set_color(WHITE))

            if min_idx != i:
                speak_and_wait(self, f"Swapping index {i} with new minimum at index {min_idx}.", f"audio_step_{i}_swap.mp3")
                self.play(*arr.swap(i, min_idx))
                arr.arr[i], arr.arr[min_idx] = arr.arr[min_idx], arr.arr[i]
                values[i], values[min_idx] = values[min_idx], values[i]

            self.play(arr.arr[i][0].animate.set_color(GREY))

        self.wait(2)

def sanitize_latex(text):
    # Escape common problematic symbols
    replacements = {
        '%': r'\%',
        '&': r'\&',
        '_': r'\_',
        '#': r'\#',
        '$': r'\$',
        '{': r'\{',
        '}': r'\}',
    }
    for symbol, escaped in replacements.items():
        text = text.replace(symbol, escaped)
    return text


if __name__ == "__main__":

    result = "∑ from n = 1 to ∞ of n"

    #result = sanitize_latex(result)
    result = Text(result, font_size=36).scale(0.8)

    print(result)

    speak_and_wait(text="magya", filename="magya.mp3")

    # with tempconfig({
    #     "media_dir": "./media",
    #     "output_file": "selection_sort",
    #     "progress_bar": "none"
    # }):
    #     scene = SelectionSortScene()
    #     scene.render()