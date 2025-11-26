#Importamos las librerías importantes 
from ..resources.Resources import ResourceMetrics
from ..operations.PolarsOperations import PolarsFrame
from ..operations.RayOperations import RayOperation
from .Frame import PipelineFrame
from ..validation.ReadData import ReadFile

#tipado 
import polars as pl 
import ray 
from typing import Union, Optional, Dict
from pathlib import Path

#logging tipado 
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s-%(message)s')
logger = logging.getLogger(__name__)

class Pipeline: 
    def __init__(self, archivo: str):
        self.model = ReadFile(archivo=archivo).read_file()
        self.frame = PipelineFrame(model=self.model)
        
        self.ray_operations = RayOperation(model=self.model)
        self.polars_operations = PolarsFrame(model=self.model)
    
    def polars(self, frame: Union[list, str]) -> None: 
        if isinstance(frame, list): 
            frame = self.polars_operations.get_frame(
                frame=frame[0], 
                frame_2=frame[1],
            )
            if isinstance(frame, pl.DataFrame): 
                frame.write_parquet(self.model.data.output_path)
            else: 
                frame.sink_parquet(
                    self.model.data.output_path,
                    compression='zstd'
                )
            return 
        frame = self.polars_operations.get_frame(frame=frame)
        if isinstance(frame, pl.DataFrame): 
                frame.write_parquet(self.model.data.output_path)
        else: 
            frame.sink_parquet(
                self.model.data.output_path,
                compression='zstd'
            )
        return 
    
    def tamaño_archivo(self, frame: Union[ray.data.Dataset, list]) -> float: 
        if isinstance(frame, list): 
            suma = 0
            for archivo in frame: 
                suma+=archivo.size_bytes()
            return suma/len(frame)
        return frame.size_bytes()
    
    def batch_size(self, archivos: Union[list, str], tamaño_archivo: float, num_cpus: int) -> Dict[str, int]: 
        if isinstance(archivos, list): 
            batch_join = max(tamaño_archivo//num_cpus, 10000)
        batch_trans = max(tamaño_archivo//(num_cpus*8), 10000)
        return {
            'batch_join' : batch_join if isinstance(archivos, list) else None, 
            'batch_general' : batch_trans
        }
    
    def ray(self, frame: Union[list, Path], num_partition: Optional[int]=4) -> None: 
        tamaño_archivo = self.tamaño_archivo(archivos=frame)
        resoruce_init = ResourceMetrics().ray_init(tamaño_archivo=tamaño_archivo)
        
        batch_size=self.batch_size(archivos=frame, tamaño_archivo=tamaño_archivo, num_cpus=resoruce_init['num_cpus'])
        
        with ray.init(num_cpus=resoruce_init['num_cpus'], object_store_memory=resoruce_init['object_store_memory']): 
            if isinstance(frame, list): 
                frame = self.ray_operations.get_ray_ds(
                    frame=frame[0], 
                    batch_size=batch_size, 
                    frame_2=frame[1], 
                    num_partition=num_partition
                )
                frame.write_parquet(self.model.data.output_path)
                return 
            frame = self.ray_operations.get_ray_ds(
                frame=frame,
                batch_size=batch_size
            )
            frame.write_parquet(self.model.data.output_path)
            return 
    
    def operaciones_frame(self, num_partition:Optional[int]=4) -> None:
        diccionario_frame = self.frame.pipeline_frame()
        frame_type = diccionario_frame['frame_type']
        frame = diccionario_frame['frame']
        
        if frame_type in ['eager', 'lazy']: 
            self.polars(frame=frame)
            logger.info(f'Se guardo {self.model.data.output_path} correctamente con los resultados para el formato {frame_type}')
            return
        else: 
            self.ray(frame=frame, num_partition=num_partition)
            logger.info(f'Se guardo {self.model.data.output_path} correctamente con los resultados para el formato {frame_type}')
            return
