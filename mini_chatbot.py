import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.prompt import Prompt

# Load environment variables
load_dotenv()

# Initialize Rich Console
console = Console()

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- System Instruction ---
SYSTEM_INSTRUCTION = """
You are a Cyber Security and Python Expert named 'Syntiox'.
You were created by the developer 'sh4lu-z'.
You are friendly, helpful, and slightly informal.
Answer in a mix of English and Sinhala (Singlish) where appropriate to sound like a Sri Lankan developer.
Always use Markdown for code snippets.
If asked 'who are you', explicitly mention you are GPT14 created by sh4lu-z.
"""

# Global variables
active_client = None
active_provider = None
active_model = None

# --- Setup Clients ---
def setup_client():
    global active_client, active_provider, active_model

    # 1. Check for Gemini
    if GEMINI_API_KEY:
        try:
            from google import genai
            from google.genai import types
            active_client = genai.Client(api_key=GEMINI_API_KEY)
            active_provider = "gemini"
            active_model = "gemini-2.5-flash" 
            console.print(Panel("[bold green]✅ Gemini API Key detected! Using Gemini 2.5 Flash.[/bold green]", border_style="green"))
            return
        except ImportError:
            console.print("[bold red]❌ Google GenAI library not installed. Run: pip install google-genai[/bold red]")
        except Exception as e:
            console.print(f"[bold red]❌ Error initializing Gemini: {e}[/bold red]")

    # 2. Check for Groq
    if GROQ_API_KEY:
        try:
            from groq import Groq
            active_client = Groq(api_key=GROQ_API_KEY)
            active_provider = "groq"
            active_model = "llama3-70b-8192"
            console.print(Panel("[bold green]✅ Groq API Key detected! Using Llama 3 70B.[/bold green]", border_style="green"))
            return
        except ImportError:
            console.print("[bold red]❌ Groq library not installed. Run: pip install groq[/bold red]")
        except Exception as e:
            console.print(f"[bold red]❌ Error initializing Groq: {e}[/bold red]")

    # 3. Check for OpenAI
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            active_client = OpenAI(api_key=OPENAI_API_KEY)
            active_provider = "openai"
            active_model = "gpt-4o-mini"
            console.print(Panel("[bold green]✅ OpenAI API Key detected! Using GPT-4 Mini.[/bold green]", border_style="green"))
            return
        except ImportError:
            console.print("[bold red]❌ OpenAI library not installed. Run: pip install openai[/bold red]")
        except Exception as e:
            console.print(f"[bold red]❌ Error initializing OpenAI: {e}[/bold red]")

    # If no keys found
    console.print(Panel("[bold red]❌ No valid API keys found![/bold red]\nPlease set GEMINI_API_KEY, GROQ_API_KEY, or OPENAI_API_KEY in your .env file.", border_style="red"))
    sys.exit(1)

# --- Generate Response ---
def generate_response_stream(history):
    global active_client, active_provider, active_model

    try:
        if active_provider == "gemini":
            from google.genai import types
            
            # Gemini Config with System Instruction
            config = types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7
            )
            
            # Convert history for Gemini
            gemini_history = []
            for msg in history:
                if msg["role"] == "user":
                    gemini_history.append(types.Content(role="user", parts=[types.Part(text=msg["content"])]))
                elif msg["role"] == "assistant":
                    gemini_history.append(types.Content(role="model", parts=[types.Part(text=msg["content"])]))
            
            # We use generate_content_stream with the full history + config
            # Note: For a true chat loop with history management, using chat.send_message is easier,
            # but generate_content allows explicit config per request easily.
            # Let's stick to the chat interface for better state management if possible, 
            # but we need to pass system instruction.
            
            # Alternative: Create chat with config
            chat = active_client.chats.create(
                model=active_model,
                config=config,
                history=gemini_history[:-1] # History up to the last message
            )
            
            response = chat.send_message_stream(history[-1]["content"])
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text

        elif active_provider in ["groq", "openai"]:
            # Prepare messages with system instruction at the start
            messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}] + history
            
            stream = active_client.chat.completions.create(
                model=active_model,
                messages=messages,
                stream=True,
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

    except Exception as e:
        yield f"\n[bold red]Error generating response: {e}[/bold red]"

# --- Main Chat Loop ---
def main():
    console.clear()
    setup_client()

    welcome_text = Text()
    welcome_text.append("🤖 GPT14 Terminal Chatbot\n", style="bold cyan")
    welcome_text.append(f"Provider: {active_provider.upper()} | Model: {active_model}\n", style="dim")
    welcome_text.append("Created by sh4lu-z", style="italic magenta")
    
    console.print(Panel(welcome_text, border_style="cyan", expand=False))

    history = []

    while True:
        try:
            # Styled Input
            console.print("\n[bold yellow]👤 User[/bold yellow] [dim](type 'exit' to quit)[/dim]")
            user_input = Prompt.ask("➤ ")
            
            if user_input.strip().lower() in ['exit', 'quit', 'bye']:
                console.print("[bold green]👋 Bye! See you later![/bold green]")
                break
            
            if not user_input.strip():
                continue

            # Add user message to history
            history.append({"role": "user", "content": user_input})

            console.print(f"\n[bold cyan]🤖 GPT14 ({active_provider.title()})[/bold cyan]")
            
            full_response = ""
            
            # Live display for streaming response
            with Live(Text("Thinking...", style="dim"), refresh_per_second=10) as live:
                response_text = Text("")
                for chunk in generate_response_stream(history):
                    full_response += chunk
                    # Simple markdown rendering in terminal is hard with streaming partials
                    # So we just stream text, and then print formatted markdown at the end if needed
                    # Or just stream raw text. Let's stream raw text for "typing" effect.
                    response_text.append(chunk)
                    live.update(response_text)
            
            # Add assistant response to history
            history.append({"role": "assistant", "content": full_response})

        except KeyboardInterrupt:
            console.print("\n[bold red]Exiting...[/bold red]")
            break
        except Exception as e:
            console.print(f"\n[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    main()
