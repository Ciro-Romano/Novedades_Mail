import requests
import feedparser

from datetime import datetime
from datetime import timedelta

from utils.clasificador import (
    determinar_prioridad
)

from utils.filtros import (
    ignorar_novedad
)

from utils.relevancia import (
    es_relevante
)


URL_FEED = (
    "https://jorgevega.com.ar/"
    "?format=feed&type=rss"
)

LIMITE_DIAS = 30
MAX_NOVEDADES = 20


def obtener_novedades():

    response = requests.get(

        URL_FEED,

        headers={
            "User-Agent": "Mozilla/5.0"
        },

        timeout=30

    )

    response.raise_for_status()

    feed = feedparser.parse(
        response.text
    )

    novedades = []

    titulos_vistos = set()

    fecha_limite = (
        datetime.now()
        - timedelta(days=LIMITE_DIAS)
    )

    for item in feed.entries:

        try:

            fecha_novedad = datetime(
                *item.published_parsed[:6]
            )

        except Exception:

            continue

        if fecha_novedad < fecha_limite:

            continue

        titulo = item.title.strip()

        if titulo in titulos_vistos:

            continue

        if ignorar_novedad(
            titulo
        ):

            continue

        if not es_relevante(
            titulo
        ):

            continue

        titulos_vistos.add(
            titulo
        )

        novedades.append({

            "fuente":
                "JORGE VEGA",

            "fecha":
                fecha_novedad.strftime(
                    "%Y-%m-%d"
                ),

            "titulo":
                titulo,

            "enlace":
                item.link,

            "prioridad":
                determinar_prioridad(
                    titulo
                )

        })

        if len(novedades) >= MAX_NOVEDADES:

            break

    return novedades


if __name__ == "__main__":

    novedades = obtener_novedades()

    print(
        f"\nSe encontraron "
        f"{len(novedades)} novedades.\n"
    )

    for novedad in novedades:

        print(
            f"[{novedad['prioridad']}]"
        )

        print(
            novedad["fecha"]
        )

        print(
            novedad["titulo"]
        )

        print(
            novedad["enlace"]
        )

        print()