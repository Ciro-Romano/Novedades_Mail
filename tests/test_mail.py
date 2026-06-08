from pathlib import Path

from mailer import enviar_html


html = """

<h1>Prueba novedades_mail</h1>

<p>
Si recibís este correo,
el sistema SMTP funciona.
</p>

"""

enviar_html(
    asunto="Prueba novedades_mail",
    html=html
)