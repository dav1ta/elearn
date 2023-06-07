# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    survey_url = fields.Char(string="Survey URL")
    lessons =fields.One2many('elearn.lesson', 'survey', string='კითხვარის კავშირი')


    def action_start_survey(self):
        action = super().action_start_survey()
        self.survey_url = action['url']
        return action

    def action_start_session(self):
        action = super().action_start_session()
        print(action)
        self.survey_url = action['url']
        return action




class Subjects(models.Model):
    _name = 'elearn.subjects'
    _description = 'elearn.subjects'

    name = fields.Char(string='სახელი', required=True)


class School(models.Model):
    _name = 'elearn.school'
    _description = 'elearn.school'

    name = fields.Char(string='სახელი', required=True)




class Teacher(models.Model):
    _name = 'elearn.teacher'
    _description = 'elearn.teacher'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string='სისტემური მომხარებელი', required=True, ondelete='cascade')
    subject_id = fields.Many2one('elearn.subjects', string='საგანი', required=True)



class Student(models.Model):
    _name = 'elearn.student'
    _description = 'elearn.student'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string='სისტემური მომხმარებელი', required=True, ondelete='cascade')
    school_id = fields.Many2one('elearn.school', string='სკოლა', required=True)
    course_ids = fields.Many2many('elearn.course', 'course_student_rela', string='კურსები')
    grade = fields.Integer(string='კლასი', required=True)
    grade_letter = fields.Char(string='კლასის იდენტიფიკატორი', required=True)


class Course(models.Model):
    _name = 'elearn.course'
    _description = 'elearn.course'
    _rec_name = 'name' 

    name = fields.Char(string='Name', required=True)
    subject_id = fields.Many2one('elearn.subjects', string='საგანი', required=True)
    teacher_id = fields.Many2one('elearn.teacher', string='მასწავლებელი', required=True)
    student_ids = fields.Many2many('elearn.student', 'course_student_rela', string='მოსწავლეები')


class Simulation(models.Model):
    _name = 'elearn.simulation'
    _description = 'elearn.simulation'
    _rec_name = 'name' 

    name = fields.Char(string='Name', required=True)
    html_url = fields.Char(string='აღწერა', required=True)
    course_id = fields.Many2one('elearn.course', string='Course', required=True)
    html = fields.Html(string='აღწერა')

    def open_simulation(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.html_url,
            'target': 'new',
        }


class Lesson(models.Model):
    _name = 'elearn.lesson'
    _description = 'elearn.lesson'

    name = fields.Char(string='სახელი', required=True)
    course_id = fields.Many2one('elearn.course', string='Course', required=True)
    content = fields.Html(string='აღწერა')
    attachment_ids = fields.One2many('ir.attachment', 'res_id', string='დამატებითი ფაილები', domain=[('res_model', '=', 'elearn.lesson')])
    date = fields.Datetime(string='თარიღი', required=False)
    survey  = fields.Many2one('survey.survey', string='დამატებითი ტესტი', required=False)


    def open_current_lesson(self):
        print("hello")
        # Import the necessary libraries
        from datetime import datetime

        # Get the current date and time in the user's timezone
        user_tz = self.env.context.get('tz') or self.env.user.tz or 'UTC'
        now_user_tz = datetime.now()

        # Search for the lesson record that matches the current date and time
        lesson = self.env['elearn.lesson'].search([('date', '<=', now_user_tz)], limit=1)

        # Return an action to open the form view of this lesson
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'elearn.lesson',
            'view_mode': 'form',
            'target': 'current',
            'res_id':1,
            'flags': {'readonly':True},
            'view_id': self.env.ref('elearn-system.view_lesson_form_student').id,
        }


    def open_survey(self):
        self.ensure_one()
        survey_url = self.survey.survey_url
        return {
            'type': 'ir.actions.act_url',
            'url': survey_url,
            'target': 'new',
        }




class UserBadge(models.Model):
    _inherit = 'gamification.badge.user'

    def get_current_user_badges(self):
        self.ensure_one()
        current_user_badges = self.env['gamification.badge.user'].search([('user_id', '=', self.env.user.id)])
        return current_user_badges
