from google.cloud import texttospeech
import os
import json
import re
from dotenv import load_dotenv
from mutagen.mp3 import MP3
from server.services.query_llm import query_llm

load_dotenv()

media_dir = "./media"  # Explicit media directory

# Set up Google Text-to-Speech client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_TTS")

PROMPT_TEMPLATE = """
You are an excellent teacher known for your deep explanations and ability to connect concepts across a lesson.

You are given a sequence of slides. For each slide:
- Expand on the content conversationally.
- Refer to prior slides to reinforce ideas.
- Add examples, analogies, and engaging explanations.
- Do NOT just read the slide verbatim.
- Imagine you're teaching live in front of curious students.

Generate narration as a numbered list where each item corresponds to a slide index.

Input slides:
{slides}

Output format:
[
  "Narration for Slide 1...",
  "Narration for Slide 2...",
  ...
]
"""

# Initialize client
client = texttospeech.TextToSpeechClient()

def get_audio_duration(filename: str) -> float:
    audio = MP3(filename)
    return audio.info.length

def speak_and_wait(text: str, filename: str):
    # Get absolute path using current config
    global media_dir
    media_dir = media_dir
    audio_dir = os.path.join(media_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    print(f"Audio directory: {audio_dir}")
    full_path = os.path.join(audio_dir, filename)

    if not os.path.exists(filename):
        text_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Studio-Q",
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.3
        )
        response = client.synthesize_speech(
            input=text_input,
            voice=voice,
            audio_config=audio_config
        )
        with open(full_path, "wb") as out:
            out.write(response.audio_content)

    duration = MP3(full_path).info.length

def generate_narration(slides):
    """
    Generate narration for a list of slides using the LLM.
    """
    # Convert dictionary to a string where each slide is labeled.
    slide_texts = []
    item_num = 1
    for slide in slides:
        # You can adjust the displayed text here; for example, you might include the title as well.
        slide_text = f"Slide {item_num}: {slide.get('title', '')}\n{slide.get('content', '')}"
        slide_texts.append(slide_text)
        item_num += 1

    final_prompt = PROMPT_TEMPLATE.format(slides="\n".join(slide_texts))
    print(f"Prompt for narration generation: {final_prompt}")
    narration = query_llm(final_prompt)
    
    # Parse the LLM output
    try:
        cleaned_narration = clean_llm_json(narration)
        parsed_narration = json.loads(cleaned_narration)  # Assuming LLM returns a valid Python list
        for i, text in enumerate(parsed_narration):
            filename = f"slide_{i + 1}_audio.mp3"
            speak_and_wait(text, filename)
            print(f"Generated audio for slide {i + 1}: {filename}")
        return True
    except Exception as e:
        print("Error parsing LLM Audio output:", e)

    return False

def clean_llm_json(raw_output):
    # Remove leading/trailing whitespace and code block markers
    cleaned = raw_output.strip()

    # Remove code block fence if present (```python or ```json or ```)
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:python|json)?", "", cleaned, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()

    return cleaned

# if __name__ == "__main__":
#     narration = generate_narration(slides)
#     for i, text in enumerate(narration):
#         filename = f"slide_{i + 1}_audio.mp3"
#         speak_and_wait(text, filename)