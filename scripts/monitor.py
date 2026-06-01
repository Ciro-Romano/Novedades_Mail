from pathlib import Path
import sys

ROOT = Path(__file__).parent.parent

sys.path.append(
    str(ROOT)
)

import json

from fuente.arca import obtener_novedades as obtener_arca
from fuente.cpcecaba import obtener_novedades as obtener_cpcecaba
from fuente.boletin_caba import obtener_novedades as obtener_boletin_caba
from fuente.boletin_nacion import obtener_novedades as obtener_boletin_nacion
from fuente.ignacio import obtener_novedades as obtener_ignacio
from fuente.jorge import obtener_novedades as obtener_jorge

from scripts.mailer import enviar_html


UMBRAL_ALERTA = 80

ARCHIVO_ALERTAS = Path(
    "data/alertas.json"
)

def cargar_alertas():

    if not ARCHIVO_ALERTAS.exists():
        return []

    with open(
        ARCHIVO_ALERTAS,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def guardar_alertas(alertas):

    with open(
        ARCHIVO_ALERTAS,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            alertas,
            f,
            ensure_ascii=False,
            indent=4
        )

def obtener_todas():

    novedades = []

    novedades.extend(obtener_arca())
    novedades.extend(obtener_cpcecaba())
    novedades.extend(obtener_boletin_caba())
    novedades.extend(obtener_boletin_nacion())
    novedades.extend(obtener_ignacio())
    novedades.extend(obtener_jorge())

    return novedades

from utils.scoring import (
    calcular_score
)

def obtener_urgentes(novedades):

    urgentes = []

    for novedad in novedades:

        texto = " ".join([

            novedad.get(
                "titulo",
                ""
            ),

            novedad.get(
                "descripcion",
                ""
            )

        ])

        score = calcular_score(
            texto
        )

        novedad["score"] = score

        if score >= UMBRAL_ALERTA:

            urgentes.append(
                novedad
            )

    return urgentes

def filtrar_no_enviadas(urgentes):

    enviadas = set(
        cargar_alertas()
    )

    nuevas = []

    for novedad in urgentes:

        titulo = novedad["titulo"]

        if titulo not in enviadas:

            nuevas.append(novedad)

    return nuevas

def generar_html(novedades):

    for n in novedades:

        print("\nDEBUG:")
        print(n)

    html = """
    <h2>🚨 Alerta Normativa</h2>
    ...
    
    </p>

    <ul>
    """

    for n in novedades:

        html += f"""
        <li>
            <b>{n['titulo']}</b>
            <br>
            Fuente: {n['fuente']}
        """

        if n.get("link"):

            html += f"""
            <br>
            <a href="{n['link']}">
                Ver publicación
            </a>
            """

        html += """
        </li>
        <br>
        """

    html += "</ul>"

    return html

def main():

    novedades = obtener_todas()

    urgentes = obtener_urgentes(
        novedades
    )

    urgentes = filtrar_no_enviadas(
        urgentes
    )

    if not urgentes:

        print(
            "[INFO] No hay alertas"
        )

        return

    html = generar_html(
        urgentes
    )

    enviar_html(
        asunto="🚨 Alerta Normativa",
        html=html,
        grupo="alertas"
    )

    historial = cargar_alertas()

    for n in urgentes:

        historial.append(
            n["titulo"]
        )

    guardar_alertas(
        historial
    )

    print(
        f"[OK] {len(urgentes)} alertas enviadas"
    )


if __name__ == "__main__":
    main()