import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

# Cargar datos
iris = load_iris(as_frame=True)
df = pd.concat([iris.data, iris.target.rename("target")], axis=1)

# Separar variables
y = df.pop("target")

# Entrenar modelo
model = RandomForestClassifier()
model.fit(df, y)

# Guardar modelo en app/
joblib.dump(model, "app/model.pkl")
print("✅ Modelo entrenado y guardado en app/model.pkl")
