# 📝 Quiz Question Generator with CrewAI

This repository provides a Python script to automatically **generate multiple-choice quiz questions** from PDF or TXT documents using [CrewAI](https://docs.crewai.com/) and **Google Gemini** LLM.

The script extracts text from a document, processes it into manageable chunks, and uses an AI agent to create **high-quality quiz questions** strictly based on the document’s content.

---

## 📂 Project Structure

```
.
├── quizgen.py             # Main script
├── THE-USA.pdf            # Example input document
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

---

## ⚙️ Requirements

* Python 3.9+
* Dependencies:

  * `crewai`
  * `langchain`
  * `langchain-community`
  * `pypdf` (for PDF loading)

Install dependencies:

```bash
pip install crewai langchain langchain-community pypdf
```

---

## 🔑 API Setup

The script uses **Google Gemini** as the LLM provider.

1. Get a Google API key from [AI Studio](https://aistudio.google.com/).
2. Set the key as an environment variable:

```bash
export GOOGLE_API_KEY="your_api_key_here"
```

3. Alternatively, replace the placeholder in `quizgen.py`:

```python
llm = LLM(
    provider="google",
    model="gemini/gemini-1.5-flash",
    api_key="your_api_key_here"  # ⚠️ Avoid hardcoding in production
)
```

---

## 🚀 Usage

1. Place your input file (PDF or TXT) in the project directory.
2. Run the script:

```bash
python quizgen.py
```

3. Example output:

```
Generated Quiz Questions:
1. What year was the Declaration of Independence signed?
   a) 1774
   b) 1775
   c) 1776 ✅
   d) 1781
...
```

---

## ⚡ Features

* **Supports PDF & TXT input files**
* Extracts text and splits into chunks for better AI context
* Generates **5 multiple-choice questions** with 4 answer options each
* Ensures **one correct answer per question**
* CrewAI `Agent` designed to **stick to document content only**

---

## 🛠️ Configuration

You can adjust quiz generation parameters in the `Task` definition:

```python
quiz_generation_task = Task(
    name="Generate Quiz Questions",
    description=f"""Based on the following text, generate 5 multiple-choice quiz questions.
Each question should have 4 answer options with exactly one clearly correct answer.
TEXT:
{extracted_text}
""",
    expected_output="A list of 5 multiple-choice questions with answers.",
)
```

To change:

* Number of questions → modify `"generate 5 multiple-choice..."`
* Answer format → adjust description prompt

---

## 🚧 Improvements & To-Do

1. **Security**

   * Remove hardcoded API key and use `.env` file with `python-dotenv`.

2. **CLI Arguments**

   * Allow running with custom inputs:

     ```bash
     python quizgen.py --file history.pdf --questions 10
     ```

3. **Save Output**

   * Store generated questions in a `.txt` or `.json` file instead of just printing.

4. **Question Quality Control**

   * Add filtering to ensure questions are not ambiguous.

5. **Front-End Integration**

   * Build a Streamlit/Flask web app to upload files and generate quizzes interactively.

6. **Batch Processing**

   * Generate quizzes from multiple documents in one run.

