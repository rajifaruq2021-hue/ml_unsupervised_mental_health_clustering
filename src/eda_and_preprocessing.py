"""
eda_and_preprocessing.py

Author: Raji Faruq Ishola
Matriculation: 4253139
Course: DLBDSMLUSL01 - Machine Learning: Unsupervised Learning and Feature Engineering
Task: Task 1 - Mental Health in Technology-related Jobs

Here I do all the initial data cleaning and exploratory data analysis.
When I first opened this survey dataset, it had 63 questions and a lot of messy answers.
Some people typed funny things for gender like 'dude' or 'unicorn'.
Some people put their age as 3 or 323 years old.
Also, there were many missing answers because self-employed people were not asked about company bosses.

In this script:
1. I load the raw CSV file.
2. I clean up the messy gender answers into 3 simple groups: Male, Female, and Non-Binary/Other.
3. I fix the crazy age numbers by using the normal middle age of 33 years.
4. I pick the 24 most important questions that matter for workplace mental health.
5. I fill in missing values so my machine learning code will not crash.
6. I draw and save neat graphs so my lecturer and HR can easily understand the survey.
"""

# I import the os module so I can join folder paths safely on my computer
import os

# I import re for regular expressions so I can search for words like 'man' or 'woman' in text
import re

# I import numpy to help me do simple math operations and handle arrays
import numpy as np

# I import pandas because it is my main tool for reading tables and working with columns
import pandas as pd

# I import matplotlib so I can draw plots and charts
import matplotlib.pyplot as plt

# I import seaborn to make my charts look colorful and clean
import seaborn as sns


class MentalHealthDataPreprocessor:
    """
    I created this class to hold all my data cleaning steps in one neat place.
    This makes it easy for me to run the whole process from start to finish.
    """

    def __init__(self, raw_data_path, output_dir):
        # I save the location of the raw CSV file that I downloaded
        self.raw_data_path = raw_data_path
        
        # I save the folder where I want to store all my results
        self.output_dir = output_dir
        
        # I create a folder for my figures so my graphs stay organized
        self.fig_dir = os.path.join(output_dir, "figures")
        
        # I create a folder for my summary tables
        self.tab_dir = os.path.join(output_dir, "tables")
        
        # I make sure these folders exist on my disk. If not, Python creates them for me
        os.makedirs(self.fig_dir, exist_ok=True)
        os.makedirs(self.tab_dir, exist_ok=True)
        
        # I set up empty variables to hold my raw table and my cleaned table
        self.df_raw = None
        self.df_clean = None

    def load_data(self):
        """
        Here I load the raw survey dataset from my CSV file.
        I also check how many rows and columns it has.
        """
        # I read the CSV file using pandas read_csv function
        self.df_raw = pd.read_csv(self.raw_data_path)
        
        # I print the size of the table so I know it loaded properly
        print(f"[INFO] I loaded raw dataset successfully with shape: {self.df_raw.shape}")
        
        # I return the table so other functions can use it if needed
        return self.df_raw

    def clean_gender(self, val):
        """
        Here I clean up the gender column.
        The survey let people type whatever they wanted, so there are over 70 different spellings.
        I group all of them into 3 clear categories:
        1. Male
        2. Female
        3. Non-Binary/Other
        """
        # If someone left the answer blank, I label it as Other
        if pd.isna(val):
            return "Other"
            
        # I turn the word into lowercase and remove extra spaces around it
        text = str(val).lower().strip()

        # These are patterns people used when they meant Male
        # For example: 'm', 'male', 'man', 'cis male', 'dude', 'guy'
        male_patterns = [
            r"^m$", r"^male", r"^man$", r"^cis male", r"^mail$", r"^cis man",
            r"^male \(cis\)", r"^dude", r"^guy", r"^masculine", r"^nb male"
        ]
        # I loop through each male pattern. If it matches, I return 'Male'
        for pattern in male_patterns:
            if re.search(pattern, text):
                return "Male"

        # These are patterns people used when they meant Female
        # For example: 'f', 'female', 'woman', 'cis female', 'fem'
        female_patterns = [
            r"^f$", r"^female", r"^woman$", r"^cis female", r"^cis woman",
            r"^female \(cis\)", r"^fem", r"^feminine"
        ]
        # I loop through each female pattern. If it matches, I return 'Female'
        for pattern in female_patterns:
            if re.search(pattern, text):
                return "Female"

        # If it is not standard male or female, like non-binary or agender, I call it Non-Binary/Other
        return "Non-Binary/Other"

    def clean_age(self, series):
        """
        Here I fix the age column.
        Some people made typing mistakes or entered joke numbers like 3 or 323.
        I find the normal middle age (median) of real working people between 18 and 75,
        and I replace any crazy numbers with that median.
        """
        # I make a fresh copy of the ages column so I do not mess up the original
        clean_ages = series.copy()
        
        # I find all the people whose age is between 18 and 75 years old
        valid_mask = (clean_ages >= 18) & (clean_ages <= 75)
        
        # I calculate the middle age (median) among these valid people
        median_age = clean_ages[valid_mask].median()
        
        # If someone's age is less than 18 or greater than 75, I give them this median age
        clean_ages[~valid_mask] = median_age
        
        # I print out what I did so I can see it in my terminal
        print(f"[INFO] I cleaned age outliers. Using median working age of {median_age:.0f} years.")
        
        # I return the cleaned ages
        return clean_ages

    def select_and_rename_features(self):
        """
        Here I select the most important questions from the survey.
        The full survey has 63 questions, but many are long free-text comments.
        I pick the 24 questions that directly answer what HR needs to know:
        - How old are they and what is their gender?
        - Do they work for a big or small company?
        - Does their company offer mental health benefits and help?
        - Are they afraid that asking for help will hurt their career?
        - Do they currently suffer from mental health challenges?
        """
        # I make a dictionary that maps long survey questions to short, easy names
        feature_mapping = {
            "What is your age?": "age",
            "What is your gender?": "gender_raw",
            "Are you self-employed?": "self_employed",
            "How many employees does your company or organization have?": "company_size",
            "Is your employer primarily a tech company/organization?": "is_tech_company",
            "Does your employer provide mental health benefits as part of healthcare coverage?": "benefits_provided",
            "Do you know the options for mental health care available under your employer-provided coverage?": "care_options_known",
            "Has your employer ever formally discussed mental health (for example, as part of a wellness campaign or other official communication)?": "formal_discussion",
            "Does your employer offer resources to learn more about mental health concerns and options for seeking help?": "resources_offered",
            "Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources provided by your employer?": "anonymity_protected",
            "If a mental health issue prompted you to request a medical leave from work, asking for that leave would be:": "leave_ease",
            "Do you think that discussing a mental health disorder with your employer would have negative consequences?": "stigma_employer",
            "Do you think that discussing a physical health issue with your employer would have negative consequences?": "stigma_physical",
            "Would you feel comfortable discussing a mental health disorder with your coworkers?": "comfort_coworkers",
            "Would you feel comfortable discussing a mental health disorder with your direct supervisor(s)?": "comfort_supervisor",
            "Do you feel that your employer takes mental health as seriously as physical health?": "seriousness_vs_physical",
            "Have you heard of or observed negative consequences for co-workers who have been open about mental health issues in your workplace?": "observed_negative_coworker",
            "Do you feel that being identified as a person with a mental health issue would hurt your career?": "perceived_career_harm",
            "Do you have a family history of mental illness?": "family_history",
            "Have you had a mental health disorder in the past?": "past_disorder",
            "Do you currently have a mental health disorder?": "current_disorder",
            "Have you ever sought treatment for a mental health issue from a mental health professional?": "treatment_sought",
            "If you have a mental health issue, do you feel that it interferes with your work when NOT being treated effectively?": "work_interference_untreated",
            "Do you work remotely?": "remote_work"
        }

        # I create a smaller table that only contains these 24 chosen columns
        df_sub = self.df_raw[list(feature_mapping.keys())].copy()
        
        # I rename the columns to my short, clean names
        df_sub.rename(columns=feature_mapping, inplace=True)

        # I clean the gender column using my clean_gender function
        df_sub["gender"] = df_sub["gender_raw"].apply(self.clean_gender)
        
        # I drop the old messy gender column now that I have a clean one
        df_sub.drop(columns=["gender_raw"], inplace=True)

        # I clean the age column using my clean_age function
        df_sub["age"] = self.clean_age(df_sub["age"])

        # I save this cleaned table into self.df_clean
        self.df_clean = df_sub
        
        # I print out how many rows and columns I have now
        print(f"[INFO] I extracted and cleaned {self.df_clean.shape[1]} core features across {self.df_clean.shape[0]} respondents.")
        
        return self.df_clean

    def handle_missing_values(self):
        """
        Here I deal with empty or missing answers.
        In this survey, self-employed people were not asked company questions.
        Instead of throwing away their rows, I fill those blanks with 'Not applicable / Don't know'.
        Also, if someone does not have a mental health condition, they did not answer about
        work interference, so I fill that with 'Not applicable'.
        This way, I keep all 1,433 respondents and don't lose any data!
        """
        df = self.df_clean.copy()

        # These are all the questions about company policies that self-employed people skipped
        policy_cols = [
            "company_size", "is_tech_company", "benefits_provided", "care_options_known",
            "formal_discussion", "resources_offered", "anonymity_protected", "leave_ease",
            "stigma_employer", "stigma_physical", "comfort_coworkers", "comfort_supervisor",
            "seriousness_vs_physical", "observed_negative_coworker"
        ]
        # I loop through each policy question and fill any missing values
        for col in policy_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna("Not applicable / Don't know")

        # For work interference when untreated, I fill missing values with 'Not applicable to me'
        df["work_interference_untreated"] = df["work_interference_untreated"].fillna("Not applicable to me")

        # I save the completed table back
        self.df_clean = df
        
        # I print the count of missing values to prove that zero missing values remain
        print(f"[INFO] I handled missing values. Remaining missing count: {self.df_clean.isnull().sum().sum()}")
        
        return self.df_clean

    def generate_eda_visualizations(self):
        """
        Here I draw two beautiful charts to show what the raw data looks like:
        - Figure 1: Which survey questions had the most missing answers.
        - Figure 2: The ages, genders, company sizes, and health status of participants.
        """
        # I use a clean white background with gridlines for my charts
        sns.set_theme(style="whitegrid", font="sans-serif")

        # FIGURE 1: Bar chart of missing answers
        plt.figure(figsize=(10, 6))
        
        # I compute the percentage of missing values for every question and pick the top 15
        raw_missing = (self.df_raw.isnull().sum() / len(self.df_raw) * 100).sort_values(ascending=False)[:15]
        
        # I plot the horizontal bar chart
        ax = sns.barplot(x=raw_missing.values, y=raw_missing.index, hue=raw_missing.index, palette="Blues_r", legend=False)
        plt.title("Figure 1: Top 15 Survey Features with Highest Proportion of Missing Responses", fontsize=12, pad=12)
        plt.xlabel("Missing Responses (%)", fontsize=11)
        plt.ylabel("Survey Feature", fontsize=11)
        
        # I write the exact percentage on the end of each bar so it is easy to read
        for p in ax.patches:
            width = p.get_width()
            ax.annotate(f"{width:.1f}%", (width + 1.0, p.get_y() + p.get_height() / 2.),
                        ha="left", va="center", fontsize=9, color="black")
                        
        plt.xlim(0, 105)
        plt.tight_layout()
        
        # I save the picture to my figures folder
        fig1_path = os.path.join(self.fig_dir, "fig1_missing_values.png")
        plt.savefig(fig1_path, dpi=300)
        plt.close()
        print(f"[INFO] I saved Figure 1 to: {fig1_path}")

        # FIGURE 2: 4-panel grid showing participant demographics
        fig, axes = plt.subplots(2, 2, figsize=(13, 10))

        # Chart A: Histogram of ages
        sns.histplot(self.df_clean["age"], bins=25, kde=True, ax=axes[0, 0], color="#2b5c8f")
        axes[0, 0].set_title("(A) Age Distribution of Survey Participants", fontsize=11, fontweight="bold")
        axes[0, 0].set_xlabel("Age (Years)", fontsize=10)
        axes[0, 0].set_ylabel("Count", fontsize=10)

        # Chart B: Pie chart of genders
        gender_counts = self.df_clean["gender"].value_counts()
        axes[0, 1].pie(gender_counts.values, labels=gender_counts.index, autopct="%1.1f%%",
                       colors=["#2b5c8f", "#d95f02", "#7570b3"], startangle=140,
                       textprops={"fontsize": 10})
        axes[0, 1].set_title("(B) Standardized Gender Identification", fontsize=11, fontweight="bold")

        # Chart C: Count of company sizes
        size_order = ["1-5", "6-25", "26-100", "100-500", "500-1000", "More than 1000", "Not applicable / Don't know"]
        present_order = [s for s in size_order if s in self.df_clean["company_size"].unique()]
        sns.countplot(data=self.df_clean, y="company_size", order=present_order, ax=axes[1, 0], hue="company_size", palette="crest", legend=False)
        axes[1, 0].set_title("(C) Employer Organization Size", fontsize=11, fontweight="bold")
        axes[1, 0].set_xlabel("Count", fontsize=10)
        axes[1, 0].set_ylabel("Organization Size", fontsize=10)

        # Chart D: Current mental health condition
        sns.countplot(data=self.df_clean, x="current_disorder", ax=axes[1, 1], hue="current_disorder", palette="Set2", legend=False)
        axes[1, 1].set_title("(D) Self-Reported Current Mental Health Disorder", fontsize=11, fontweight="bold")
        axes[1, 1].set_xlabel("Current Disorder Status", fontsize=10)
        axes[1, 1].set_ylabel("Count", fontsize=10)

        # I add a clear main title above the 4 charts
        plt.suptitle("Figure 2: Demographic and Organizational Characteristics of Survey Participants", fontsize=13, y=0.99)
        plt.tight_layout()
        
        # I save the 4-panel image to my figures folder
        fig2_path = os.path.join(self.fig_dir, "fig2_demographics_eda.png")
        plt.savefig(fig2_path, dpi=300)
        plt.close()
        print(f"[INFO] I saved Figure 2 to: {fig2_path}")

    def save_clean_data(self):
        """
        Here I save my cleaned data to a CSV file so that my next script
        (feature engineering) can load it right away.
        """
        clean_path = os.path.join(self.output_dir, "clean_mental_health_data.csv")
        self.df_clean.to_csv(clean_path, index=False)
        print(f"[INFO] I saved the cleaned dataset to: {clean_path}")
        return clean_path


# This block lets me run this file directly from my terminal
if __name__ == "__main__":
    # I set the path to where my raw data is stored
    raw_path = r"D:\IU INTERNATIONAL UNIVERSITY\3 semester\Machine Learning - Unsupervised Learning and Feature Engineering (DLBDSMLUSL)\Case Study - Mental Health in Tech\data\mental-heath-in-tech-2016_20161114.csv"
    
    # I set the path to where my outputs should go
    out_dir = r"D:\IU INTERNATIONAL UNIVERSITY\3 semester\Machine Learning - Unsupervised Learning and Feature Engineering (DLBDSMLUSL)\Case Study - Mental Health in Tech\outputs"

    # I create my preprocessor object and run each step one after the other
    preprocessor = MentalHealthDataPreprocessor(raw_path, out_dir)
    preprocessor.load_data()
    preprocessor.select_and_rename_features()
    preprocessor.handle_missing_values()
    preprocessor.generate_eda_visualizations()
    preprocessor.save_clean_data()
    
    print("[SUCCESS] I completed exploratory data analysis and preprocessing successfully.")
