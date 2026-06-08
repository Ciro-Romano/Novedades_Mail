import json
from pathlib import Path
from datetime import datetime


ARCHIVO = Path("tests/enviados_prueba.json")


def cargar_enviados():

    if not ARCHIVO.exists():
        return []

    with open(
        ARCHIVO,
        "r",
        encoding="utf-8"
    ) as archivo:

        return json.load(archivo)


def guardar_enviados(enviados):

    with open(
        ARCHIVO,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            enviados,
            archivo,
            ensure_ascii=False,
            indent=4
        )


def fue_enviada(novedad):

    historial = cargar_enviados()

    titulo = (
        novedad["titulo"]
        .strip()
        .lower()
    )

    for boletin in historial:

        for item in boletin.get(
            "novedades",
            []
        ):

            if (
                item["titulo"]
                .strip()
                .lower()
                == titulo
            ):

                return True

    return False


def registrar_envio(novedades):

    historial = cargar_enviados()

    boletin = {

        "fecha_boletin": (
            datetime.now()
            .strftime("%Y-%m-%d")
        ),

        "novedades": []

    }

    for novedad in novedades:

        boletin["novedades"].append({

            "titulo": novedad["titulo"],

            "fuente": novedad["fuente"],

            "score": novedad.get(
                "score",
                0
            ),

            "fecha": novedad.get(
                "fecha"
            ),

            "link": (
                novedad.get("link")
                or novedad.get("enlace")
            )

        })

        historial.append(
            boletin
        )

        guardar_enviados(
            historial
        )


def obtener_semana_anterior():

    historial = cargar_enviados()

    if not historial:
        return []

    ultimo_boletin = historial[-1]

    return ultimo_boletin.get(
        "novedades",
        []
    )