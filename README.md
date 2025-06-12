# Intelligent Candidate Screening for Odoo Recruitment

This project is an AI-powered enhancement to the Odoo `hr_recruitment` module. It introduces **Intelligent Candidate Screening** capabilities that automatically parse resumes, extract skills, match them with job requirements, and calculate relevance scores — helping recruiters shortlist the best candidates faster and more accurately.

## 🔍 Features

- ✅ Resume parsing and skill extraction
- ✅ Must-have and Good-to-have skill matching
- ✅ Total score computation (resume + skill match)
- ✅ Custom Owl components:
  - Circular pie chart for skill match percentage
  - Green-highlighted matched skills
- ✅ Visual UI integration into the applicant form
- ✅ Easily extendable for NLP-based enhancements

## 📂 Module Structure
intelligent_candidate_screening/
├── init.py
├── manifest.py
├── models/
│ └── hr_applicant.py
├── views/
│ └── hr_applicant_views.xml
├── static/
│ └── src/
│ ├── js/
│ │ └── matched_skills_highlight.js
│ ├── css/
│ │ └── matched_skills_highlight.css
│ └── xml/
│ └── matched_skills_highlight.xml
