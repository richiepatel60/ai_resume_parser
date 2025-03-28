import fitz  # PyMuPDF for PDF reading
import docx
import spacy
import re
import sqlite3

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Predefined skill set
SKILL_SET = {"Python", "Java", "SQL", "Machine Learning", "NLP", "TensorFlow", "Data Science"}


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file"""
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_name(text):
    """Extract candidate name using NLP"""
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Not Found"


def extract_email(text):
    """Extract email using regex"""
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else "Not Found"


def extract_phone(text):
    """Extract phone number using regex"""
    match = re.search(r"\+?\d{10,13}", text)
    return match.group(0) if match else "Not Found"


def extract_job_title(text):
    """Extract job title using NLP"""
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "TITLE":
            return ent.text
    return "Not Found"


def extract_skills(text):
    """Extract skills by matching predefined skills"""
    found_skills = [skill for skill in SKILL_SET if skill.lower() in text.lower()]
    return found_skills if found_skills else "Not Found"


# Store data in SQLite
def store_in_db(data):
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS resumes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name TEXT, email TEXT, phone TEXT, job_title TEXT, skills TEXT)''')

    cursor.execute("INSERT INTO resumes (name, email, phone, job_title, skills) VALUES (?, ?, ?, ?, ?)",
                   (data["name"], data["email"], data["phone"], data["job_title"], ", ".join(data["skills"])))

    conn.commit()
    conn.close()


# Example Usage:
if __name__ == "__main__":
    file_path = "sample_resume.pdf"  # Change to a real file
    text = extract_text_from_pdf(file_path)  # Use extract_text_from_docx() for DOCX files

    resume_data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "job_title": extract_job_title(text),
        "skills": extract_skills(text)
    }

    print("Extracted Data:", resume_data)

    # Store in database
    store_in_db(resume_data)
