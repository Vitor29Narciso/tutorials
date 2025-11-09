from odoo import models, fields, api
from odoo.exceptions import UserError

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')

    @api.constrains('name')
    def _check_tag_name_unique(self):
        for record in self:
            if record.name:
                existing = self.search([('name', '=', record.name), ('id', '!=', record.id)])
                if existing:
                    raise UserError('A property tag name must be unique.')
