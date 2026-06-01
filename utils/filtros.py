from utils.palabras_clave import (
    PALABRAS_IGNORAR
)


def ignorar_novedad(titulo):

    titulo = titulo.lower().strip()

    if any(
        palabra in titulo
        for palabra in PALABRAS_IGNORAR
    ):
        return True

    # Aviso Oficial

    if titulo == "aviso oficial":
        return True

    return False