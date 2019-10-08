## JS Direcciones en Portal

**Nombre técnico** : js\_direcciones\_portal
**Dependencias** :
    portal
    website
    website\_sale

Versión Odoo: Community 11.0
Versión módulo: 1.0.0

**Descripción**

**-** Cuando un contacto cliente tiene precios específicos, sólo se muestran en la web si está logueado como él mismo, como el contacto padre; los hijos heredan las tarifas del padre pero no los precios específicos.
Pero en la lista de contactos para dar permisos de portal, Odoo sólo muestra al contacto padre cuando éste no tiene hijos: en cuanto hay una dirección de facturación o de envío, el padre desaparece de la lista. Así que a la fuerza hay que asignar acceso al portal a un hijo, con la consiguiente pérdida de las tarifas específicas.
A nosotros nos interesa asignar permisos de portal siempre al contacto padre, que es el que tiene las tarifas específicas.

**-** Una empresa sólo puede tener una dirección de facturación. Si hay otra dirección de facturación, se debe crear otro contacto.

**1.** Este módulo fuerza que sólo se pueda asignar acceso al portal al contacto padre, pues es el único que va a aparecer en el listado.
 ![](data:image/*;base64,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)
Los usuarios de portal previos a la instalación del módulo se mantienen.

**2.** Al crear manualmente un contacto, se crea automáticamente una dirección de facturación con los mismos datos en el momento de guardarlo. Esta dirección se puede editar, como siempre.
**3.** El módulo impide la creación manual de más de una dirección de facturación desde el panel de contacto.

# **1. Asignación de usuario de portal únicamente al contacto padre**

Esto se hace en **js\_direcciones\_portal** / **wizard** / **direcciones.py**.
En un override de la función **onchange\_portal().**
Ahora pone **contact\_partners = [partner]**
donde antes ponía **contact\_partners = partner.child\_ids or [partner]**

**for** partner **in** self.env[&#39;res.partner&#39;].sudo().browse(partner\_ids):

_    # Aquí se decide cuales son los partners que aparecen en el listado._

    **contact\_partners**  **=** **[partner]**

    **for** contact **in** contact\_partners:

**2. Creación automática de una dirección de facturación al crear un contacto empresa**

Se hace un override en la función **\_handle\_first\_contact\_creation()** de **js\_direcciones\_portal** / **models** / **partner.py**

Al guardar un contacto por vez primera, se genera una dirección de facturación con los datos del padre.
Es posible crear una dirección de facturación con datos distintos si la creamos y guardamos el contacto padre al mismo tiempo.
No se crea automáticamente si ya hay previamente creado un contacto hijo porque el condicional child\_ids == 0 no comprueba de que tipo son los hijos.
De todas formas siempre se puede editar esta única dirección de facturación.

_# Generar automáticamante una dirección de facturación al momento de crear el contacto empresa_

**if** (self.is\_company **and** len(self.child\_ids) ==0):

    invoice\_address = parent.create({

        &#39;is\_company&#39;    : False,

        &#39;type&#39;          : &#39;invoice&#39;,

        &#39;name&#39;          : self.name,

        &#39;display\_name&#39;  : self.display\_name,

        &#39;street&#39;        : self.street,

        &#39;street2&#39;       : self.street2,

        &#39;city&#39;          : self.city,

        &#39;state\_id&#39;      : self.state\_id.id,

        &#39;zip&#39;           : self.zip,

        &#39;country\_id&#39;    : self.country\_id.id,

        &#39;phone&#39;         : self.phone,

        &#39;mobile&#39;        : self.mobile,

        &#39;email&#39;         : self.email,

        &#39;parent\_id&#39;     : self.id,

    })

**3. Impedir la creación de más de una dirección de facturación**

Una empresa solo debería tener una dirección de facturación.
Override de la función **create()** de **res.partner** en **js\_direcciones\_portal** / **models** / **partner.py**
Se hace un return en la función **create()** si el **res.partner** es de tipo **invoice** y no hay otro **invoice** entre los hijos.

_# no ejecutar si es invoice y ya hay otras direcciones invoice_

hijos =self.env[&#39;res.partner&#39;].browse([vals.get(&#39;parent\_id&#39;)]).child\_ids

**for** hijo **in** hijos:

    **if** vals.get(&#39;type&#39;) ==&#39;invoice&#39; **and** hijo.type ==&#39;invoice&#39;:

        **return**

**4. dirección de facturación, si la tiene**

En las ventas **web** , Odoo siempre asigna como dirección de facturación al contacto parent. Da igual que tenga un contacto hijo que sea Dirección de facturación; lo ignora.
Para que se asigne un hijo de tipo **Dirección de Facturación** (si lo tiene) se hace un override de la función **\_prepare\_sale\_order\_values()**. Esta función sólo se ejecuta al principio, cuando el cliente web no tiene ningún pedido activo; un pedido vacío sin artículos (como un carrito abandonado) también es un pedido activo.

_# comprobar si el padre tiene algún hijo que sea dirección de facturación y asignarlo a &#39;partner\_invoice\_id&#39;_

**if** partner.child\_ids:

**    for** hijo **in** partner.child\_ids:

        **if** hijo.type ==&#39;invoice&#39;:

            values[&#39;partner\_invoice\_id&#39;] = hijo.id

También hay un **direcciones\_checkout.xml** para reemplazar el código de la página de checkout para que coja **partner\_invoice\_id** en vez de **partner\_id**.

**\&lt;template** id=&quot;js\_direcciones\_portal\_checkout&quot;inherit\_id=&quot;website\_sale.checkout&quot;name=&quot;JS Direcciones Portal Checkout&quot; **\&gt;**

**  \&lt;xpath** expr=&quot;//t[@t-set=&#39;contact&#39;][@t-value=&#39;order.partner\_id&#39;]&quot;position=&quot;replace&quot; **\&gt;**

    **\&lt;t** t-if=&quot;order.partner\_invoice\_id&quot; **\&gt;**

      **\&lt;t** t-set=&quot;contact&quot;t-value=&quot;order.partner\_invoice\_id&quot; **/\&gt;**

      **\&lt;/t\&gt;**

      **\&lt;t** t-else=&quot;&quot; **\&gt;**

        **\&lt;t** t-set=&quot;contact&quot;t-value=&quot;order.partner\_id&quot; **/\&gt;**

      **\&lt;/t\&gt;**

  **\&lt;/xpath\&gt;**

**\&lt;/template\&gt;**

**SIRET: cambiar XML de los PDFs, módulo**  **js\_custom\_reports**

_\&lt;!--_

_Presupuesto y   Pedido_

_Devis       y   Commande_

_--\&gt;_

_\&lt;!-- el id debería ser js\_pedido\_venta en vez de js\_condiciones\_de\_venta\_pedido\_venta, pero no me deja cambiarlo --\&gt;_

**\&lt;template** id=&quot; **js\_condiciones\_de\_venta\_pedido\_venta**&quot;inherit\_id=&quot;sale.report\_saleorder\_document&quot;name=&quot;JIM pedido venta&quot; **\&gt;**

_  \&lt;!-- Quitar la dirección extra que aparece en superior/derecha del PDF --\&gt;_

  **\&lt;xpath** expr=&quot;//div[@class=&#39;page&#39;]/div[@class=&#39;row&#39;]/div[@class=&#39;col-xs-5 col-xs-offset-1&#39;]&quot;position=&quot;replace&quot; **\&gt;\&lt;/xpath\&gt;**

_    \&lt;!-- Añadir siret y vat a la dirección de facturación --\&gt;_

    **\&lt;xpath** expr=&quot;//div[@class=&#39;page&#39;]/div[@class=&#39;row&#39;]/div[@class=&#39;col-xs-6&#39;]&quot;position=&quot;inside&quot; **\&gt;**

      **\&lt;span** t-if=&quot;doc.partner\_id.vat&quot; **\&gt;\&lt;t** t-esc=&quot;doc.company\_id.country\_id.vat\_label or &#39;TIN&#39;&quot; **/\&gt;** : **\&lt;span** t-field=&quot;doc.partner\_id.vat&quot; **/\&gt;**** &amp;#160;&amp;#160; ****\&lt;/span\&gt;**

      **\&lt;t** t-if=&quot;doc.partner\_id.parent\_id.siret&quot; **\&gt;**

        **\&lt;span\&gt;** SIRET: **\&lt;span** t-field=&quot;doc.partner\_id.parent\_id.siret&quot; **/\&gt;\&lt;/span\&gt;**

      **\&lt;/t\&gt;**

      **\&lt;t** t-else=&quot;&quot; **\&gt;**

        **\&lt;span** t-if=&quot;doc.partner\_id.siret&quot; **\&gt;** SIRET: **\&lt;span** t-field=&quot;doc.partner\_id.siret&quot; **/\&gt;\&lt;/span\&gt;**

      **\&lt;/t\&gt;**

**  \&lt;/xpath\&gt;**



_\&lt;!-- Añadir el SIRET --\&gt;_

**\&lt;template** id=&quot; **js\_factura\_de\_venta**&quot;inherit\_id=&quot;sale.report\_invoice\_document\_inherit\_sale&quot;name=&quot;JIM factura de venta&quot; **\&gt;**

**  \&lt;xpath** expr=&quot;//div/div[@t-if=&#39;o.partner\_id.vat&#39;]&quot;position=&quot;after&quot; **\&gt;**

    _\&lt;!-- poner el SIRET del padre si lo tiene --\&gt;_

    **\&lt;t** t-if=&quot;o.partner\_id.parent\_id.siret&quot; **\&gt;**

      **\&lt;div\&gt;** SIRET: **\&lt;t** t-esc=&quot;o.partner\_id.parent\_id.siret&quot; **/\&gt;\&lt;/div\&gt;**

    **\&lt;/t\&gt;**

    **\&lt;t** t-else=&quot;&quot; **\&gt;**

      **\&lt;div** t-if=&quot;o.partner\_id.siret&quot; **\&gt;** SIRET: **\&lt;t** t-esc=&quot;o.partner\_id.siret&quot; **/\&gt;\&lt;/div\&gt;**

    **\&lt;/t\&gt;**

  **\&lt;/xpath\&gt;**

**\&lt;/template\&gt;**