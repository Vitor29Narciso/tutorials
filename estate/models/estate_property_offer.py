from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string='Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date.date(), days=record.validity)
            else:
                # Fallback during creation when create_date is not set yet
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                # Fallback when create_date is not set yet (during creation)
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            # Check if another offer is already accepted for this property
            existing_accepted = record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted' and o.id != record.id)
            if existing_accepted:
                raise UserError("Only one offer can be accepted per property.")
            
            # Accept this offer
            record.status = 'accepted'
            
            # Set the selling price on the property
            record.property_id.selling_price = record.price
            
            # Update property state to offer_accepted
            record.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    @api.constrains('price')
    def _check_offer_price(self):
        for record in self:
            if float_compare(record.price, 0.0, precision_digits=2) <= 0:
                raise UserError('An offer price must be strictly positive.')