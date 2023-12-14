import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from scipy.stats import shapiro
from scipy.stats import mannwhitneyu
from statsmodels.graphics.gofplots import qqplot
import seaborn as sns

def read_csv_pandas(path_to_file):
    df = pd.read_csv(path_to_file,sep=';')
    return(df)

def plot_histogram_all(df, colors):
    grouped_df = df.groupby('species')

    for (species, group), color in zip(grouped_df, colors):
        plt.hist(group['mean'], label=species, alpha=0.5, color=color, edgecolor='black')
        mean_value = group['mean'].mean()
        plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=2, label=f'Mean ({species}): {mean_value:.2f}')

    plt.title('Histogram wartości średnich według gatunku')
    plt.xlabel('Wartości średnie NDVI')
    plt.ylabel('Częstotliwość')
    plt.legend()

    plt.show()

def plot_histogram(df, species, color):
    df_species = df[df['species'] == species]

    # Tworzymy histogram z kolorem ramki wokół prostokątów
    plt.hist(df_species['mean'], bins=40, label=species, alpha=0.5, edgecolor='black', color=color)

    # Dodajemy linię reprezentującą średnią wartość
    mean_value = df_species['mean'].mean()
    plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_value:.2f}')

    # Ustawiamy etykiety osi
    plt.xlabel('Mean Value')
    plt.ylabel('Frequency')

    # Ustawiamy zakres osi x od minimum do maksimum danych
    plt.xlim(df_species['mean'].min(), df_species['mean'].max())

    # Dodajemy legendę
    plt.legend()

    # Dodajemy tytuł
    plt.title(f'Histogram dla species=\'{species}\'')

    # Wyświetlamy histogram
    plt.show()


def descriptive_statistics(data, species):
    # Filtrujemy dane dla danego gatunku
    data_species = data[data['species'] == species]['mean']

    # Miary pozycyjne
    mean_value = data_species.mean()
    median_value = data_species.median()
    mode_value = data_species.mode().iloc[0]  # Mode może mieć więcej niż jedną wartość, dlatego wybieramy pierwszą

    # Miary przeciętne
    arithmetic_mean = data_species.mean()
    harmonic_mean = 1 / (1 / data_species).mean()
    geometric_mean = data_species.prod() ** (1 / len(data_species))

    # Miary zmienności klasyczne
    variance_value = data_species.var()
    std_deviation_value = data_species.std()

    # Miary pozycyjne dla zmiennych ilościowych
    q1 = data_species.quantile(0.25)
    q3 = data_species.quantile(0.75)
    interquartile_range = q3 - q1

    # Wyświetlanie wyników
    print(f"Statystyki opisowe dla gatunku '{species}':")
    print("\nMiary pozycyjne:")
    print(f"Średnia arytmetyczna: {mean_value}")
    print(f"Mediana: {median_value}")
    print(f"Moda: {mode_value}")

    print("\nMiary przeciętne:")
    print(f"Średnia arytmetyczna: {arithmetic_mean}")
    print(f"Średnia harmoniczna: {harmonic_mean}")
    print(f"Średnia geometryczna: {geometric_mean}")

    print("\nMiary zmienności klasyczne:")
    print(f"Wariancja: {variance_value}")
    print(f"Odchylenie standardowe: {std_deviation_value}")

    print("\nMiary pozycyjne dla zmiennych ilościowych:")
    print(f"Kwartyl 1 (Q1): {q1}")
    print(f"Kwartyl 3 (Q3): {q3}")
    print(f"Rozstęp międzykwartylowy: {interquartile_range}")

def assess_normality(data, species):
    # Filtrujemy dane dla danego gatunku
    data_species = data[data['species'] == species]['mean']

    # Wykres QQ
    qqplot(data_species, line='s')
    plt.title(f'Q-Q Plot dla gatunku {species}')
    plt.show()

    # Histogram
    plt.hist(data_species, bins=20, density=True, alpha=0.5, color='blue', edgecolor='black')
    plt.title(f'Histogram dla gatunku {species}')
    plt.xlabel('Wartości średnie')
    plt.ylabel('Częstotliwość')
    plt.show()

    # Test Shapiro-Wilka
    stat, p_value = shapiro(data_species)
    print(f'Test Shapiro-Wilka dla gatunku {species}:')
    print(f'Statystyka testowa: {stat}')
    print(f'Wartość p: {p_value}')
    if p_value > 0.05:
        print('Nie ma podstaw do odrzucenia hipotezy zerowej - dane mogą pochodzić z rozkładu normalnego.')
    else:
        print('Hipoteza zerowa (rozkład normalny) jest odrzucana.')


def compare_groups(data, group1_name, group2_name):
    # Wyodrębnienie grup
    group1 = data[data['species'] == group1_name]['mean']
    group2 = data[data['species'] == group2_name]['mean']

    # Przeprowadzenie testu U Manna-Whitneya
    u_stat, p_value = mannwhitneyu(group1, group2)
    print(f"Test U Manna-Whitneya: statystyka U = {u_stat}, p-wartość = {p_value}")

    # Wykres pudełkowy dla obu grup
    sns.boxplot(x='species', y='mean', data=data)
    plt.title(f'Porównanie grup {group1_name} i {group2_name}')
    plt.xlabel('Species')
    plt.ylabel('Mean Value')
    plt.show()


def compare_wilcoxon(data, group1_name, group2_name, alpha=0.05):
    # Wyodrębnienie grup
    group1 = data[data['species'] == group1_name]['mean']
    group2 = data[data['species'] == group2_name]['mean']

    # Test Wilcoxona dla dwóch grup
    stat, p_value = wilcoxon(group1, group2)

    # Sprawdzenie istotności statystycznej i wypisanie wyniku
    if p_value < alpha:
        print("Istnieją istotne różnice między grupami.")
    else:
        print("Brak istotnych różnic między grupami.")

    return stat, p_value

df = read_csv_pandas('D:/Output/trees.csv')

print(df.shape)
print(df.head())

#Średnia wartość parametru NDVI
print(df['mean'].mean())

#ŚRednia wartość parametru NDVI w rozbiciu na gatunki

print(df.groupby('species')['mean'].mean())

#ŚRednia wartość parametru NDVI w rozbiciu na gatunki i wiek

print(df.pivot_table(index='species', columns='age',values=('mean')))

#histogram danych
"""
colors = ['orange', 'blue']

plot_histogram_all(df, colors)
plot_histogram(df, species='SO', color='orange')
plot_histogram(df, species='DB', color='blue')
descriptive_statistics(df,species='DB')
assess_normality(df, species='SO')
assess_normality(df, species='DB')
compare_groups(df, 'SO', 'DB')

"""