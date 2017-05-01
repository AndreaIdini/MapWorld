# Takes a dataframe and analyzes data column to extrapolate an index based
# on Ordinary Least Squares and calculating
# slope (as growth) and variance (as volatility) indicators

import statsmodels.api as sm #In the future stay tuned for evolution of pandas
import pandas as pd
import numpy as np

def add_Index_with_OLS(df):
    plot = False

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

    x0 = range(0,len(datacols))

    if plot:
        plot_fun(x0,datalist[0])

    param_list=[]
    for elem in datalist:
        if None not in elem:
            param = ols_param(x0,elem)
            param_list.append(param)
        else:
            param_list.append([None,None,None,None])
#

    A = np.array(param_list,dtype=np.float)
#    print A[0,:] #lines for a given postcode
#    print A[:,0] #column of all slopes

    mean_slp     = np.nanmean(A[:,0]); mean_trcpt     = np.nanmean(A[:,1])
    mean_err_slp = np.nanmean(A[:,2]); mean_err_trcpt = np.nanmean(A[:,3])
    means = [mean_slp,mean_trcpt,mean_err_slp,mean_err_trcpt]

    print param,means
    print calc_index(param,means)

    return df;

def calc_index(par,means):
    p = np.square(par)
    m = np.square(means)
    upandcom = (p[0] - m[0])/m[2]
    traditio = (p[1] - m[1])/m[3]
    risk     = p[2]/m[2] + p[3]/m[3]

    index = upandcom + traditio - risk
    index = np.sqrt(index)

    return index;

def ols_param(x,y):
# output[0] #slope output[1] #intercept output[2] #err slope output[3] #err intercept
    x = sm.add_constant(x)  # Adds a constant term, not included in the fit
    est = sm.OLS(y, x)
    est = est.fit()

    return [est.params[0],est.params[1],est.bse[0],est.bse[1]];

def plot_fun(x,y):
    import matplotlib.pyplot as plt

    x = sm.add_constant(x)  # Adds a constant term, not included in the fit

    est = sm.OLS(y, x)

    est = est.fit()

    print est.summary()

    # We pick 100 hundred points equally spaced from the min to the max
    X_prime = np.linspace(x.min(), x.max(), 100)[:, np.newaxis]
    X_prime = sm.add_constant(X_prime)  # add constant as we did before

    # Now we calculate the predicted values
    y_hat = est.predict(X_prime)

    plt.scatter(x[:,1], y, alpha=0.3)  # Plot the raw data
    plt.plot(X_prime[:,1], y_hat, 'r', alpha=0.9)  # Add the regression line, colored in red
    plt.show()
