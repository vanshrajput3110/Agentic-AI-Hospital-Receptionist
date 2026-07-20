from ai import classify_patient

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay,
)

import matplotlib.pyplot as plt


# -------------------------------
# Test Dataset (Ground Truth)
# -------------------------------

test_cases = [

    ("High fever and cough", "General"),
    ("Fever with headache", "General"),
    ("Stomach pain", "General"),
    ("Vomiting", "General"),
    ("Cold and cough", "General"),
    ("Food poisoning", "General"),
    ("Body pain", "General"),
    ("Migraine headache", "General"),

    ("Chest pain", "Emergency"),
    ("Heart attack symptoms", "Emergency"),
    ("Road accident", "Emergency"),
    ("Heavy bleeding", "Emergency"),
    ("Stroke symptoms", "Emergency"),
    ("Unconscious patient", "Emergency"),
    ("Difficulty breathing", "Emergency"),
    ("Severe burns", "Emergency"),

    ("Anxiety", "Mental Health"),
    ("Depression", "Mental Health"),
    ("Stress", "Mental Health"),
    ("Panic attacks", "Mental Health"),
    ("Unable to sleep due to anxiety", "Mental Health"),
    ("Feeling hopeless", "Mental Health"),
    ("Mental stress", "Mental Health"),
    ("Emotional breakdown", "Mental Health"),

    ("Child with fever", "Pediatrics"),
    ("Baby with cough", "Pediatrics"),
    ("5 year old child vomiting", "Pediatrics"),
    ("Infant with cold", "Pediatrics"),
    ("Child stomach pain", "Pediatrics"),
    ("Baby has high fever", "Pediatrics"),
    ("3 year old coughing", "Pediatrics"),
    ("Toddler ear pain", "Pediatrics"),

    ("Fracture in arm", "Orthopedics"),
    ("Broken leg", "Orthopedics"),
    ("Joint pain", "Orthopedics"),
    ("Knee injury", "Orthopedics"),
    ("Shoulder dislocation", "Orthopedics"),
    ("Back pain after fall", "Orthopedics"),
    ("Bone fracture", "Orthopedics"),
    ("Ankle sprain", "Orthopedics"),

]


# -------------------------------
# Run Evaluation
# -------------------------------

y_true = []
y_pred = []

print("\nPrediction Results\n")
print("-" * 80)

for symptoms, actual in test_cases:

    result = classify_patient(symptoms)

    predicted = result["department"]

    print(f"Symptoms : {symptoms}")
    print(f"Actual    : {actual}")
    print(f"Predicted : {predicted}")
    print("-" * 80)

    y_true.append(actual)
    y_pred.append(predicted)


# -------------------------------
# Metrics
# -------------------------------

accuracy = accuracy_score(y_true, y_pred)

precision = precision_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

print("\n==============================")
print("MODEL EVALUATION")
print("==============================")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nClassification Report\n")

print(
    classification_report(
        y_true,
        y_pred,
        zero_division=0
    )
)

cm = confusion_matrix(y_true, y_pred)

print("\nConfusion Matrix\n")

print(cm)


# -------------------------------
# Plot Confusion Matrix
# -------------------------------

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=[
        "Emergency",
        "General",
        "Mental Health",
        "Orthopedics",
        "Pediatrics",
    ],
)

disp.plot(cmap="Blues")
plt.title("Confusion Matrix")
plt.tight_layout()

plt.savefig("confusion_matrix.png", dpi=300)

plt.show()