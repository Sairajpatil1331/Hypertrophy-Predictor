from django.shortcuts import render
import pandas as pd
import joblib  # or pickle, depending on how you saved your model
import os

# Load your trained model (make sure path matches where your model file lives)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "hypertrophy_model.pkl")
model = joblib.load(MODEL_PATH)


def predict_view(request):
    prediction_result = None

    if request.method == "POST":
        # 1. Capture the inputs from the HTML form fields
        muscle_group = request.POST.get("muscle_group")
        weekly_sets = float(request.POST.get("weekly_sets"))
        intensity = float(request.POST.get("intensity"))

        # 2. Format inputs exactly how your Scikit-Learn model expects them
        # (Modify the keys/columns below to match your specific dataset features)
        input_data = pd.DataFrame(
            [
                {
                    "weekly_sets": weekly_sets,
                    "intensity": intensity,
                    # If your model needs encoding for muscle groups, handle it here
                }
            ]
        )

        # 3. Predict using your ML pipeline
        raw_prediction = model.predict(input_data)[0]

        # Format output neatly (e.g., rounding numerical growth or handling class labels)
        prediction_result = f"{round(raw_prediction, 2)}% Growth Index"

    return render(request, "analytics/index.html", {"prediction": prediction_result})
