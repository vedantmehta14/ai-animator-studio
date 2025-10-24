import { NextResponse } from "next/server";
import { spawn } from "child_process";
import path from "path";

export async function POST(request: Request) {
  try {
    const { prompt } = await request.json();

    if (!prompt) {
      return NextResponse.json({ error: "Prompt is required" }, { status: 400 });
    }

    // Path to the Python executable in the virtual environment
    const venvPython = path.join(process.cwd(), 'manim-ai-tool', 'venv', 'bin', 'python');
    // Path to your main Python script
    const scriptPath = path.join(process.cwd(), 'manim-ai-tool', 'main.py');

    const processPromise = new Promise((resolve, reject) => {
      const pyProcess = spawn(venvPython, [scriptPath, prompt]);
      
      let output = "";
      let errorOutput = "";

      pyProcess.stdout.on("data", (data) => {
        console.log(`stdout: ${data}`);
        output += data.toString();
      });

      pyProcess.stderr.on("data", (data) => {
        console.error(`stderr: ${data}`);
        errorOutput += data.toString();
      });
      
      pyProcess.on("close", (code) => {
        if (code !== 0) {
          return reject(new Error(`Python script exited with code ${code}\n${errorOutput}`));
        }
        // Extract timestamp from output to construct the correct video path
        const timestampMatch = output.match(/---TIMESTAMP---(\d+)---ENDTIMESTAMP---/);
        const timestamp = timestampMatch ? timestampMatch[1] : Date.now();
        
        // Manim saves files to public/media with the new configuration
        const videoFileName = "GeneratedScene.mp4";
        const videoRelativePath = `/media/videos/generated_scene_${timestamp}/480p15/${videoFileName}`;

        // Extract the code from the specially marked output
        const codeMatch = output.match(/---CODE---([\s\S]*)---ENDCODE---/);
        const generatedCode = codeMatch ? codeMatch[1].trim() : "Could not extract code.";
        
        resolve({ videoUrl: videoRelativePath, generatedCode });
      });
    });

    const result: any = await processPromise;

    return NextResponse.json(result);
  } catch (error: any) {
    console.error(error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}