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
    responsible_id = fields.Many2one('res.users', ondelete="set null", string='Responsible', index=True,)
    session_ids = fields.One2many('academic.session', 'course_id', string='Sessions', copy=True,)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count([("name", "=like", u"Copy of {}%".format(self.name))])

        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default["name"] = new_name
        return super(Course, self).copy(default)