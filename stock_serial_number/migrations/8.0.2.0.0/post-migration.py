# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    cr.execute("""UPDATE product_template SET use_serial_number = TRUE
                  WHERE id IN (
                    SELECT product_tmpl_id
                    FROM product_product WHERE use_serial_number=TRUE)""")
    cr.execute("""ALTER TABLE product_product DROP COLUMN use_serial_number""")
