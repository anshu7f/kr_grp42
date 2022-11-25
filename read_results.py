import pandas as pd
import calendar
import datetime, time
import numpy as np
df = pd.read_csv('results_basic_dpll_9x9.csv')
results = df[["Runtime", "Computationaltime", "Backtracks"]]
# print(results)

results["Runtime"]= pd.to_timedelta(results["Runtime"]).view(np.int64) / 1e9
results["Computationaltime"]= pd.to_timedelta(results["Computationaltime"]).view(np.int64) / 1e9

results.loc['mean'] = results.mean()

print(results)
results.to_csv("Results/final_results_DPLL_9x9.csv", index=False)