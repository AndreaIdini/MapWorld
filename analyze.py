# Takes a dataframe and analyzes data column to extrapolate an index based
# on Ordinary Least Squares and calculating
# slope (as growth) and variance (as volatility) indicators

import statsmodels.api as sm

def add_Index_with_OLS(df):
    plot = True

# read name where data are, that are names where "20" appears, since the year
    colnames = list(df.columns.values)
    datacols = []
    for col in colnames:
        if col is not None:
            if '20' in col:
                datacols.append(col)

# create DataFrame with only data
    df_data = df[datacols]

    datalist = df_data.values.tolist()
    if plot:
        plot_fun(range(0,len(datacols)),datalist[0])

    
    return df;

def plot_fun(x,y):
        import matplotlib.pyplot as plt
        import numpy as np

        x = sm.add_constant(x)  # Adds a constant term, not included in the fit

        est = sm.OLS(y, x)

        est = est.fit()

        print est.summary()
        print 'parameters= '
        print est.params

        # We pick 100 hundred points equally spaced from the min to the max
        X_prime = np.linspace(x.min(), x.max(), 100)[:, np.newaxis]
        X_prime = sm.add_constant(X_prime)  # add constant as we did before

        # Now we calculate the predicted values
        y_hat = est.predict(X_prime)

        plt.scatter(x[:,1], y, alpha=0.3)  # Plot the raw data
        plt.plot(X_prime[:,1], y_hat, 'r', alpha=0.9)  # Add the regression line, colored in red
        plt.show()
