import os
import subprocess
import google.generativeai as genai
import typer
from dotenv import load_dotenv
import sys

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = typer.Typer()

def create_llm_prompt(user_prompt: str) -> str:
    # This function does NOT need to be changed.
    # The prompt structure works well for any capable LLM.
    return f"""
    You are an expert Manim programmer. Your task is to generate a single, complete Manim scene in a Python script based on the user's prompt.
    Constraints:
    - The script must be a single block of Python code.
    - Do NOT include any explanations, comments, or text outside of the code.
    - The scene class MUST be named `GeneratedScene`.
    - The code must be runnable with `manim -pql generated_scene.py GeneratedScene`.
    Example:
    User prompt: "A circle turning into a square."
    Your output:
    ```python
    from manim import *
    class GeneratedScene(Scene):
        def construct(self):
            circle = Circle()
            square = Square()
            self.play(Create(circle))
            self.play(Transform(circle, square))
            self.play(FadeOut(square))
    ```
    User prompt: "{user_prompt}"
    Your output:
    """

def get_manim_code(prompt: str) -> str:
    """Sends the prompt to the LLM and gets Manim code back."""
    print("🤖 Calling Gemini API to generate Manim code...")
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(create_llm_prompt(prompt))
        
        code = response.text.strip()
        if code.startswith("```python"):
            code = code[9:]
        if code.endswith("```"):
            code = code[:-3]
        return code.strip()
    except Exception as e:
        print(f"❌ Error calling Gemini API: {e}")
        raise typer.Exit(1)

def render_manim_scene(code: str):
    """Saves the code to a file and renders it with Manim."""
    import time
    timestamp = int(time.time())
    scene_file = f"generated_scene_{timestamp}.py"
    scene_name = f"GeneratedScene_{timestamp}"
    
    with open(scene_file, "w") as f:
        f.write(code)

    # 1. Print the code so the Node.js server can capture it
    print("---CODE---")
    print(code)
    print("---ENDCODE---")
    print(f"---TIMESTAMP---{timestamp}---ENDTIMESTAMP---")
    sys.stdout.flush() # Ensure the output is sent immediately

    print(f"✅ Manim code saved to {scene_file}")
    print("🎬 Starting Manim render...")

    # Use the full path to manim in the virtual environment
    venv_manim = os.path.join(os.path.dirname(__file__), "venv", "bin", "manim")
    
    # Set the media directory to point to public/media
    media_dir = os.path.join(os.path.dirname(__file__), "..", "public", "media")
    
    # Ensure the media directory exists
    os.makedirs(media_dir, exist_ok=True)
    
    command = [
        venv_manim,
        "-ql",
        "--media_dir", media_dir,
        scene_file,
        scene_name
    ]

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        if process.returncode != 0:
            print(f"❌ Manim rendering failed with exit code {process.returncode}.")
        else:
            print("🎉 Video rendered successfully!")
            # Print the actual video file path
            video_path = f"public/media/generated_scene_{timestamp}/480p15/GeneratedScene.mp4"
            print(f"---VIDEO_PATH---{video_path}---ENDVIDEO_PATH---")

    except FileNotFoundError:
        print("❌ Error: 'manim' command not found. Is Manim installed correctly in your environment?")
        raise typer.Exit(1)
    except Exception as e:
        print(f"❌ An unexpected error occurred during rendering: {e}")
        raise typer.Exit(1)

@app.command()
def main(prompt: str = typer.Argument(..., help="The animation you want to create.")):
    """
    Generates and renders a Manim animation from a text prompt.
    """
    manim_code = get_manim_code(prompt)
    if manim_code:
        render_manim_scene(manim_code)

if __name__ == "__main__":
    app()