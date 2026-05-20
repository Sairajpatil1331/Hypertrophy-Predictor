import os
import django
import pandas as pd

# 1. Boot up the Django Environment
# (Replace 'portfolio_core' with your actual project folder name if it's different)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_core.settings')
django.setup()

# 2. Import your database models (MUST happen after django.setup())
from analytics.models import PerformanceSet, DailyLog

def extract_training_data():
    print("Fetching data from MySQL...")
    
    # Query the database using Django's ORM
    # We use select_related to join the Workout and Exercise tables efficiently
    query_set = PerformanceSet.objects.select_related('workout', 'exercise').values(
        'workout__date',
        'workout__split_name',
        'exercise__name',
        'weight',
        'reps',
        'rpe'
    )
    
    # Convert directly to a Pandas DataFrame
    df = pd.DataFrame(list(query_set))
    
    if df.empty:
        print("No data found! Go add some sets in the Admin panel.")
        return df

    # Feature Engineering: Calculate total tonnage moved
    df['weight'] = df['weight'].astype(float)
    df['volume_load'] = df['weight'] * df['reps']
    
    return df

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

if __name__ == "__main__":
    df = extract_training_data()
    
    if not df.empty:
        print("\n--- Pandas DataFrame Loaded Successfully! ---")
        print(df.head())
        print(f"\nTotal Rows Analyzed: {len(df)}")

        # --- MACHINE LEARNING PIPELINE ---
        
        # We need more than 1 row to train a model properly. 
        # But we will write the code so it works as you add data!
        if len(df) > 5:
            print("\n--- Training Hypertrophy Prediction Model ---")
            
            # 1. Define Features (X) and Target (y)
            # We want to predict Volume Load based on Reps and RPE
            X = df[['reps', 'rpe']].fillna(0) # Features
            y = df['volume_load']             # Target variable
            
            # 2. Split Data (80% Training, 20% Testing)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # 3. Initialize and Train the Model
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            # 4. Test the Model
            predictions = model.predict(X_test)
            error = mean_squared_error(y_test, predictions)
            
            print(f"Model trained successfully!")
            print(f"Mean Squared Error: {error:.2f}")
            
            # 5. Make a Prediction!
            # E.g., "If I plan to do 8 reps at an RPE of 9, what volume should I expect?"
            sample_prediction = model.predict([[8, 9]])
            print(f"\nPredicted Volume Load for 8 reps @ 9 RPE: {sample_prediction[0]:.2f} kg")
            
        else:
            print("\n[!] Skipping ML training: Need at least 6 rows of data.")
            print("Go to the Admin panel and log a few more Performance Sets!")