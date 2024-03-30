import numpy as np
import math
from classification_model.predict import make_prediction

def test_make_prediction(sample_input_data):
    #Given
    expected_first_pred_proba = 0.30002649
    expected_num_preds = 262
    
    #When
    result = make_prediction(input_data=sample_input_data)
    
    #Then
    preds = result.get('predictions')
    preds_proba = result.get('predictions_proba')
    
    assert isinstance(preds, list)
    assert isinstance(preds_proba[0], np.float64)
    assert result.get('errors') is None
    assert len(preds) == expected_num_preds
    assert math.isclose(preds_proba[0], expected_first_pred_proba, abs_tol=0.0001)