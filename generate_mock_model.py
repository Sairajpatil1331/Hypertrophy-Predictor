import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# 1. Create dummy training data
data = pd.DataFrame(
    [
        {"weekly_sets": 10, "intensity": 8, "growth": 5.0},
        {"weekly_sets": 20, "intensity": 9, "growth": 12.5},
        {"weekly_sets": 5, "intensity": 7, "growth": 2.1},
    ]
)

X = data[["weekly_sets", "intensity"]]
y = data["growth"]

# 2. Train a basic linear regression model
model = LinearRegression()
model.fit(X, y)

# 3. Define the destination inside the 'analytics' folder
target_path = os.path.join(
    os.path.dirname(__file__), "analytics", "hypertrophy_model.pkl"
)

# 4. Save the pickle file
joblib.dump(model, target_path)
print(f"🎉 Success! Mock model saved cleanly to: {target_path}")
