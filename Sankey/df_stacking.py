#example code for stacking columns
import pandas as pd
import sankey as sk

art = pd.DataFrame({'nationality':['A', 'A', 'B', 'C'],
                   'gender':['M', 'M', 'F', 'M'],
                   'decade':['1930', '1940', '1930', '1940']})
print(art)

#extract out nationality and gender
ng = art[['nationality', 'gender']]
ng.columns = ['src', 'targ']
#extract out gender and decade
gd = art[['gender', 'decade']]
gd.columns = ['src', 'targ']
#axis=0 is concat vertical where axis=1 is horizontally - this aligns based on column names so have NaN
stacked = pd.concat([ng, gd], axis=0)
print(stacked)

sk.make_sankey(stacked, 'src', 'targ')


