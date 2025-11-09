from odoo import models, fields, api
from odoo.exceptions import UserError

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(string='Offer Count', compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    @api.constrains('name')
    def _check_type_name_unique(self):
        for record in self:
            if record.name:
                existing = self.search([('name', '=', record.name), ('id', '!=', record.id)])
                if existing:
                    raise UserError('A property type name must be unique.')