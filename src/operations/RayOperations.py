#Importamos librerías importates
import polars as pl 
import ray
import pyarrow as pa
from pydantic import BaseModel
from typing import Optional, Dict
from .PolarsOperations import GroupJoinData, GroupJoinExpr, PolarsExprList

class GorupJoinData: 
    def __init__(self, model: BaseModel):
        self.model = model
        self.group = model.agg_data
        self.join = model.join_data
    
    def group(self, frame: ray.data.Dataset) -> ray.data.Dataset: 
        return frame.groupby(self.group.col)
    
    def join(self, 
        frame: ray.data.Dataset, 
        frame_2: ray.data.Dataset, 
        num_partition: int=4) -> ray.data.Dataset: 
        
        return frame.join(frame_2, on=self.join.join_on, join_type=self.join.join_type, num_partitions=num_partition)

class BatchExpr: 
    def __init__(self, model: BaseModel):
        self.group = GroupJoinData(model=model)
        self.li_expr = PolarsExprList(model=model)
        self.filter_post_join = GroupJoinExpr(model=model)
    
    def batch_operations(self, batch: pa.Table, filter_post_join: bool=False) -> pa.Table: 
        frame= pl.from_arrow(batch).lazy()
        
        if filter_post_join: 
            ds_filtered = frame.filter(self.filter_post_join.post_join_filter_data())
            return ds_filtered.collect(engine='streaming').to_arrow()
        
        ds_transformed = frame.with_columns(self.li_expr.list_expr())
        return ds_transformed.collect(engine='streaming').to_arrow()
    
    def batch_group_operation(self, batch: pa.Table) -> pa.Table: 
        frame= pl.from_arrow(batch).lazy()
        ds_transformed = self.group.group_data(frame=frame)
        return ds_transformed.collect(engine='streaming').to_arrow()

class RayBatch: 
    def __init__(self, model: BaseModel):
        self.batch = BatchExpr(model=model)
    
    def ray_operations(self, frame: ray.data.Dataset, batch_size: int, filter_post_join: bool=False) -> ray.data.Dataset: 
        return frame.map_batches(
            lambda batch: self.batch.batch_operations(batch=batch, filter_post_join=filter_post_join), 
            batch_size=batch_size, 
            batch_format='pyarrow'
        )
    
    def ray_group_operation(self, frame_grouped: ray.data.Dataset) -> ray.data.Dataset: 
        return frame_grouped.map_groups(
            lambda batch: self.batch.batch_group_operation(batch=batch),
            batch_format='pyarrow'
        )

#Aqui falta poner la logica del diccionario en base a los chunks de datos segun tipo de operacion que se haga 
class RayOperation: 
    def __init__(self, model: BaseModel):
        self.model = model
        
        self.join_group = GorupJoinData(model=self.model) 
        self.batch_operation = RayBatch(model=self.model)
    
    def get_ray_ds(self, 
        frame: ray.data.dataset,
        batch_size: Dict[str, int],
        frame_2: Optional[ray.data.Dataset], 
        num_partition: Optional[int]=4) -> ray.data.Dataset: 
        ds_transformed = self.batch_operation.ray_operations(frame=frame, batch_size=batch_size['batch_general'])
        
        if isinstance(self.model.data.input_path, list): 
            ds_join = self.join_group.join(frame=ds_transformed, frame_2=frame_2, num_partition=num_partition)
            if self.model.join_data.post_filter: 
                ds_post_join_filter = self.batch_operation.ray_operations(frame=ds_join, batch_size=batch_size['batch_join'], filter_post_join=True)
                return ds_post_join_filter
            return ds_join
        
        group_ds = self.join_group.group(frame=ds_transformed)
        grouped_ds = self.batch_operation.ray_group_operation(frame_grouped=group_ds)
        
        return grouped_ds

