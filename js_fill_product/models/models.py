# -*- coding: utf-8 -*-
# © 2018 Miguel Ángel García <info@miguel-angel-garcia.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, api
import urllib
import base64

class js_fill_product(models.Model):
     _name = 'js_fill_product.js_fill_product'

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _name = 'product.template'
    
    # Descarga las imágenes para el producto desde el servidor de Jim Sports
    @api.one
    def js_download_images(self):
        
        # Comprobamos que el producto tenga asignado código
        if self.default_code == False or self.default_code == None or self.default_code == '':
            return(False)
            
        # URL de las imágenes
        URL = "http://resources.jimsports.website/Intranet/images/"
        # Nombre del fichero
        image_name = self.default_code + ".jpg"
        
        # Carga la imagen principal
        try:
            image = urllib.request.urlopen(URL + image_name).read()
        except urllib.error.URLError as e:
            print("ERROR en la descarga de la imagen: ", e.reason)
            return(False)        
        imageBase64 = base64.b64encode(image)
        self.image_medium = imageBase64
        
        # Carga las imágenes secundarias
        images = []        
        i = 1
        # Bucle para generar las combinaciones de nombres
        while True:
            image_name = self.default_code + '-' + str(i)
            try:
                image = urllib.request.urlopen(URL + image_name + ".jpg").read()
            except urllib.error.URLError as e:
                # Borramos las imágenes antiguas
                for product_image in self.product_image_ids:
                    product_image.unlink()

                # Si la combinación de nombre no se encuentra, guardamos las imágenes encontradas y salimos
                self.write({'product_image_ids': [(6, 0, images)]})
                return(True)
            imageBase64 = base64.b64encode(image)
            new_image = self.product_image_ids.create({'name': image_name, 'image': imageBase64})
            images.append(new_image.id)
            i += 1

    @api.model
    def batch_update(self):
        print('[js_fill_product] ****** Inicio del proceso de descarga de imágenes ******')
        product_list = self.search([('sale_ok', '=', True),
                                        ('default_code', '!=', False),
                                        # ('default_code', 'not like', '%ñ%'),
                                        # ('default_code', 'not like', '%Ñ%'),
                                        ('type', '=', 'product')],
                                        order='id')

        debug_total = str(len(product_list))
        print('[js_fill_product] Se recorrerán {} productos'.format(debug_total))
        
        for product in product_list:
            if product.js_download_images():
                print('[js_fill_product] Descargadas las imágenes de {}'.format(product.default_code))

        print('[js_fill_product] ****** Fin del proceso de descarga de imágenes ******')


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _name = 'product.product'
    
    @api.one
    def js_download_images(self):
        # Llamamos a la función del template para que no dé error desde product.product
        self.product_tmpl_id.js_download_images()

