
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import joblib
import numpy as np
import re
from resume_ai.resume_parser import extract_text_from_pdf  
from sklearn.ensemble import RandomForestRegressor

FEATURE_WEIGHTS = {
    'skills_count': 25.0,
    'experience_years': 15.0,
    'education_score': 20.0,
    'projects_count': 10.0,
    'certifications': 10.0,
    'publications': 10.0,
    'awards': 15.0,
    'leadership_exp': 30.0,
    'industry_relevance': 10.0
}

FEATURE_CAPS = {
    'skills_count': 5,           
    'experience_years': 5,       
    'education_score': 3,        
    'projects_count': 3,         
    'certifications': 3,         
    'publications': 2,          
    'awards': 2,                 
    'leadership_exp': 1.0,
    'industry_relevance': 1.0
}


def extract_features_from_text(text):
    if isinstance(text, np.ndarray):
        text = text.item() if text.size == 1 else str(text)

    common_skills = [
        'python', 'java', 'javascript', 'sql', 'machine learning',
        'data analysis', 'react', 'node.js', 'aws', 'docker',
        'kubernetes', 'tensorflow', 'odoo'
    ]
    skills_count = sum(1 for skill in common_skills if skill.lower() in text.lower())
    experience_years = extract_experience_years(text)
    education_score = extract_education_level(text)
    projects_count = count_projects(text)
    certifications = count_certifications(text)
    publications = count_publications(text)
    awards = count_awards(text)
    leadership_exp = detect_leadership_experience(text)
    industry_relevance = calculate_industry_relevance(text)

    return {
        'skills_count': skills_count,
        'experience_years': experience_years,
        'education_score': education_score,
        'projects_count': projects_count,
        'certifications': certifications,
        'publications': publications,
        'awards': awards,
        'leadership_exp': leadership_exp,
        'industry_relevance': industry_relevance
    }

def predict_resume_score(pdf_path, avg_skill_match=None):
    text = extract_text_from_pdf(pdf_path)

    if not text.strip():
        print("⚠️ Resume text is empty — returning score 0")
        return 0, 0 

    features = extract_features_from_text(text)

    weighted_sum = 0
    max_possible = 0

    for key in features:
        value = min(features[key], FEATURE_CAPS[key])
        weighted_sum += value * FEATURE_WEIGHTS[key]
        max_possible += FEATURE_CAPS[key] * FEATURE_WEIGHTS[key]

    resume_score = round((weighted_sum / max_possible) * 100, 2)

    if avg_skill_match is not None:
        total_score = round((0.4 * resume_score) + (0.6 * avg_skill_match), 2)
        print(f"✅ Resume Score: {resume_score}, Skill Match: {avg_skill_match}, Total Score: {total_score}")
        return resume_score, total_score
    else:
        print(f"✅ Resume Score (AI only): {resume_score}")
        return resume_score, resume_score  


def extract_experience_years(text):
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?experience',
        r'experience\s*(?:of\s*)?(\d+)\+?\s*(?:years?|yrs?)',
        r'worked\s*(?:for\s*)?(\d+)\+?\s*(?:years?|yrs?)'
    ]
    max_years = 0
    for pattern in patterns:
        matches = re.finditer(pattern, text.lower())
        for match in matches:
            years = int(match.group(1))
            max_years = max(max_years, years)
    return max_years

def extract_education_level(text):
    education_scores = {
        'phd': 4,
        'doctorate': 4,
        'master': 3,
        'mba': 3,
        'bachelor': 2,
        'undergraduate': 2,
        'high school': 1
    }
    max_score = 0
    for edu, score in education_scores.items():
        if edu in text.lower():
            max_score = max(max_score, score)
    return max_score

def count_projects(text):
    patterns = [r'project[s]?:?', r'developed', r'implemented', r'created', r'built']
    return min(sum(len(re.findall(p, text.lower())) for p in patterns), 10)

def count_certifications(text):
    patterns = [r'certification[s]?', r'certified', r'certificate[s]?']
    return min(sum(len(re.findall(p, text.lower())) for p in patterns), 5)

def count_publications(text):
    patterns = [r'publication[s]?', r'published', r'journal', r'conference paper', r'research paper']
    return min(sum(len(re.findall(p, text.lower())) for p in patterns), 5)

def count_awards(text):
    patterns = [r'award[s]?', r'recognition[s]?', r'achievement[s]?', r'honor[s]?', r'won']
    return min(sum(len(re.findall(p, text.lower())) for p in patterns), 5)

def detect_leadership_experience(text):
    keywords = ['lead', 'manager', 'supervisor', 'head', 'chief', 'director', 'coordinator', 'team leader']
    return min(sum(1 for k in keywords if k in text.lower()) / len(keywords), 1)

def calculate_industry_relevance(text):
    keywords = ['software', 'development', 'programming', 'web', 'mobile', 'cloud', 'database', 'api', 'agile', 'devops', 'odoo']
    return sum(1 for k in keywords if k in text.lower()) / len(keywords)





