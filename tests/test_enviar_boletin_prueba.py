from pathlib import Path
import sys

ROOT = Path(__file__).parent.parent

sys.path.append(
    str(ROOT)
)

from pathlib import Path
import subprocess
import sys

from scripts.mailer import enviar_html


ROOT = Path(__file__).parent.parent


def generar_boletin():

    subprocess.run(
        [sys.executable, str(ROOT / "tests" / "test_main.py")],
        check=True
    )


def leer_html():

    with open(
        ROOT / "boletin.html",
        "r",
        encoding="utf-8"
    ) as f:

        html = f.read()

    with open(
        ROOT / "static" / "estilos.css",
        "r",
        encoding="utf-8"
    ) as f:

        css = f.read()

    html = html.replace(
        "</head>",
        f"<style>{css}</style></head>"
    )

    return html

def obtener_boletin_anterior():

    carpeta = ROOT / "tests" / "boletines_prueba"

    if not carpeta.exists():
        return None

    archivos = sorted(
        carpeta.glob("*.html")
    )

    if len(archivos) < 2:
        return None

    return str(
        archivos[-2]
    )

if __name__ == "__main__":

    print("Generando boletín...")

    generar_boletin()

    print("Leyendo HTML...")

    html = leer_html()

    print("Enviando correo...")

    boletin_anterior = (
        obtener_boletin_anterior()
    )

    adjuntos = []

    if boletin_anterior:

        adjuntos.append(
            boletin_anterior
        )

    enviar_html(
        asunto="Boletín de Novedades",
        html=html,
        grupo="pruebas",
        adjuntos=adjuntos
    )

    print("Proceso finalizado.")
