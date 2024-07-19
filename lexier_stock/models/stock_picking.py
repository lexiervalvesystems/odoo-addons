# Copyright 2022 NuoBiT - Frank Cespedes <fcespedes@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    pickup_address_id = fields.Many2one(
        comodel_name="res.partner",
        states={"done": [("readonly", True)], "cancel": [("readonly", True)]},
        tracking=True,
    )
