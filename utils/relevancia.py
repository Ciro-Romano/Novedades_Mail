from utils.palabras_clave import (
    PALABRAS_CRITICAS
)

def es_relevante(texto):

    texto = texto.lower()

    return any(
        palabra in texto
        for palabra in PALABRAS_CRITICAS
    )