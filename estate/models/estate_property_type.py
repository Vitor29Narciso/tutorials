from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'name'

    name = fields.Char(string='Name', required=True)