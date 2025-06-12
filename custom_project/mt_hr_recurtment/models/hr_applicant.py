import sys
import os, base64, tempfile, re
import pandas as pd

from odoo import models, fields, api
from odoo.exceptions import ValidationError

sys.path.append('/Users/arthpatel/Desktop/odooprojects')

from resume_ai.predict import predict_resume_score
from resume_ai.resume_parser import extract_text_from_pdf

countries_df = pd.read_csv('custom_project/mt_hr_recurtment/security/countries.csv')
states_df = pd.read_csv('custom_project/mt_hr_recurtment/security/states.csv')
cities_df = pd.read_csv('custom_project/mt_hr_recurtment/security/cities.csv')

all_locations = set(countries_df['name'].str.lower()) | \
                set(states_df['name'].str.lower()) | \
                set(cities_df['name'].str.lower())
ALLOWED_LOCATIONS = {'new york', 'san francisco', 'bangalore', 'mumbai'}  
def extract_locations_from_text(text):
    text = text.lower()
    words = set(re.findall(r'\b[a-z]{2,}\b', text)) 
    matched_locations = words & all_locations
    return list(matched_locations)


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    resume_atteched = fields.Binary(string="Resume Upload")
    resume_atteched_filename = fields.Char(string="Attached Filename")
    resume_score = fields.Float("Resume Score (%)")
    must_have_matched_skills_ids = fields.Many2many(
        'hr.skill',
        'applicant_must_have_skill_rel',
        'applicant_id', 'skill_id',
        string="Matched Must-Have Skills"
    )

    good_to_have_matched_skills_ids = fields.Many2many(
        'hr.skill',
        'applicant_good_to_have_skill_rel',
        'applicant_id', 'skill_id',
        string="Matched Good-to-Have Skills"
    )

    avg_skill_progress = fields.Integer(string="Avg Must-Have Skill Match (%)")
    total_score = fields.Float(string="Total Score (%)", compute="_compute_total_score", store=True)

    @api.depends('resume_score', 'avg_skill_progress')
    def _compute_total_score(self):
        for record in self:
            resume_score = record.resume_score or 0.0
            skill_score = record.avg_skill_progress or 0.0
            weighted_score = (0.4 * resume_score) + (0.6 * skill_score)
            record.total_score = round(weighted_score, 2)

    @api.model
    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if vals.get('stage_id'):
                stage_name = self.env['hr.recruitment.stage'].browse(vals['stage_id']).name.lower()
                if stage_name == 'initial qualification' and record.resume_atteched:

                    pdf_data = base64.b64decode(record.resume_atteched)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
                        temp.write(pdf_data)
                        temp_path = temp.name


                    score, _ = predict_resume_score(temp_path)
                    record.resume_score = score


                    resume_text = extract_text_from_pdf(temp_path).lower()


                    os.unlink(temp_path)


                    if not re.search(r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}', resume_text):
                        raise ValidationError("Resume appears to be missing an email address.")
                    if not re.search(r'(\+?\d{1,3})?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}', resume_text):
                        raise ValidationError("Phone number not found in resume.")

                    resume_locations = extract_locations_from_text(resume_text)
                    if not resume_locations:
                        raise ValidationError("Location not detected in resume.")

                    if not any(loc in ALLOWED_LOCATIONS for loc in resume_locations):
                        raise ValidationError("Candidate location does not meet job location requirements.")

                    if not re.search(r'\bexperience\b', resume_text, re.IGNORECASE):
                        raise ValidationError("Keyword 'experience' not found in resume.")
                    if not re.search(r'\bskills?\b', resume_text, re.IGNORECASE):
                        raise ValidationError("Keyword 'skill' or 'skills' not found in resume.")


                    matched_skills = []
                    match_percents = []

                    for rel in record.job_id.must_have_skill_rel_ids:
                        skill_name = rel.skill_id.name.lower()
                        if skill_name in resume_text:
                            matched_skills.append(rel.skill_id.id)
                            match_percents.append(rel.match_percent)


                    record.must_have_matched_skills_ids = [(6, 0, matched_skills)]
                    record.avg_skill_progress = round(
                        sum(match_percents) / len(match_percents), 2
                    ) if match_percents else 0.0

        return res
