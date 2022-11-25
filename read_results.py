import pandas as pd
import calendar
import datetime, time
import numpy as np
df = pd.read_csv('TEST2_results_JW1.csv')
results = df[["Runtime", "Computationaltime", "Backtracks"]]
# print(results)

results["Runtime"]= pd.to_timedelta(results["Runtime"]).view(np.int64) / 1e9
results["Computationaltime"]= pd.to_timedelta(results["Computationaltime"]).view(np.int64) / 1e9

results.loc['mean'] = results.mean()
results.loc['std'] = results.std()

print(results)
results.to_csv("Results/final_results_JW1_9x9.csv", index=False)