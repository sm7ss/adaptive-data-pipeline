# 🚀 Adaptive Data Pipeline

[![Ray](https://img.shields.io/badge/Ray-Distributed__Computing-blue.svg)](https://ray.io/)
[![Polars](https://img.shields.io/badge/Polars-Fast__DataFrames-red.svg)](https://pola.rs/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Data__Validation-green.svg)](https://pydantic-docs.helpmanual.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Adaptive-orange.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Un sistema de procesamiento de datos **auto-adaptativo** que selecciona inteligentemente entre modos de ejecución (Eager/Lazy/Ray) basado en el tamaño de los datos y recursos disponibles, integrando Polars para máximo rendimiento y Pydantic para validación robusta.

## 🌟 Características Principales

### 🧠 **Inteligencia Adaptativa**
- **Selección automática** del modo de procesamiento óptimo
- **Gestión inteligente de memoria** y recursos
- **Decision-making en tiempo real** basado en métricas del sistema

### ⚡ **Multi-Modal Processing**
- **Eager Mode**: Para datasets pequeños (Polars DataFrame)
- **Lazy Mode**: Para datasets medianos (Polars LazyFrame)  
- **Distributed Mode**: Para big data (Ray Cluster)

### 🛡️ **Robustez Empresarial**
- **Validación completa** de schemas y configuraciones
- **Manejo automático de errores** y recuperación
- **Soporte múltiples formatos** (YAML/TOML)


## 🏗️ Arquitectura del Sistema

adaptive-data-pipeline/
├── 📁 core/ # Núcleo del sistema
│ ├── PipelineDataPreProcessing.py # Orquestador principal
│ └── Frame.py # Gestor de frames adaptativo
├── 📁 operations/ # Operaciones de procesamiento
│ ├── RayOperations.py # Procesamiento distribuido
│ └── PolarsOperations.py # Operaciones Polars
├── 📁 validation/ # Validación y configuración
│ ├── Validator.py # Validación de schemas
│ └── ReadData.py # Lectura de configuraciones
├── 📁 resources/ # Gestión de recursos
│ └── Resources.py # Optimización de recursos Ray
└── 📁 strategies/ # Estrategias y patrones
└── Strategy.py # Enums y estrategias

## 🎯 Toma de Decisiones Inteligente

### **Algoritmo de Selección de Modo**

```python
def frame_decision(self, size: int, memory: int) -> str:
    eager_threshold = 0.1 * memory    # 10% of available RAM
    lazy_threshold = 0.75 * memory    # 75% of available RAM
    
    if tamaño < umbral_eager:
        return 'eager'    # Polars DataFrame
    elif tamaño < umbral_lazy:
        return 'lazy'     # Polars LazyFrame  
    else:
        return ‘ray’      # Ray Distributed
```

### **Automatic Resource Management**

```python 
def ray_init(file_size: float) -> Dict[str, Any]:
    memory = psutil.virtual_memory().available
    cpus = psutil.cpu_count(logical=False)
    
    num_cpus = max(1, cpus - 1)  # Reserve 1 CPU for the system
    object_store_memory = max(memory * 0.3, file_size * 1.5)
    
    return {
        ‘num_cpus’: num_cpus,
        ‘object_store_memory’: object_store_memory
    }
```

## 🚀 Ejemplos de Uso

### **Basic Configuration (YAML)**

```yaml 
data:
  input_path: ‘data/megaline_calls.csv’
  output_path: ‘processed_data.parquet’

clean_data:
  operation: ‘drop_nulls’
  col: 'value'

window_data:
  operation: ‘rolling_mean’
  col: ‘value’
  window: 5
  over: ‘value’

join_data:
  join_on: ‘value_1’
  join_type: ‘inner’
  post_filter:
    operations: [‘value > 100’]
```

### **Automatic Execution**

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

## 🔧 Supported Operations

### 📊 **Data Transformations**

- Cleaning: Drop nulls, filtering by conditions
- Moving Windows: Rolling means, sums, min/max
- Aggregations: GroupBy with multiple operations
- Joins: Inner, left, right, outer with post-filtering

### ⚡ **Execution Modes**

| Modo	          | Caso de Uso	       | Tecnología       |
|-----------------|--------------------|------------------|
| **Eager**          | Datasets < 10% RAM | Polars DataFrame |
| **Lazy**          | Datasets < 75% RAM | Polars LazyFrame |
| **Distributed** |    Big Data > 75% RAM | Ray Cluster      |

### 🛡️ **Validations**

- Schemas: Verificación de columnas y tipos
- Recursos: Validación de memoria y CPU disponibles
- Configuración: Sintaxis YAML/TOML y constraints

## 📦 Installation

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
  # Clone the repository
  git clone https://github.com/sm7ss/adaptive-data-pipeline.git
  cd adaptive-data-pipeline

# Instalación en desarrollo
pip install -e .

# O instalar dependencias directamente
pip install -r requirements.txt
```

## 🎪 Processing Flow

### **1. Data Analysis**

```python 
# El sistema analiza tamaño de datos y recursos
tamaño = archivo.stat().st_size
memory = psutil.virtual_memory().available
decision = self.frame_decision(tamaño, memory)
```

### **2. Technology Selection**

```python 
  if decision == ‘eager’:
      frame = PolarsFrame.read_eager(path)
  elif decision == ‘lazy’:
      frame = PolarsFrame.read_lazy(path)  
  elif decision == ‘ray’:
      frame = RayFrame.read_ray(path)
```

### **3. Optimized Processing**

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

### 🏪 **E-commerce analytics**

```yaml
  data:
    input_path: [“users.csv”, “purchases.csv”]
    output_path: 'customer_analytics.parquet'

  window_data:
    operation: “rolling_sum”
    col: “purchase_amount”
    window: 30
    over: “customer_id”

  join_data:
    join_on: “customer_id”
    join_type: “left”
```

### 🏥 **Healthcare processing**

```yaml
  data:
  input_path: “patient_records.csv”
  output_path: “medical_features.parquet”

  clean_data:
  operation: “drop_nulls”
  col: “blood_pressure”

  agg_data:
  operation: “mean”
  col: “heart_rate”
  group_by: “patient_group”
```

### 📱 **Telecommunications analysis**

```yaml
  data:
    input_path: [“customers.csv”, “usage_data.csv”]
    output_path: 'telecom_features.parquet'

  window_data:
    operation: “rolling_mean”
    col: “data_usage”
    window: 7
    over: “user_id”

  join_data:
    join_on: “user_id”
    join_type: “inner”
    post_filter:
      operations: [“data_usage > 5000”]
```

## 🤝 Contribution

¡Contribuciones son bienvenidas! Este proyecto utiliza arquitectura modular:

1. Fork el proyecto
2. Crea una rama (git checkout -b feature/nueva-operacion)
3. Commit cambios (git commit -m 'Agregar nueva operación de ventana')
4. Push a la rama (git push origin feature/nueva-operacion)
5. Abre un Pull Request

## 👩‍💻 About the Project

**Adaptive Data Pipeline** representa la culminación de mi journey en data engineering, combinando técnicas avanzadas de procesamiento distribuido con inteligencia artificial aplicada a la gestión de recursos.

The system demonstrates how intelligent automation can optimize complex data pipelines, selecting the optimal technology for each scenario without manual intervention.

**¿Preguntas técnicas?** ¡No dudes en abrir un issue!

