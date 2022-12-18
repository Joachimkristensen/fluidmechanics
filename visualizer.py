from matplotlib import pyplot as plt
from matplotlib import colors
import plotly.express as px
import pandas as pd

# plt.rcParams["figure.figsize"] = [10.00, 10.00]
# plt.rcParams["figure.autolayout"] = True
#df = pd.read_csv("flow_output_formatted_new.txt", sep=" ")
df = pd.read_csv("output_14.0s.txt", sep=" ")
fig = px.scatter(df, x="x", y='y', color='v',
                 title="setting up colour palette",
                 color_continuous_scale=["Blue", "Turquoise", "lightgreen", "Green", "Yellow", "Orange", "salmon", "red"], range_color=[0, 25], width=800, height=800)
fig.show()
# x = df['A']
# y = df['B']
# c = df['C']
# cm = plt.cm.get_cmap('viridis')

# sc = plt.scatter(x, y, c=c, cmap=cm)
# plt.show()
