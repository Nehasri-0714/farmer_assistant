import subprocess
import os
from colorama import Fore, Style, init

init(autoreset=True)

# === CONFIGURATION ===
LLAMA_EXE = os.path.join("llama_backend", "llama-run.exe")
MODEL_PATH = os.path.join("llama_backend", "TinyLlama.gguf")
MAX_TOKENS = "200"
TEMPERATURE = "0.7"
TOP_K = "40"
TOP_P = "0.9"
REPEAT_PENALTY = "1.1"

# === CHAT MEMORY ===
chat_history = []

# === PROMPT TEMPLATE ===
SYSTEM_PROMPT = "You are a helpful offline farming assistant for Indian farmers. Respond clearly in simple English."

def build_prompt(user_input):
    prompt = SYSTEM_PROMPT + "\n\n"
    for turn in chat_history[-5:]:  # keep last 5 exchanges
        prompt += f"User: {turn['question']}\nAssistant: {turn['answer']}\n"
    prompt += f"User: {user_input}\nAssistant:"
    return prompt

def run_llama(prompt):
    try:
        result = subprocess.run(
            [
                LLAMA_EXE,
                "-m", MODEL_PATH,
                "-p", prompt,
                "-n", MAX_TOKENS,
                "--temp", TEMPERATURE,
                "--top_k", TOP_K,
                "--top_p", TOP_P,
                "--repeat_penalty", REPEAT_PENALTY
            ],
            capture_output=True,
            text=True,
            shell=False
        )

        if result.returncode != 0:
            return f"{Fore.RED}❌ Model execution failed:\n{result.stderr.strip()}"

        output = result.stdout.strip()

        # Try to get the model's final answer after the last "Assistant:" marker
        if "Assistant:" in output:
            response = output.split("Assistant:")[-1].strip()
        else:
            response = output

        if not response:
            return f"{Fore.RED}⚠️ No meaningful response. Try rephrasing your question."

        return response

    except FileNotFoundError:
        return f"{Fore.RED}❌ llama-run.exe not found. Check the path in LLAMA_EXE."
    except Exception as e:
        return f"{Fore.RED}❌ Unexpected Error: {e}"

def main():
    print(Fore.GREEN + "\n🌾 Welcome to Farmer's Offline Assistant (LLM powered by llama.cpp)")
    print(Fore.YELLOW + "🧑 Type your farming questions (type 'exit' to quit)\n")

    while True:
        user_input = input(Fore.CYAN + "🧑 You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print(Fore.MAGENTA + "\n👋 Exiting... Stay healthy, farmer!")
            break

        print(Fore.LIGHTGREEN_EX + "\n🦙 Llama is thinking...\n")

        prompt = build_prompt(user_input)
        answer = run_llama(prompt)

        print(Fore.LIGHTYELLOW_EX + "🦙 Assistant:", Fore.WHITE + answer + "\n")
        chat_history.append({"question": user_input, "answer": answer})

if __name__ == "__main__":
    main()
