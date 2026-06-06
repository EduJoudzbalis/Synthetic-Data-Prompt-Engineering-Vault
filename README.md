# 🧠 Polar Metrics - Synthetic Data & Prompt Engineering Vault

Este repositorio centraliza las instrucciones lógicas, restricciones operativas y prompts avanzados utilizados para la generación de datasets sintéticos estructurados de alta fidelidad para proyectos de Data Science y Machine Learning.

## 📂 Repositorio de Prompts Disponibles

### 🏭 Caso 1: Monitoreo Térmico en Planta Papelera
* **Objetivo:** Generar telemetría de sensores para variables acopladas (Velocidad M/min y Temperatura °C) con desbalance crítico de clases para entrenamiento de modelos predictivos.
* **Proyecto Vinculado:** [Repositorio Principal: Monitoreo Predictivo de Fallas Térmicas](https://github.com/EduJoudzbalis/polarmetrics-ia)
* **Prompt de Síntesis:** [Ver prompt_termico_industrial.txt](./prompt_termico_industrial.txt)
* **Script de Generación:** [Ver generador_dataset_termico.py](./generador_dataset_termico.py) (Script en Python diseñado por la IA que interpreta las reglas lógicas del prompt para compilar y exportar el CSV crudo final).
* **Dataset Crudo:** [Ver thermal_production_data](./thermal_production_data.csv) (Archivo en formato CSV generado sintéticamente que contiene la telemetría base de velocidad y temperatura con ruido estructural para el entrenamiento).

---
*Firma: Polar Metrics*
