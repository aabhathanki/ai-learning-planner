# 🧠 AI Learning Planner

An AI-powered learning planner that helps you organize and personalize your learning journey using the Groq API.

---

## 📋 Prerequisites

Before you begin, make sure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- A [Groq API Key](https://console.groq.com) (free to get)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/aabhathanki/ai-learning-planner.git
cd ai-learning-planner
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root of the project:

```bash
# Windows
copy NUL .env

# Mac/Linux
touch .env
```

Add your Groq API key to the `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
```

> 🔑 Get your free API key at [console.groq.com](https://console.groq.com)

---

## ▶️ How to Run the App Locally

Make sure your virtual environment is activated, then run:

```bash
python app.py
```

The app will start and you can access it in your browser at:

```
http://localhost:8501
```
> *(Port may vary depending on the framework used)*

---

## 📁 Project Structure

```
ai-learning-planner/
│
├── components/         # UI or reusable components
├── planner/            # Core planner logic
├── utils/              # Helper/utility functions
├── app.py              # Main application entry point
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not committed)
└── README.md           # Project documentation
```

---

## 🔒 Security Note

Never share or commit your `.env` file. It is already added to `.gitignore` to keep your API keys safe.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
