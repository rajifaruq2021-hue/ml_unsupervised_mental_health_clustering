"""
test_pipeline.py

Author: Raji Faruq Ishola
Matriculation: 4253139
Course: DLBDSMLUSL01 - Machine Learning: Unsupervised Learning and Feature Engineering
Task: Task 1 - Mental Health in Technology-related Jobs

Here I write automated unit tests using pytest to make sure my code is working properly.
Testing is an essential part of quality assurance in data science.
I test:
1. Gender cleaning: verifies that different spellings like 'm', 'cis male', and 'woman' are cleaned correctly.
2. Age bounding: verifies that joke ages like 3 or 323 are replaced with the realistic median.
3. Feature scaling: verifies that my scaled matrix has mean close to 0 and std close to 1.
4. Cluster profiles: verifies that all 3 personas are generated and sum to the full 1,433 participants.
"""

# I import the os and sys modules to set up folder paths for testing
import os
import sys

# I import pytest to run my test assertions
import pytest

# I import numpy and pandas to check numerical arrays and tables
import numpy as np
import pandas as pd

# I add the src folder to sys.path so pytest can easily import my classes
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), "src")
if src_dir not in sys.path:
    sys.path.append(src_dir)

# I import my classes from src
from eda_and_preprocessing import MentalHealthDataPreprocessor
from feature_engineering import MentalHealthFeatureEngineer


def test_gender_cleaning():
    """
    Here I test that my clean_gender function correctly standardizes free-text entries.
    """
    pre = MentalHealthDataPreprocessor("dummy", "dummy")
    
    # I check that male variants map to Male
    assert pre.clean_gender("male") == "Male"
    assert pre.clean_gender("M") == "Male"
    assert pre.clean_gender("Cis Male") == "Male"
    assert pre.clean_gender("dude") == "Male"
    
    # I check that female variants map to Female
    assert pre.clean_gender("female") == "Female"
    assert pre.clean_gender("woman") == "Female"
    assert pre.clean_gender("F") == "Female"
    
    # I check that diverse or non-binary entries map to Non-Binary/Other
    assert pre.clean_gender("non-binary") == "Non-Binary/Other"
    assert pre.clean_gender("Agender") == "Non-Binary/Other"


def test_age_outlier_removal():
    """
    Here I test that my clean_age function replaces unrealistic age outliers with the median.
    """
    pre = MentalHealthDataPreprocessor("dummy", "dummy")
    
    # I create a sample series with valid ages [25, 30, 35] and two extreme outliers [3, 323]
    ages = pd.Series([25, 30, 35, 3, 323])
    cleaned = pre.clean_age(ages)
    
    # I assert that all cleaned ages are now between 18 and 75
    assert cleaned.min() >= 18
    assert cleaned.max() <= 75
    
    # I assert that the outlier at index 3 was replaced with the median of [25, 30, 35] which is 30.0
    assert cleaned.iloc[3] == 30.0


def test_feature_scaling_properties():
    """
    Here I test that my scaled feature matrix has mean = 0 and std = 1 across all 26 dimensions.
    """
    base_dir = os.path.dirname(current_dir)
    scaled_csv = os.path.join(base_dir, "outputs", "scaled_features_matrix.csv")
    
    if os.path.exists(scaled_csv):
        df_scaled = pd.read_csv(scaled_csv)
        
        # I check that the table has all 1,433 rows and 26 engineered columns
        assert df_scaled.shape[0] == 1433
        assert df_scaled.shape[1] == 26
        
        # I verify that every column mean is very close to 0.0
        np.testing.assert_allclose(df_scaled.mean(), 0.0, atol=1e-2)
        
        # I verify that every column standard deviation is very close to 1.0
        np.testing.assert_allclose(df_scaled.std(), 1.0, atol=1e-2)


def test_cluster_profiles_generated():
    """
    Here I test that the final persona summary table has exactly 3 clusters
    and that their headcounts add up to 1,433 employees.
    """
    base_dir = os.path.dirname(current_dir)
    profile_csv = os.path.join(base_dir, "outputs", "tables", "cluster_summary_profiles.csv")
    
    if os.path.exists(profile_csv):
        df_prof = pd.read_csv(profile_csv)
        
        # I check that there are exactly 3 rows for the 3 clusters
        assert len(df_prof) == 3
        
        # I check that the sum of headcounts equals the total survey participants
        assert df_prof["Headcount"].sum() == 1433
