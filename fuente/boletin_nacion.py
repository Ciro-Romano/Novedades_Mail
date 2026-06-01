import re
import requests

from bs4 import BeautifulSoup

from utils.clasificador import (
    determinar_prioridad
)

from utils.filtros import (
    ignorar_novedad
)

from utils.relevancia import (
    es_relevante
)

from utils.organismos import (
    ORGANISMOS_NACION,
    organismo_valido
)


URL = (
    "https://www.boletinoficial.gob.ar/"
    "seccion/primera"
)

HEADERS = {

    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0.0.0 "
        "Safari/537.36"
    )

}


def limpiar(texto):

    return re.sub(
        r"\s+",
        " ",
        texto
    ).strip()


def obtener_novedades():

    try:

        response = requests.get(

            URL,

            headers=HEADERS,

            timeout=30

        )

        response.raise_for_status()

        soup = BeautifulSoup(

            response.text,

            "html.parser"

        )

        novedades = []

        avisos = soup.select(
            "a[href*='/detalleAviso/']"
        )

        for aviso in avisos:

            organismo_tag = aviso.select_one(
                "p.item"
            )

            detalle_tags = aviso.select(
                "p.item-detalle"
            )

            if not organismo_tag:
                continue

            organismo = limpiar(
                organismo_tag.get_text()
            )

            titulo = ""

            if detalle_tags:

                titulo = limpiar(
                    detalle_tags[0].get_text()
                )

            texto = (
                f"{organismo} {titulo}"
            )

            if not organismo_valido(
                organismo,
                ORGANISMOS_NACION
            ):
                continue

            if ignorar_novedad(
                texto
            ):
                continue

            if not es_relevante(
                texto
            ):
                continue

            href = aviso.get(
                "href",
                ""
            )

            enlace = (
                "https://www.boletinoficial.gob.ar"
                + href
            )

            novedades.append({

                "fuente":
                    "BOLETIN_NACION",

                "prioridad":
                    determinar_prioridad(
                        texto
                    ),

                "titulo":
                    titulo,

                "organismo":
                    organismo,

                "enlace":
                    enlace,

            })

        return novedades

    except Exception as e:

        print(
            f"[ERROR BOLETIN] {e}"
        )

        return []


if __name__ == "__main__":

    novedades = obtener_novedades()

    print(
        f"\nNovedades encontradas: "
        f"{len(novedades)}"
    )