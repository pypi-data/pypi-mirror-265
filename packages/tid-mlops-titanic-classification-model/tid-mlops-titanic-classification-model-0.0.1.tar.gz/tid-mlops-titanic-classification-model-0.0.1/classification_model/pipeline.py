from sklearn.pipeline import Pipeline
from feature_engine.imputation import CategoricalImputer, AddMissingIndicator, MeanMedianImputer
from feature_engine.encoding import RareLabelEncoder, OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from classification_model.config.core import config
from classification_model.processing import features as custom_features

CATEGORICAL_VARIABLES = config.model_config.categorical_variables
NUMERICAL_VARIABLES = config.model_config.numerical_variables
CABIN = list(config.model_config.cabin_variable)

# set up the pipeline
titanic_pipe = Pipeline([

    # ===== IMPUTATION =====
    # impute categorical variables with string 'missing'
    ('categorical_imputation', CategoricalImputer(imputation_method='missing',
                                                     variables=CATEGORICAL_VARIABLES)), 

    # add missing indicator to numerical variables
    ('missing_indicator', AddMissingIndicator(variables=NUMERICAL_VARIABLES)), 

    # impute numerical variables with the median
    ('median_imputation', MeanMedianImputer(imputation_method='median', variables=NUMERICAL_VARIABLES)), 


    # Extract first letter from cabin
    ('extract_letter', custom_features.ExtractLetterTransformer(variables=CABIN)), 


    # == CATEGORICAL ENCODING ======
    # remove categories present in less than 5% of the observations (0.05)
    # group them in one category called 'Rare'
    ('rare_label_encoder', RareLabelEncoder(tol=0.05, n_categories=1, variables=CATEGORICAL_VARIABLES)),


    # encode categorical variables using one hot encoding into k-1 variables
    ('categorical_encoder', OneHotEncoder(variables=CATEGORICAL_VARIABLES, drop_last=True)),

    # scale using standardization
    ('scaler', StandardScaler()),

    # logistic regression (use C=0.0005 and random_state=0)
    ('Logit', LogisticRegression(C=config.model_config.c_value, random_state=config.model_config.random_state)),
])