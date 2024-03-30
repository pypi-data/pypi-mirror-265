from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from classification_model.config.core import config

def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    
    validated_data = input_data.copy()
    new_vars_w_na = [
        var for var in config.model_config.features
        if var not in
        config.model_config.categorical_variables
        + config.model_config.numerical_variables
        and validated_data[var].isna().sum() > 0
    ]
    validated_data.dropna(subset=new_vars_w_na, inplace=True)
    
    return validated_data

def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    validated_data = drop_na_inputs(input_data=input_data)
    errors = None
    
    try:
        MultipleTitanicDataInputs(
            inputs=validated_data.replace({np.nan:None}).to_dict(orient='records')
        )
    except ValidationError as error:
        errors = error.json()
        
    return validated_data, errors

class TitanicDataInputSchema(BaseModel):
    pclass: Optional[int]
    sex: Optional[str]
    age: Optional[int]
    sibsp: Optional[int]
    parch: Optional[int]
    fare: Optional[float]
    cabin: Optional[str]
    embarked: Optional[str]
    title: Optional[str]
    
class MultipleTitanicDataInputs(BaseModel):
    inputs: List[TitanicDataInputSchema]
