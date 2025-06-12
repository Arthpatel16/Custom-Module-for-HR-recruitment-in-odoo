from odoo import models, fields,api

class HrJobSkill(models.Model):
    _name = 'hr.job.skill'
    _description = 'Job Skill'

    job_id = fields.Many2one('hr.job', string="Job")
    name = fields.Char("Skill Name", required=True)
   
class HrJobSkillRel(models.Model):
    _name = 'hr.job.skill.rel'
    _description = 'Must-Have Job Skill Relation'

    job_id = fields.Many2one('hr.job', required=True, ondelete='cascade')
    skill_id = fields.Many2one('hr.skill', required=True, ondelete='cascade')

    level_id = fields.Many2one(
        'hr.skill.level',
        string='Skill Level',
    )

    match_percent = fields.Integer(
        string='Match %',
        required=True,
        default=100.0
    )

    @api.onchange('level_id')
    def _onchange_level_id(self):
        for rec in self:
            if rec.level_id:
                rec.match_percent = rec.level_id.level_progress


class HrJob(models.Model):
    _inherit = 'hr.job'

    must_have_skill_rel_ids = fields.One2many(
        'hr.job.skill.rel', 
        'job_id', 
        string='Must-Have Skills'
    )

    good_to_have_skill_ids = fields.Many2many(
        'hr.skill', 
        'hr_job_good_skill_rel',
        'job_id', 
        'skill_id', 
        string='Good to Have Skills'
    )

    optional_skill_ids = fields.Many2many(
        'hr.skill', 
        'hr_job_optional_skill_rel', 
        'job_id', 
        'skill_id', 
        string='Optional / Any Skills'
    )
