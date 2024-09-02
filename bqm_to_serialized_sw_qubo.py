# -*- coding: utf-8 -*-
"""BQM to serialized_SW_QUBO.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YLCH9PnE4b3R1WuNNu7FK7eBahrLnh14
"""

!pip install  pyqubo



import numpy as np
import pandas as pd
import pyqubo


# Load the data from the Excel file
from google.colab import files
uploaded = files.upload()

asset_returns = pd.read_excel("asset_return_data.xlsx", index_col=0)

# Compute the covariance matrix
covariance_matrix = np.cov(asset_returns.T)

# Define the PyQubo variables
N = len(asset_returns.columns)  # Number of assets
x = pyqubo.Array.create('x', shape=(N, N), vartype='BINARY')

# Define the number of runs and the range of alpha values to use
num_runs = 6
alpha_values = np.linspace(0.1, 100, num_runs)
beta = 10  # Penalty parameter

# Loop over the range of alpha values
for i, alpha in enumerate(alpha_values):
    # Define the Hamiltonian terms
    returns_term = sum([asset_returns.iloc[:, j].mean() * sum(x[j, :]) for j in range(N)])
    risk_term = -alpha * sum([sum([covariance_matrix[j, k] * x[j, i] * x[k, i] for j in range(N) for k in range(N)]) for i in range(N)])
    penalty_term = beta * (sum([sum(x[j, :]) - 1 for j in range(N)]) ** 2)

    # Define the Hamiltonian
    H = returns_term + risk_term + penalty_term

    # Compile the Hamiltonian into a QUBO model
    model = H.compile()

    # Convert the model to a BQM
    bqm = model.to_bqm()

    # Convert the BQM to a serializable object
    bqm_serializable = bqm.to_serializable()

    # Define the filename for this alpha value
    filename = f'model_{alpha:.1f}.txt'

    # Open the file for writing
    with open(filename, 'w') as f:
        # Write the serializable object to the file
        f.write(str(bqm_serializable))

    # Download the file
    files.download(filename)

"""new stuff with SR and plot"""