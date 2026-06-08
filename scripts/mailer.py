import json
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

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
    grupo="boletin",
    adjuntos=None
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

    if adjuntos:

        for archivo in adjuntos:

            ruta = Path(archivo)

            if not ruta.exists():
                continue

            with open(ruta, "rb") as f:

                parte = MIMEBase(
                    "application",
                    "octet-stream"
                )

                parte.set_payload(
                    f.read()
                )

            encoders.encode_base64(
                parte
            )

            parte.add_header(
                "Content-Disposition",
                f'attachment; filename="{ruta.name}"'
            )

            mensaje.attach(
                parte
            )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as servidor:

        servidor.login(
            remitente,
            password
        )

        print(
            f"DESTINATARIOS: {lista_destinatarios}"
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