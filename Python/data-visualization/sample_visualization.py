import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

df = pd.DataFrame({'a': np.random.randint(0, 50, 1000)})
df['b'] = df['a'] + np.random.normal(0, 10, 1000) # positively correlated with 'a'
df['c'] = 100 - df['a'] + np.random.normal(0, 5, 1000) # negatively correlated with 'a'
df['d'] = np.random.randint(0, 50, 1000) # not correlated with 'a'
df.corr()

#pd.scatter_matrix(df, figsize=(6, 6))
#plt.show()

def my_scatter_matrix():
    pd.scatter_matrix(df, figsize=(6, 6))
    plt.show()

def my_correlation_matrix():
    plt.matshow(df.corr())
    plt.xticks(range(len(df.columns)), df.columns)
    plt.yticks(range(len(df.columns)), df.columns)
    plt.colorbar()
    plt.show()

def positive_corr():
    np.random.seed(1)
    # 1000 random integers between 0 and 50
    x = np.random.randint(0, 50, 1000)
    # Positive Correlation with some noise
    y = x + np.random.normal(0, 10, 1000)
    np.corrcoef(x, y)
    plt.scatter(x, y)
    plt.show()

def negative_corr():
    # 1000 random integers between 0 and 50
    x = np.random.randint(0, 50, 1000)
    # Negative Correlation with some noise
    y = 100 - x + np.random.normal(0, 5, 1000)
    np.corrcoef(x, y)
    plt.scatter(x, y)
    plt.show()

def weak_corr():
    x = np.random.randint(0, 50, 1000)
    y = np.random.randint(0, 50, 1000)
    np.corrcoef(x, y)
    plt.scatter(x, y)
    plt.show()

my_scatter_matrix()
my_correlation_matrix()
positive_corr()
negative_corr()
weak_corr()