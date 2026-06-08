from datetime import datetime

from utils.fechas import formatear_fecha
from utils.categorias import obtener_categoria


MESES = [
    "Enero", "Febrero", "Marzo", "Abril",
    "Mayo", "Junio", "Julio", "Agosto",
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

DIAS = [
    "Lunes", "Martes", "Miércoles",
    "Jueves", "Viernes", "Sábado", "Domingo"
]


def es_normativa(novedad):

    titulo = novedad["titulo"].lower().strip()

    return (
        titulo.startswith("resolución")
        or titulo.startswith("resolucion")
        or titulo.startswith("resolución general")
        or titulo.startswith("resolucion general")
        or titulo.startswith("disposición")
        or titulo.startswith("disposicion")
        or titulo.startswith("decreto")
        or titulo.startswith("aviso oficial")
    )


def obtener_badge(score, recordatorio=False):

    if recordatorio:
        return (
            "novedad-recordatorio",
            "badge-recordatorio",
            "RECORDATORIO"
        )

    if score >= 50:
        return (
            "novedad-critica",
            "badge-critica",
            "CRÍTICA"
        )

    if score >= 30:
        return (
            "novedad-importante",
            "badge-importante",
            "IMPORTANTE"
        )

    return (
        "novedad-normal",
        "badge-normal",
        "INFORMATIVA"
    )


def renderizar_novedad(
    novedad,
    recordatorio=False
):

    enlace = (
        novedad.get("link")
        or novedad.get("enlace")
        or "#"
    )

    fecha = formatear_fecha(
        novedad.get("fecha", "")
    )

    score = novedad.get("score", 0)

    (
        clase,
        badge_css,
        badge_texto
    ) = obtener_badge(
        score,
        recordatorio
    )

    resumen = ""

    if novedad.get("resumen"):

        resumen = f"""
        <div class="resumen">
            {novedad['resumen']}
        </div>
        """

    meta_fecha = ""

    if fecha:

        meta_fecha = (
            f" | Fecha: {fecha}"
        )

    return f"""
    <div class="{clase}">

        <span class="badge {badge_css}">
            {badge_texto}
        </span>

        <div class="titulo">
            {novedad['titulo']}
        </div>

        <div class="meta">
            Fuente: {novedad['fuente']}
            {meta_fecha}
        </div>

        {resumen}

        <a
            class="btn-leer"
            href="{enlace}"
            target="_blank"
        >
            Leer publicación completa →
        </a>

    </div>
    """


def generar_html(
    nuevas,
    semana_anterior
):

    hoy = datetime.now()

    fecha_boletin = (
        f"{DIAS[hoy.weekday()]} "
        f"{hoy.day} de "
        f"{MESES[hoy.month - 1]} "
        f"de {hoy.year}"
    )

    destacadas = [

        n

        for n in nuevas

        if n.get("score", 0) >= 60

    ]

    destacadas = sorted(

        destacadas,

        key=lambda x:
            x.get("score", 0),

        reverse=True

    )

    categorias = {

        "Tributario": [],
        "Laboral": [],
        "Seguridad Social": [],
        "Societario": [],
        "General": []

    }

    normativas = []

    for n in nuevas:

        if es_normativa(n):

            normativas.append(n)

        else:

            categoria = obtener_categoria(
                n["titulo"]
            )

            if categoria not in categorias:
                categoria = "General"

            categorias[categoria].append(n)

    def render(lista):

        if not lista:
            return ""

        return "".join(
            renderizar_novedad(x)
            for x in lista
        )
    
    def render_seccion(
        titulo,
        novedades
    ):

        if not novedades:
            return ""

        return f"""
        <section class="seccion">

            <h2>{titulo}</h2>

            {render(novedades)}

        </section>
        """

    FUENTES_FIJAS = [

        (
            "ARCA",
            "https://www.arca.gob.ar"
        ),

        (
            "BOLETIN NACION",
            "https://www.boletinoficial.gob.ar"
        ),

        (
            "CPCECABA",
            "https://www.consejo.org.ar"
        ),

        (
            "IGNACIO ONLINE",
            "https://www.ignacioonline.com.ar"
        ),

        (
            "JORGE VEGA",
            "https://jorgevega.com.ar"
        )

    ]

    fuentes_html = ""

    for nombre, url in FUENTES_FIJAS:

        fuentes_html += f"""
        <li>
            <a
                href="{url}"
                target="_blank"
            >
                {nombre}
            </a>
        </li>
        """

    if semana_anterior:

        semana_anterior_html = "".join(

            renderizar_novedad(
                x,
                recordatorio=True
            )

            for x in semana_anterior

        )

    else:

        semana_anterior_html = """
        <div class="novedad-recordatorio">

            <span class="badge badge-recordatorio">
                SIN NOVEDADES
            </span>

            <div class="titulo">
                No existe un boletín anterior
            </div>

        </div>
        """

    bloques = {

        "FECHA_BOLETIN":
            fecha_boletin,

        "ESTUDIO_NOMBRE":
            "Estudio Fadelli S.A.",

        "DESTACADAS":
            render(destacadas),

        "TRIBUTARIO":
            render_seccion(
                "Tributario",
                categorias["Tributario"]
            ),

        "LABORAL":
            render_seccion(
                "laboral",
                categorias["Laboral"]
            ),

        "SEGURIDAD_SOCIAL":
            render_seccion(
                "Seguridad Social",
                categorias["Seguridad Social"]
            ),

        "NORMATIVA":
            render_seccion(
                "Normativa Oficial",
                normativas
            ),

        "SEMANA_ANTERIOR":
            semana_anterior_html,

        "FUENTES":
            fuentes_html

    }

    with open(
        "html/base_boletin.html",
        "r",
        encoding="utf-8"
    ) as f:

        html = f.read()

    for key, value in bloques.items():

        html = html.replace(
            f"{{{{ {key} }}}}",
            value
        )

    return html