from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np
import pandas as pd
import joblib

def read_csv_pandas(path_to_file):
    df = pd.read_csv(path_to_file, sep=';')
    return df

df = read_csv_pandas('D:/Output/trees.csv')

# Podziel dane na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(df['mean'].values.reshape(-1, 1), df['species'], test_size=0.2, random_state=42)

# Wytrenuj prosty model regresji logistycznej
model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

# Określ ścieżkę, pod którą zapiszesz model
model_path = 'D:/Output/so_db_model.joblib'

# Zapisz model do zmiennej 'model_path'
joblib.dump(model, model_path)

# Przewiduj na zbiorze testowym
y_pred = model.predict(X_test)

# Ocen jakość modelu
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

# Wyświetl wyniki
print(f'Accuracy: {accuracy:.2f}')
print(f'Confusion Matrix:\n{conf_matrix}')
print(f'Classification Report:\n{classification_rep}')
