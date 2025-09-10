import os
from crewai import Agent, Task, Crew, LLM
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Initialize LLM
llm = LLM(
    provider="google",
    model="gemini/gemini-1.5-flash",
    api_key="AIzaSyA3FeYSioIDTLAADAk73jdCzRlHu20jqqw"  # ⚠️ Do NOT expose this key in real projects!
)

# Agent: Quiz Question Generator
quiz_generator_agent = Agent(
    role="Quiz Question Generator",
    goal="Generate quiz questions strictly from the document content provided, not from task instructions.",
    backstory="A teacher who uses textbooks and lesson plans to write high-quality multiple-choice questions.",
    llm=llm,
    verbose=True
)

# Function to extract text
def extract_text_from_document(document_path: str) -> str:
    if document_path.lower().endswith(".pdf"):
        try:
            loader = PyPDFLoader(document_path)
            pages = loader.load_and_split()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            docs = text_splitter.split_documents(pages)
            return "\n\n".join([doc.page_content for doc in docs])
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return ""
    elif document_path.lower().endswith(".txt"):
        try:
            with open(document_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading TXT file: {e}")
            return ""
    else:
        raise ValueError("Unsupported document format. Please provide a .pdf or .txt file.")

# Main function to run CrewAI
def run_quiz_generation_crew(document_path: str):
    extracted_text = extract_text_from_document(document_path)

    if not extracted_text.strip():
        print("No text was extracted from the document.")
        return

    quiz_generation_task = Task(
        name="Generate Quiz Questions",
        description=f"""Based on the following text, generate 5 multiple-choice quiz questions.
Each question should have 4 answer options with exactly one clearly correct answer.

TEXT:
{extracted_text}
""",
        agent=quiz_generator_agent,
        expected_output="A list of 5 multiple-choice questions with answers.",
        context=[]  # Empty context: all necessary input is embedded in `description`
    )

    crew = Crew(
        agents=[quiz_generator_agent],
        tasks=[quiz_generation_task],
        verbose=True
    )

    result = crew.kickoff()
    return result

# Run the script
if __name__ == "__main__":
    document_path = "THE-USA.pdf"
    quiz_questions = run_quiz_generation_crew(document_path)
    if quiz_questions:
        print("\nGenerated Quiz Questions:\n", quiz_questions)
