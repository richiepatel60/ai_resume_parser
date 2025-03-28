import streamlit as st
import sqlite3
import fitz  # PyMuPDF for PDFs
import docx
import spacy
import re

# Load NLP Model
nlp = spacy.load("en_core_web_sm")

# Connect to SQLite Database
conn = sqlite3.connect("resumes.db")
cursor = conn.cursor()


# Function to Extract Text from Resume
def extract_text(file):
    if file.name.endswith(".pdf"):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    return ""


# Function to Extract Name, Email, Phone, Skills
def extract_info(text):
    doc = nlp(text)

    # Extract Name
    name = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), "Not Found")

    # Extract Email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    email = email_match.group(0) if email_match else "Not Found"

    # Extract Phone Number
    phone_match = re.search(r"\+?\d{10,13}", text)
    phone = phone_match.group(0) if phone_match else "Not Found"

    # Extract Skills (Using Keywords)
    skills = [token.text for token in doc if token.pos_ == "NOUN"]

    return name, email, phone, ", ".join(set(skills))


# Function to Store in Database
def store_data(name, email, phone, skills):
    cursor.execute("INSERT INTO resumes (name, email, phone, skills) VALUES (?, ?, ?, ?)",
                   (name, email, phone, skills))
    conn.commit()


# Create Table if Not Exists
cursor.execute('''CREATE TABLE IF NOT EXISTS resumes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, 
                    email TEXT, 
                    phone TEXT, 
                    skills TEXT)''')
conn.commit()

# Streamlit UI
st.title("📄 Resume Parser App")

# Upload Resume
uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    text = extract_text(uploaded_file)
    name, email, phone, skills = extract_info(text)

    st.subheader("Extracted Information")
    st.write(f"**📛 Name:** {name}")
    st.write(f"**📧 Email:** {email}")
    st.write(f"**📞 Phone:** {phone}")
    st.write(f"**🛠 Skills:** {skills}")

    # Store Data in DB
    store_data(name, email, phone, skills)
    st.success("✅ Resume stored successfully!")

# Show All Resumes from DB
if st.button("📂 Show All Resumes"):
    cursor.execute("SELECT name, email, phone, skills FROM resumes")
    resumes = cursor.fetchall()

    if resumes:
        st.subheader("Stored Resumes")
        for idx, resume in enumerate(resumes, start=1):
            st.write(f"📌 **Resume {idx}**")
            st.write(f"🔹 **Name:** {resume[0]}")
            st.write(f"🔹 **Email:** {resume[1]}")
            st.write(f"🔹 **Phone:** {resume[2]}")
            st.write(f"🔹 **Skills:** {resume[3]}")
            st.markdown("---")
    else:
        st.info("No resumes stored yet.")

