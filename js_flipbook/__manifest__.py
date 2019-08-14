{
    "name": "JS Flipbook",
    "summary": "Libro online basado en la librería turn.js",
    "description": """
    Basado en el modelo http://www.turnjs.com/#samples/magazine1

    Intrucciones:

    - Cambiar la URL en el controlador.
    - Las opciones de la librería se añaden en el <script> final del xml. Consultar la web de la librería http://www.turnjs.com/#api
    - Extraer los jpg del PDF.
    - Añadir los jpg en static/img/magazine/pages.
        - 1.jpg, 2.jpg, 3.jpg ... son las páginas normales 1, 2, 3 ...
        - 1-large.jpg, 2-large.jpg,, 1-large.jpg, ... son los jpg de las páginas en zoom.
        - 1-thumb, 2-thumb, 3-thumb ... serían las minuaturas de las páginas.
        - Los #-regions.json son para habilitar áreas clicables dentro de las páginas, con enlaces.
    """,
    "version": "1.0",
    "license": "AGPL-3",
    "author": "Jim Sports",
    "category": "Uncategorized",
    "website": "https://jimsports.com",
    'data': [
         'views/flipbook.xml',        
    ],    
    'depends': ['website'],
}
