"""Academic Model Class
"""
# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Course(models.Model):
    """Course Model

    Berikut ini detail field table Course. Setiap Course ada penanggungjawabnya (responsible) yang
    ink ke table User odoo.

    Extends:
        models.Model

    Variables:
        _name {str} -- Model Name
        name {char} -- Course Name
        description {text} -- Course Description
        responsible_id {many2one} -- Course PIC
        session_ids {one2many} -- Course Sessions
    """
    _name = 'academic.course'

    name = fields.Char(string='Name', size=100, required=True,)
    description = fields.Text(string='Description',)
    responsible_id = fields.Many2one('res.users', string='Responsible', required=True,)
    session_ids = fields.One2many('academic.session', 'course_id', string='Sessions',)

class Session(models.Model):
    """Session Model

    Berikut ini detail field table Session, table yang mencatat Session yang dimiliki oleh suatu
    Course. Setiap Session ada Instructor-nya yang link ke table Partner odoo.

    Extends:
        models.Model

    Variables:
        _name {str} -- Model Name
        name {char} -- Session Name
        course_id {many2one} -- Session Course
        instructor_id {many2one} -- Session Instructor
        start_date {date} -- Session Start Date
        duration {float} -- Session Duration
        seats {int} -- Seats Taken
        active {boolean} -- Session Status
    """
    _name = 'academic.session'

    name = fields.Char(string='Name', size=100, required=True,)
    course_id = fields.Many2one('academic.course', string='Course', required=True,)
    instructor_id = fields.Many2one('res.partner', string='Instructor', required=True,)
    start_date = fields.Date(string='Date', required=True,)
    duration = fields.Float(digits=(6, 2), help='Duration in days', string='Duration')
    seats = fields.Integer(string='Number of seats',)
    active = fields.Boolean(string='Active',)
