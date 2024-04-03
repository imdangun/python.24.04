import pandas as pd

df = pd.read_csv('gapminder.tsv', sep='\t')
print(df)

lifeExp = df['lifeExp']
print(lifeExp)

print(lifeExp.mean())
print(lifeExp.median())
print(lifeExp.min())
print(lifeExp.max())
print(lifeExp.std())

print(lifeExp.describe())

print(lifeExp.drop_duplicates())

print(lifeExp[lifeExp > lifeExp.mean()])

print(lifeExp.sort_values())
print(lifeExp.sort_values(ascending=False))

print(lifeExp + 100)