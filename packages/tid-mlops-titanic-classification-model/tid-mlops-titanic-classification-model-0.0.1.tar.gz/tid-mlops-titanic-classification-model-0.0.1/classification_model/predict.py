import typing

import pandas as pd

from classification_model import __version__ as _version
from classification_model.config.core import config
from classification_model.processing.data_manager import load_pipeline
from classification_model.processing.validation import validate_inputs

pipeline_filename = f'{config.app_config.pipeline_save_file}{_version}.pkl'
_titanic_pipe = load_pipeline(file_name=pipeline_filename)

def make_prediction(*, input_data: typing.Union[pd.DataFrame, dict]) -> dict: ##The union typing means the input can be either or df or dict
    
    data = pd.DataFrame(input_data)
    validated_data, errors = validate_inputs(input_data=data)
    results = {'predictions': None, 'version': _version, 'errors': errors}
    
    if not errors:
        predictions = list(_titanic_pipe.predict(X=validated_data))
        predictions_proba = _titanic_pipe.predict_proba(X=validated_data)[:, 1]
        # print(predictions)
        
        results = {'predictions': predictions,
                   'predictions_proba': predictions_proba, 
                   'version': _version, 
                   'errors': errors
                   }
        
    return results