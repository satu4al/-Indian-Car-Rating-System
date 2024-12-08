import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sample Car Data (This can be connected to a CSV or a live database)
car_data = pd.DataFrame([
    {'Name': 'Maruti Swift', 'Price': 6, 'Mileage': 22, 'Maintenance': 4, 'Resale': 8, 'Safety': 6, 'Brand': 9, 'Technology': 7, 'Comfort': 7, 'Design': 8, 'EMI': 8},
    {'Name': 'Hyundai Creta', 'Price': 10, 'Mileage': 18, 'Maintenance': 5, 'Resale': 9, 'Safety': 9, 'Brand': 9, 'Technology': 9, 'Comfort': 9, 'Design': 9, 'EMI': 6},
    {'Name': 'Tata Nexon', 'Price': 8, 'Mileage': 20, 'Maintenance': 6, 'Resale': 7, 'Safety': 10, 'Brand': 8, 'Technology': 8, 'Comfort': 8, 'Design': 8, 'EMI': 7},
    {'Name': 'Kia Seltos', 'Price': 12, 'Mileage': 16, 'Maintenance': 7, 'Resale': 9, 'Safety': 9, 'Brand': 8, 'Technology': 10, 'Comfort': 9, 'Design': 9, 'EMI': 5},
    {'Name': 'Mahindra XUV700', 'Price': 14, 'Mileage': 15, 'Maintenance': 8, 'Resale': 9, 'Safety': 10, 'Brand': 9, 'Technology': 10, 'Comfort': 10, 'Design': 10, 'EMI': 4},
    {'Name': 'Toyota Innova', 'Price': 20, 'Mileage': 12, 'Maintenance': 9, 'Resale': 10, 'Safety': 10, 'Brand': 10, 'Technology': 8, 'Comfort': 10, 'Design': 9, 'EMI': 3}
])

# Step 1: Get User Preferences
print("Rate the importance of the following factors from 1 to 10 (1 = Least Important, 10 = Most Important)")
preferences = {
    'Price': int(input('How important is Price? (1-10): ')),
    'Mileage': int(input('How important is Mileage? (1-10): ')),
    'Maintenance': int(input('How important is Maintenance? (1-10): ')),
    'Resale': int(input('How important is Resale Value? (1-10): ')),
    'Safety': int(input('How important is Safety? (1-10): ')),
    'Brand': int(input('How important is Brand Reputation? (1-10): ')),
    'Technology': int(input('How important is Technology/Features? (1-10): ')),
    'Comfort': int(input('How important is Comfort & Space? (1-10): ')),
    'Design': int(input('How important is Aesthetics/Design? (1-10): ')),
    'EMI': int(input('How important is Loan/EMI Affordability? (1-10): '))
}

# Step 2: Normalize Preferences (Sum of all weights should be 1)
total_weight = sum(preferences.values())
normalized_preferences = {k: v / total_weight for k, v in preferences.items()}

# Step 3: Score each car based on user preferences
def calculate_score(car, weights):
    """ Calculate the weighted score for a car based on the user's preferences """
    score = 0
    for feature, weight in weights.items():
        score += car[feature] * weight  # Weighted contribution of each factor
    return round(score, 2)

car_data['Score'] = car_data.apply(lambda row: calculate_score(row, normalized_preferences), axis=1)

# Step 4: Rank cars based on scores
car_data = car_data.sort_values(by='Score', ascending=False)

# Display the top recommendations
print("\n=== Top Car Recommendations for You ===\n")
print(car_data[['Name', 'Score']].head(5))

# === Generate Graphs ===

# 1. User Preference Weights - Bar Plot
plt.figure(figsize=(10, 6))
sns.barplot(x=list(normalized_preferences.keys()), y=list(normalized_preferences.values()), palette='viridis')
plt.title('User Preferences Weight Distribution')
plt.xlabel('Factors')
plt.ylabel('Normalized Weight')
plt.xticks(rotation=45)
plt.show()

# 2. Car Scores - Bar Plot
plt.figure(figsize=(10, 6))
sns.barplot(x='Name', y='Score', data=car_data, palette='coolwarm')
plt.title('Car Scores Based on User Preferences')
plt.xlabel('Car Name')
plt.ylabel('Score')
plt.xticks(rotation=45)
plt.show()

# 3. Radar/Spider Chart for the Top Car
from math import pi

# Top car's attributes
top_car = car_data.iloc[0]
attributes = ['Price', 'Mileage', 'Maintenance', 'Resale', 'Safety', 'Brand', 'Technology', 'Comfort', 'Design', 'EMI']
values = [top_car[feature] for feature in attributes]

# Close the loop for radar chart
values += values[:1]
categories = attributes + [attributes[0]]

# Create radar chart
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]

# Draw one line for each category and add labels
plt.xticks(angles[:-1], categories, color='grey', size=10)
ax.plot(angles, values, linewidth=2, linestyle='solid', label=top_car['Name'])
ax.fill(angles, values, color='red', alpha=0.25)
plt.title(f'Attribute Breakdown for {top_car["Name"]}')
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
plt.show()

