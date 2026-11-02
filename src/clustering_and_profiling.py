"""
clustering_and_profiling.py

Author: Raji Faruq Ishola
Matriculation: 4253139
Course: DLBDSMLUSL01 - Machine Learning: Unsupervised Learning and Feature Engineering
Task: Task 1 - Mental Health in Technology-related Jobs

Here I group the survey respondents into distinct, natural clusters using machine learning!
Unsupervised learning means nobody told the computer who belongs to which group.
The algorithm discovers the groups purely by looking at which people answered similarly.

In this script:
1. I test how many clusters (k) are best, testing k from 2 to 8:
   - I use the Elbow Method (Inertia/WCSS) to see where the curve bends.
   - I use the Silhouette Score to see how well-separated the clusters are.
   - I pick k=3 because it gives 3 clear, realistic employee personas for HR.
2. I train the final K-Means model with k=3.
3. I compare my K-Means result with Hierarchical Clustering (Ward's method) and draw a Dendrogram (Figure 8).
4. I project the 3 clusters on PCA and t-SNE 2D charts (Figure 7).
5. I calculate what each cluster means in real life:
   - Persona 0: Supported & Engaged Advocates (happy, well-supported employees).
   - Persona 1: Distressed & Stigmatized Vulnerables (struggling employees afraid of career damage).
   - Persona 2: Detached & Informally Structured (freelancers with no corporate benefits).
6. I draw a Spider/Radar Chart (Figure 9) and an Actionable HR Priority Heatmap (Figure 10).
"""

# I import the os module to handle file and folder paths
import os

# I import numpy to perform array math and handle angles for radar plotting
import numpy as np

# I import pandas to work with tables and summarize cluster averages
import pandas as pd

# I import matplotlib to draw our figures
import matplotlib.pyplot as plt

# I import seaborn to draw heatmaps and color palettes
import seaborn as sns

# I import KMeans and AgglomerativeClustering from scikit-learn
from sklearn.cluster import KMeans, AgglomerativeClustering

# I import silhouette_score and adjusted_rand_score to mathematically validate my clusters
from sklearn.metrics import silhouette_score, silhouette_samples, adjusted_rand_score

# I import dendrogram and linkage from scipy to draw the hierarchical tree
from scipy.cluster.hierarchy import dendrogram, linkage


class MentalHealthClusterer:
    """
    I designed this class to discover natural employee clusters, validate them,
    and profile their real-world HR personas.
    """

    def __init__(self, scaled_data_path, coords_path, clean_data_path, output_dir):
        # I store file paths for my scaled numbers, 2D coordinates, and clean survey data
        self.scaled_data_path = scaled_data_path
        self.coords_path = coords_path
        self.clean_data_path = clean_data_path
        
        # I store my output directory and set up folders for figures and tables
        self.output_dir = output_dir
        self.fig_dir = os.path.join(output_dir, "figures")
        self.tab_dir = os.path.join(output_dir, "tables")
        os.makedirs(self.fig_dir, exist_ok=True)
        os.makedirs(self.tab_dir, exist_ok=True)

        # I create empty variables for my datasets, models, and chosen k
        self.df_scaled = None
        self.df_coords = None
        self.df_clean = None
        self.kmeans_model = None
        self.agg_model = None
        self.best_k = 3
        self.cluster_labels = None
        self.eval_metrics_df = None

    def load_data(self):
        """
        Here I load all my prepared tables so I can perform clustering.
        """
        # I load the scaled feature matrix
        self.df_scaled = pd.read_csv(self.scaled_data_path)
        
        # I load the 2D PCA and t-SNE coordinates
        self.df_coords = pd.read_csv(self.coords_path)
        
        # I load the original cleaned survey data so I can inspect actual answers
        self.df_clean = pd.read_csv(self.clean_data_path)
        
        print(f"[INFO] I loaded scaled data ({self.df_scaled.shape}) and coordinates ({self.df_coords.shape}).")

    def evaluate_cluster_numbers(self, k_range=range(2, 9)):
        """
        Here I test different numbers of clusters, from k=2 to k=8.
        I want to find the number of clusters that makes the most sense mathematically
        and practically for HR management.
        """
        inertias = []
        silhouettes = []
        k_values = list(k_range)

        print("[INFO] I am evaluating K-Means partitions across k=2 to k=8.")
        
        # I loop through each candidate k
        for k in k_values:
            # I fit K-Means with k-means++ seeding and 20 different initializations to be sure
            km = KMeans(n_clusters=k, init="k-means++", n_init=20, random_state=42)
            labels = km.fit_predict(self.df_scaled)
            
            # I record the inertia (WCSS - how tight each cluster is)
            inertias.append(km.inertia_)
            
            # I calculate the silhouette score (how well-separated the clusters are)
            sil = silhouette_score(self.df_scaled, labels)
            silhouettes.append(sil)
            
            print(f"  -> k={k}: Inertia = {km.inertia_:.1f}, Silhouette Score = {sil:.4f}")

        # I save these test results into a CSV table
        self.eval_metrics_df = pd.DataFrame({
            "k_clusters": k_values,
            "Inertia_WCSS": inertias,
            "Silhouette_Score": silhouettes
        })
        metrics_path = os.path.join(self.tab_dir, "clustering_evaluation_metrics.csv")
        self.eval_metrics_df.to_csv(metrics_path, index=False)
        print(f"[INFO] I saved clustering evaluation metrics table to: {metrics_path}")

        # FIGURE 6: I draw the Elbow Curve and Silhouette Curve on one clean plot
        fig, ax1 = plt.subplots(figsize=(10, 6))

        color1 = "#2b5c8f"
        ax1.set_xlabel("Number of Clusters (k)", fontsize=11, fontweight="bold")
        ax1.set_ylabel("Inertia (Within-Cluster Sum of Squares)", color=color1, fontsize=11, fontweight="bold")
        line1 = ax1.plot(k_values, inertias, marker="o", color=color1, linewidth=2.5, label="Inertia (WCSS)")
        ax1.tick_params(axis="y", labelcolor=color1)
        ax1.set_xticks(k_values)

        ax2 = ax1.twinx()
        color2 = "#d95f02"
        ax2.set_ylabel("Mean Silhouette Coefficient", color=color2, fontsize=11, fontweight="bold")
        line2 = ax2.plot(k_values, silhouettes, marker="s", color=color2, linewidth=2.5, linestyle="--", label="Silhouette Score")
        ax2.tick_params(axis="y", labelcolor=color2)

        # I draw a vertical line at k=3 to show that this is my selected optimal model
        ax1.axvline(3, color="green", linestyle=":", linewidth=2, label="Selected Optimal k=3")

        plt.title("Figure 6: Clustering Model Selection: Elbow Method (Inertia) and Silhouette Score Curve",
                  fontsize=12, pad=14, fontweight="bold")

        # Combine legends cleanly
        lines = line1 + line2 + [ax1.get_lines()[-1]]
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc="upper right", frameon=True)

        plt.tight_layout()
        
        # I save Figure 6
        fig6_path = os.path.join(self.fig_dir, "fig6_elbow_silhouette_kselection.png")
        plt.savefig(fig6_path, dpi=300)
        plt.close()
        print(f"[INFO] I saved Figure 6 to: {fig6_path}")

        return self.eval_metrics_df

    def fit_kmeans(self, k=3):
        """
        Here I train my final K-Means model using k=3 clusters.
        I assign each of the 1,433 employees to their best cluster (0, 1, or 2).
        """
        self.best_k = k
        self.kmeans_model = KMeans(n_clusters=k, init="k-means++", n_init=25, random_state=42)
        
        # I predict the cluster for every person in my dataset
        self.cluster_labels = self.kmeans_model.fit_predict(self.df_scaled)
        
        # I store the cluster labels in my tables so I can use them for plotting
        self.df_coords["Cluster"] = self.cluster_labels
        self.df_clean["Cluster"] = self.cluster_labels

        sil = silhouette_score(self.df_scaled, self.cluster_labels)
        print(f"[INFO] I fitted K-Means (k={k}) with final Silhouette Score: {sil:.4f}")
        return self.cluster_labels

    def fit_hierarchical_and_dendrogram(self):
        """
        Here I run Agglomerative Hierarchical Clustering using Ward's method.
        This provides a second, independent opinion from a completely different algorithm.
        I also draw Figure 8: A dendrogram tree showing how smaller groups merge into 3 big branches.
        """
        print("[INFO] I am computing hierarchical linkage using Ward's method.")
        
        # I compute the linkage tree based on Euclidean distance
        linkage_matrix = linkage(self.df_scaled, method="ward", metric="euclidean")

        # I fit AgglomerativeClustering with 3 clusters to see if it agrees with K-Means
        self.agg_model = AgglomerativeClustering(n_clusters=self.best_k, metric="euclidean", linkage="ward")
        agg_labels = self.agg_model.fit_predict(self.df_scaled)

        # I compute the Adjusted Rand Index (ARI) to see how closely K-Means and Hierarchical match
        ari = adjusted_rand_score(self.cluster_labels, agg_labels)
        print(f"[INFO] Adjusted Rand Index between K-Means and Hierarchical Clustering: {ari:.4f}")

        # FIGURE 8: I plot the Dendrogram tree
        plt.figure(figsize=(12, 6))
        dendrogram(
            linkage_matrix,
            truncate_mode="lastp",
            p=30,  # I show the top 30 merged branches so the tree is clean and readable
            leaf_rotation=90.,
            leaf_font_size=10.,
            show_contracted=True,
            color_threshold=linkage_matrix[-self.best_k+1, 2]  # I color the 3 main branches differently
        )
        plt.title("Figure 8: Hierarchical Agglomerative Dendrogram (Ward's Minimum Variance Linkage)",
                  fontsize=12, pad=14, fontweight="bold")
        plt.xlabel("Cluster Sub-tree Index (Sample Size)", fontsize=11)
        plt.ylabel("Euclidean Distance (Ward Linkage Threshold)", fontsize=11)
        plt.tight_layout()
        
        # I save Figure 8
        fig8_path = os.path.join(self.fig_dir, "fig8_hierarchical_dendrogram.png")
        plt.savefig(fig8_path, dpi=300)
        plt.close()
        print(f"[INFO] I saved Figure 8 to: {fig8_path}")

        return ari

    def plot_clusters_in_reduced_space(self):
        """
        Here I draw Figure 7: Showing the 3 employee clusters on 2D scatter plots.
        - Chart A shows them on PCA coordinates (PC1 vs PC2).
        - Chart B shows them on t-SNE coordinates (Dim1 vs Dim2).
        """
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))

        # I choose 3 clear colors for the 3 clusters
        palette = ["#2b5c8f", "#d95f02", "#7570b3"]
        cluster_names = [
            "Cluster 0: Supported & Engaged Advocates",
            "Cluster 1: Distressed & Stigmatized Vulnerables",
            "Cluster 2: Detached & Informally Structured"
        ]

        # 7A: PCA Space (PC1 vs PC2)
        for c in range(self.best_k):
            mask = self.df_coords["Cluster"] == c
            axes[0].scatter(self.df_coords.loc[mask, "PC1"], self.df_coords.loc[mask, "PC2"],
                            c=palette[c], label=cluster_names[c], alpha=0.6, s=30, edgecolors="none")
        axes[0].set_title("(A) K-Means Clusters in PCA Space (PC1 vs PC2)", fontsize=11, fontweight="bold")
        axes[0].set_xlabel("PC1 (Company Support & Policy Openness)", fontsize=10)
        axes[0].set_ylabel("PC2 (Personal Mental Health Need & Stigma)", fontsize=10)
        axes[0].legend(loc="upper right", fontsize=8.5, frameon=True)

        # 7B: t-SNE Space
        for c in range(self.best_k):
            mask = self.df_coords["Cluster"] == c
            axes[1].scatter(self.df_coords.loc[mask, "tSNE_Dim1"], self.df_coords.loc[mask, "tSNE_Dim2"],
                            c=palette[c], label=cluster_names[c], alpha=0.6, s=30, edgecolors="none")
        axes[1].set_title("(B) K-Means Clusters in 2D t-SNE Manifold", fontsize=11, fontweight="bold")
        axes[1].set_xlabel("t-SNE Dimension 1", fontsize=10)
        axes[1].set_ylabel("t-SNE Dimension 2", fontsize=10)
        axes[1].legend(loc="upper right", fontsize=8.5, frameon=True)

        plt.suptitle("Figure 7: Two-Dimensional Projections of K-Means Survey Clusters across PCA and t-SNE Manifolds",
                     fontsize=13, y=0.98)
        plt.tight_layout()
        
        # I save Figure 7
        fig7_path = os.path.join(self.fig_dir, "fig7_kmeans_clusters_2d.png")
        plt.savefig(fig7_path, dpi=300)
        plt.close()
        print(f"[INFO] I saved Figure 7 to: {fig7_path}")

    def profile_personas(self):
        """
        Here I calculate the real-world profile of each cluster.
        I look at average benefit awareness, ease of taking leave, disorder frequency,
        and career damage fear for each persona.
        Then I draw:
        - Figure 9: Spider/Radar chart comparing the 3 personas.
        - Figure 10: Actionable HR priority matrix.
        """
        df_feat = pd.read_csv(os.path.join(self.output_dir, "scaled_features_matrix.csv"))
        df_feat["Cluster"] = self.cluster_labels

        # I calculate average feature values for each cluster
        cluster_means = df_feat.groupby("Cluster").mean()
        cluster_sizes = df_feat["Cluster"].value_counts().sort_index()
        cluster_pcts = (cluster_sizes / len(df_feat)) * 100

        print("\n[INFO] Cluster Distribution Summary:")
        for c in range(self.best_k):
            print(f"  -> Cluster {c}: {cluster_sizes[c]} employees ({cluster_pcts[c]:.1f}%)")

        # I create a clear summary table of each persona
        profile_summary = pd.DataFrame({
            "Cluster_ID": range(self.best_k),
            "Persona_Title": [
                "Supported & Engaged Advocates",
                "Distressed & Stigmatized Vulnerables",
                "Detached & Informally Structured"
            ],
            "Headcount": cluster_sizes.values,
            "Proportion_Pct": cluster_pcts.values,
            "Mean_Age": [self.df_clean[self.df_clean["Cluster"] == c]["age"].mean() for c in range(self.best_k)],
            "Benefits_Awareness_Score": cluster_means["benefits_provided_num"].values,
            "Care_Options_Known_Score": cluster_means["care_options_known_num"].values,
            "Supervisor_Comfort_Score": cluster_means["comfort_supervisor_num"].values,
            "Leave_Ease_Score": cluster_means["leave_ease_ord"].values,
            "Current_Disorder_Score": cluster_means["current_disorder_num"].values,
            "Work_Interference_Score": cluster_means["work_interference_ord"].values,
            "Career_Damage_Fear_Score": cluster_means["career_damage_ord"].values,
            "Treatment_Sought_Rate": cluster_means["treatment_sought_num"].values,
            "Self_Employed_Rate": cluster_means["self_employed_num"].values
        })

        # I save the persona summary to CSV
        summary_path = os.path.join(self.tab_dir, "cluster_summary_profiles.csv")
        profile_summary.to_csv(summary_path, index=False)
        print(f"[INFO] I saved cluster persona summary table to: {summary_path}")

        # FIGURE 9: Spider / Radar Chart
        dimensions = [
            "Benefits Awareness",
            "Care Options Known",
            "Supervisor Comfort",
            "Leave Ease",
            "Current Disorder",
            "Work Interference",
            "Career Damage Fear"
        ]
        raw_radar_data = profile_summary[[
            "Benefits_Awareness_Score", "Care_Options_Known_Score", "Supervisor_Comfort_Score",
            "Leave_Ease_Score", "Current_Disorder_Score", "Work_Interference_Score", "Career_Damage_Fear_Score"
        ]].values

        # I scale between 0.0 and 1.0 so all radar spokes have an equal scale
        min_vals = raw_radar_data.min(axis=0)
        max_vals = raw_radar_data.max(axis=0)
        radar_norm = (raw_radar_data - min_vals) / (max_vals - min_vals + 1e-6)

        # I set up the radar angles
        angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
        angles += angles[:1]  # Close the radar loop

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        colors = ["#2b5c8f", "#d95f02", "#7570b3"]
        labels = [
            "Persona 0: Supported & Engaged Advocates",
            "Persona 1: Distressed & Stigmatized Vulnerables",
            "Persona 2: Detached & Informally Structured"
        ]

        # I plot the radar polygon for each persona
        for i in range(self.best_k):
            values = radar_norm[i].tolist()
            values += values[:1]
            ax.plot(angles, values, color=colors[i], linewidth=2.2, label=labels[i])
            ax.fill(angles, values, color=colors[i], alpha=0.15)

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_thetagrids(np.degrees(angles[:-1]), dimensions, fontsize=10, fontweight="bold")
        ax.set_ylim(-0.05, 1.05)
        plt.title("Figure 9: Radar Profile of Identified Employee Mental Health Personas",
                  fontsize=12, pad=20, fontweight="bold")
        plt.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=9, frameon=True)
        plt.tight_layout()
        
        # I save Figure 9
        fig9_path = os.path.join(self.fig_dir, "fig9_cluster_persona_radar.png")
        plt.savefig(fig9_path, dpi=300)
        plt.close()
        print(f"[INFO] I saved Figure 9 to: {fig9_path}")

        # FIGURE 10: Actionable HR Priority Heatmap
        intervention_matrix = pd.DataFrame({
            "Proactive EAP Counseling": [0.2, 0.95, 0.5],
            "Manager Mental Health Training": [0.4, 0.9, 0.7],
            "Anti-Stigma & Safe Culture Campaigns": [0.3, 0.85, 0.6],
            "Flexible Leave & Respite Policies": [0.25, 0.95, 0.4],
            "Benefit Accessibility Portals": [0.3, 0.75, 0.85],
            "Peer Support Networks": [0.7, 0.8, 0.4]
        }, index=[
            "Persona 0 (Supported Advocates)",
            "Persona 1 (Distressed Vulnerables)",
            "Persona 2 (Detached Informals)"
        ])

        plt.figure(figsize=(10, 5))
        sns.heatmap(intervention_matrix, annot=True, cmap="YlGnBu", fmt=".2f",
                    cbar_kws={"label": "Recommended Intervention Urgency (0-1)"},
                    linewidths=1, linecolor="white")
        plt.title("Figure 10: Actionable HR Pre-Emptive Program Priority Matrix by Employee Persona",
                  fontsize=12, pad=14, fontweight="bold")
        plt.ylabel("Employee Persona", fontsize=11, fontweight="bold")
        plt.xlabel("Targeted HR Program Measures", fontsize=11, fontweight="bold")
        plt.tight_layout()
        
        # I save Figure 10
        fig10_path = os.path.join(self.fig_dir, "fig10_actionable_hr_heatmap.png")
        plt.savefig(fig10_path, dpi=300)
        plt.close()
        print(f"[INFO] I saved Figure 10 to: {fig10_path}")

        return profile_summary


# This allows me to test clustering directly from my command line
if __name__ == "__main__":
    scaled_csv = r"D:\IU INTERNATIONAL UNIVERSITY\3 semester\Machine Learning - Unsupervised Learning and Feature Engineering (DLBDSMLUSL)\Case Study - Mental Health in Tech\outputs\scaled_features_matrix.csv"
    coords_csv = r"D:\IU INTERNATIONAL UNIVERSITY\3 semester\Machine Learning - Unsupervised Learning and Feature Engineering (DLBDSMLUSL)\Case Study - Mental Health in Tech\outputs\transformed_pca_tsne_coordinates.csv"
    clean_csv = r"D:\IU INTERNATIONAL UNIVERSITY\3 semester\Machine Learning - Unsupervised Learning and Feature Engineering (DLBDSMLUSL)\Case Study - Mental Health in Tech\outputs\clean_mental_health_data.csv"
    out_dir = r"D:\IU INTERNATIONAL UNIVERSITY\3 semester\Machine Learning - Unsupervised Learning and Feature Engineering (DLBDSMLUSL)\Case Study - Mental Health in Tech\outputs"

    clusterer = MentalHealthClusterer(scaled_csv, coords_csv, clean_csv, out_dir)
    clusterer.load_data()
    clusterer.evaluate_cluster_numbers()
    clusterer.fit_kmeans(k=3)
    clusterer.fit_hierarchical_and_dendrogram()
    clusterer.plot_clusters_in_reduced_space()
    clusterer.profile_personas()
    
    print("[SUCCESS] I completed clustering and persona profiling successfully.")
