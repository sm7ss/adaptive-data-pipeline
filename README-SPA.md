# 🚀 Adaptive Data Pipeline

[![Ray](https://img.shields.io/badge/Ray-Distributed__Computing-blue.svg)](https://ray.io/)
[![Polars](https://img.shields.io/badge/Polars-Fast__DataFrames-red.svg)](https://pola.rs/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Data__Validation-green.svg)](https://pydantic-docs.helpmanual.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Adaptive-orange.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Un sistema de procesamiento de datos **autoadaptativo** que selecciona de forma inteligente entre los modos de ejecución (Eager/Lazy/Ray) en función del tamaño de los datos y los recursos disponibles, integrando Polars para obtener el máximo rendimiento y Pydantic para una validación robusta.

## 🌟 Características principales

### 🧠 **Inteligencia adaptativa**
- **Selección automática** del modo de procesamiento óptimo
- **Gestión inteligente de la memoria y los recursos**
- **Toma de decisiones en tiempo real** basada en métricas del sistema

### ⚡ **Procesamiento multimodal**
- **Modo Eager**: para conjuntos de datos pequeños (Polars DataFrame)
- **Modo Lazy**: para conjuntos de datos medianos (Polars LazyFrame)  
- **Modo distribuido**: para big data (Ray Cluster)

### 🛡️ **Robustez empresarial**
- **Validación completa del esquema y la configuración**
- **Gestión y recuperación automáticas de errores**
- **Compatibilidad con múltiples formatos** (YAML/TOML)

## 🏗️ Arquitectura del Sistema

```text 
  adaptive-data-pipeline/
  ├── 📁config # Configuraciones
  ├── 📁 data # Los datos
  ├── 📁 src/
  │ ├── 📁 core/ # Procesamiento y obtención de los resultados
  │ ├── 📁 operations/ # Operaciones de procesamiento
  │ ├── 📁 validation/ # Validación y configuración
  │ ├── 📁 resources/ # Gestión de recursos
  │ └── 📁 strategies/ # Estrategias y patrones
```

## 🎯 Toma de Decisiones Inteligente

### **Algoritmo de Selección de Modo**

```python
def frame_decision(self, tamaño: int, memory: int) -> str:
    umbral_eager = 0.1 * memory    # 10% de RAM disponible
    umbral_lazy = 0.75 * memory    # 75% de RAM disponible
    
    if tamaño < umbral_eager:
        return 'eager'    # Polars DataFrame
    elif tamaño < umbral_lazy:
        return 'lazy'     # Polars LazyFrame  
    else:
        return 'ray'      # Ray Distributed
```

### **Gestión Automática de Recursos**

```python 
def ray_init(tamaño_archivo: float) -> Dict[str, Any]:
    memory = psutil.virtual_memory().available
    cpus = psutil.cpu_count(logical=False)
    
    num_cpus = max(1, cpus - 1)  # Reservar 1 CPU para el sistema
    object_store_memory = max(memory * 0.3, tamaño_archivo * 1.5)
    
    return {
        'num_cpus': num_cpus,
        'object_store_memory': object_store_memory
    }
```

## 🚀 Ejemplos de Uso

### **Configuración Básica (YAML)**

```yaml 
data:
  input_path: 'data/megaline_calls.csv'
  output_path: 'processed_data.parquet'

clean_data:
  operation: 'drop_nulls'
  col: 'value'

window_data:
  operation: 'rolling_mean'
  col: 'value'
  window: 5
  over: 'value'

join_data:
  join_on: 'value_1'
  join_type: 'inner'
  post_filter:
    operations: ['value > 100']
```

### **Ejecución Automática**

```python 
    from src.core.PipelineDataPreProcessing import Pipeline

    # El sistema elige automáticamente el mejor modo de procesamiento
    pipeline = Pipeline('config.yaml')
    pipeline.operaciones_frame()

    # Según el tamaño de datos y recursos, ejecutará:
    # - Polars Eager (datasets pequeños)
    # - Polars Lazy (datasets medianos) 
    # - Ray Distributed (big data)
```

## 🔧 Operaciones Soportadas

### 📊 **Transformaciones de Datos**

- Limpieza: Drop nulls, filtrado por condiciones
- Ventanas Móviles: Rolling means, sums, min/max
- Agregaciones: GroupBy con múltiples operaciones
- Joins: Inner, left, right, outer con post-filtrado

### ⚡ **Modos de Ejecución**

| Modo	          | Caso de Uso	       | Tecnología       |
|-----------------|--------------------|------------------|
| **Eager**	      | Datasets < 10% RAM | Polars DataFrame |
| **Lazy**	      | Datasets < 75% RAM | Polars LazyFrame |
| **Distributed** |	Big Data > 75% RAM | Ray Cluster      |

### 🛡️ **Validaciones**

- Schemas: Verificación de columnas y tipos
- Recursos: Validación de memoria y CPU disponibles
- Configuración: Sintaxis YAML/TOML y constraints

## 📦 Instalación

### **Requirements**

```bash 
    polars==1.38.1
    pyarrow==23.0.1
    pydantic==2.12.5
    PyYAML==6.0.3
    ray==2.54.0
    tomli==2.4.0
```

### **Instalación Completa**

```bash
  # Clonar el repositorio
  git clone https://github.com/sm7ss/adaptive-data-pipeline.git
  cd adaptive-data-pipeline

  # O instalar dependencias directamente
  pip install -r requirements.txt
```

## 🎪 Flujo de Procesamiento

### **1. Análisis de Datos**

```python 
  # El sistema analiza tamaño de datos y recursos
  tamaño = archivo.stat().st_size
  memory = psutil.virtual_memory().available
  decision = self.frame_decision(tamaño, memory)
```

### **2. Selección de Tecnología**

```python 
  if decision == 'eager':
      frame = PolarsFrame.leer_eager(path)
  elif decision == 'lazy':
      frame = PolarsFrame.leer_lazy(path)  
  elif decision == 'ray':
      frame = RayFrame.leer_ray(path)
```

### **3. Procesamiento Optimizado**

```python 
  # Aplicación de transformaciones según configuración
  df_transform = frame.with_columns(self.expr.list_expr())

  # Operaciones complejas (joins, agrupaciones)
  if necesita_join:
      resultado = self.group_join.join_data(frame1, frame2)
```

### **4. Escritura de Resultados**

```python
  # Guardado optimizado según el modo
  if es_eager:
      resultado.write_parquet(output_path)
  else:
      resultado.sink_parquet(output_path, compression='zstd')
```

## 🔍 Casos de Uso

### 🏪 **E-commerce Analytics**

```yaml
  data:
    input_path: ['users.csv', 'purchases.csv']
    output_path: 'customer_analytics.parquet'

  window_data:
    operation: 'rolling_sum'
    col: 'purchase_amount'
    window: 30
    over: 'customer_id'

  join_data:
    join_on: 'customer_id'
    join_type: 'left'
```

### 🏥 **Healthcare Processing**

```yaml
  data:
  input_path: 'patient_records.csv'
  output_path: 'medical_features.parquet'

  clean_data:
  operation: 'drop_nulls'
  col: 'blood_pressure'

  agg_data:
  operation: 'mean'
  col: 'heart_rate'
  group_by: 'patient_group'
```

### 📱 **Telecomm Analytics**

```yaml
  data:
    input_path: ['customers.csv', 'usage_data.csv']
    output_path: 'telecom_features.parquet'

  window_data:
    operation: 'rolling_mean'
    col: 'data_usage'
    window: 7
    over: 'user_id'

  join_data:
    join_on: 'user_id'
    join_type: 'inner'
    post_filter:
      operations: ['data_usage > 5000']
```

## 🤝 Contribución

¡Contribuciones son bienvenidas! Este proyecto utiliza arquitectura modular:

1. Fork el proyecto
2. Crea una rama (git checkout -b feature/nueva-operacion)
3. Commit cambios (git commit -m 'Agregar nueva operación de ventana')
4. Push a la rama (git push origin feature/nueva-operacion)
5. Abre un Pull Request

## 👩‍💻 Sobre el Proyecto

**Adaptive Data Pipeline** representa la culminación de mi journey en data engineering, combinando técnicas avanzadas de procesamiento distribuido con inteligencia artificial aplicada a la gestión de recursos.

El sistema demuestra cómo la automatización inteligente puede optimizar pipelines de datos complejos, seleccionando la tecnología óptima para cada escenario sin intervención manual.

**¿Preguntas técnicas?** ¡No dudes en abrir un issue!
