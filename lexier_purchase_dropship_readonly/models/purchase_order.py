# Copyright 2022 NuoBiT - Frank Cespedes <fcespedes@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    dest_address_id = fields.Many2one(states={}, tracking=True)
