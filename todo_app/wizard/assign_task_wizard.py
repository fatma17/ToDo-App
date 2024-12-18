from odoo import models , fields
from odoo.exceptions import UserError


class AssignTask (models.TransientModel):
    _name = 'assign.task'

    task_ids = fields.Many2many('todo.task', string="Tasks")
    employee_id = fields.Many2one('res.users', string='Related User')

    def action_confirm (self):
        invalid_tasks = self.task_ids.filtered(lambda task: task.status in ['completed', 'closed'])
        if invalid_tasks:
            raise UserError("You cannot select tasks that are already completed or closed.")
        for task in self.task_ids:
            task.write({'assign_to_id': self.employee_id.id})
        return {'type': 'ir.actions.act_window_close'}

