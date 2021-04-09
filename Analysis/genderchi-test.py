import pandas as pd
import numpy as np
from scipy import stats

def test_proportion():
    # a = [[1227, 773], [1331,669], [1127, 873], [1326, 674]]
    
    # a = [[1227, 1331, 1127, 1326], [773, 669, 873, 674]]
    # df = pd.DataFrame(a, columns=['AP_Greedy', 'Pagerank', 'random', 'Constraint'])
    
    # a = [[1227, 1331], [773, 669]]
    # df = pd.DataFrame(a, columns=['AP_Greedy', 'Pagerank'])

    a = [[1227, 1331, 1127], [773, 669, 873]]
    df = pd.DataFrame(a, columns=['AP_Greedy', 'Pagerank', 'random'])

    df.index = ['men', 'women']
    aLen = len(a[0])
    print(df)
    f_obs = np.array([df.iloc[0][0:aLen].values,
                  df.iloc[1][0:aLen].values])

    print(stats.chi2_contingency(f_obs))


if __name__ == '__main__':
    test_proportion()
    
    