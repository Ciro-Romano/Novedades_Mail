from pathlib import Path
import sys

ROOT = Path(__file__).parent.parent

sys.path.append(
    str(ROOT)
)

from fuente.arca import obtener_novedades as obtener_arca
from fuente.cpcecaba import obtener_novedades as obtener_cpcecaba
from fuente.boletin_caba import obtener_novedades as obtener_boletin_caba
from fuente.boletin_nacion import obtener_novedades as obtener_boletin_nacion
from fuente.ignacio import obtener_novedades as obtener_ignacio
from fuente.jorge import obtener_novedades as obtener_jorge
from pathlib import Path
from datetime import datetime

from utils.deduplicador import (
    eliminar_duplicados
)

from utils.scoring import (
    calcular_score
)

from tests.historial_prueba import (
    fue_enviada,
    registrar_envio,
    obtener_semana_anterior
)

from templates.boletin import (
    generar_html
)

MODO_PRUEBA = True

def obtener_todas_las_novedades():

    novedades = []

    fuentes = [

        ("ARCA", obtener_arca),
        ("CPCECABA", obtener_cpcecaba),
        ("BOLETIN_CABA", obtener_boletin_caba),
        ("BOLETIN_NACION", obtener_boletin_nacion),
        ("IGNACIO_ONLINE", obtener_ignacio),
        ("JORGE_VEGA", obtener_jorge),

    ]

    for nombre, funcion in fuentes:

        try:

            resultado = funcion()

            novedades.extend(resultado)

            print(
                f"[OK] {nombre}: {len(resultado)} novedades"
            )

        except Exception as e:

            print(
                f"[ERROR] {nombre}: {e}"
            )

    return novedades


def asignar_scores(novedades):

    for novedad in novedades:

        texto = " ".join([
            novedad.get("titulo", ""),
            novedad.get("descripcion", "")
        ])

        novedad["score"] = calcular_score(texto)

    return novedades


def ordenar_novedades(novedades):

    return sorted(
        novedades,
        key=lambda x: x.get("score", 0),
        reverse=True
    )


def mostrar_resumen_fuentes(novedades):

    fuentes = {}

    for n in novedades:

        fuente = n["fuente"]

        fuentes[fuente] = fuentes.get(fuente, 0) + 1

    print("\nRESUMEN POR FUENTE\n")

    for fuente, cantidad in sorted(
        fuentes.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"{fuente}: {cantidad}")


def mostrar_top_novedades(novedades, cantidad=10):

    print("\nTOP NOVEDADES\n")

    for n in novedades[:cantidad]:

        print(f"[{n.get('score',0):03d}] {n['titulo']}")


if __name__ == "__main__":

    novedades = obtener_todas_las_novedades()

    total_original = len(novedades)

    novedades = eliminar_duplicados(novedades)

    total_final = len(novedades)

    print(f"\nDuplicados eliminados: {total_original - total_final}")
    print(f"Total original: {total_original}")
    print(f"Total final: {total_final}")

    novedades = asignar_scores(novedades)
    novedades = ordenar_novedades(novedades)

    novedades = [
        n for n in novedades
        if n.get("score", 0) >= 15
    ]

    nuevas = []
    repetidas = []

    for novedad in novedades:

        if fue_enviada(novedad):
            repetidas.append(novedad)
        else:
            nuevas.append(novedad)

    semana_anterior = (
        obtener_semana_anterior()
    )

    print(f"\nNuevas: {len(nuevas)}")
    print(f"Repetidas: {len(repetidas)}")
    print(f"Semana anterior: {len(semana_anterior)}")

    print("\nNOVEDADES NUEVAS\n")
    for n in nuevas:
        print(f"[{n.get('score',0):03d}] {n['titulo']}")

    if semana_anterior:

        print("\nSEMANA ANTERIOR\n")

        for n in semana_anterior:
            print(f"[{n.get('score',0):03d}] {n['titulo']}")

    mostrar_resumen_fuentes(novedades)
    mostrar_top_novedades(novedades)

    html = generar_html(
        nuevas,
        semana_anterior
    )

    with open("boletin.html", "w", encoding="utf-8") as archivo:
        archivo.write(html)

    print("\n[OK] boletin.html generado")

    carpeta_historial = Path(
        "tests/boletines_prueba"
    )

    carpeta_historial.mkdir(
        parents=True,
        exist_ok=True
    )

    fecha = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    archivo_historial = (
        carpeta_historial /
        f"{fecha}.html"
    )

    with open(
        archivo_historial,
        "w",
        encoding="utf-8"
    ) as archivo:

        archivo.write(html)

    print(
        f"[OK] Historial guardado: {archivo_historial}"
    )
    
    if nuevas:

        registrar_envio(nuevas)

        if MODO_PRUEBA:

            print(
                f"[PRUEBA] Registradas {len(nuevas)} novedades en enviados_prueba.json"
            )

        else:

            print(
                f"[OK] Registradas {len(nuevas)} novedades"
            )

    else:

        print(
            "[INFO] No hay novedades nuevas"
        )