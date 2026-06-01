from datetime import datetime


def formatear_fecha(fecha):

    if not fecha:
        return ""

    formatos = [

        "%Y-%m-%d",
        "%d/%m/%Y",

    ]

    for formato in formatos:

        try:

            return (
                datetime.strptime(
                    fecha,
                    formato
                )
                .strftime(
                    "%d/%m/%Y"
                )
            )

        except:

            pass

    return fecha