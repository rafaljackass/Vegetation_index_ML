import os
import csv
import tkinter as tk
from tkinter import filedialog

#utworzenie okna głównego
root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory()

print(folder_path)
#ścieżka dokatalogu zawierającego pliki

path = folder_path

with open(path+'/lista_plików.csv', mode='w') as csv_file:
    fieldnames = ['Nazwa pliku', 'Ścieżka']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()  # zapisujemy nagłówek

    # iterujemy przez pliki w katalogu
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        # sprawdzamy, czy to plik (a nie katalog)
        if os.path.isfile(file_path):
            # zapisujemy nazwę pliku i ścieżkę do pliku CSV
            writer.writerow({'Nazwa pliku': file_name, 'Ścieżka': file_path})