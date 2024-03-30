from typing import List
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from classification_model import __version__ as _version
from classification_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config

def load_dataset(*, file_name: str) -> pd.DataFrame:
    df = pd.read_csv(Path(f'{DATASET_DIR}/{file_name}'))
    
    return df

def save_pipeline(*, pipeline_to_save: Pipeline) -> None:
    
    save_file_name = f'{config.app_config.pipeline_save_file}{_version}.pkl'
    save_path = TRAINED_MODEL_DIR / save_file_name
    
    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_save, save_path)
    
def load_pipeline(*, file_name: str) -> Pipeline:
    
    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model

def remove_old_pipelines(*, files_to_keep: List[str]) -> None:
    
    do_not_delete = files_to_keep + ['__init__.py']
    for mod_file in TRAINED_MODEL_DIR.iterdir():
        if mod_file.name not in do_not_delete:
            mod_file.unlink()