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


URL = "https://www.consejo.org.ar/"


def obtener_novedades():

    response = requests.get(

        URL,

        timeout=15,

        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/137.0 Safari/537.36"
            )
        }

    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    novedades = []

    for a in soup.find_all(
        "a",
        href=True
    ):

        titulo = a.get_text(
            strip=True
        )

        link = a["href"]

        if not titulo:
            continue

        if "/noticias/" not in link:
            continue

        if ignorar_novedad(
            titulo
        ):
            continue

        if not es_relevante(
            titulo
        ):
            continue

        novedades.append({

            "fuente":
                "CPCECABA",

            "prioridad":
                determinar_prioridad(
                    titulo
                ),

            "titulo":
                titulo,

            "link":
                link

        })

    return novedades


if __name__ == "__main__":

    novedades = obtener_novedades()

    print(
        "\n=== NOVEDADES CPCECABA ===\n"
    )

    for n in novedades:

        print(
            f"[{n['prioridad']}]"
        )

        print(
            n["titulo"]
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