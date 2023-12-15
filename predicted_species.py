import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt

# Wczytaj model (upewnij się, że wcześniej model został zapisany)
model_path = 'D:/Output/so_db_model.joblib'
model = joblib.load(model_path)

# Wczytaj dane testowe z pliku CSV
test_data = pd.read_csv('D:/Output/trees_results_for_testing_model.csv', sep=';')

# Dodaj numer ID do danych wynikowych
test_data['id'] = test_data['id'].astype(str)  # Jeśli numer ID jest liczbą, zamień na tekst
test_data['id'] = test_data['id'] + '_predicted'  # Dodaj '_predicted' do numeru ID

# Przewiduj gatunki dla danych testowych
predicted_classes = model.predict(test_data['mean'].values.reshape(-1, 1))
predicted_probabilities = model.predict_proba(test_data['mean'].values.reshape(-1, 1))[:, 1]

# Dodaj przewidziane gatunki i prawdopodobieństwa do danych wynikowych
test_data['predicted_species'] = predicted_classes
test_data['predicted_probabilities'] = predicted_probabilities

# Sprawdź dokładność modelu
accuracy = accuracy_score(test_data['species'], predicted_classes)
conf_matrix = confusion_matrix(test_data['species'], predicted_classes)
classification_rep = classification_report(test_data['species'], predicted_classes)

# Wyświetl wyniki dokładności
print(f'Accuracy: {accuracy:.2f}')
print(f'Confusion Matrix:\n{conf_matrix}')
print(f'Classification Report:\n{classification_rep}')

# Oblicz krzywą ROC
fpr, tpr, thresholds = roc_curve(test_data['species'], predicted_probabilities, pos_label='SO')
roc_auc = auc(fpr, tpr)

# Wykres krzywej ROC
plt.figure(figsize=(8, 8))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()

# Zapisz wyniki do nowego pliku CSV
test_data.to_csv('D:/Output/test_results.csv', index=False)

# Wyświetl wyniki
print(test_data[['id', 'mean', 'species', 'predicted_species', 'predicted_probabilities']])