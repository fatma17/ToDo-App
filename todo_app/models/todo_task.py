from odoo import models , fields , api
from odoo.exceptions import ValidationError
from odoo.exceptions import AccessError


class TodoTask (models.Model):
    _name = 'todo.task'
    _description = 'Task'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char()
    assign_to_id=fields.Many2one('res.users', string='Related User')
    description = fields.Text()
    due_date = fields.Date(tracking=1)
    status = fields.Selection([('new','New'),
                               ('inprogress','in Progress'),
                               ('completed','Completed'),
                               ('closed','Closed')],default='new')

    ref=fields.Char(default='New',readonly=1)
    timesheet_ids= fields.One2many('time.sheet','todo_task_id')
    estimated_time=fields.Float( )
    active=fields.Boolean(default=True ,readonly=1)
    is_late= fields.Boolean()


    @api.constrains('timesheet_ids', 'estimated_time')
    def _check_total_sheet_time(self):
        for record in self:
            total_hours = sum(line.hours for line in record.timesheet_ids)
            if total_hours > record.estimated_time:
                raise ValidationError("The total hours in sheet lines cannot exceed the estimated time value!")


    def action_new (self):
        for rec in self :
            rec.status = 'new'

    def action_inprogress (self):
        for rec in self :
            rec.status = 'inprogress'

    def action_completed (self):
        for rec in self :
            rec.sudo().write({
                'status':'completed'
            })
            #rec.status = 'completed'

    def action_closed(self):
        for rec in self:
            rec.status = 'closed'

    def check_due_date (self):
        todo_task_ids=self.search([])
        for rec in todo_task_ids :
            if rec.due_date and rec.due_date < fields.date.today() and (rec.status == 'new'  or rec.status == 'inprogress' ) :
                rec.is_late=True

    def action_assign_task_wizard(self):
        action = self.env.ref('todo_app.assign_task_wizard_action').sudo().read()[0]
        action['context']={'default_task_ids':self.ids}
        return action

    @api.model
    def create(self, vals):
        res = super(TodoTask,self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('todo_seq')
        return res

    @api.model
    def write(self, vals):
        user_groups = self.env.user.groups_id.mapped('id')
        restricted_group = self.env.ref('todo_app.todo_user_group').id
        restricted_fields = ['name', 'assign_to_id' ,'description' , 'due_date' , 'timesheet_ids' ,'estimated_time']

        if  restricted_group in user_groups:
            if any(field in vals for field in restricted_fields):
                raise AccessError("You are not allowed to edit this field.")

        return super(TodoTask, self).write(vals)



class TimeSheet (models.Model):
    _name = 'time.sheet'

    todo_task_id=fields.Many2one('todo.task')
    day = fields.Date()
    description = fields.Text()
    hours=fields.Float()

