import pandas as pd
import random
import datetime
from flask import Flask, render_template, request, Response

# --- Inicializamos la aplicación Flask ---
app = Flask(__name__)

# --- Aquí va todo tu código de funciones (sin cambios) ---
# (Pegué tus funciones aquí para que sea un solo bloque)

def generar_fallas_y_frecuencia(estado_equipos):
    fallas = []
    if estado_equipos == "muy bueno":
        num_fallas = random.randint(1, 3)
        frecuencia = "Cada 3 años"
    elif estado_equipos == "bueno":
        num_fallas = random.randint(3, 6)
        frecuencia = "Cada 2 años"
    elif estado_equipos == "mediano":
        num_fallas = random.randint(6, 9)
        frecuencia = "Anual"
    elif estado_equipos == "malo":
        num_fallas = random.randint(9, 12)
        frecuencia = "Cada 6 meses"
    else:  # estado_equipos == "muy malo"
        num_fallas = random.randint(12, 15)
        frecuencia = "Mensual"
    for _ in range(num_fallas):
        falla_fecha = datetime.date(random.randint(2013, datetime.datetime.now().year),
                                    random.randint(1, 12), random.randint(1, 28))
        fallas.append(falla_fecha)
    return fallas, frecuencia

def obtener_costo_equipo(tipo_equipo):
    costos = {
        'Ventilador mecánico': round(random.uniform(15000, 50000), 2),
        'Monitor multiparámetros': round(random.uniform(8000, 25000), 2),
        # ... (el resto de tu diccionario de costos)
        'Incubadora para neonatos': round(random.uniform(30000, 60000), 2),
        'Monitor de presión intracraneal': round(random.uniform(10000, 25000), 2),
    }
    return costos.get(tipo_equipo, 10000)

# --- FIN de tus funciones ---


# Esta es la función principal que ahora genera el DataFrame
# Le pasamos los parámetros que antes pedíamos con input()
def generar_inventario_dataframe(cantidad_equipos, estado_hospital, estado_equipos):
    # Parámetros que antes estaban fuera
    equipos_tipo_detal = ['Ventilador mecánico', 'Monitor multiparámetros', 'Bomba de infusión', 'ECG portátil', 'Desfibrilador', 'Incubadora', 'Termómetro', 'Oxímetro de pulso', 'Resonador magnético (RMN)', 'Tomógrafo (CT)', 'Rayos X', 'Mamógrafo', 'Endoscopio', 'Laparoscopia', 'Analizador de gases en sangre', 'Microscopio', 'Centrífuga', 'Espectrómetro', 'Sierra para huesos', 'Electrobisturíe', 'Bomba de infusión para cirugía', 'Incubadora para neonatos', 'Monitor de presión intracraneal']
    frecuencias_uso = ['1-2h', '3-5h', '6-8h', '9-13h', '14+h']
    downtime = ['Muy poco', 'Poco', 'Regular', 'Mucho', 'Excesivo']
    tipos_equipo = ['Otros', 'Análisis', 'Diagnóstico', 'Terapéutico', 'Soporte vital']
    eficiencia_clinica = ['Muy eficiente', 'Media (Eficiencia)', 'No eficiente']
    obsolescencia = ['Nada', 'Media Obsolescencia', 'Obsoleto']
    costos = ['Excede mucho', 'Excede poco', 'Aceptable', 'Dentro del presupuesto']
    mantenimiento = ['Inspección', '1 vez/año', '2 veces/año', '3+ veces/año']
    riesgo_paciente = ['Sin riesgo', 'Diagnóstico errado', 'Dolor', 'Muerte']
    dificultad_centro = ['Ninguna', 'Media (Dificultad)', 'Alta']
    disponibilidad_soporte = ['Sí', 'No']

    # Aquí va toda la lógica de tu función `generar_inventario_interactivo`
    # ... (el resto de tu lógica para crear el dataframe)
    
    # ¡Importante! En lugar de guardar en un archivo, devolvemos el DataFrame
    # (He simplificado la lógica de distribución para el ejemplo, puedes pegar la tuya)
    data = []
    for i in range(cantidad_equipos):
        equipo_nombre = random.choice(equipos_tipo_detal)
        fallas, frecuencia_fallas = generar_fallas_y_frecuencia(estado_equipos)
        data.append({
            'Código': f'ID{str(i+1).zfill(4)}',
            'Nombre': equipo_nombre,
            'Fecha Adquisición': datetime.date(random.randint(2013, datetime.datetime.now().year), random.randint(1, 12), random.randint(1, 28)),
            'Frecuencia de Uso': random.choice(frecuencias_uso),
            'Fallas': "; ".join([str(f) for f in fallas]),
            'Frecuencia de Fallas': frecuencia_fallas,
            'Tipo de Equipo': random.choice(tipos_equipo),
            'Costo Soles': obtener_costo_equipo(equipo_nombre)
        })

    df = pd.DataFrame(data)
    return df


# --- Definimos las rutas de nuestra aplicación web ---

# Ruta para la página principal ('/'). Muestra el formulario HTML.
@app.route('/')
def index():
    return render_template('index.html')

# Ruta '/generar', que se activa cuando el usuario envía el formulario.
@app.route('/generar', methods=['POST'])
def generar_csv():
    # 1. Obtenemos los datos del formulario que mandó el usuario
    cantidad_equipos = int(request.form.get('cantidad_equipos'))
    estado_hospital = request.form.get('estado_hospital')
    estado_equipos = request.form.get('estado_equipos')
    
    # 2. Llamamos a nuestra función para crear el DataFrame
    df = generar_inventario_dataframe(cantidad_equipos, estado_hospital, estado_equipos)
    
    # 3. Convertimos el DataFrame a un string en formato CSV
    output_csv = df.to_csv(index=False, encoding='utf-8')
    
    # 4. Creamos una respuesta HTTP para que el navegador descargue el archivo
    return Response(
        output_csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=inventario_hospital.csv"})
