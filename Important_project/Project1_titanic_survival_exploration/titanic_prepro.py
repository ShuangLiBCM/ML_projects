import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from collections import Counter
from imblearn.over_sampling import SMOTE

train_data = pd.read_csv('train.csv')
pd.options.display.max_rows = 999
train_data.head()