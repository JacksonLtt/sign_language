# importing pandas and numpy libraries
import pandas as pd
import numpy as np

# creating and initializing a nested list
values_list = [[15, 2.5, 100], [20, 4.5, 50], [25, 5.2, 80],
               [45, 5.8, 48], [40, 6.3, 70], [41, 6.4, 90],
               [51, 2.3, 111]]

# creating a pandas dataframe
df = pd.DataFrame(values_list, columns=['Field_1', 'Field_2', 'Field_3'],
                  index=['a', 'b', 'c', 'd', 'e', 'f', 'g'])
print(df)

# Apply function numpy.square() to square
# the values of one row only i.e. row
# with index name 'd'
# df = df.apply(lambda x: print(x["Field_1"]," ",x["Field_2"],"\n"),axis=1)
#
#
# print("after lambda")
# printing dataframe
print(df.iloc[1,:]['Field_1'])