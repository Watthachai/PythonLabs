import plotly.express as px
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import missingno as msno

import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv('GraphVisualization/src/database/tourism-receipts-from-international-tourist-arrivals_2018.csv')
print(data.shape)

data['Country'] = data['Country'].dropna().apply(lambda x :  x.replace(' ,',',').replace(', ',',').split(','))
lst_col = 'Country'
data2 = pd.DataFrame({
      col :  np.repeat(data[col].values, data[lst_col].str.len())
      for col in data.columns.drop(lst_col)}
    ).assign(**{lst_col:np.concatenate(data[lst_col].values)})[data.columns.tolist()]

year_country2 = data2.groupby('No. of Arrivals')['Country'].value_counts().reset_index(name='counts')

fig = px.choropleth(year_country2, locations="Country", color="counts", 
                    locationmode='country names',
                    animation_frame='No. of Arrivals',
                    range_color=[0, 9000000],
                    color_continuous_scale=px.colors.sequential.OrRd
                   )

fig.update_layout(title='Comparison by country')
fig.show()