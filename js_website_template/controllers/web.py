# -*- coding: utf-8 -*-
from odoo import http, tools, _
from odoo.addons.web.controllers.main import Binary
import os

class JsBinary(Binary):
    # Para cambiar la imágen por defecto cuando no hay una
    def placeholder(self, image='placeholder.png'):
        if image == 'placeholder.png':
            js_website_template_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            return open(os.path.join(js_website_template_path, 'static', 'img', image), 'rb').read()
        return super(JsBinary, self).placeholder(image)
