import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import sys

print("Starting model training-")

try:
    # 1. Load the dataset
    df = pd.read_csv('symptom_data.csv')

    # 2. Check if the dataframe is empty
    if df.empty:
        print("\nERROR: 'symptom_data.csv' is empty or could not be read correctly.")
        print("Please ensure you have copied the new, smaller dataset into the file.")
        sys.exit(1)

    # 3. Separate features (X) from the target (y)
    # The target 'prognosis' is the last column
    X = df.drop('prognosis', axis=1)
    y = df['prognosis']

    # 4. Get the list of symptom columns
    model_columns = list(X.columns)
    print(f"Model will be trained on these {len(model_columns)} symptoms: {model_columns}")

    # 5. Create and train the model
    print("\nTraining the RandomForest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    print("Model training complete.")

    # 6. Save the trained model and the columns
    joblib.dump(model, 'disease_prediction_model.joblib')
    joblib.dump(model_columns, 'model_columns.joblib')

    print("\nSuccess! Model trained and saved.")
    print("You are finally ready to run 'ai_server.py'.")

except FileNotFoundError:
    print("\nERROR: 'symptom_data.csv' not found.")
    print("Please make sure the dataset file is created and has the new data.")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")