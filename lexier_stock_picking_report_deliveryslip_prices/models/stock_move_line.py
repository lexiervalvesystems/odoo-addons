# Copyright 2022 NuoBiT - Frank Cespedes <fcespedes@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_product_quantities(self, **kwargs):
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        for move_line in self:
            name = move_line.product_id.display_name
            description = move_line.move_id.description_picking
            if description == name or description == move_line.product_id.name:
                description = False
            uom = move_line.product_uom_id
            line_key = (
                str(move_line.product_id.id)
                + "_"
                + name
                + (description or "")
                + "uom "
                + str(uom.id)
            )

            if line_key in aggregated_move_lines:
                aggregated_move_lines[line_key][
                    "sale_line"
                ] = move_line.move_id.sale_line_id
                aggregated_move_lines[line_key][
                    "sale_price_unit"
                ] = move_line.move_id.sale_price_unit
                aggregated_move_lines[line_key][
                    "line_amounts"
                ] = move_line.move_id._get_amounts()
        return aggregated_move_lines
