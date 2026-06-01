import json

with open(
    "data/enviados.json",
    "w",
    encoding="utf-8"
) as archivo:

    json.dump(
        [],
        archivo,
        indent=4
    )

print(
    "[OK] Historial reiniciado"
)