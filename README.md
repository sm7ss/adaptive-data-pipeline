# 🚀 Adaptive Data Pipeline

[![Ray](https://img.shields.io/badge/Ray-Distributed__Computing-blue.svg)](https://ray.io/)
[![Polars](https://img.shields.io/badge/Polars-Fast__DataFrames-red.svg)](https://pola.rs/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Data__Validation-green.svg)](https://pydantic-docs.helpmanual.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Adaptive-orange.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A **self-adaptive** data processing system that intelligently selects between execution modes (Eager/Lazy/Ray) based on data size and available resources, integrating Polars for maximum performance and Pydantic for robust validation.

## 🌟 Key features

### 🧠 **Adaptive intelligence**
- **Automatic selection** of the optimal processing mode
- **Intelligent memory and resource management**
- **Real-time decision making** based on system metrics

### ⚡ **Multimodal processing**
- **Eager mode**: for small datasets (Polars DataFrame)
- **Lazy mode**: for medium-sized datasets (Polars LazyFrame)
- **Distributed mode**: for big data (Ray Cluster)

### 🛡️ **Enterprise robustness**
- **Full schema and configuration validation**
- **Automatic error handling and recovery**
- **Support for multiple formats** (YAML/TOML)

## 🏗️ System Architecture

```text 
  adaptive-data-pipeline/
  ├── 📁config # Configurations
  ├── 📁 data # Data
  ├── 📁 src/
  │ ├── 📁 core/ # Processing and obtaining results
  │ ├── 📁 operations/ # Processing operations
  │ ├── 📁 validation/ # Validation and configuration
  │ ├── 📁 resources/ # Resource management
  │ └── 📁 strategies/ # Strategies and patterns
```

## 🎯 Intelligent Decision Making

### **Mode Selection Algorithm**

```python
def frame_decision(self, size: int, memory: int) -> str:
    eager_threshold = 0.1 * memory    # 10% of available RAM
    lazy_threshold = 0.75 * memory    # 75% of available RAM
    
    if size < eager_threshold:
        return ‘eager’    # Polars DataFrame
    elif size < lazy_threshold:
        return ‘lazy’     # Polars LazyFrame  
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

## 🚀 Examples of Use

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

    # The system automatically chooses the best processing mode.
    pipeline = Pipeline(‘config.yaml’)
    pipeline.operaciones_frame()

    # Depending on the size of the data and resources, it will execute:
    # - Polars Eager (small datasets)
    # - Polars Lazy (medium datasets) 
    # - Ray Distributed (big data)
```

## 🔧 Supported Operations

### 📊 **Data Transformations**

- Cleaning: Drop nulls, filtering by conditions
- Moving Windows: Rolling means, sums, min/max
- Aggregations: GroupBy with multiple operations
- Joins: Inner, left, right, outer with post-filtering

### ⚡ **Execution Modes**

| Mode              | Use Case           | Technology       |
|-----------------|--------------------|------------------|
| **Eager**          | Datasets < 10% RAM | Polars DataFrame |
| **Lazy**          | Datasets < 75% RAM | Polars LazyFrame |
| **Distributed** |    Big Data > 75% RAM | Ray Cluster      |

### 🛡️ **Validations**

- Schemas: Column and type verification
- Resources: Available memory and CPU validation
- Configuration: YAML/TOML syntax and constraints

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

### **Full Installation**

```bash
  # Clone the repository
  git clone https://github.com/sm7ss/adaptive-data-pipeline.git
  cd adaptive-data-pipeline

  # Or install dependencies directly
  pip install -r requirements.txt
```

## 🎪 Processing Flow

### **1. Data Analysis**

```python 
  # The system analyzes data size and resources.
  size = file.stat().st_size
  memory = psutil.virtual_memory().available
  decision = self.frame_decision(size, memory)
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
  # Application of transformations according to configuration
  df_transform = frame.with_columns(self.expr.list_expr())

  # Complex operations (joins, groupings)
  if join_needed:
      result = self.group_join.join_data(frame1, frame2)
```

### **4. Writing Results**

```python
  # Optimized saving according to mode
  if eager:
      result.write_parquet(output_path)
  else:
      result.sink_parquet(output_path, compression=‘zstd’)
```

## 🔍 Use Cases

### 🏪 **E-commerce Analytics**

```yaml
  data:
    input_path: [‘users.csv’, ‘purchases.csv’]
    output_path: 'customer_analytics.parquet'

  window_data:
    operation: ‘rolling_sum’
    col: ‘purchase_amount’
    window: 30
    over: ‘customer_id’

  join_data:
    join_on: ‘customer_id’
    join_type: ‘left’
```

### 🏥 **Healthcare Processing**

```yaml
  data:
  input_path: ‘patient_records.csv’
  output_path: ‘medical_features.parquet’

  clean_data:
  operation: ‘drop_nulls’
  col: ‘blood_pressure’

  agg_data:
  operation: ‘mean’
  col: ‘heart_rate’
  group_by: 'patient_group'
```

### 📱 **Telecomm Analytics**

```yaml
  data:
    input_path: [‘customers.csv’, ‘usage_data.csv’]
    output_path: 'telecom_features.parquet'

  window_data:
    operation: ‘rolling_mean’
    col: ‘data_usage’
    window: 7
    over: ‘user_id’

  join_data:
    join_on: ‘user_id’
    join_type: ‘inner’
    post_filter:
      operations: [‘data_usage > 5000’]
```

## 🤝 Contribution

Contributions are welcome! This project uses modular architecture:

1. Fork the project
2. Create a branch (git checkout -b feature/new-operation)
3. Commit changes (git commit -m ‘Add new window operation’)
4. Push to the branch (git push origin feature/new-operation)
5. Open a Pull Request

## 👩‍💻 About the Project

**Adaptive Data Pipeline** represents the culmination of my journey in data engineering, combining advanced distributed processing techniques with artificial intelligence applied to resource management.

The system demonstrates how intelligent automation can optimize complex data pipelines, selecting the optimal technology for each scenario without manual intervention.

**Technical questions?** Feel free to open an issue!

