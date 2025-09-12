import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

# --- 1. Data Loading and Preprocessing ---
def load_and_prepare_data(file_path):
    """
    Loads and preprocesses the dataset.
    """
    try:
        df = pd.read_csv(file_path)
        
        # Clean column names
        df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
        
        # Drop rows with any missing values to ensure consistency for model training
        df.dropna(inplace=True)
        
        # Convert Admission_Year to integer
        df['Admission_Year'] = df['Admission_Year'].astype(int)
        
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found. Please ensure it's in the same directory.")
        return None

# --- 2. AI Model Training ---
def train_model(df):
    """
    Trains an AI model to predict medical conditions based on age and year.
    """
    # Features for the model
    features = ['Admission_Year', 'Age']
    X = df[features].copy()
    y = df['Medical_Condition']
    
    # Encode the categorical target variable
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Train a Random Forest Classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y_encoded)
    
    return model, le

# --- 3. Predictive Analysis and Visualization ---
def run_analysis(df, model, label_encoder):
    """
    Performs predictive analysis and generates visualizations.
    """
    # Create a directory to save visualizations
    if not os.path.exists('visualizations'):
        os.makedirs('visualizations')

    # --- Predictive Conclusion: Where is a disease more likely to occur? ---
    print("\n--- AI Model Predictive Conclusion ---")
    
    # Find the most common disease in each area
    area_disease_counts = df.groupby('Area')['Medical_Condition'].agg(
        lambda x: x.mode()[0] if not x.empty else None
    ).reset_index(name='Most_Common_Disease')
    
    print("\nBased on the dataset, here are the most common diseases in each area:")
    print(area_disease_counts)

    # --- Graphical Visualizations and Professional Insights ---
    print("\n--- Generating Professional Graphs and Insights ---")

    # Chart 1: Corrected Line Plot for Unique Diseases Over Time
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='Admission_Year', y='Medical_Condition', estimator=lambda x: len(np.unique(x)))
    plt.title('Total Number of Unique Diseases Over Time', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Unique Diseases', fontsize=12)
    plt.grid(True)
    plt.savefig('visualizations/diseases_over_time.png')
    print("Chart 1: 'diseases_over_time.png' saved.")
    plt.close()

    # Chart 2: Disease Distribution by Age (Histogram)
    plt.figure(figsize=(12, 6))
    sns.histplot(data=df, x='Age', hue='Medical_Condition', multiple='stack', bins=20)
    plt.title('Disease Distribution by Patient Age', fontsize=16)
    plt.xlabel('Age', fontsize=12)
    plt.ylabel('Number of Cases', fontsize=12)
    plt.savefig('visualizations/disease_age_distribution.png')
    print("Chart 2: 'disease_age_distribution.png' saved.")
    plt.close()
    
    # Chart 3: Disease Cases by Area (Bar Plot)
    plt.figure(figsize=(14, 8))
    sns.countplot(data=df, y='Area', hue='Medical_Condition', orient='h')
    plt.title('Disease Cases per Area', fontsize=16)
    plt.xlabel('Number of Cases', fontsize=12)
    plt.ylabel('Area', fontsize=12)
    plt.legend(title='Disease', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('visualizations/disease_by_area.png')
    print("Chart 3: 'disease_by_area.png' saved.")
    plt.close()
    
    # Chart 4: Cases of Top 5 Diseases by Area (Clustered Bar Chart)
    top_diseases = df['Medical_Condition'].value_counts().nlargest(5).index
    top_diseases_df = df[df['Medical_Condition'].isin(top_diseases)]

    plt.figure(figsize=(14, 8))
    sns.countplot(data=top_diseases_df, y='Area', hue='Medical_Condition', orient='h')
    plt.title('Top 5 Diseases by Area', fontsize=16)
    plt.xlabel('Number of Cases', fontsize=12)
    plt.ylabel('Area', fontsize=12)
    plt.legend(title='Disease', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('visualizations/top5_diseases_by_area.png')
    print("Chart 4: 'top5_diseases_by_area.png' saved.")
    plt.close()

# --- Main Script Execution ---
if __name__ == "__main__":
    file_name = 'dataset_with_random_year.csv'
    
    # Load and preprocess data
    preprocessed_df = load_and_prepare_data(file_name)
    
    if preprocessed_df is not None:
        # Train the AI model
        ai_model, label_encoder = train_model(preprocessed_df)
        
        # Run analysis and generate visualizations
        run_analysis(preprocessed_df, ai_model, label_encoder)
        
        print("\nAnalysis complete. Check the 'visualizations' folder for the generated graphs.")
