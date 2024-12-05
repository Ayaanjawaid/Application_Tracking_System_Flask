from flask import Flask, render_template, request
from ats_utils import parse_resume, extract_keywords, match_keywords

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    suggestions = None
    unmatched_keywords = None

    if request.method == "POST":
        # Get form data
        resume_file = request.files.get("resume")
        job_description = request.form.get("job_description")

        if resume_file and job_description:
            # Parse resume
            resume_text = parse_resume(resume_file)

            # Extract keywords from job description
            keywords = extract_keywords(job_description)

            # Match keywords
            matched_keywords, match_percentage = match_keywords(resume_text, keywords)

            # Suggestions for improvement
            unmatched_keywords = [kw for kw in keywords if kw not in matched_keywords]
            suggestions = (
                f"The following keywords were not found in the resume: {', '.join(unmatched_keywords)}."
                if unmatched_keywords
                else "Great job! Your resume aligns well with the job description."
            )

            # Results to display
            result = {
                "match_percentage": match_percentage,
                "matched_keywords": matched_keywords,
                "suggestions": suggestions,
            }

    return render_template("index.html", result=result, unmatched_keywords=unmatched_keywords)

if __name__ == "__main__":
    app.run(debug=True)
