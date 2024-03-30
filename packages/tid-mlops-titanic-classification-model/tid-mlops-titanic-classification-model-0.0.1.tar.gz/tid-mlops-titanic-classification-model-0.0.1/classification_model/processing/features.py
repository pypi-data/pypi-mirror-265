from sklearn.base import BaseEstimator, TransformerMixin

class ExtractLetterTransformer(BaseEstimator, TransformerMixin):
    # Extract fist letter of variable

    def __init__(self, variables):
        self.variables = variables


    def fit(self, X, y=None):
        
        return self
        

    def transform(self, X):
        X = X.copy()
        # print(self.variables)
        for var in self.variables:
            # X[var].apply(lambda val: re.sub(r'[^A-Za-z]', '', val) if not pd.isna(val) else val)
            # print(var)
            X[var] = X[var].str[0]
            
        return X
