# AI Powered Resume Parser

The AI Powered Resume Parser is a practical application designed to streamline the resume processing workflow. It efficiently extracts essential information from PDF and DOCX format resumes, including candidate names, email addresses, phone numbers, job titles, and relevant skills. Built with a user-friendly Streamlit interface, the application allows users to simply upload resumes and instantly view the extracted information. The system leverages Natural Language Processing (NLP) through spaCy for accurate name and job title extraction, while utilizing regular expressions for contact information parsing. All extracted data is systematically stored in a SQLite database, enabling easy access and management of multiple resumes. This tool is particularly valuable for HR professionals and recruiters, significantly reducing the time spent on manual resume screening and data entry tasks.



### Technologies Used
1. Core Libraries :
- spacy : For NLP tasks
- PyMuPDF (fitz): For PDF processing
- python-docx : For DOCX processing
- sqlite3 : For database operations
- streamlit : For web interface
2. NLP Model :
- Uses spaCy's en_core_web_sm model for entity recognition
### How It Works
1. Upload Process :
- User uploads a resume through Streamlit interface
- System checks file format (PDF/DOCX)
- Extracts text content
2. Information Extraction :
- Processes text through various extraction functions
- Uses NLP for name and job title
- Uses regex for contact details
- Matches skills against predefined list
3. Storage :
- Stores extracted information in SQLite database
- Creates table if not exists
- Each resume gets unique ID
4. Display :
- Shows extracted information immediately after upload
- Provides option to view all stored resumes
