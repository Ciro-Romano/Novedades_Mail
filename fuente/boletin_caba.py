import requests

from utils.clasificador import (
    determinar_prioridad
)

from utils.filtros import (
    ignorar_novedad
)

from utils.organismos import (
    ORGANISMOS_CABA,
    organismo_valido
)


URL = (
    "https://api-restboletinoficial.buenosaires.gob.ar/"
    "obtenerBoletin/0/true"
)


def obtener_novedades():

    response = requests.get(

        URL,

        headers={
            "User-Agent": "Mozilla/5.0"
        },

        timeout=30

    )

    response.raise_for_status()

    data = response.json()

    fecha = data["boletin"][
        "fecha_publicacion"
    ]

    novedades = []

    normas = data["normas"]["normas"]

    for poder, tipos in normas.items():

        for tipo_norma, organismos in tipos.items():

            for organismo, items in organismos.items():

                if not organismo_valido(
                    organismo,
                    ORGANISMOS_CABA
                ):
                    continue

                for item in items:

                    titulo = item.get(
                        "nombre",
                        ""
                    )

                    resumen = item.get(
                        "sumario",
                        ""
                    )

                    texto = (
                        f"{titulo} {resumen}"
                    )

                    if ignorar_novedad(
                        texto
                    ):
                        continue

                    novedades.append({

                        "fuente":
                            "BOLETIN_CABA",

                        "prioridad":
                            determinar_prioridad(
                                texto
                            ),

                        "fecha":
                            fecha,

                        "titulo":
                            titulo,

                        "resumen":
                            resumen,

                        "link":
                            item.get(
                                "url_norma",
                                ""
                            ),

                        "organismo":
                            organismo,

                        "tipo":
                            tipo_norma,

                        "poder":
                            poder,

                    })

    return novedades


if __name__ == "__main__":

    novedades = obtener_novedades()

    print(
        f"\nTotal relevantes: "
        f"{len(novedades)}"
    )