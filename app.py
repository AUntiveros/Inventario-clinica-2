# app.py (VERSIÓN FINAL Y ROBUSTA)

import pandas as pd
import random
import datetime
from flask import Flask, render_template, request, Response
from flask_cors import CORS

# --- Configuración de Flask y CORS ---
app = Flask(__name__)
CORS(app) 

# --- Listas de parámetros que tu script usa ---
# (He copiado todas tus listas originales para que no falte nada)
equipos_tipo_detal = [
    'Ventilador mecánico', 'Monitor multiparámetros', 'Bomba de infusión', 'ECG portátil', 'Desfibrilador', 'Incubadora', 'Termómetro', 'Oxímetro de pulso',
    'Resonador magnético (RMN)', 'Tomógrafo (CT)', 'Rayos X', 'Mamógrafo', 'Endoscopio', 'Laparoscopia',
    'Analizador de gases en sangre', 'Microscopio', 'Centrífuga', 'Espectrómetro', 'Sierra para huesos', 'Electrobisturíe', 'Bomba de infusión para cirugía',
    'Incubadora para neonatos', 'Monitor de presión intracraneal'
]
frecuencias_uso = ['1-2h', '3-5h', '6-8h', '9-13h', '14+h']
tipos_equipo = ['Otros', 'Análisis', 'Diagnóstico', 'Terapéutico', 'Soporte vital']
eficiencia_clinica = ['Muy eficiente', 'Media (Eficiencia)', 'No eficiente']
obsolescencia = ['Nada', 'Media Obsolescencia', 'Obsoleto']
costos = ['Excede mucho', 'Excede poco', 'Aceptable', 'Dentro del presupuesto']
mantenimiento = ['Inspección', '1 vez/año', '2 veces/año', '3+ veces/año']
riesgo_paciente = ['Sin riesgo', 'Diagnóstico errado', 'Dolor', 'Muerte']
dificultad_centro = ['Ninguna', 'Media (Dificultad)', 'Alta']
disponibilidad_soporte = ['Sí', 'No']

# --- Tus funciones de generación de datos (sin cambios) ---
def generar_fallas_y_frecuencia(estado_equipos):
    # ... (tu lógica de fallas aquí)
    fallas = []
    estado_map = {"muy bueno": (1, 3, "Cada 3 años"), "bueno": (3, 6, "Cada 2 años"), "mediano": (6, 9, "Anual"), "malo": (9, 12, "Cada 6 meses"), "muy malo": (12, 15, "Mensual")}
    min_f, max_f, frecuencia = estado_map.get(estado_equipos, (6, 9, "Anual"))
    num_fallas = random.randint(min_f, max_f)
    for _ in range(num_fallas):
        falla_fecha = datetime.date(random.randint(2013, datetime.datetime.now().year), random.randint(1, 12), random.randint(1, 28))
        fallas.append(falla_fecha)
    return fallas, frecuencia

def generar_tiempos_uptime_downtime():
    uptime = round(random.uniform(3000, 7000), 2)
    downtime_val = round(random.uniform(50, 400), 2) # Cambiado nombre de variable para evitar conflicto
    return uptime, downtime_val

def obtener_costo_equipo(tipo_equipo):
    # ... (tu lógica de costos aquí)
    costos_base = {'Ventilador mecánico': (15000, 50000), 'Monitor multiparámetros': (8000, 25000), 'Bomba de infusión': (3000, 15000), 'ECG portátil': (7000, 20000), 'Desfibrilador': (10000, 30000), 'Incubadora': (20000, 40000), 'Termómetro': (50, 150), 'Oxímetro de pulso': (50, 250), 'Resonador magnético (RMN)': (700000, 1200000), 'Tomógrafo (CT)': (500000, 800000), 'Rayos X': (100000, 300000), 'Mamógrafo': (100000, 200000), 'Endoscopio': (50000, 150000), 'Laparoscopia': (10000, 25000), 'Analizador de gases en sangre': (20000, 70000), 'Microscopio': (1000, 5000), 'Centrífuga': (3000, 10000), 'Espectrómetro': (10000, 30000), 'Sierra para huesos': (5000, 15000), 'Electrobisturíe': (10000, 30000), 'Bomba de infusión para cirugía': (5000, 20000), 'Incubadora para neonatos': (30000, 60000), 'Monitor de presión intracraneal': (10000, 25000)}
    min_c, max_c = costos_base.get(tipo_equipo, (1000, 10000))
    return round(random.uniform(min_c, max_c), 2)

# --- FUNCIÓN PRINCIPAL QUE USA TU LÓGICA COMPLETA ---
def generar_inventario_dataframe(cantidad_equipos, estado_hospital, estado_equipos):
    equipos_base = { "muy bueno": {'Ventilador mecánico': 50, 'Monitor multiparámetros': 40, 'Bomba de infusión': 35, 'ECG portátil': 35, 'Desfibrilador': 25, 'Incubadora': 20, 'Termómetro': 60, 'Oxímetro de pulso': 55, 'Resonador magnético (RMN)': 3, 'Tomógrafo (CT)': 5, 'Rayos X': 7, 'Mamógrafo': 2, 'Endoscopio': 4, 'Laparoscopia': 3, 'Analizador de gases en sangre': 8, 'Microscopio': 8, 'Centrífuga': 8, 'Espectrómetro': 4, 'Sierra para huesos': 6, 'Electrobisturíe': 10, 'Bomba de infusión para cirugía': 6, 'Incubadora para neonatos': 10, 'Monitor de presión intracraneal': 3}, "bueno": {'Ventilador mecánico': 45, 'Monitor multiparámetros': 40, 'Bomba de infusión': 30, 'ECG portátil': 30, 'Desfibrilador': 20, 'Incubadora': 15, 'Termómetro': 50, 'Oxímetro de pulso': 45, 'Resonador magnético (RMN)': 2, 'Tomógrafo (CT)': 3, 'Rayos X': 5, 'Mamógrafo': 1, 'Endoscopio': 3, 'Laparoscopia': 2, 'Analizador de gases en sangre': 6, 'Microscopio': 6, 'Centrífuga': 6, 'Espectrómetro': 3, 'Sierra para huesos': 5, 'Electrobisturíe': 8, 'Bomba de infusión para cirugía': 5, 'Incubadora para neonatos': 8, 'Monitor de presión intracraneal': 2}, "mediano": {'Ventilador mecánico': 40, 'Monitor multiparámetros': 35, 'Bomba de infusión': 30, 'ECG portátil': 30, 'Desfibrilador': 20, 'Incubadora': 15, 'Termómetro': 50, 'Oxímetro de pulso': 45, 'Resonador magnético (RMN)': 2, 'Tomógrafo (CT)': 3, 'Rayos X': 4, 'Mamógrafo': 1, 'Endoscopio': 2, 'Laparoscopia': 2, 'Analizador de gases en sangre': 6, 'Microscopio': 6, 'Centrífuga': 6, 'Espectrómetro': 3, 'Sierra para huesos': 5, 'Electrobisturíe': 7, 'Bomba de infusión para cirugía': 5, 'Incubadora para neonatos': 7, 'Monitor de presión intracraneal': 3}, "malo": {'Ventilador mecánico': 30, 'Monitor multiparámetros': 30, 'Bomba de infusión': 25, 'ECG portátil': 25, 'Desfibrilador': 15, 'Incubadora': 10, 'Termómetro': 40, 'Oxímetro de pulso': 35, 'Resonador magnético (RMN)': 2, 'Tomógrafo (CT)': 3, 'Rayos X': 4, 'Mamógrafo': 1, 'Endoscopio': 2, 'Laparoscopia': 2, 'Analizador de gases en sangre': 5, 'Microscopio': 5, 'Centrífuga': 5, 'Espectrómetro': 3, 'Sierra para huesos': 4, 'Electrobisturíe': 6, 'Bomba de infusión para cirugía': 4, 'Incubadora para neonatos': 6, 'Monitor de presión intracraneal': 2}, "pesimo": {'Ventilador mecánico': 20, 'Monitor multiparámetros': 20, 'Bomba de infusión': 15, 'ECG portátil': 15, 'Desfibrilador': 10, 'Incubadora': 5, 'Termómetro': 30, 'Oxímetro de pulso': 25, 'Resonador magnético (RMN)': 1, 'Tomógrafo (CT)': 2, 'Rayos X': 3, 'Mamógrafo': 1, 'Endoscopio': 2, 'Laparoscopia': 2, 'Analizador de gases en sangre': 4, 'Microscopio': 4, 'Centrífuga': 4, 'Espectrómetro': 2, 'Sierra para huesos': 3, 'Electrobisturíe': 5, 'Bomba de infusión para cirugía': 3, 'Incubadora para neonatos': 5, 'Monitor de presión intracraneal': 2}}
    equipos_cantidades_ajustadas = equipos_base.get(estado_hospital, equipos_base["mediano"]).copy()
    
    total_base = sum(equipos_cantidades_ajustadas.values())
    if cantidad_equipos > total_base:
        equipos_restantes = cantidad_equipos - total_base
        for equipo in equipos_cantidades_ajustadas:
            equipos_cantidades_ajustadas[equipo] += equipos_restantes // len(equipos_cantidades_ajustadas)
        if 'Ventilador mecánico' in equipos_cantidades_ajustadas:
            equipos_cantidades_ajustadas['Ventilador mecánico'] += equipos_restantes % len(equipos_cantidades_ajustadas)
    
    data_ajustada = []
    codigo = 1
    equipos_generados = []
    for equipo, cantidad in equipos_cantidades_ajustadas.items():
        for _ in range(cantidad):
            equipos_generados.append(equipo)

    random.shuffle(equipos_generados)

    for equipo_nombre in equipos_generados[:cantidad_equipos]:
        fallas, frecuencia = generar_fallas_y_frecuencia(estado_equipos)
        uptime, downtime_val = generar_tiempos_uptime_downtime()
        costo_soles = obtener_costo_equipo(equipo_nombre)
        año_adquisicion = random.randint(2013, datetime.datetime.now().year)
        fecha_adquisicion = datetime.date(año_adquisicion, random.randint(1, 12), random.randint(1, 28))
        
        data_ajustada.append({
            'Código': f'ID{str(codigo).zfill(4)}', 'Nombre': equipo_nombre, 'Fecha Adquisición': fecha_adquisicion,
            'Frecuencia de Uso': random.choice(frecuencias_uso), 'Fallas': "; ".join([str(f) for f in fallas]),
            'Frecuencia de Fallas': frecuencia, 'Downtime': downtime_val, 'Tipo de Equipo': random.choice(tipos_equipo),
            'Eficiencia Clínica': random.choice(eficiencia_clinica), 'Obsolescencia': random.choice(obsolescencia),
            'Costos': random.choice(costos), 'Mantenimiento': random.choice(mantenimiento),
            'Riesgo al Paciente': random.choice(riesgo_paciente), 'Dificultad para el Centro': random.choice(dificultad_centro),
            'Disponibilidad de Soporte': random.choice(disponibilidad_soporte), 'Ubicación': f'Ubicación {random.randint(1, 10)}',
            'Costo Reparaciones': round(random.uniform(50, 500), 2), 'Tiempo Uptime (hrs)': uptime,
            'Tiempo Downtime (hrs)': downtime_val, 'Costo Soles': costo_soles
        })
        codigo += 1

    return pd.DataFrame(data_ajustada)

# --- Rutas de Flask (Endpoints de la API) ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar_csv():
    try:
        cantidad_equipos = int(request.form.get('cantidad_equipos', 1000))
        estado_hospital = request.form.get('estado_hospital', 'mediano')
        estado_equipos = request.form.get('estado_equipos', 'mediano')
        
        df = generar_inventario_dataframe(cantidad_equipos, estado_hospital, estado_equipos)
        
        # --- LA MODIFICACIÓN CLAVE ESTÁ AQUÍ ---
        # Forzamos la codificación y los finales de línea para que sean idénticos a los de Windows
        output_csv = df.to_csv(
            index=False, 
            encoding='utf-8-sig',      # 'utf-8-sig' es más compatible con Excel que 'utf-8'
            line_terminator='\r\n'     # Forzamos el final de línea de Windows (CRLF)
        )
        
        return Response(
            output_csv,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=inventario_hospital.csv"}
        )
    except Exception as e:
        print(f"Error en la generación de CSV: {e}")
        return "Error interno del servidor al generar el archivo.", 500