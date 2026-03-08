import json

# --- CONFIGURACIÓN TÉCNICA DEL SISTEMA ---
CAT_SISTEMA = ("Proteína", "Vegetal", "Especia", "Otros")
SUB_CAT = {
    "Proteína": ("Animal", "Vegetal"), "Vegetal": ("Fruta", "Verdura"),
    "Especia": ("Hierba Fresca", "Seca", "Semilla", "Polvo"),
    "Otros": ("Lácteo", "Fruto Seco", "Aceite", "Grano")
}
GUSTOS = ("Salado", "Dulce", "Ácido", "Amargo", "Umami", "Graso", "Sutil", "Fuerte")
SENSACIONES = ("Picante", "Enchiloso", "Astringente", "Fresco", "Cálido", "Metálico", "Jugoso")
NOTAS = ("Frutal", "Herbal", "Floral", "Amaderado", "Terroso", "Tostado", "Cítrico", "Lácteo", "Marino", "Ahumado", "Sangriento", "Cárnico")
TEXTURAS = ("Firme", "Crujiente", "Suave", "Fibrosa", "Untuosa", "Líquida", "Granulosa", "Elástica", "Tierna", "Resistente")
INTENSIDADES = ("Baja", "Media", "Alta")

def cargar_json(archivo):
    try:
        with open(archivo, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError: return {}

def guardar_json(datos, archivo):
    with open(archivo, "w", encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def pedir_multiples(mensaje, tupla_ref):
    print(f"\n{mensaje}:")
    print(f"Opciones: {tupla_ref}")
    entrada = input("Selecciona (separa con comas): ").split(",")
    return [x.strip().capitalize() for x in entrada if x.strip().capitalize() in tupla_ref]

def chatbot():
    db = cargar_json("conocimiento.json")
    interfaz = cargar_json("interfaz.json")
    
    for msj in interfaz.get("mensajes_bienvenida", ["Bienvenido"]): print(msj)
    
    estado = input("\nBot: Antes de empezar, ¿cómo te encuentras el día de hoy? \n").strip().lower()
    respuestas = interfaz.get("respuestas_estado", {})

    if "bien" in estado:
        print(respuestas.get("bien"))
    elif "mal" in estado:
        print(respuestas.get("mal"))
    else:
        print(respuestas.get("desconocido"))

    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Consultar ingrediente")
        print("2. Ingresar nuevo ingrediente")
        print("3. Salir")
        opcion = input("Bot: Selecciona una opción (1/2/3): ").strip()

        if opcion == "1":
            if not db:
                print("Bot: La base está vacía.")
                continue
            print("\nIngredientes en sistema:", ", ".join(db.keys()))
            busqueda = input("Bot: ¿Qué ingrediente deseas analizar? ").strip().capitalize()
            
            if busqueda in db:
                i = db[busqueda]
                print(f"\n>>> FICHA TÉCNICA: {busqueda.upper()} <<<")
                print(f"Gustos: {i['quimica']['gustos']} | Intensidad: {i['quimica']['intensidad']}")
                print(f"Aromas: {i['notas_estado']['crudo']} (Crudo) -> {i['notas_estado']['cocido']} (Cocido)")
                print(f"Textura: {i['textura_estado']['crudo']} -> {i['textura_estado']['cocido']}")
            else:
                print("Bot: Ingrediente no registrado.")

        elif opcion == "2":
            item = input("\nBot: Nombre del ingrediente: ").strip().capitalize()
            cat = input(f"Categoría {CAT_SISTEMA}: ").strip().capitalize()
            sub = input(f"Subcategoría {SUB_CAT.get(cat, ['General'])}: ").strip().capitalize()
            
            gustos_sel = pedir_multiples("Gustos Básicos", GUSTOS)
            sens_sel = pedir_multiples("Sensaciones Químicas", SENSACIONES)
            
            notas_crudo = pedir_multiples("Notas Aromáticas (CRUDO)", NOTAS)
            notas_cocido = pedir_multiples("Notas Aromáticas (COCIDO)", NOTAS)
            
            inte = input(f"Intensidad {INTENSIDADES}: ").strip().capitalize()
            
            t_crudo = pedir_multiples("Texturas (CRUDO)", TEXTURAS)
            t_cocido = pedir_multiples("Texturas (COCIDO)", TEXTURAS)

            db[item] = {
                "taxonomia": {"categoria": cat, "subcategoria": sub},
                "quimica": {"gustos": gustos_sel, "sensaciones": sens_sel, "intensidad": inte},
                "notas_estado": {"crudo": notas_crudo, "cocido": notas_cocido},
                "textura_estado": {"crudo": t_crudo, "cocido": t_cocido}
            }
            guardar_json(db, "conocimiento.json")
            print(f"Bot: '{item}' registrado exitosamente.")

        elif opcion == "3":
            print(interfaz.get("despedida", "Cerrando sistema..."))
            break

if __name__ == "__main__":
    chatbot()