# utils/organismos.py

ORGANISMOS_NACION = [

    "AGENCIA DE RECAUDACIÓN Y CONTROL ADUANERO",
    "ARCA",

    "ADMINISTRACIÓN NACIONAL DE LA SEGURIDAD SOCIAL",
    "ANSES",

    "SUPERINTENDENCIA DE RIESGOS DEL TRABAJO",

    "MINISTERIO DE ECONOMÍA",
    "SECRETARÍA DE HACIENDA",
    "SECRETARÍA DE FINANZAS",

]


ORGANISMOS_CABA = [

    "AGIP",

    "ADMINISTRACION GUBERNAMENTAL DE INGRESOS PUBLICOS",

    "MINISTERIO DE HACIENDA",

    "MINISTERIO DE HACIENDA Y FINANZAS",

]

# utils/organismos.py

def organismo_valido(
    organismo,
    organismos_validos
):

    organismo = (
        organismo or ""
    ).upper()

    return any(

        org.upper()
        in organismo

        for org in
        organismos_validos

    )