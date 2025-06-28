# app.py (VERSIÓN CON LINTERMINATOR CORREGIDO)

import pandas as pd
import random
import datetime
from flask import Flask, render_template, request, Response
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

# --- Listas de parámetros ---
equipos_tipo_detal = ['Ventilador mecánico', 'Monitor multiparámetros', 'Bomba de infusión', 'ECG portátil', 'Desfibrilador', 'Incubadora', 'Termómetro', 'Oxímetro de pulso', 'Resonador magnético (RMN)', 'Tomógrafo (CT)', 'Rayos X', 'Mamógrafo', 'Endoscopio', 'Laparoscopia', 'Analizador de gases en sangre', 'Microscopio', 'Centrífuga', 'Espectrómetro', 'Sierra para huesos', 'Electrobisturíe', 'Bomba de infusión para cirugía', 'Incubadora para neonatos', 'Monitor de presión intracraneal']
frecuencias_uso = ['1-2h', '3-5h', '6-8h', '9-13h', '14+h']
tipos_equipo = ['Otros', 'Análisis', 'Diagnóstico', 'Terapéutico', 'Soporte vital']
eficiencia_clinica = ['Muy eficiente', 'Media (Eficiencia)', 'No eficiente']
obsolescencia = ['Nada', 'Media Obsolescencia', 'Obsoleto']
costos = ['Excede mucho', 'Excede poco', 'Aceptable', 'Dentro del presupuesto']
mantenimiento = ['Inspección', '1 vez/año', '2 veces/año', '3+ veces/año']
riesgo_paciente = ['Sin riesgo', 'Diagnóstico errado', 'Dolor', 'Muerte']
dificultad_centro = ['Ninguna', 'Media (Dificultad)', 'Alta']
disponibilidad_soporte = ['Sí', 'No']

# --- Funciones de generación ---
def generar_fallas_y_frecuencia(estado_equipos):
    estado_map = {"muy bueno": (1, 3, "Cada 3 años"), "bueno": (3, 6, "Cada 2 años"), "mediano": (6, 9, "Anual"), "malo": (9, 12, "Cada 6 meses"), "muy malo": (12, 15, "Mensual")}
    min_f, max_f, frecuencia = estado_map.get(estado_equipos, (6, 9, "Anual"))
    num_fallas = random.randint(min_f, max_f)
    return "; ".join([str(datetime.date(random.randint(2013, datetime.datetime.now().year), random.randint(1, 12), random.randint(1, 28))) for _ in range(num_fallas)]), frecuencia

def generar_tiempos_uptime_downtime():
    return round(random.uniform(3000, 7000), 2), round(random.uniform(50, 400), 2)

def obtener_costo_equipo(tipo_equipo):
    costos_base = {'Ventilador mecánico': (15000, 50000), 'Monitor multiparámetros': (8000, 25000), 'Bomba de infusión': (3000, 15000), 'ECG portátil': (7000, 20000), 'Desfibrilador': (10000, 30000), 'Incubadora': (20000, 40000), 'Termómetro': (50, 150), 'Oxímetro de pulso': (50, 250), 'Resonador magnético (RMN)': (700000, 1200000), 'Tomógrafo (CT)': (500000, 800000), 'Rayos X': (100000, 300000), 'Mamógrafo': (100000, 200000), 'Endoscopio': (50000, 150000), 'Laparoscopia': (10000, 25000), 'Analizador de gases en sangre': (20000, 70000), 'Microscopio': (1000, 5000), 'Centrífuga': (3000, 10000), 'Espectrómetro': (10000, 30000), 'Sierra para huesos': (5000, 15000), 'Electrobisturíe': (10000, 30000), 'Bomba de infusión para cirugía': (5000, 20000), 'Incubadora para neonatos': (30000, 60000), 'Monitor de presión intracraneal': (10000, 25000)}
    min_c, max_c = costos_base.get(tipo_equipo, (1000, 10000))
    return round(random.uniform(min_c, max_c), 2)

# --- Rutas de Flask ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar_csv():
    try:
        cantidad_equipos = int(request.form.get('cantidad_equipos', 1000))
        estado_equipos = request.form.get('estado_equipos', 'mediano')
        
        data_list = []
        for i in range(cantidad_equipos):
            nombre_equipo = random.choice(equipos_tipo_detal)
            fallas_str, frecuencia_fallas = generar_fallas_y_frecuencia(estado_equipos)
            uptime, downtime = generar_tiempos_uptime_downtime()
            
            data_list.append({
                'Código': f'ID{str(i+1).zfill(4)}', 'Nombre': nombre_equipo, 'Fecha Adquisición': datetime.date(random.randint(2013, datetime.datetime.now().year), random.randint(1, 12), random.randint(1, 28)),
                'Frecuencia de Uso': random.choice(frecuencias_uso), 'Fallas': fallas_str, 'Frecuencia de Fallas': frecuencia_fallas, 'Downtime': downtime, 'Tipo de Equipo': random.choice(tipos_equipo),
                'Eficiencia Clínica': random.choice(eficiencia_clinica), 'Obsolescencia': random.choice(obsolescencia), 'Costos': random.choice(costos), 'Mantenimiento': random.choice(mantenimiento),
                'Riesgo al Paciente': random.choice(riesgo_paciente), 'Dificultad para el Centro': random.choice(dificultad_centro), 'Disponibilidad de Soporte': random.choice(disponibilidad_soporte),
                'Ubicación': f'Ubicación {random.randint(1, 10)}', 'Costo Reparaciones': round(random.uniform(50, 500), 2), 'Tiempo Uptime (hrs)': uptime,
                'Tiempo Downtime (hrs)': downtime, 'Costo Soles': obtener_costo_equipo(nombre_equipo)
            })

        df = pd.DataFrame(data_list)
        
        output = io.StringIO()
        df.to_csv(
            output, 
            index=False, 
            encoding='utf-8-sig', 
            lineterminator='\r\n'  # ¡CORREGIDO! Sin guion bajo
        )
        csv_data = output.getvalue()
        
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=inventario_hospital.csv"}
        )
    except Exception as e:
        app.logger.error(f"Error en /generar: {e}")
        return "Error interno del servidor al generar el archivo.", 500