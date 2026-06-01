from utils.palabras_clave import (
    PALABRAS_SCORE
)

def calcular_score(texto):

    texto = texto.lower()

    score = 0

    for palabra, puntos in (
        PALABRAS_SCORE.items()
    ):

        if palabra in texto:

            score += puntos

    return score