from classification_model.config.core import config
from classification_model.processing.features import ExtractLetterTransformer

def test_first_extractionz(sample_input_data):
    #Given
    extractor = ExtractLetterTransformer(variables=config.model_config.cabin_variable)
    
    assert sample_input_data['cabin'].loc[7] == 'C104'
    
    # when  
    test = extractor.fit_transform(sample_input_data)
    
    # then
    assert test['cabin'].loc[7] == 'C'