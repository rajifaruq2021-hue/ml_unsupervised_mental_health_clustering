# Unsupervised Learning & Feature Engineering: Workplace Mental Health Segmentation

**Course**: DLBDSMLUSL01 – Machine Learning: Unsupervised Learning and Feature Engineering  
**Institution**: IU International University of Applied Sciences  
**Student**: Raji Faruq Ishola  
**Matriculation Number**: 4253139  
**Examination Type**: Case Study Report & Code Implementation  
**Chosen Task**: Task 1 – Mental Health in Technology-related Jobs  
**Dataset**: OSMI Mental Health in Tech Survey 2016 (1,433 respondents, 63 survey attributes)

---

## 1. Project Overview

This repository presents my complete empirical implementation for the IU International University Case Study in **Machine Learning: Unsupervised Learning and Feature Engineering (DLBDSMLUSL01)**. 

As a data scientist collaborating with Human Resources (HR) in a technology organization, I was tasked with analyzing high-dimensional, complex employee survey microdata to design targeted, pre-emptive workplace mental health interventions. 

### Core Analytical Methodology
1. **Exploratory Data Analysis & Text Harmonization**: Standardizing over 70 free-text gender strings, cleaning age recording anomalies (ages 3 to 323), and handling domain-informed structural missingness.
2. **Feature Engineering & Standardization**: Ordinal ranking of survey response scales, binary/ternary mapping of benefit awareness, one-hot encoding of nominal demographics, and standard z-score scaling across 26 dense dimensions.
3. **Dimensionality Reduction**: Principal Component Analysis (PCA) revealing eigenvalues, scree spectrum, and factor loadings (PC1: Institutional Support vs. PC2: Personal Mental Health Need), complemented by non-linear 2D t-SNE manifold projections.
4. **Unsupervised Clustering & Validation**: K-Means clustering evaluated via Within-Cluster Sum of Squares (Inertia/Elbow method) and Silhouette Analysis across $k \in [2, 8]$, benchmarked against Agglomerative Hierarchical Clustering (Ward's minimum variance criterion).
5. **Persona Profiling & HR Action Plan**: Synthesizing three distinct employee segments into operational personas to guide targeted organizational policy, anonymous Employee Assistance Programs (EAPs), and empathetic leadership training.

---

## 2. Identified Employee Personas

From my unsupervised clustering analysis ($k=3$), three distinct segments naturally emerge across the workforce:

| Persona | Title | Headcount (%) | Key Characteristics | Recommended HR Leverage Points |
|---|---|---|---|---|
| **Cluster 0** | **Supported & Engaged Advocates** | 539 (37.6%) | High benefit awareness, high comfort discussing concerns with supervisors, easy medical leave, low fear of career damage. | Train as certified Mental Health First Aiders and internal peer champions. |
| **Cluster 1** | **Distressed & Stigmatized Vulnerables** | 607 (42.4%) | High active mental disorder prevalence, high work interference, severe fear of career damage, low comfort speaking to leadership. | Deploy 100% anonymous third-party EAPs, flexible respite leave, and anti-stigma campaigns. |
| **Cluster 2** | **Detached & Informally Structured** | 287 (20.0%) | Exclusively self-employed and small contractors, no corporate benefit access, moderate disorder frequency. | Extend digital wellness app subscriptions, asynchronous support, and virtual communities. |

---

## 3. Repository Structure

```text
├── data/
│   └── mental-heath-in-tech-2016_20161114.csv  # Raw OSMI 2016 survey microdata
├── src/
│   ├── eda_and_preprocessing.py                 # Data cleaning, gender regex, age bounding
│   ├── feature_engineering.py                  # Ordinal mapping, one-hot encoding, standard scaling
│   ├── dimensionality_reduction.py             # PCA (variance, loadings) and t-SNE manifold
│   ├── clustering_and_profiling.py             # K-Means, Ward's hierarchical, radar & heatmap
│   └── main_pipeline.py                        # Unified end-to-end execution runner
├── tests/
│   └── test_pipeline.py                        # Pytest suite verifying scaling, shapes, and profiles
├── outputs/
│   ├── figures/                                # 10 publication-quality academic figures
│   │   ├── fig1_missing_values.png
│   │   ├── fig2_demographics_eda.png
│   │   ├── fig3_pca_explained_variance.png
│   │   ├── fig4_pca_feature_loadings.png
│   │   ├── fig5_tsne_projection.png
│   │   ├── fig6_elbow_silhouette_kselection.png
│   │   ├── fig7_kmeans_clusters_2d.png
│   │   ├── fig8_hierarchical_dendrogram.png
│   │   ├── fig9_cluster_persona_radar.png
│   │   └── fig10_actionable_hr_heatmap.png
│   └── tables/                                 # Quantitative CSV summary metrics
├── build_case_study_report.py                  # Generates formal IU academic Word and PDF reports
├── requirements.txt                            # Python library dependencies
└── README.md                                   # Comprehensive documentation
```

---

## 4. Setup and Execution

### Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Pip package manager

### Installation
```bash
git clone https://github.com/rajifaruq2021-hue/ml_unsupervised_mental_health_clustering.git
cd ml_unsupervised_mental_health_clustering
pip install -r requirements.txt
```

### Running the End-to-End Pipeline
```bash
python src/main_pipeline.py
```

### Running Automated Unit Tests
```bash
pytest tests/test_pipeline.py -v
```

### Building Academic Word and PDF Reports
```bash
python build_case_study_report.py
```

---

## 5. Author and Academic Integrity
- **Author**: Raji Faruq Ishola
- **Matriculation**: 4253139
- **Course**: DLBDSMLUSL01 – Machine Learning: Unsupervised Learning and Feature Engineering
- **Institution**: IU International University of Applied Sciences
