# Importacion de librerías importantes 
import psutil 
from typing import Dict, Any
class ResourceMetrics: 
    @staticmethod
    def ray_init(tamaño_archivo: float) -> Dict[str, Any]: 
        memory = psutil.virtual_memory().available
        cpus = psutil.cpu_count(logical=False)
        
        num_cpus = max(1, cpus -1)
        object_store_memory = max(memory*0.3, tamaño_archivo*1.5)
        
        return {
            'num_cpus' : num_cpus, 
            'object_store_memory': object_store_memory
        }