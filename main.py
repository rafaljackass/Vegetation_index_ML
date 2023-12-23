import tkinter as tk
from tkinter import filedialog
import Vegetation_indices
import Cut_to_polygon_MT

def run_vegetation_indices():
    Vegetation_indices.main()

def run_cut_to_polygon():
    root = tk.Tk()
    root.withdraw()

    # Wybierz plik wektorowy
    input_vector = filedialog.askopenfilename(title="Wybierz plik wektorowy", filetypes=[("Shapefiles", "*.shp")])

    # Sprawdź, czy użytkownik wybrał plik
    if not input_vector:
        print("Anulowano wybór pliku wektorowego.")
        return

    # Wybierz plik rastrowy
    input_raster = filedialog.askopenfilename(title="Wybierz plik rastrowy", filetypes=[("TIFF Files", "*.tif")])

    # Sprawdź, czy użytkownik wybrał plik
    if not input_raster:
        print("Anulowano wybór pliku rastrowego.")
        return

    # Wybierz folder do zapisu plików przyciętych
    output_dir = filedialog.askdirectory(title="Wybierz folder do zapisu plików przyciętych")

    # Sprawdź, czy użytkownik wybrał folder
    if not output_dir:
        print("Anulowano wybór folderu do zapisu plików przyciętych.")
        return

    # Wywołaj funkcję przycinania rastrowego z wybranymi ścieżkami
    Cut_to_polygon_MT.main(input_vector, input_raster, output_dir)

def main():
    root = tk.Tk()
    root.title("Menu Skryptów")
    root.geometry("500x500")  # Ustaw rozmiar okna

    frame = tk.Frame(root)
    frame.pack(pady=10)

    btn_vegetation_indices = tk.Button(frame, text="Obliczanie indeksu wegetacji", command=run_vegetation_indices)
    btn_vegetation_indices.pack(pady=5, side=tk.TOP)

    btn_cut_to_polygon = tk.Button(frame, text="Przycinanie poligonu do maski", command=run_cut_to_polygon)
    btn_cut_to_polygon.pack(pady=5, side=tk.TOP)

    # Dodaj przyciski dla innych skryptów

    root.mainloop()

if __name__ == "__main__":
    main()
