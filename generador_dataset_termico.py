import pandas as pd
import numpy as np
import random

# Configuración de semilla para reproducibilidad
np.random.seed(42)
random.seed(42)

def generar_dataset_completo():
    print("Iniciando simulación de proceso industrial...")
    total_entradas = 1112
    
    # --- FASE 1: GENERACIÓN DE DATOS FÍSICOS (Comportamiento Realista) ---
    
    # Tiempo y Máquinas
    timestamps = pd.date_range(start="2026-03-01 06:00:00", periods=total_entradas, freq='4T')
    machine_ids = np.random.choice(['MAQ-ROY-01', 'MAQ-ROY-02', 'MAQ-ROY-03'], size=total_entradas)
    
    # Distribución de Papel (80% dominante)
    paper_grades = np.random.choice(
        ['Standard', 'Eco', 'Top Coated'], 
        size=total_entradas, 
        p=[0.8, 0.1, 0.1]
    )
    
    # Temperaturas Objetivo
    target_map = {'Standard': 170, 'Eco': 160, 'Top Coated': 175}
    target_temps = [target_map[g] for g in paper_grades]
    
    # Listas para almacenar la simulación
    sensor_temps = []
    statuses = []
    speeds = []
    ambient_temps = []
    vibrations = []
    
    current_temp = 170.0
    
    # Bucle de simulación física
    for i in range(total_entradas):
        target = target_temps[i]
        
        # Temperatura ambiente (ciclo diario + ruido)
        ambient = 22 + np.sin(i / 50) * 3 + np.random.normal(0, 0.5)
        ambient_temps.append(round(ambient, 1))
        
        # Lógica de Estado
        if np.random.random() < 0.03: # 3% probabilidad de Idle
            status = 'Idle'
            current_temp = current_temp - (current_temp - ambient) * 0.1 # Enfriamiento
            speed = 0
            vibration = 0.1
        else:
            status = 'Running'
            drift = np.random.normal(0, 1.5)
            correction = (target - current_temp) * 0.2
            current_temp += drift + correction
            speed = int(np.random.normal(600, 20))
            vibration = np.random.normal(2.5, 0.3)
            
            # Lógica de Sobrecalentamiento
            if current_temp > target * 1.08:
                status = 'Overheating'
                vibration += 1.5
            elif current_temp < target * 0.90:
                status = 'Warming_Up'

        sensor_temps.append(current_temp)
        statuses.append(status)
        speeds.append(speed)
        vibrations.append(round(vibration, 2))

    # Inyección de 5 Casos de Borde (Safety Stops)
    print("Inyectando 5 paradas críticas de seguridad...")
    safety_indices = np.random.choice(range(50, total_entradas-50), 5, replace=False)
    for idx in safety_indices:
        target = target_temps[idx]
        sensor_temps[idx] = target + np.random.uniform(30, 50) # Pico de calor
        statuses[idx] = 'Safety_Stop'
        speeds[idx] = 0
        vibrations[idx] = 8.5
        # Enfriamiento posterior
        for k in range(1, 10):
            if idx + k < total_entradas:
                sensor_temps[idx+k] = sensor_temps[idx+k-1] * 0.95
                statuses[idx+k] = 'Maintenance'
                speeds[idx+k] = 0

    # Crear DataFrame Base
    df = pd.DataFrame({
        'Timestamp': timestamps,
        'Machine_ID': machine_ids,
        'Sensor_Temp_C': np.round(sensor_temps, 2),
        'Target_Temp_C': target_temps,
        'Production_Speed_Mmin': speeds,
        'Paper_Grade': paper_grades,
        'Status': statuses,
        'Ambient_Temp_C': ambient_temps,
        'Vibration_Level_mm_s': vibrations
    })

    # --- FASE 2: DATA WRANGLING (Inyección de Suciedad) ---
    print("Corrompiendo datos para ejercicio de limpieza...")
    
    # 1. Valores Nulos (Missing Values)
    # Simulamos pérdida de señal en sensores
    indices_null = np.random.choice(df.index, size=int(total_entradas * 0.05), replace=False)
    df.loc[indices_null, 'Sensor_Temp_C'] = np.nan
    
    indices_null_status = np.random.choice(df.index, size=int(total_entradas * 0.02), replace=False)
    df.loc[indices_null_status, 'Status'] = np.nan

    # 2. Errores de Formato (Dirty Strings)
    # Convertir velocidad a object y mezclar números con strings con unidades
    df['Production_Speed_Mmin'] = df['Production_Speed_Mmin'].astype(object)
    indices_units = np.random.choice(df.index, size=30, replace=False)
    for idx in indices_units:
        val = df.loc[idx, 'Production_Speed_Mmin']
        df.loc[idx, 'Production_Speed_Mmin'] = f"{val} m/min" # "600 m/min"

    # 3. Inconsistencias Categóricas (Typos)
    # Errores humanos al registrar el tipo de papel
    typo_map = {'Standard': 'Std', 'Eco': 'eco', 'Top Coated': 'Top_Coated'}
    indices_typo = np.random.choice(df.index, size=40, replace=False)
    for idx in indices_typo:
        original = df.loc[idx, 'Paper_Grade']
        if original in typo_map:
            df.loc[idx, 'Paper_Grade'] = typo_map[original]

    # 4. Datos Ilógicos (Negative Values)
    # Error de calibración: velocidad negativa
    indices_neg = np.random.choice(df.index, size=5, replace=False)
    df.loc[indices_neg, 'Production_Speed_Mmin'] = -random.randint(100, 500)

    # 5. Duplicados
    # Registros duplicados por error de base de datos
    rows_to_dup = df.sample(n=15)
    df = pd.concat([df, rows_to_dup], ignore_index=True)

    # Ordenar por tiempo (opcional, pero realista tener duplicados desordenados al final)
    # Dejamos los duplicados al final para que sean más obvios si haces .tail()

    return df

# Ejecutar y Guardar
df_sucio = generar_dataset_completo()
filename = 'produccion_termica_raw_data.csv'
df_sucio.to_csv(filename, index=False)

print(f"\nGeneración Exitosa.")
print(f"Archivo guardado como: {filename}")
print(f"Dimensiones finales (incluyendo duplicados): {df_sucio.shape}")
print("-" * 30)
print("Muestra de datos sucios (fíjate en los NaN y formatos extraños):")
print(df_sucio.sample(10))

# Código para descargar en Google Colab
try:
    from google.colab import files
    files.download(filename)
except ImportError:
    print("\nNota: Si no estás en Colab, busca el archivo en tu directorio local.")