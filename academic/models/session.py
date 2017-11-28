from odoo import models, fields, api, exceptions
from datetime import timedelta

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
    course_id = fields.Many2one('academic.course', ondelete="cascade", string='Course', required=True,)
    instructor_id = fields.Many2one('res.partner', string='Instructor', domain=[("is_instructor", "=", True), ("category_id.name", "ilike", "Teacher")])
    start_date = fields.Date(string='Start Date', default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help='Duration in days',)
    end_date = fields.Date(string="End Date", store=True, compute="_get_end_date", inverse="_set_end_date")
    seats = fields.Integer(string='Number of seats',)
    attendee_ids = fields.Many2many("res.partner", string="Attendees",)
    taken_seats = fields.Float(string="Taken seats", compute="_compute_taken_seats",)
    color = fields.Integer()
    is_active = fields.Boolean(default=True,)
    hours = fields.Float(string="Duration in hours", compute="_get_hours", inverse="_set_hours",)
    attendees_count = fields.Integer(string="Attendees count", compute="_compute_attendeec_count",)

    @api.depends("seats", "attendee_ids")
    def _compute_taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.depends("start_date", "end_date")
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            start_date = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                continue

            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1

    @api.depends("duration")
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24

    @api.depends('attendee_ids')
    def _compute_amount(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)


    @api.onchange("seats", "attendee_ids")
    def _onchange_verify_valid_seats(self):
        self._compute_taken_seats()
        if self.seats < 0:
            return {
                "warning": {
                    "title": "Incorrect 'seats' value",
                    "message": "The number of available seats may not be negative"
                }
            }
        if self.seats < len(self.attendee_ids):
            return {
                "warning": {
                    "title": "Too many attendees",
                    "message": "Increase seats or remove excess attendees"
                }
            }

    @api.constrains("instructor_id", "attendee_ids")
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")