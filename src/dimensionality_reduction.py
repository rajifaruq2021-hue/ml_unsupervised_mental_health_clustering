"""
dimensionality_reduction.py

Author: Raji Faruq Ishola
Matriculation: 4253139
Course: DLBDSMLUSL01 - Machine Learning: Unsupervised Learning and Feature Engineering
Task: Task 1 - Mental Health in Technology-related Jobs

Here I reduce the 26 features down to 2 or 3 main dimensions so that I can easily
understand the patterns and draw simple 2D plots.
When data has 26 dimensions, humans cannot visualize it in a 3D or 2D world.
Dimensionality reduction solves this problem.

In this script:
1. I load the scaled 26-feature numbers from my previous step.
2. I run Principal Component Analysis (PCA):
   - I check how much variance each component captures.
   - I draw Figure 3 (Scree plot) to see where the curve bends.
   - I inspect what PC1 and PC2 actually mean (Factor Loadings in Figure 4).
     * PC1 represents company mental health support (benefits, open talk, leave).
     * PC2 represents personal mental health struggles (current illness, therapy, career fear).
3. I run t-SNE (t-Distributed Stochastic Neighbor Embedding):
   - This bends the high-dimensional space into a 2D map (Figure 5) so I can see natural clusters of people.
4. I save the new 2D coordinates so my clustering script can color them by persona!
"""

# I import the os module to handle file paths
import os

# I import numpy to do array math
import numpy as np

# I import pandas to work with tables
import pandas as pd

# I import matplotlib to draw charts
import matplotlib.pyplot as plt

# I import seaborn for nice visual styles
import seaborn as sns

# I import PCA and TSNE from scikit-learn
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


class MentalHealthDimensionalityReducer:
    """
    I created this class to run PCA and t-SNE on my survey features.
    It reduces 26 complicated dimensions into simple, readable 2D maps.
    """

    def __init__(self, scaled_data_path, output_dir):
        # I save the path to my scaled features table
        self.scaled_data_path = scaled_data_path
        
        # I save the folder paths for figures and tables
        self.output_dir = output_dir
        self.fig_dir = os.path.join(output_dir, "figures")
        self.tab_dir = os.path.join(output_dir, "tables")
        os.makedirs(self.fig_dir, exist_ok=True)
        os.makedirs(self.tab_dir, exist_ok=True)

        # I create empty variables to hold my models and projected numbers
        self.df_scaled = None
        self.pca_full = None
        self.pca_coords = None
        self.tsne_coords = None
        self.loadings_df = None

    def load_scaled_data(self):
        """
        Here I load the scaled feature matrix produced by my feature engineering step.
        """
        self.df_scaled = pd.read_csv(self.scaled_data_path)
        print(f"[INFO] I loaded scaled features matrix with shape: {self.df_scaled.shape}")
        return self.df_scaled

    def run_pca_full(self):
        """
        Here I run full PCA across all 26 dimensions.
        I want to find out how much information (variance) each principal component explains.
        """
        n_features = self.df_scaled.shape[1]
        
        # I initialize PCA with all 26 components and a fixed random state for reproducibility
        self.pca_full = PCA(n_components=n_features, random_state=42)
        
        # I fit PCA on my scaled numbers
        self.pca_full.fit(self.df_scaled)

        # I get the eigenvalues and percentage of variance explained by each component
        eigenvalues = self.pca_full.explained_variance_
        var_ratios = self.pca_full.explained_variance_ratio_ * 100
        cum_var = np.cumsum(var_ratios)

        # I create a neat summary table of all 26 components
        pca_summary = pd.DataFrame({
            "Principal Component": [f"PC{i+1}" for i in range(n_features)],
            "Eigenvalue": eigenvalues,
            "Explained Variance (%)": var_ratios,
            "Cumulative Variance (%)": cum_var
        })
        
        # I save this summary table to my tables folder
        summary_path = os.path.join(self.tab_dir, "pca_variance_explained.csv")
        pca_summary.to_csv(summary_path, index=False)
        print(f"[INFO] I saved PCA variance explained summary to: {summary_path}")

        # I count how many components have an eigenvalue of 1.0 or greater (Kaiser-Guttman rule)
        kaiser_components = np.sum(eigenvalues >= 1.0)
        
        # I find how many components I need to capture 70% and 80% of the total survey information
        comp_70 = np.argmax(cum_var >= 70.0) + 1
        comp_80 = np.argmax(cum_var >= 80.0) + 1
        
        print(f"[INFO] PCA Kaiser-Guttman criterion (eigenvalue >= 1.0): {kaiser_components} components.")
        print(f"[INFO] PCA components needed for 70% cumulative variance: {comp_70} components.")
        print(f"[INFO] PCA components needed for 80% cumulative variance: {comp_80} components.")

        return pca_summary

    def extract_loadings(self):
        """
        Here I calculate the factor loadings.
        Factor loadings tell me which original survey questions are most strongly connected
        to PC1 and PC2. This gives each component a clear, real-world human meaning!
        """
        # I calculate factor loadings by multiplying components by the square root of eigenvalues
        loadings = self.pca_full.components_.T * np.sqrt(self.pca_full.explained_variance_)
        
        # I store this in a dataframe where rows are questions and columns are PC1, PC2, etc.
        self.loadings_df = pd.DataFrame(
            loadings,
            index=self.df_scaled.columns,
            columns=[f"PC{i+1}" for i in range(self.df_scaled.shape[1])]
        )

        # I save the loadings table to CSV
        loadings_path = os.path.join(self.tab_dir, "pca_component_loadings.csv")
        self.loadings_df.to_csv(loadings_path)
        print(f"[INFO] I saved PCA factor loadings table to: {loadings_path}")
        
        return self.loadings_df

    def plot_pca_variance(self):
        """
        Here I draw Figure 3: A Scree Plot.
        It shows the bars for individual variance and a line for cumulative variance.
        """
        n_features = self.df_scaled.shape[1]
        var_ratios = self.pca_full.explained_variance_ratio_ * 100
        cum_var = np.cumsum(var_ratios)

        fig, ax1 = plt.subplots(figsize=(11, 6))

        # I plot the individual variance bars in blue
        bars = ax1.bar(range(1, n_features + 1), var_ratios, color="#2b5c8f", alpha=0.8,
                       label="Individual Explained Variance (%)")
        ax1.set_xlabel("Principal Component Index", fontsize=11, fontweight="bold")
        ax1.set_ylabel("Individual Explained Variance (%)", fontsize=11, color="#2b5c8f", fontweight="bold")
        ax1.set_xticks(range(1, n_features + 1))
        ax1.set_ylim(0, max(var_ratios) + 5)
        ax1.tick_params(axis="y", labelcolor="#2b5c8f")

        # I add a second y-axis on the right for cumulative variance in orange
        ax2 = ax1.twinx()
        line = ax2.plot(range(1, n_features + 1), cum_var, color="#d95f02", marker="o",
                        linewidth=2.5, label="Cumulative Explained Variance (%)")
        ax2.set_ylabel("Cumulative Explained Variance (%)", fontsize=11, color="#d95f02", fontweight="bold")
        ax2.set_ylim(0, 105)
        ax2.tick_params(axis="y", labelcolor="#d95f02")

        # I draw reference dashed lines at 70% and 80% marks
        ax2.axhline(70, color="gray", linestyle="--", alpha=0.7, label="70% Variance Threshold")
        ax2.axhline(80, color="darkgreen", linestyle=":", alpha=0.7, label="80% Variance Threshold")

        plt.title("Figure 3: Scree Plot and Cumulative Explained Variance across Principal Components",
                  fontsize=12, pad=14, fontweight="bold")

        # I combine the legends so they look clean in one box
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="center right", frameon=True)

        plt.tight_layout()
        
        # I save Figure 3 to disk
        fig3_path = os.path.join(self.fig_dir, "fig3_pca_explained_variance.png")
        plt.savefig(fig3_path, dpi=300)
        plt.close()
        print(f"[INFO] I saved Figure 3 to: {fig3_path}")

    def plot_pca_loadings(self):
        """
        Here I draw Figure 4: Horizontal bar charts showing which questions define PC1 and PC2.
        - PC1 is defined by company benefits, resources, and ease of leave.
        - PC2 is defined by current disorder, therapy sought, and fear of career harm.
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 7), sharey=False)

        # Plot for PC1
        pc1_loadings = self.loadings_df["PC1"].sort_values()
        top_pc1 = pd.concat([pc1_loadings.head(5), pc1_loadings.tail(5)])
        colors_pc1 = ["#d95f02" if x < 0 else "#2b5c8f" for x in top_pc1.values]
        axes[0].barh(top_pc1.index, top_pc1.values, color=colors_pc1)
        axes[0].set_title("(A) PC1 Loadings: Company Support & Openness vs. Freelance",
                          fontsize=11, fontweight="bold")
        axes[0].set_xlabel("Factor Loading on PC1", fontsize=10)
        axes[0].axvline(0, color="black", linestyle="--", linewidth=0.8)

        # Plot for PC2
        pc2_loadings = self.loadings_df["PC2"].sort_values()
        top_pc2 = pd.concat([pc2_loadings.head(5), pc2_loadings.tail(5)])
        colors_pc2 = ["#d95f02" if x < 0 else "#7570b3" for x in top_pc2.values]
        axes[1].barh(top_pc2.index, top_pc2.values, color=colors_pc2)
        axes[1].set_title("(B) PC2 Loadings: Personal Health Struggles & Stigma",
                          fontsize=11, fontweight="bold")
        axes[1].set_xlabel("Factor Loading on PC2", fontsize=10)
        axes[1].axvline(0, color="black", linestyle="--", linewidth=0.8)

        plt.suptitle("Figure 4: Dominant Survey Feature Factor Loadings for the First Two Principal Components",
                     fontsize=13, y=0.98)
        plt.tight_layout()
        
        # I save Figure 4
        fig4_path = os.path.join(self.fig_dir, "fig4_pca_feature_loadings.png")
        plt.savefig(fig4_path, dpi=300)
        plt.close()
        print(f"[INFO] I saved Figure 4 to: {fig4_path}")

    def run_tsne(self):
        """
        Here I run t-SNE to create a 2D non-linear map of all 1,433 survey respondents.
        t-SNE puts people who gave similar answers close together on the screen.
        """
        print("[INFO] I am computing 2D t-SNE coordinates for non-linear visualization.")
        
        # I configure t-SNE with perplexity 35 and 2 dimensions
        tsne = TSNE(n_components=2, perplexity=35, learning_rate="auto", init="pca", random_state=42)
        self.tsne_coords = tsne.fit_transform(self.df_scaled)

        # I draw the unclustered scatter plot (Figure 5)
        plt.figure(figsize=(9, 7))
        plt.scatter(self.tsne_coords[:, 0], self.tsne_coords[:, 1], c="#2b5c8f", alpha=0.6, s=25, edgecolors="none")
        plt.title("Figure 5: Unsupervised 2D Manifold Projection of Survey Respondents via t-SNE",
                  fontsize=12, pad=12, fontweight="bold")
        plt.xlabel("t-SNE Dimension 1", fontsize=11)
        plt.ylabel("t-SNE Dimension 2", fontsize=11)
        plt.tight_layout()
        
        # I save Figure 5
        fig5_path = os.path.join(self.fig_dir, "fig5_tsne_projection.png")
        plt.savefig(fig5_path, dpi=300)
        plt.close()
        print(f"[INFO] I saved Figure 5 to: {fig5_path}")

        return self.tsne_coords

    def export_transformed_coordinates(self):
        """
        Here I combine the top 5 PCA coordinates and 2 t-SNE coordinates into one clean table.
        This makes it very easy for my clustering script to visualize the clusters later.
        """
        # I transform the scaled data using the top 5 principal components
        pca_5 = PCA(n_components=5, random_state=42)
        pca_transformed = pca_5.fit_transform(self.df_scaled)

        # I build a DataFrame with PC1-PC5 and t-SNE Dim1-Dim2
        df_coords = pd.DataFrame({
            "PC1": pca_transformed[:, 0],
            "PC2": pca_transformed[:, 1],
            "PC3": pca_transformed[:, 2],
            "PC4": pca_transformed[:, 3],
            "PC5": pca_transformed[:, 4],
            "tSNE_Dim1": self.tsne_coords[:, 0],
            "tSNE_Dim2": self.tsne_coords[:, 1]
        }, index=self.df_scaled.index)

        # I save the combined coordinates to CSV
        coords_path = os.path.join(self.output_dir, "transformed_pca_tsne_coordinates.csv")
        df_coords.to_csv(coords_path, index=False)
        print(f"[INFO] I saved transformed PCA and t-SNE coordinates to: {coords_path}")
        
        return df_coords


# This allows me to test dimensionality reduction directly from my command prompt
if __name__ == "__main__":
    scaled_csv = r"D:\IU INTERNATIONAL UNIVERSITY\3 semester\Machine Learning - Unsupervised Learning and Feature Engineering (DLBDSMLUSL)\Case Study - Mental Health in Tech\outputs\scaled_features_matrix.csv"
    out_dir = r"D:\IU INTERNATIONAL UNIVERSITY\3 semester\Machine Learning - Unsupervised Learning and Feature Engineering (DLBDSMLUSL)\Case Study - Mental Health in Tech\outputs"

    reducer = MentalHealthDimensionalityReducer(scaled_csv, out_dir)
    reducer.load_scaled_data()
    reducer.run_pca_full()
    reducer.extract_loadings()
    reducer.plot_pca_variance()
    reducer.plot_pca_loadings()
    reducer.run_tsne()
    reducer.export_transformed_coordinates()
    
    print("[SUCCESS] I completed dimensionality reduction successfully.")
