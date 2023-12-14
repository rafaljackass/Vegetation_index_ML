import joblib
import numpy as np

# Wczytaj model (upewnij się, że wcześniej model został zapisany)
model_path = 'D:/Output/so_db_model.joblib'
model = joblib.load(model_path)

# Przewiduj prawdopodobieństwa dla surowego wyniku
raw_ndvi_value = float(input('Podaj wynik NDVI')) # tu podaj swoją wartość NDVI
predicted_probabilities = model.predict_proba([[raw_ndvi_value]])

# Pobierz indeks klasy przewidzianej jako max
predicted_class_index = np.argmax(predicted_probabilities)

# Pobierz wartość pewności dla przewidzianej klasy
confidence = predicted_probabilities[0, predicted_class_index]

# Dostępne klasy
classes = model.classes_

# Przewidziana klasa i pewność dla wartości NDVI
predicted_class = classes[predicted_class_index]
print(f'Przewidziana klasa dla wartości NDVI {raw_ndvi_value}: {predicted_class} z pewnością {confidence:.2f}')