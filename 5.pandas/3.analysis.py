import pandas as pd

df = pd.read_csv('gapminder.tsv', sep='\t')
a = (df['country'])             # Series
b = (df[['country', 'year']])   # DataFrame

print(df)
#           country continent  year  lifeExp       pop   gdpPercap
# 0     Afghanistan      Asia  1952   28.801   8425333  779.445314
# 1     Afghanistan      Asia  1957   30.332   9240934  820.853030
# ...           ...       ...   ...      ...       ...         ...
# 1702     Zimbabwe    Africa  2002   39.989  11926563  672.038623
# 1703     Zimbabwe    Africa  2007   43.487  12311143  469.709298

c = df.loc[0] # Series, Name field value == 0
print(c)
# country      Afghanistan
# continent           Asia
# year                1952
# lifeExp           28.801
# pop              8425333
# gdpPercap     779.445314

d = df.iloc[0] # Series, 0번째 row
print(d)
# country      Afghanistan
# continent           Asia
# year                1952
# lifeExp           28.801
# pop              8425333
# gdpPercap     779.445314

e = df.loc[[0, 10, 100]]
print(e)
#          country continent  year  lifeExp       pop   gdpPercap
# 0    Afghanistan      Asia  1952   28.801   8425333  779.445314
# 10   Afghanistan      Asia  2002   42.129  25268405  726.734055
# 100   Bangladesh      Asia  1972   45.252  70759295  630.233627

f = df.iloc[[0, 10, 100]]
print(f)
#          country continent  year  lifeExp       pop   gdpPercap
# 0    Afghanistan      Asia  1952   28.801   8425333  779.445314
# 10   Afghanistan      Asia  2002   42.129  25268405  726.734055
# 100   Bangladesh      Asia  1972   45.252  70759295  630.233627

g = df.loc[[0, 10, 100], ['country', 'year']]
print(g)
#          country  year
# 0    Afghanistan  1952
# 10   Afghanistan  2002
# 100   Bangladesh  1972

h = df.iloc[[0, 10, 100], [0, 2]]
print(h)
#          country  year
# 0    Afghanistan  1952
# 10   Afghanistan  2002
# 100   Bangladesh  1972

print(df['year'].mean()) # 1979.5
print(df[df['year'] > df['year'].mean()])

df1 = pd.read_csv('concat_1.csv')
df2 = pd.read_csv('concat_2.csv')
df3 = pd.read_csv('concat_3.csv')

result = pd.concat([df1, df2, df3])
print(result)

result = pd.concat([df1, df2, df3], ignore_index=True)
print(result)

result = pd.concat([df1, df2, df3], axis=1)
print(result)

result = pd.concat([df1, df2, df3], axis=1, ignore_index=True)
print(result)

site = pd.read_csv('site.csv')
visited = pd.read_csv('visited.csv')

result = visited.merge(site, left_on='site', right_on='name')
print(result)