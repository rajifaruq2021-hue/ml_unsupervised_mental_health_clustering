"""
feature_engineering.py

Author: Raji Faruq Ishola
Matriculation: 4253139
Course: DLBDSMLUSL01 - Machine Learning: Unsupervised Learning and Feature Engineering
Task: Task 1 - Mental Health in Technology-related Jobs

Here I turn all the survey words and text answers into real numbers.
Computers and machine learning algorithms cannot do math on words like 'Yes', 'No', or 'Very easy'.
They need clean numbers.

In this script:
1. I load the cleaned survey data from my previous step.
2. I turn ordered answers into numbers that respect their rank:
   - For example, company sizes from small to big: 1-5 is 1, up to more than 1000 which is 6.
   - For ease of medical leave: Very difficult is 1, Very easy is 5.
3. I turn Yes/No/Unsure questions into 0.0, 0.5, and 1.0.
4. I use One-Hot Encoding for words with no order like gender and remote work habits.
5. I scale all numbers using StandardScaler so that no single feature dominates just because its numbers are bigger.
6. I save the finished numbers table into a CSV file ready for PCA and Clustering!
"""

# I import the os module to handle file paths properly
import os

# I import numpy to perform numerical calculations and array operations
import numpy as np

# I import pandas to work with dataframes and manipulate columns
import pandas as pd

# I import StandardScaler from scikit-learn to normalize my numbers to mean 0 and standard deviation 1
from sklearn.preprocessing import StandardScaler


class MentalHealthFeatureEngineer:
    """
    I designed this class to take my cleaned survey data and engineer all the numerical
    features that my machine learning algorithms need.
    """

    def __init__(self, clean_data_path, output_dir):
        # I store the path to the cleaned CSV file that I saved earlier
        self.clean_data_path = clean_data_path
        
        # I store the output folder where I will save my feature tables
        self.output_dir = output_dir
        
        # I create a tables folder so everything stays neatly organized
        self.tab_dir = os.path.join(output_dir, "tables")
        os.makedirs(self.tab_dir, exist_ok=True)
        
        # I set up placeholders for my cleaned table, engineered features, and scaled matrix
        self.df_clean = None
        self.df_features = None
        self.scaled_matrix = None
        
        # I initialize the StandardScaler tool from scikit-learn
        self.scaler = StandardScaler()
        
        # I create an empty list to keep track of all my feature names
        self.feature_names = []

    def load_clean_data(self):
        """
        Here I load the cleaned dataset that I created in eda_and_preprocessing.py.
        """
        # I read the cleaned CSV file into a pandas DataFrame
        self.df_clean = pd.read_csv(self.clean_data_path)
        
        # I print the dimensions so I can confirm all rows are present
        print(f"[INFO] I loaded cleaned data with shape: {self.df_clean.shape}")
        
        return self.df_clean

    def encode_ordinal_and_binary_features(self):
        """
        Here I convert every survey question into numbers.
        I pay careful attention to whether answers have an order (like small to big)
        or if they are simple Yes/No questions.
        """
        # I work on a fresh copy of the table
        df = self.df_clean.copy()
        
        # I make a new empty dataframe that will store only my engineered numbers
        feat = pd.DataFrame(index=df.index)

        # 1. AGE: This is already a number, so I simply make sure it is a float
        feat["age"] = df["age"].astype(float)

        # 2. COMPANY SIZE: Has a natural order from small teams to huge corporations
        # I map: Not applicable/Don't know -> 0, 1-5 -> 1, 6-25 -> 2, 26-100 -> 3, 100-500 -> 4, 500-1000 -> 5, >1000 -> 6
        size_map = {
            "Not applicable / Don't know": 0.0,
            "1-5": 1.0,
            "6-25": 2.0,
            "26-100": 3.0,
            "100-500": 4.0,
            "500-1000": 5.0,
            "More than 1000": 6.0
        }
        feat["company_size_ord"] = df["company_size"].map(size_map).fillna(0.0).astype(float)

        # 3. MEDICAL LEAVE EASE: Ranges from Very difficult (1) to Very easy (5)
        # If someone doesn't know, I give them the neutral middle score of 3.0
        leave_map = {
            "Very difficult": 1.0,
            "Somewhat difficult": 2.0,
            "Neither easy nor difficult": 3.0,
            "Not applicable / Don't know": 3.0,
            "I don't know": 3.0,
            "Somewhat easy": 4.0,
            "Very easy": 5.0
        }
        feat["leave_ease_ord"] = df["leave_ease"].map(leave_map).fillna(3.0).astype(float)

        # 4. WORK INTERFERENCE UNTREATED: Ranges from Never (0) to Often (3)
        interfere_map = {
            "Not applicable": 0.0,
            "Not applicable to me": 0.0,
            "Never": 0.0,
            "Rarely": 1.0,
            "Sometimes": 2.0,
            "Often": 3.0
        }
        feat["work_interference_ord"] = df["work_interference_untreated"].map(interfere_map).fillna(0.0).astype(float)

        # 5. CAREER DAMAGE PERCEPTION: Are they afraid having mental health issues will hurt their career?
        # No -> 0.0, Maybe -> 1.0, Yes -> 2.0
        career_map = {
            "No, I don't think it would": 0.0,
            "No, it has not": 0.0,
            "No": 0.0,
            "Maybe": 1.0,
            "Yes, I think it would": 2.0,
            "Yes, it has": 2.0,
            "Yes": 2.0
        }
        feat["career_damage_ord"] = df["perceived_career_harm"].map(career_map).fillna(1.0).astype(float)

        # 6. COMPANY BENEFITS & POLICY AWARENESS:
        # I map: No -> 0.0, Unsure/Don't know -> 0.5, Yes -> 1.0
        tri_map = {
            "No": 0.0,
            "Not eligible": 0.0,
            "Not eligible for coverage / N/A": 0.0,
            "I don't know": 0.5,
            "I am not sure": 0.5,
            "Not applicable / Don't know": 0.5,
            "Maybe": 0.5,
            "Yes": 1.0
        }
        feat["benefits_provided_num"] = df["benefits_provided"].map(tri_map).fillna(0.5).astype(float)
        feat["care_options_known_num"] = df["care_options_known"].map(tri_map).fillna(0.5).astype(float)
        feat["formal_discussion_num"] = df["formal_discussion"].map(tri_map).fillna(0.5).astype(float)
        feat["resources_offered_num"] = df["resources_offered"].map(tri_map).fillna(0.5).astype(float)
        feat["anonymity_protected_num"] = df["anonymity_protected"].map(tri_map).fillna(0.5).astype(float)

        # 7. STIGMA & WORKPLACE COMFORT:
        # How comfortable they feel talking to coworkers and supervisors
        feat["stigma_employer_num"] = df["stigma_employer"].map(tri_map).fillna(0.5).astype(float)
        feat["stigma_physical_num"] = df["stigma_physical"].map(tri_map).fillna(0.5).astype(float)
        feat["comfort_coworkers_num"] = df["comfort_coworkers"].map(tri_map).fillna(0.5).astype(float)
        feat["comfort_supervisor_num"] = df["comfort_supervisor"].map(tri_map).fillna(0.5).astype(float)
        feat["seriousness_physical_num"] = df["seriousness_vs_physical"].map(tri_map).fillna(0.5).astype(float)

        # 8. OBSERVED NEGATIVE CONSEQUENCES FOR COWORKERS:
        # Have they seen coworkers get treated badly when being open about mental health?
        feat["observed_negative_coworker_num"] = df["observed_negative_coworker"].apply(
            lambda x: 1.0 if str(x).strip().lower() == "yes" else 0.0
        )

        # 9. PERSONAL MENTAL HEALTH PROFILE:
        # Family history, past struggles, current struggles, and seeking professional therapy
        feat["family_history_num"] = df["family_history"].map(tri_map).fillna(0.5).astype(float)
        feat["past_disorder_num"] = df["past_disorder"].map(tri_map).fillna(0.5).astype(float)
        feat["current_disorder_num"] = df["current_disorder"].map(tri_map).fillna(0.5).astype(float)
        feat["treatment_sought_num"] = df["treatment_sought"].astype(float)

        # 10. EMPLOYMENT STATUS & TECH ROLE:
        feat["self_employed_num"] = df["self_employed"].astype(float)
        feat["is_tech_company_num"] = df["is_tech_company"].apply(
            lambda x: 1.0 if str(x).strip() in ["1.0", "1", "Yes"] else 0.0
        )

        # 11. ONE-HOT ENCODING FOR CATEGORICAL WORDS:
        # For Gender: I create an indicator for Female and an indicator for Non-Binary/Other (leaving Male as baseline)
        feat["gender_female"] = (df["gender"] == "Female").astype(float)
        feat["gender_nonbinary_other"] = (df["gender"].isin(["Non-Binary/Other", "Other"])).astype(float)

        # For Remote Work: I create indicators for Sometimes and Always (leaving Never as baseline)
        feat["remote_sometimes"] = (df["remote_work"] == "Sometimes").astype(float)
        feat["remote_always"] = (df["remote_work"] == "Always").astype(float)

        # I save the engineered features table
        self.df_features = feat
        self.feature_names = list(feat.columns)
        
        # I print out the count of engineered features
        print(f"[INFO] I engineered {len(self.feature_names)} numerical features from survey responses.")
        
        return self.df_features

    def scale_features(self):
        """
        Here I scale all my numbers using StandardScaler (z-score normalization).
        This is super important because:
        - Age is around 30 to 50.
        - Binary answers are 0 or 1.
        Without scaling, the algorithm would think age is 40 times more important than benefits!
        Scaling puts every single feature on a level playing field with mean = 0 and std = 1.
        """
        # I fit the scaler and transform my numbers
        self.scaled_matrix = self.scaler.fit_transform(self.df_features)

        # I turn the scaled matrix back into a nice pandas table with the proper column headers
        df_scaled = pd.DataFrame(self.scaled_matrix, columns=self.feature_names, index=self.df_features.index)

        # I save a summary table of the scaled numbers into my tables folder
        summary_path = os.path.join(self.tab_dir, "feature_engineering_summary.csv")
        df_scaled.describe().T[["mean", "std", "min", "25%", "50%", "75%", "max"]].to_csv(summary_path)
        print(f"[INFO] I saved feature scaling summary table to: {summary_path}")

        # I save the full scaled matrix to CSV so my PCA and clustering scripts can load it
        scaled_csv_path = os.path.join(self.output_dir, "scaled_features_matrix.csv")
        df_scaled.to_csv(scaled_csv_path, index=False)
        print(f"[INFO] I saved scaled feature matrix to: {scaled_csv_path}")

        return self.scaled_matrix, df_scaled


# This lets me run this file directly to test my feature engineering logic
if __name__ == "__main__":
    clean_csv = r"D:\IU INTERNATIONAL UNIVERSITY\3 semester\Machine Learning - Unsupervised Learning and Feature Engineering (DLBDSMLUSL)\Case Study - Mental Health in Tech\outputs\clean_mental_health_data.csv"
    out_dir = r"D:\IU INTERNATIONAL UNIVERSITY\3 semester\Machine Learning - Unsupervised Learning and Feature Engineering (DLBDSMLUSL)\Case Study - Mental Health in Tech\outputs"

    engineer = MentalHealthFeatureEngineer(clean_csv, out_dir)
    engineer.load_clean_data()
    engineer.encode_ordinal_and_binary_features()
    scaled_mat, df_sc = engineer.scale_features()
    
    print(f"[SUCCESS] I completed feature engineering successfully with scaled shape: {scaled_mat.shape}")
