def obtener_categoria(titulo):

    titulo = titulo.lower()

    if any(p in titulo for p in [
        "ganancias", "iva", "monotributo", "arca",
        "agip", "impuesto", "tributario",
        "tributaria", "ingresos brutos"
    ]):
        return "Tributario"

    if any(p in titulo for p in [
        "paritaria", "escala", "salario",
        "uocra", "uecara", "empleado",
        "trabajo", "casas particulares"
    ]):
        return "Laboral"

    if any(p in titulo for p in [
        "anses", "asignaciones",
        "jubilación", "jubilaciones",
        "aportes", "contribuciones"
    ]):
        return "Seguridad Social"

    if any(p in titulo for p in [
        "igj", "sociedad", "sociedades"
    ]):
        return "Societario"

    return "General"