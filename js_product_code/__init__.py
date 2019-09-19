# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from . import models

def init_template_code(cr, registry):
    # Copiar a template_code el campo default_code
    cr.execute("""UPDATE product_template
        SET template_code = default_code
        WHERE default_code IS NOT NULL
        AND template_code IS NULL""")
    return True

def restore_default_code(cr, registry):
    # Copiar a default_code el campo template_code
    cr.execute("""UPDATE product_template
        SET default_code = template_code""")
    # Eliminar la columna template_code
    cr.execute("""ALTER TABLE product_template
        DROP COLUMN template_code""")
    return True
