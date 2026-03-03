# 🤖 GPT14 Terminal Chatbot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Gemini](https://img.shields.io/badge/Gemini-2.5-orange?style=for-the-badge&logo=google)
![Groq](https://img.shields.io/badge/Groq-Llama_3-purple?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT_4-green?style=for-the-badge&logo=openai)

**A powerful, multi-provider terminal chatbot created by [sh4lu-z](https://github.com/sh4lu-z).**

</div>

---

## 🔥 Features

- **🧠 Multi-Brain Support**: Automatically detects and uses the best available API key:
  - **Google Gemini** (Gemini 2.5 Flash) - *Fast & Free Tier available*
  - **Groq** (Llama 3 70B) - *Blazing fast*
  - **OpenAI** (GPT-4 Mini) - *Reliable & Smart*
- **💬 GPT14 Persona**: A custom Cyber Security & Python Expert persona that speaks in **Singlish** (Sinhala + English).
- **🎨 Beautiful UI**: Built with `rich` library for a VS Code-like terminal experience with colors, panels, and markdown support.
- **⚡ Streaming**: Real-time typing effect for responses.

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sh4lu-z/gpt14-terminal-bot.git
   cd gpt14-terminal-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API Keys:**
   Create a `.env` file in the root directory and add **at least one** of the following keys:
   ```env
   # Choose your fighter! (You only need one)
   GEMINI_API_KEY="your_gemini_key_here"
   GROQ_API_KEY="your_groq_key_here"
   OPENAI_API_KEY="your_openai_key_here"
   ```

## 🎮 Usage

Run the bot with a single command:

```bash
python mini_chatbot.py
```

## 🛠️ Configuration

You can customize the `SYSTEM_INSTRUCTION` in `mini_chatbot.py` to change the bot's personality. Currently, it is set to:

> "You are a Cyber Security and Python Expert named 'GPT14'. You were created by the developer 'sh4lu-z'. Answer in a mix of English and Sinhala (Singlish)..."

## 📜 License

This project is licensed under the MIT License.

---
<div align="center">
Made with ❤️ by <a href="https://github.com/sh4lu-z">sh4lu-z</a>
</div>
