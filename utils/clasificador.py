from utils.palabras_clave import (
    PALABRAS_CRITICAS
)


def determinar_prioridad(titulo):

    titulo = titulo.lower()

    if any(
        palabra in titulo
        for palabra in PALABRAS_CRITICAS
    ):
        return "CRITICA"

    return "NORMAL"