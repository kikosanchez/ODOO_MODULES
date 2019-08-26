# -*- coding: utf-8 -*-
from odoo import http, tools, _
from odoo.addons.web.controllers.main import Binary
import os

class JsBinary(Binary):
    # Para cambiar la imágen por defecto cuando no hay una
    def placeholder(self, image='placeholder.png'):
        if image == 'placeholder.png':
            addons_path = http.addons_manifest['web']['addons_path']
            return open(os.path.join(addons_path, 'js_website_template', 'static', 'img', image), 'rb').read()
        return super(JsBinary, self).placeholder(image)
