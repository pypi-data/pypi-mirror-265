from config.core import config
from pipeline import titanic_pipe
from processing.data_manager import load_dataset, save_pipeline

def run_training() -> None:
    train_data = load_dataset(file_name=config.app_config.training_data_file)
    # test_data = load_dataset(file_name=config.app_config.test_data_file)
    
    X_train = train_data.drop(columns=[config.model_config.target])
    y_train = train_data[config.model_config.target]
    # X_test = test_data.drop(columns=config.model_config.target)
    # y_test = test_data[config.model_config.target]
    
    titanic_pipe.fit(X_train, y_train)
    
    save_pipeline(pipeline_to_save=titanic_pipe)
    
if __name__ == '__main__':
    run_training()
