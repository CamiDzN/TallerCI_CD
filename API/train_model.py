# train_model.py
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

# Cargar datos (ejemplo Iris)
iris = load_iris(as_frame=True)
df = pd.concat([iris.data, iris.target.rename('target')], axis=1)

# Entrenar modelo
y = df.pop('target')
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(df, y)

# Guardar modelo
joblib.dump(model, 'app/model.pkl')
print("Modelo entrenado y guardado en app/model.pkl")