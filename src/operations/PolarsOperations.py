#Importamos librerías importates
import polars as pl 
from pydantic import BaseModel
from typing import List, Union, Optional

class CleanData: 
    def __init__(self, model: BaseModel):
        self.clean = model.clean_data
    
    def drop_nulls(self) -> pl.Expr: 
        return pl.col(self.clean.col).is_not_null().alias(f'{self.clean.col}_not_nulls')

class WindowData: 
    def __init__(self, model: BaseModel):
        self.window = model.window_data
    
    def window_data(self) -> pl.Expr: 
        return (
            getattr(pl.col(self.window.col), self.window.operation)
            (self.window.window)
            .over(self.window.over)
            .alias(f'{self.window.col}_window')
        )

class PolarsExprList: 
    def __init__(self, model: BaseModel):
        self.model = model
        self.clean = CleanData(model=self.model)
        self.window = WindowData(model=self.model)
    
    def list_expr(self) -> List[pl.Expr]:
        lista_expresiones = []
        
        if self.model.clean_data: 
            lista_expresiones.append(self.clean.drop_nulls())
        if self.model.window_data: 
            lista_expresiones.append(self.window.window_data())
        
        return lista_expresiones

class GroupJoinExpr: 
    def __init__(self, model: BaseModel):
        self.model = model.agg_data
        self.join = model.join_data.post_filter
    
    def agg_data(self) -> pl.Expr: 
        return (
            getattr(pl.col(self.model.col), self.model.operation)()
            .alias(f'{self.model.col}_expr')
        )
    
    def post_join_filter_data(self) -> List[pl.Expr]: 
        try: 
            return [
                pl.sql_expr(expr)
                for expr in self.join.operations
            ]
        except Exception as e: 
            raise ValueError(f'Las expresiones no son validas: {e}')

class GroupJoinData:
    def __init__(self, model: BaseModel):
        self.model = model
        self.group = self.model.agg_data
        self.join = self.model.join_data
        self.agg_expr = GroupJoinExpr(model=self.model)
    
    def group_data(self, frame: Union[pl.DataFrame, pl.LazyFrame, ]) -> Union[pl.DataFrame, pl.LazyFrame]: 
        return frame.group_by(self.group.group_by).agg(self.agg_expr.agg_data())
    
    def join_data(self, frame_1: Union[pl.DataFrame,pl.LazyFrame], frame_2: Union[pl.DataFrame, pl.LazyFrame]) -> Union[pl.DataFrame, pl.LazyFrame]: 
        join = frame_1.join(frame_2, how=self.join.join_type, on=self.join.join_on) 
        if self.model.join_data.post_filter: 
            filter_data = join.filter(self.agg_expr.post_join_filter_data())
            return filter_data
        return join

class PolarsFrame: 
    def __init__(self, model: BaseModel):
        self.model = model
        
        self.expr = PolarsExprList(model=self.model)
        self.group_join = GroupJoinData(model=self.model)
    
    def get_frame(self, 
        frame: Union[pl.DataFrame, pl.LazyFrame], 
        frame_2: Optional[Union[pl.DataFrame, pl.LazyFrame]]) -> Union[pl.DataFrame, pl.LazyFrame]: 
        df_transform = frame.with_columns(self.expr.list_expr())
        
        if isinstance(self.model.data, list): 
            return self.group_join.join_data(frame_1=df_transform, frame_2=frame_2)
        
        return self.group_join.group_data(frame=df_transform)


