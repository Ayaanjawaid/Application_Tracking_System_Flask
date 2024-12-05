import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer

def parse_resume(file_obj):
    """Extract text from a PDF resume."""
    reader = PyPDF2.PdfReader(file_obj)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_keywords(job_description, top_n=10):
    """Extract top N keywords from a job description using TF-IDF."""
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([job_description])
    keywords = sorted(
        list(zip(vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0])),
        key=lambda x: x[1],
        reverse=True
    )
    return [word for word, score in keywords[:top_n]]

def match_keywords(resume_text, job_keywords):
    """Match keywords from the resume text with job keywords."""
    matched = [word for word in job_keywords if word in resume_text.lower()]
    match_percentage = (len(matched) / len(job_keywords)) * 100
    return matched, match_percentage
