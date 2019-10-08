# JS Direcciones en Portal

**Nombre técnico**: js\_direcciones\_portal

**Dependencias**:  
    portal  
    website  
    website\_sale  

Versión Odoo: Community 11.0  
Versión módulo: 1.0.0

## **Descripción**

**-** Cuando un contacto cliente tiene precios específicos, sólo se muestran en la web si está logueado como él mismo, como el contacto padre; los hijos heredan las tarifas del padre pero no los precios específicos.  
Pero en la lista de contactos para dar permisos de portal, Odoo sólo muestra al contacto padre cuando éste no tiene hijos: en cuanto hay una dirección de facturación o de envío, el padre desaparece de la lista. Así que a la fuerza hay que asignar acceso al portal a un hijo, con la consiguiente pérdida de las tarifas específicas.  
A nosotros nos interesa asignar permisos de portal siempre al contacto padre, que es el que tiene las tarifas específicas.

**-** Una empresa sólo puede tener una dirección de facturación. Si hay otra dirección de facturación, se debe crear otro contacto.

**1.** Este módulo fuerza que sólo se pueda asignar acceso al portal al contacto padre, pues es el único que va a aparecer en el listado.
Los usuarios de portal previos a la instalación del módulo se mantienen.

**2.** Al crear manualmente un contacto, se crea automáticamente una dirección de facturación con los mismos datos en el momento de guardarlo. Esta dirección se puede editar, como siempre.

**3.** El módulo impide la creación manual de más de una dirección de facturación desde el panel de contacto.

## **1. Asignación de usuario de portal únicamente al contacto padre**

Esto se hace en **js\_direcciones\_portal** / **wizard** / **direcciones.py**.  
En un override de la función **onchange\_portal().**  
Ahora pone **contact\_partners = [partner]**
donde antes ponía **contact\_partners = partner.child\_ids or [partner]**

## **2. Creación automática de una dirección de facturación al crear un contacto empresa**

Se hace un override en la función **\_handle\_first\_contact\_creation()** de **js\_direcciones\_portal** / **models** / **partner.py**

Al guardar un contacto por vez primera, se genera una dirección de facturación con los datos del padre.  
Es posible crear una dirección de facturación con datos distintos si la creamos y guardamos el contacto padre al mismo tiempo.  
No se crea automáticamente si ya hay previamente creado un contacto hijo porque el condicional child\_ids == 0 no comprueba de que tipo son los hijos.  
De todas formas siempre se puede editar esta única dirección de facturación.

## **3. Impedir la creación de más de una dirección de facturación**

Una empresa solo debería tener una dirección de facturación.  
Override de la función **create()** de **res.partner** en **js\_direcciones\_portal** / **models** / **partner.py**.  
Se hace un return en la función **create()** si el **res.partner** es de tipo **invoice** y no hay otro **invoice** entre los hijos.

## **4. Dirección de facturación, si la tiene**

En las ventas **web** , Odoo siempre asigna como dirección de facturación al contacto parent. Da igual que tenga un contacto hijo que sea Dirección de facturación; lo ignora.  
Para que se asigne un hijo de tipo **Dirección de Facturación** (si lo tiene) se hace un override de la función **\_prepare\_sale\_order\_values()**.  
Esta función sólo se ejecuta al principio, cuando el cliente web no tiene ningún pedido activo; un pedido vacío sin artículos (como un carrito abandonado) también es un pedido activo.

También hay un **direcciones\_checkout.xml** para reemplazar el código de la página de checkout para que coja **partner\_invoice\_id** en vez de **partner\_id**.
