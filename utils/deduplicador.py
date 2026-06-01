from difflib import SequenceMatcher
import re


PALABRAS_IGNORAR = {

    # Fuentes
    "arca",
    "afip",
    "anses",
    "agip",
    "cpcecaba",
    "ignacio",
    "online",
    "jorge",
    "vega",

    # Ruido normativo
    "resolucion",
    "resolución",
    "general",
    "rg",
    "ley",
    "decreto",

}


def normalizar(texto):

    texto = texto.lower()

    texto = re.sub(
        r"[^a-záéíóúñ0-9 ]",
        " ",
        texto
    )

    palabras = texto.split()

    palabras = [

        palabra

        for palabra in palabras

        if palabra not in PALABRAS_IGNORAR

    ]

    return " ".join(
        palabras
    )


def son_parecidos(
    titulo_1,
    titulo_2
):

    titulo_1 = normalizar(
        titulo_1
    )

    titulo_2 = normalizar(
        titulo_2
    )

    similitud = SequenceMatcher(

        None,

        titulo_1,

        titulo_2

    ).ratio()

    return similitud >= 0.60


def eliminar_duplicados(
    novedades
):

    resultado = []

    eliminados = 0

    for novedad in novedades:

        duplicado = False

        for existente in resultado:

            if son_parecidos(

                novedad["titulo"],
                existente["titulo"]

            ):

                duplicado = True
                eliminados += 1
                break

        if not duplicado:

            resultado.append(
                novedad
            )

    print(
        f"[INFO] Duplicados eliminados: "
        f"{eliminados}"
    )

    return resultado