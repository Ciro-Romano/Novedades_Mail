import requests

from datetime import datetime
from datetime import timedelta

from utils.clasificador import (
    determinar_prioridad
)

from utils.filtros import (
    ignorar_novedad
)


URL = (
    "https://servicioscf.afip.gob.ar/publico/"
    "sitio/contenido/novedad/listado.aspx/ListarNovedades"
)

LIMITE_DIAS = 30


def obtener_novedades():

    response = requests.post(

        URL,

        json={},

        headers={
            "Content-Type": (
                "application/json; charset=utf-8"
            ),
            "User-Agent": "Mozilla/5.0"
        },

        timeout=30

    )

    response.raise_for_status()

    data = response.json()

    novedades = []

    fecha_limite = (
        datetime.now()
        - timedelta(days=LIMITE_DIAS)
    )

    for item in data["d"]["data"]:

        try:

            fecha_novedad = datetime.strptime(

                item["FechaString"],
                "%d/%m/%Y"

            )

        except Exception:

            continue

        if fecha_novedad < fecha_limite:

            continue

        titulo = item["Titulo"]

        resumen = item["Copete"]

        texto = (
            f"{titulo} {resumen}"
        )

        if ignorar_novedad(texto):

            continue

        prioridad = determinar_prioridad(
            texto
        )

        novedades.append({

            "fuente": "ARCA",

            "prioridad": prioridad,

            "fecha": item["FechaString"],

            "titulo": titulo,

            "resumen": resumen,

            "link": (
                "https://servicioscf.afip.gob.ar/"
                "publico/sitio/contenido/novedad/"
                f"ver.aspx?id={item['Id']}"
            )

        })

    return novedades


if __name__ == "__main__":

    novedades = obtener_novedades()

    print(
        "\n=== NOVEDADES ARCA ===\n"
    )

    for n in novedades:

        print(
            f"[{n['prioridad']}]"
        )

        print(
            n["fecha"]
        )

        print(
            n["titulo"]
        )

        print(
            n["resumen"]
        )

        print(
            n["link"]
        )

        print(
            "-" * 80
        )

    print(
        f"\nTotal relevantes: "
        f"{len(novedades)}"
    )