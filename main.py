from src.core.PipelineDataPreProcessing import Pipeline
from pathlib import Path

path_config= Path(__file__).resolve().parent / 'config' / 'config.yaml'

Pipeline(archivo=path_config).operaciones_frame()