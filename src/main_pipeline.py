"""
main_pipeline.py

Author: Raji Faruq Ishola
Matriculation: 4253139
Course: DLBDSMLUSL01 - Machine Learning: Unsupervised Learning and Feature Engineering
Task: Task 1 - Mental Health in Technology-related Jobs

Here I run the whole project from start to finish with one single command!
I import all my modular Python files that I built:
1. eda_and_preprocessing: cleans raw text and handles missing answers.
2. feature_engineering: turns survey answers into scaled numbers.
3. dimensionality_reduction: runs PCA and t-SNE for 2D maps.
4. clustering_and_profiling: runs K-Means, validates with Ward's method, and profiles personas.

Whenever someone runs this file, it executes every step cleanly, prints progress,
and saves all 10 figures and summary tables into the outputs/ folder.
"""

# I import os and sys so I can add my src folder to Python's module search path
import os
import sys

# I import time so I can measure exactly how many seconds the whole pipeline takes
import time

# I get the folder where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# If current_dir is not in sys.path, I add it so my other modules import cleanly
if current_dir not in sys.path:
    sys.path.append(current_dir)

# I import each of my custom classes from their separate files
from eda_and_preprocessing import MentalHealthDataPreprocessor
from feature_engineering import MentalHealthFeatureEngineer
from dimensionality_reduction import MentalHealthDimensionalityReducer
from clustering_and_profiling import MentalHealthClusterer


def run_full_pipeline():
    """
    Here I run the complete data science workflow in 4 clear, logical steps.
    """
    # I start my stopwatch
    start_time = time.time()
    
    print("=" * 75)
    print("IU INTERNATIONAL UNIVERSITY - DLBDSMLUSL01 CASE STUDY PIPELINE")
    print("Student: Raji Faruq Ishola (Matriculation: 4253139)")
    print("Task: Mental Health in Technology-related Jobs (OSMI 2016 Survey)")
    print("=" * 75)

    # I set up file paths to my data and output folders
    base_dir = os.path.dirname(current_dir)
    raw_csv = os.path.join(base_dir, "data", "mental-heath-in-tech-2016_20161114.csv")
    out_dir = os.path.join(base_dir, "outputs")
    clean_csv = os.path.join(out_dir, "clean_mental_health_data.csv")
    scaled_csv = os.path.join(out_dir, "scaled_features_matrix.csv")
    coords_csv = os.path.join(out_dir, "transformed_pca_tsne_coordinates.csv")

    # STEP 1: I clean the data and inspect missing values
    print("\n>>> STEP 1: I execute Exploratory Data Analysis and Preprocessing.")
    preprocessor = MentalHealthDataPreprocessor(raw_csv, out_dir)
    preprocessor.load_data()
    preprocessor.select_and_rename_features()
    preprocessor.handle_missing_values()
    preprocessor.generate_eda_visualizations()
    preprocessor.save_clean_data()

    # STEP 2: I engineer features and apply standard scaling
    print("\n>>> STEP 2: I execute Feature Engineering and Scaling.")
    engineer = MentalHealthFeatureEngineer(clean_csv, out_dir)
    engineer.load_clean_data()
    engineer.encode_ordinal_and_binary_features()
    engineer.scale_features()

    # STEP 3: I reduce dimensions using PCA and t-SNE
    print("\n>>> STEP 3: I execute Dimensionality Reduction (PCA and t-SNE).")
    reducer = MentalHealthDimensionalityReducer(scaled_csv, out_dir)
    reducer.load_scaled_data()
    reducer.run_pca_full()
    reducer.extract_loadings()
    reducer.plot_pca_variance()
    reducer.plot_pca_loadings()
    reducer.run_tsne()
    reducer.export_transformed_coordinates()

    # STEP 4: I run K-Means, hierarchical clustering, and profile HR personas
    print("\n>>> STEP 4: I execute Clustering, Evaluation, and Persona Profiling.")
    clusterer = MentalHealthClusterer(scaled_csv, coords_csv, clean_csv, out_dir)
    clusterer.load_data()
    clusterer.evaluate_cluster_numbers()
    clusterer.fit_kmeans(k=3)
    clusterer.fit_hierarchical_and_dendrogram()
    clusterer.plot_clusters_in_reduced_space()
    clusterer.profile_personas()

    # I stop the timer and report total execution time
    elapsed = time.time() - start_time
    print("\n" + "=" * 75)
    print(f"[SUCCESS] I completed the entire pipeline in {elapsed:.1f} seconds.")
    print("All 10 academic figures and tabular reports are saved in outputs/.")
    print("=" * 75)


# This runs the pipeline when I type 'python main_pipeline.py'
if __name__ == "__main__":
    run_full_pipeline()
