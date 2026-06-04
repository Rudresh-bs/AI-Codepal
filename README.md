# ⌨ CodePal — AI Coding Assistant

> A dark-themed, terminal-inspired AI coding assistant built with **Streamlit** and the **Anthropic Claude API**.

![Python](https://img.shields.io/badge/Python-3.9%2B-black?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=flat-square)
![Claude API](https://img.shields.io/badge/Claude-API-00ff88?style=flat-square&labelColor=0a0a0a)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

- 🤖 **Powered by Claude** — Sonnet & Haiku models available
- 🎯 **5 Coding Modes** — General Assistant, Code Reviewer, Bug Fixer, Code Explainer, Algorithm Helper
- 🌐 **Multi-language support** — Python, JavaScript, Java, C++, SQL, React and more
- 🎨 **3 Response styles** — Detailed, Code only, or Concise
- 📊 **Live token tracker** — see usage per session
- 🖤 **Dark terminal UI** — Space Mono + Syne fonts, green accent theme
- 💬 **Full conversation memory** — context preserved across the session

---

## 🎯 Coding Modes

| Mode | What it does |
|------|-------------|
| 🧑‍💻 General Assistant | Write, explain, and improve code |
| 🔍 Code Reviewer | Review for bugs, performance, best practices |
| 🐛 Bug Fixer | Find and fix errors with explanations |
| 📖 Code Explainer | Break down code line by line |
| 🧠 Algorithm Helper | Solve DSA problems, analyze complexity |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/codepal.git
cd codepal
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get your Anthropic API key

Sign up at [console.anthropic.com](https://console.anthropic.com) and create a free API key.

### 4. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501), enter your API key in the sidebar, and start coding!

---

## 🗂 Project Structure

```
codepal/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Dependencies
├── .streamlit/
│   └── config.toml         # Dark theme config
├── .gitignore
└── README.md
```

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | Web UI framework |
| [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python) | Claude API client |
| [Space Mono + Syne](https://fonts.google.com) | Terminal-inspired typography |

---

## 📄 License

MIT — free to use, fork, and build on.

---

<p align="center">Built by <strong>Rudresh BS</strong> · <a href="https://github.com/Rudresh-bs/Rudresh-B-S">GitHub</a></p>
