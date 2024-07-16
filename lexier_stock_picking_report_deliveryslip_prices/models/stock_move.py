# Copyright 2022 NuoBiT - Frank Cespedes <fcespedes@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_uom_rate_conversion(self, uom_from, uom_to):
        def _get_uom_rate(uom):
            uom_rate = uom.factor_inv
            if uom.uom_type == "smaller":
                uom_rate = 1 / uom_rate
            return uom_rate

        if not uom_from or not uom_to:
            return 1
        if uom_from == uom_to:
            return 1
        if uom_from.category_id != uom_to.category_id:
            raise UserError(
                _("Cannot convert the units of the product %s")
                % (self.product_id.default_code or self.product_id.name)
            )
        return _get_uom_rate(uom_from) / _get_uom_rate(uom_to)

    sale_price_unit = fields.Float(
        "Sale unit price",
        compute="_compute_move_price_unit",
        digits="Product Price",
    )

    def _compute_move_price_unit(self):
        for rec in self:
            factor_rate = rec._get_uom_rate_conversion(
                rec.sale_line_id.product_uom, rec.product_uom
            )
            rec.sale_price_unit = (
                rec.sale_line_id.price_unit
                / factor_rate
                * (1 - (rec.sale_line_id.discount or 0.0) / 100.0)
            )

    def _get_amounts(self):
        self.ensure_one()
        taxes = self.sale_line_id.tax_id.compute_all(
            self.sale_price_unit,
            self.sale_line_id.order_id.currency_id,
            self.product_qty,
            product=self.product_id,
            partner=self.picking_id.partner_id,
        )
        return {
            "tax": sum(t.get("amount", 0.0) for t in taxes.get("taxes", [])),
            "total": taxes["total_included"],
            "subtotal": taxes["total_excluded"],
        }
