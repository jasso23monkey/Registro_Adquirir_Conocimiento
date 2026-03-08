from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# --- CONFIGURACIÓN TÉCNICA (Copia esto al inicio de app.py) ---
CAT_SISTEMA = ("Proteína", "Vegetal", "Especia", "Otros")
SUB_CAT = {
    "Proteína": ("Animal", "Vegetal"),
    "Vegetal": ("Fruta", "Verdura"),
    "Especia": ("Hierba Fresca", "Seca", "Semilla", "Polvo"),
    "Otros": ("Lácteo", "Fruto Seco", "Aceite", "Grano")
}
GUSTOS = ("Salado", "Dulce", "Ácido", "Amargo", "Umami", "Graso", "Sutil", "Fuerte")
SENSACIONES = ("Picante", "Enchiloso", "Astringente", "Fresco", "Cálido", "Metálico", "Jugoso")
NOTAS = ("Frutal", "Herbal", "Floral", "Amaderado", "Terroso", "Tostado", "Cítrico", "Lácteo", "Marino", "Ahumado", "Sangriento", "Cárnico", "Neutro")
TEXTURAS = ("Firme", "Crujiente", "Suave", "Fibrosa", "Untuosa", "Líquida", "Granulosa", "Elástica", "Tierna", "Resistente")
INTENSIDADES = ("Baja", "Media", "Alta")

# Rutas de archivos
DB_PATH = "conocimiento.json"
INTERFAZ_PATH = "interfaz.json"

def cargar_datos(ruta):
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_datos(datos, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# --- RUTAS DEL SERVIDOR ---

@app.route('/')
def index():
    # Esta ruta servirá tu archivo HTML unificado
    return render_template('index.html')

@app.route('/get_config', methods=['GET'])
def get_config():
    return jsonify({
        "cat_sistema": CAT_SISTEMA,
        "sub_cat": SUB_CAT,
        "gustos": GUSTOS,
        "sensaciones": SENSACIONES,
        "notas": NOTAS,
        "texturas": TEXTURAS,
        "intensidades": INTENSIDADES
    })

@app.route('/get_interfaz', methods=['GET'])
def get_interfaz():
    # Envía los mensajes de saludo y estados (bien/mal)
    return jsonify(cargar_datos(INTERFAZ_PATH))

@app.route('/get_conocimiento', methods=['GET'])
def get_conocimiento():
    # Envía la lista de ingredientes guardados
    return jsonify(cargar_datos(DB_PATH))

@app.route('/guardar_ingrediente', methods=['POST'])
def guardar_ingrediente():
    nuevo_item = request.json # Recibe el objeto desde JS
    nombre = nuevo_item.get("nombre")
    
    db = cargar_datos(DB_PATH)
    
    # Estructura del ADN del ingrediente
    db[nombre] = {
        "taxonomia": nuevo_item["taxonomia"],
        "quimica": nuevo_item["quimica"],
        "notas_estado": nuevo_item["notas_estado"],
        "textura_estado": nuevo_item["textura_estado"]
    }
    
    guardar_datos(db, DB_PATH)
    return jsonify({"status": "success", "message": f"'{nombre}' guardado correctamente."})

if __name__ == '__main__':
    # El servidor correrá en http://127.0.0.1:5000
    app.run(debug=True)