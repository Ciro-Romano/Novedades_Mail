import json
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from pathlib import Path


ROOT = Path(__file__).parent.parent

CONFIG_DIR = ROOT / "config"


def cargar_config():

    with open(
        CONFIG_DIR / "mail.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def cargar_destinatarios():

    with open(
        CONFIG_DIR / "destinatarios.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def enviar_html(
    asunto,
    html,
    grupo="boletin"
):

    config = cargar_config()

    destinatarios = cargar_destinatarios()

    remitente = config["email"]
    password = config["password"]

    lista_destinatarios = (
        destinatarios[grupo]
    )

    mensaje = MIMEMultipart("alternative")

    mensaje["Subject"] = asunto
    mensaje["From"] = remitente
    mensaje["To"] = ", ".join(
        lista_destinatarios
    )

    mensaje.attach(

        MIMEText(
            html,
            "html",
            "utf-8"
        )

    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as servidor:

        servidor.login(
            remitente,
            password
        )

        servidor.sendmail(
            remitente,
            lista_destinatarios,
            mensaje.as_string()
        )

    print(
        f"Mail enviado a "
        f"{len(lista_destinatarios)} "
        f"destinatarios"
    )