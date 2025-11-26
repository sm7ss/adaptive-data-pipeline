#Importamos las librerías necesarias
import ray
import polars as pl 
import psutil
from pydantic import BaseModel
from pathlib import Path
from typing import Dict, Any

class PolarsFrame: 
    @staticmethod
    def leer_eager(path: Path) -> pl.DataFrame: 
        if path.suffix == '.csv': 
            return pl.read_csv(path)
        else:
            return pl.read_parquet(path)
    
    @staticmethod
    def leer_lazy(path: Path) -> pl.LazyFrame: 
        if path.suffix == '.csv': 
            return pl.scan_csv(path) 
        else: 
            return pl.scan_parquet(path)

class RayFrame: 
    @staticmethod
    def leer_ray(path: Path) -> ray.data.Dataset: 
        if path.suffix == '.csv': 
            return ray.data.read_csv(path)
        else: 
            return ray.data.read_parquet(path)

class PipelineFrame: 
    def __init__(self, model: BaseModel):
        self.model_data = model.data
    
    def frame_decision(self, tamaño: int, memory: int) -> str: 
        if tamaño > (5*memory): 
            raise ValueError(f'El archivo tiene un tamaño de {tamaño} bytes y es demasiado grande para la RAM disponible {memory} bytes')
        
        umbral_eager = 0.1 * memory
        umbral_lazy = 0.75 * memory 
        
        if tamaño < umbral_eager: 
            return 'eager'
        elif tamaño < umbral_lazy: 
            return 'lazy'
        else:
            return 'ray'
    
    def pipeline_frame(self) -> Dict[str, Any]: 
        archivo = self.model_data.input_path
        
        if isinstance(archivo, list):
            decisiones = []
            
            for path in archivo:
                tamaño= path.stat().st_size
                memory= psutil.virtual_memory().available
                decision = self.frame_decision(tamaño=tamaño, memory=memory)
                decisiones.append(decision)
            
            if len(set(decisiones)) > 1: 
                raise ValueError("No se permite mezclar 'eager', 'lazy' y 'ray' en el mismo pipeline.")
            
            decision = decisiones[0]
            lista_frames = []
            
            for path in archivo:
                if decision == 'eager':
                    lista_frames.append(PolarsFrame.leer_eager(path=path))
                elif decision == 'lazy': 
                    lista_frames.append(PolarsFrame.leer_lazy(path=path))
                elif decision == 'ray':
                    lista_frames.append(RayFrame.leer_ray(path=path))
            
            return {
                'frame_type': decision, 
                'frame' : lista_frames
            }
        
        tamaño = archivo.stat().st_size 
        memory = psutil.virtual_memory().available
        decision = self.frame_decision(tamaño=tamaño, memory=memory)
        
        if decision == 'eager': 
            frame = PolarsFrame.leer_eager(path=archivo)
        elif decision == 'lazy': 
            frame = PolarsFrame.leer_lazy(path=archivo)
        elif decision == 'ray': 
            frame = RayFrame.leer_ray(path=archivo)
            
        return {
            'frame_type': decision, 
            'frame' : frame
        }




