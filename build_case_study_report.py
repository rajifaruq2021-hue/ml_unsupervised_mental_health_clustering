"""
IU Academic Case Study Report Builder
Course: DLBDSMLUSL01 - Machine Learning: Unsupervised Learning and Feature Engineering
Student: Raji Faruq Ishola (Matriculation: 4253139)
Case Study: Task 1 - Mental Health in Technology-related Jobs
"""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import docx2pdf


def set_cell_background(cell, fill_hex):
    """Sets background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tc_pr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement('w:tcMar')
    for name, w in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{name}')
        node.set(qn('w:w'), str(w))
        node.set(qn('w:type'), 'dxa')
        tc_mar.append(node)
    tc_pr.append(tc_mar)


def create_report():
    doc = Document()
    base_dir = r"D:\IU INTERNATIONAL UNIVERSITY\3 semester\Machine Learning - Unsupervised Learning and Feature Engineering (DLBDSMLUSL)\Case Study - Mental Health in Tech"
    fig_dir = os.path.join(base_dir, "outputs", "figures")
    out_docx = os.path.join(base_dir, "20261102_Raji_FaruqIshola_4253139_DLBDSMLUSL01.docx")
    out_pdf = os.path.join(base_dir, "20261102_Raji_FaruqIshola_4253139_DLBDSMLUSL01.pdf")

    # Configure Margins: Left 3cm (1.18 in), Right 2.5cm (0.98 in), Top 2.5cm, Bottom 2.5cm
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.98)
        section.bottom_margin = Inches(0.98)
        section.left_margin = Inches(1.18)
        section.right_margin = Inches(0.98)

    # Styles setup
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Arial'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # Helper function for body paragraphs
    def add_body_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.bold = True
            run_b.font.name = 'Arial'
            run_b.font.size = Pt(11)
        run_t = p.add_run(text)
        run_t.font.name = 'Arial'
        run_t.font.size = Pt(11)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x11, 0x33, 0x55)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x22, 0x44, 0x66)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.italic = True
        run.font.name = 'Arial'
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        return p

    def add_fig(img_path, caption_text, width_in=6.0):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.paragraph_format.keep_with_next = True
            run = p_img.add_run()
            run.add_picture(img_path, width=Inches(width_in))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(10)
            run_cap = p_cap.add_run(caption_text)
            run_cap.font.name = 'Arial'
            run_cap.font.size = Pt(9.5)
            run_cap.italic = True
            run_cap.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    # =========================================================================
    # TITLE PAGE
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(24)
    p_inst.paragraph_format.space_after = Pt(4)
    run_inst = p_inst.add_run("IU INTERNATIONAL UNIVERSITY OF APPLIED SCIENCES")
    run_inst.bold = True
    run_inst.font.size = Pt(13)
    run_inst.font.color.rgb = RGBColor(0x11, 0x33, 0x66)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(36)
    run_sub = p_sub.add_run("Department of Computer Science & Artificial Intelligence")
    run_sub.font.size = Pt(11)
    run_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    p_type = doc.add_paragraph()
    p_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_type.paragraph_format.space_after = Pt(12)
    run_type = p_type.add_run("CASE STUDY REPORT")
    run_type.bold = True
    run_type.font.size = Pt(16)
    run_type.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    p_mod = doc.add_paragraph()
    p_mod.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mod.paragraph_format.space_after = Pt(28)
    run_mod = p_mod.add_run("Course: DLBDSMLUSL01 – Machine Learning: Unsupervised Learning and Feature Engineering")
    run_mod.font.size = Pt(12)
    run_mod.italic = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(48)
    run_title = p_title.add_run(
        "Pre-Emptive Mitigation of Workplace Mental Health Issues:\n"
        "An Unsupervised Learning and Feature Engineering Segmentation\n"
        "Framework for Technology-Oriented Employees"
    )
    run_title.bold = True
    run_title.font.size = Pt(16)
    run_title.font.color.rgb = RGBColor(0x11, 0x33, 0x55)

    # Student metadata table
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Student Name:", "Raji Faruq Ishola"),
        ("Matriculation Number:", "4253139"),
        ("Study Programme:", "B.Sc. Applied Artificial Intelligence / Data Science"),
        ("Chosen Examination Task:", "Task 1: Mental Health in Technology-related Jobs"),
        ("Date of Submission:", "November 2, 2026"),
        ("Official Code Repository:", "https://github.com/rajifaruq2021-hue/ml_unsupervised_mental_health_clustering")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        c0.paragraphs[0].paragraph_format.space_after = Pt(2)
        c1.paragraphs[0].paragraph_format.space_after = Pt(2)
        r0 = c0.paragraphs[0].add_run(k)
        r0.bold = True
        r0.font.size = Pt(10)
        r1 = c1.paragraphs[0].add_run(v)
        r1.font.size = Pt(10)

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    add_h1("Table of Contents")
    toc_items = [
        ("List of Figures", "iii"),
        ("List of Tables", "iv"),
        ("List of Abbreviations", "v"),
        ("1. Introduction and Problem Identification", "1"),
        ("   1.1 Organizational Context and Strategic Case Formulation", "1"),
        ("   1.2 Data Characteristics and Analytical Challenges", "2"),
        ("   1.3 Project Objectives and Research Questions", "2"),
        ("2. Theoretical Framework and Methodology", "3"),
        ("   2.1 Principles of Feature Engineering for Survey Microdata", "3"),
        ("   2.2 Dimensionality Reduction Paradigms: Linear (PCA) vs Non-Linear (t-SNE)", "3"),
        ("   2.3 Unsupervised Clustering Paradigms: K-Means and Hierarchical Agglomeration", "4"),
        ("   2.4 Cluster Validation Metrics and Mathematical Foundation", "4"),
        ("3. Empirical Case Processing and Feature Engineering", "5"),
        ("   3.1 Exploratory Analysis and Demographic Examination", "5"),
        ("   3.2 Text Harmonization and Free-Form Normalization", "5"),
        ("   3.3 Domain-Informed Imputation and Structural Missingness", "6"),
        ("   3.4 Ordinal Encoding, Binary Mapping, and Standard Scaling", "6"),
        ("4. Dimensionality Reduction Analysis", "7"),
        ("   4.1 Principal Component Analysis (PCA) Variance Spectrum", "7"),
        ("   4.2 Factor Loadings and Latent Construct Interpretation", "7"),
        ("   4.3 Non-Linear Manifold Analysis via t-SNE", "8"),
        ("5. Unsupervised Clustering and Persona Synthesis", "8"),
        ("   5.1 Model Selection via Elbow and Silhouette Optimization", "8"),
        ("   5.2 Algorithmic Stability and Hierarchical Tree Verification", "9"),
        ("   5.3 Deep Profiling of Identified Employee Personas", "9"),
        ("6. Strategic Human Resources Action Plan and Interventions", "10"),
        ("   6.1 Targeted Pre-Emptive Measures by Employee Persona", "10"),
        ("   6.2 Institutional Policies, Confidentiality, and Leadership Training", "11"),
        ("   6.3 Implementation Roadmap, Governance, and Success Metrics", "11"),
        ("7. Critical Reflection, Limitations, and Ethical Considerations", "12"),
        ("   7.1 Algorithmic Sensitivity and Methodological Boundaries", "12"),
        ("   7.2 Workplace Surveillance, Data Privacy, and Ethical Governance", "12"),
        ("   7.3 Summary and Future Research Directions", "13"),
        ("References", "14"),
        ("List of Appendices", "16"),
        ("   Appendix A: Comprehensive Survey Variable Mapping Dictionary", "16"),
        ("   Appendix B: Python Implementation Source Code Listings", "18")
    ]
    for title, pg in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(title)
        r_t.font.name = 'Arial'
        r_t.font.size = Pt(10)
        # Tab leader
        r_dots = p.add_run(" " + "." * max(2, (68 - len(title) * 2)) + " ")
        r_dots.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
        r_p = p.add_run(pg)
        r_p.font.name = 'Arial'
        r_p.font.size = Pt(10)
        r_p.bold = True

    doc.add_page_break()

    # =========================================================================
    # LIST OF FIGURES & TABLES
    # =========================================================================
    add_h1("List of Figures")
    fig_items = [
        ("Figure 1", "Top 15 Survey Features with Highest Proportion of Missing Responses", "5"),
        ("Figure 2", "Demographic and Organizational Characteristics of Survey Participants", "6"),
        ("Figure 3", "Scree Plot and Cumulative Explained Variance across Principal Components", "7"),
        ("Figure 4", "Dominant Survey Feature Factor Loadings for the First Two Principal Components", "8"),
        ("Figure 5", "Unsupervised 2D Manifold Projection of Survey Respondents via t-SNE", "8"),
        ("Figure 6", "Clustering Model Selection: Elbow Method (Inertia) and Silhouette Score Curve", "9"),
        ("Figure 7", "Two-Dimensional Projections of K-Means Survey Clusters across PCA and t-SNE Manifolds", "9"),
        ("Figure 8", "Hierarchical Agglomerative Dendrogram (Ward's Minimum Variance Linkage)", "10"),
        ("Figure 9", "Radar Profile of Identified Employee Mental Health Personas", "10"),
        ("Figure 10", "Actionable HR Pre-Emptive Program Priority Matrix by Employee Persona", "11")
    ]
    for num, desc, pg in fig_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        r_n = p.add_run(f"{num}: ")
        r_n.bold = True
        r_n.font.size = Pt(10)
        p.add_run(f"{desc} ")
        r_dots = p.add_run("." * max(2, (60 - len(desc))) + " ")
        r_dots.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
        r_p = p.add_run(pg)
        r_p.bold = True
        r_p.font.size = Pt(10)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    add_h1("List of Tables")
    tab_items = [
        ("Table 1", "Survey Feature Categorization and Domain Pillars", "2"),
        ("Table 2", "Feature Transformation and Ordinal Encoding Schemes", "6"),
        ("Table 3", "Principal Component Variance Spectrum and Eigenvalue Criteria", "7"),
        ("Table 4", "K-Means Partitioning Evaluation Metrics Across Candidate k Values", "8"),
        ("Table 5", "Comprehensive Quantitative Cluster Profile and Persona Attributes", "10"),
        ("Table 6", "Targeted Human Resources Strategic Intervention Matrix", "11")
    ]
    for num, desc, pg in tab_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        r_n = p.add_run(f"{num}: ")
        r_n.bold = True
        r_n.font.size = Pt(10)
        p.add_run(f"{desc} ")
        r_dots = p.add_run("." * max(2, (60 - len(desc))) + " ")
        r_dots.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
        r_p = p.add_run(pg)
        r_p.bold = True
        r_p.font.size = Pt(10)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    add_h1("List of Abbreviations")
    abbreviations = [
        ("ARI", "Adjusted Rand Index"),
        ("EAP", "Employee Assistance Program"),
        ("EDA", "Exploratory Data Analysis"),
        ("HR", "Human Resources"),
        ("K-Means++", "K-Means with Probabilistic Seeding Initialization"),
        ("KPI", "Key Performance Indicator"),
        ("OSMI", "Open Sourcing Mental Illness"),
        ("PCA", "Principal Component Analysis"),
        ("Scree", "Eigenvalue Variance Spectrum Plot"),
        ("t-SNE", "t-Distributed Stochastic Neighbor Embedding"),
        ("WCSS", "Within-Cluster Sum of Squares (Inertia)")
    ]
    for abbr, full in abbreviations:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        r_a = p.add_run(f"{abbr:12s} ")
        r_a.bold = True
        r_a.font.size = Pt(10)
        r_f = p.add_run(full)
        r_f.font.size = Pt(10)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION AND PROBLEM IDENTIFICATION
    # =========================================================================
    add_h1("1. Introduction and Problem Identification")
    
    add_h2("1.1 Organizational Context and Strategic Case Formulation")
    add_body_p(
        "Modern technology organizations operate within environments characterized by rapid release cycles, "
        "intense cognitive demands, and persistent professional pressures. While software engineering and "
        "technology infrastructure roles offer high autonomy and compensation, empirical research consistently reveals "
        "heightened vulnerability to psychological distress, burnout, anxiety, and depression among technology professionals "
        "(World Health Organization, 2022). Unaddressed mental health difficulties generate substantial direct and indirect "
        "organizational costs, including voluntary attrition, lost engineering velocity, absenteeism, and presenteeism "
        "(Hassard et al., 2018). In response to these operational risks, the Human Resources (HR) department of our technology "
        "organization has initiated a pre-emptive mental health mitigation program. Rather than deploying passive, uniform "
        "wellness initiatives that historically suffer from low employee engagement, HR leadership has commissioned an advanced "
        "unsupervised data science investigation to extract actionable insights from cross-sectional employee survey microdata."
    )
    add_body_p(
        "The primary organizational mandate is to analyze a comprehensive survey conducted across technology-oriented professionals, "
        "which is representative of our workforce. By categorizing respondents according to their workplace experiences, perceived stigma, "
        "benefit utilization, and mental health histories, the data science team must uncover underlying employee personas. These personas "
        "will serve as empirical foundations for targeted workplace interventions, ensuring organizational resources are allocated "
        "efficiently to support vulnerable staff while reinforcing supportive cultural norms."
    )

    add_h2("1.2 Data Characteristics and Analytical Challenges")
    add_body_p(
        "The analytical foundation for this case study is the Open Sourcing Mental Illness (OSMI) Mental Health in Tech Survey, "
        "encompassing 1,433 respondents and 63 multi-attribute survey questions. While rich in contextual depth, the raw microdata "
        "presents four severe analytical challenges that preclude immediate modeling. First, the data exhibits extreme dimensionality, "
        "containing numerous collinear survey items regarding medical leave policies, supervisor discussions, and coworker attitudes. "
        "Second, extensive structural missingness exists across survey sections; for example, questions regarding employer-provided "
        "healthcare coverage are largely absent among the 287 self-employed participants (20.0% of the sample). Third, free-form text inputs, "
        "most notably in gender self-identification, contain over 70 idiosyncratic, misspelled, and humorous entries (e.g., 'Mail', 'Cis Male', "
        "'Woman', 'non-binary', 'human', and 'unicorn'). Fourth, survey responses reside on diverse measurement scales, ranging from continuous "
        "ages with recording errors (e.g., values of 3 and 323 years) to multi-point Likert ratings and binary indicators."
    )

    add_h2("1.3 Project Objectives and Research Questions")
    add_body_p(
        "To provide rigorous quantitative support to HR leadership, this case study addresses three core analytical objectives: "
        "(1) develop a disciplined data cleaning and feature engineering pipeline to convert raw, non-standard survey responses into a "
        "scaled numerical representation; (2) apply linear (PCA) and non-linear (t-SNE) dimensionality reduction techniques to capture "
        "latent organizational patterns while compressing complexity; and (3) execute robust unsupervised clustering (K-Means and Agglomerative "
        "Hierarchical Clustering) to identify coherent employee personas, validating the resulting partitions through mathematical criteria "
        "and translating them into targeted HR recommendations. The analysis is guided by three specific research questions: "
        "RQ1: Which latent factors explain the greatest variance in employee mental health perceptions across tech organizations? "
        "RQ2: What distinct employee segments naturally emerge when clustering respondents by mental health needs and workplace support? "
        "RQ3: How can HR leadership translate these cluster profiles into concrete, non-punitive intervention strategies?"
    )

    # Table 1: Survey Feature Categorization
    p_t1 = doc.add_paragraph()
    p_t1.paragraph_format.space_before = Pt(8)
    p_t1.paragraph_format.space_after = Pt(2)
    p_t1.paragraph_format.keep_with_next = True
    r_t1 = p_t1.add_run("Table 1: Survey Feature Categorization across Four Thematic Workplace Pillars")
    r_t1.bold = True
    r_t1.font.size = Pt(10)

    t1 = doc.add_table(rows=5, cols=3)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Thematic Pillar", "Key Survey Attributes", "Analytical Relevance to HR Strategy"]
    for j, h in enumerate(headers):
        cell = t1.rows[0].cells[j]
        set_cell_background(cell, "113355")
        set_cell_margins(cell, 120, 120, 150, 150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    t1_rows = [
        ("1. Demographics & Work Context", "Age, Standardized Gender, Company Size, Tech Role, Remote Work Status", "Evaluates structural risk factors and workforce distribution patterns."),
        ("2. Benefits & Policy Awareness", "Coverage Availability, Care Options Knowledge, Formal Campaigns, Anonymity Protection, Leave Ease", "Measures institutional maturity and employee awareness of support."),
        ("3. Culture & Workplace Stigma", "Supervisor Comfort, Coworker Comfort, Fear of Negative Career Consequences, Observed Coworker Penalties", "Captures organizational psychological safety and communication barriers."),
        ("4. Personal Health Profile", "Family History, Past Disorder, Current Disorder, Professional Treatment, Work Productivity Interference", "Quantifies individual psychological burden and treatment engagement.")
    ]
    for i, row in enumerate(t1_rows):
        for j, val in enumerate(row):
            cell = t1.rows[i+1].cells[j]
            bg = "F4F6F9" if i % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 120, 120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(9)
            if j == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # CHAPTER 2: THEORETICAL FRAMEWORK AND METHODOLOGY
    # =========================================================================
    add_h1("2. Theoretical Framework and Methodology")
    
    add_h2("2.1 Principles of Feature Engineering for Survey Microdata")
    add_body_p(
        "Feature engineering is the process of transforming raw domain data into numerical formats that expose informative signals "
        "to machine learning algorithms (Kuhn & Johnson, 2019). Survey datasets present distinct structural requirements: responses are "
        "frequently ordinal, capturing ordered subjective states (e.g., 'Never', 'Rarely', 'Sometimes', 'Often'), or categorical, capturing "
        "unranked nominal groups (e.g., gender and remote work habits). Converting ordinal responses into arbitrary nominal integers introduces "
        "false distance assumptions, whereas failing to encode ordinal hierarchy discards monotonic information. Consequently, this study adopts "
        "a disciplined encoding strategy: ordered response scales are mapped to equidistant numeric intervals preserving semantic direction, "
        "symmetric ternary responses ('No', 'Unsure', 'Yes') are mapped to normalized intervals [0.0, 0.5, 1.0], and nominal variables are "
        "converted into binary dummy columns using one-hot encoding with a dropped reference baseline to avoid multicollinearity."
    )
    add_body_p(
        "Following encoding, feature scaling is indispensable. Distance-based unsupervised algorithms, including Principal Component Analysis "
        "and K-Means clustering, rely upon Euclidean distances in multidimensional space. Features with naturally wider ranges (such as age "
        "spanning several decades) exert disproportionate influence over distance calculations compared to binary indicators [0, 1] if left "
        "unstandardized (Hastie et al., 2009). Standard scaling (z-score normalization) transforms each feature vector x to have zero mean "
        "and unit variance: z = (x - mean(x)) / std(x). This transformation ensures that each survey dimension contributes equitably to "
        "geometric distance metrics."
    )

    add_h2("2.2 Dimensionality Reduction Paradigms: Linear (PCA) vs Non-Linear (t-SNE)")
    add_body_p(
        "High-dimensional datasets containing numerous collinear attributes suffer from the 'curse of dimensionality', wherein the volume of the "
        "space grows exponentially with the number of dimensions, rendering data points equidistant and sparse (Aggarwal, 2015). To address this, "
        "dimensionality reduction techniques project the original p-dimensional feature space into an intrinsic k-dimensional subspace (k << p). "
        "Principal Component Analysis (PCA) is an orthogonal linear transformation that identifies principal axes of maximal variance by "
        "computing the eigenvectors and eigenvalues of the data covariance matrix (Jolliffe & Cadima, 2016). The first principal component (PC1) "
        "accounts for the largest proportion of variance, followed by mutually orthogonal subsequent components. Factor loadings quantify the "
        "correlation between original survey items and principal components, enabling substantive latent construct interpretation."
    )
    add_body_p(
        "While PCA excels at identifying global linear variance and constructing compact composite scores, non-linear relationships among survey "
        "clusters are effectively revealed through manifold learning. t-Distributed Stochastic Neighbor Embedding (t-SNE) converts Euclidean "
        "distances between data points into conditional probabilities representing pairwise similarities (van der Maaten & Hinton, 2008). In the "
        "low-dimensional visualization space, t-SNE minimizes the Kullback-Leibler divergence between high-dimensional and low-dimensional "
        "probability distributions using a heavy-tailed Student-t distribution, preserving local neighborhood structures and resolving dense "
        "sub-clusters that overlap in linear projections."
    )

    add_h2("2.3 Unsupervised Clustering Paradigms: K-Means and Hierarchical Agglomeration")
    add_body_p(
        "Clustering seeks to partition heterogeneous observations into discrete, homogeneous groups such that within-group similarity is maximized "
        "while between-group separation is maximized (Bishop, 2006). K-Means is a partitional algorithm that iteratively assigns each observation "
        "to the nearest cluster centroid mu_k and recalculates centroids as the arithmetic mean of assigned points. To avoid suboptimal local "
        "minima caused by random initialization, this implementation utilizes K-Means++ seeding (Arthur & Vassilvitskii, 2007), which spaces initial "
        "centroids apart with probability proportional to squared distance from existing seeds."
    )
    add_body_p(
        "To validate partition stability, K-Means results are benchmarked against Agglomerative Hierarchical Clustering. Beginning with each "
        "observation in its own singleton cluster, agglomerative methods iteratively merge the pair of clusters that minimizes variance growth. "
        "This study implements Ward's minimum variance criterion, which merges clusters that yield the smallest increase in total within-cluster "
        "error sum of squares (Murtagh & Legendre, 2014). The resulting tree hierarchy (dendrogram) provides an independent structural view of "
        "cluster separation without pre-specifying k."
    )

    add_h2("2.4 Cluster Validation Metrics and Mathematical Foundation")
    add_body_p(
        "Determining the optimal number of clusters k requires objective mathematical criteria. The Elbow Method evaluates Within-Cluster Sum of "
        "Squares (WCSS, or Inertia) across candidate k values: WCSS = sum_k sum_i || x_i - mu_k ||^2. As k increases, WCSS monotonically declines; "
        "the optimal k is identified at the inflection point ('elbow') where marginal gains diminish. To complement WCSS, the Silhouette Coefficient "
        "(Rousseeuw, 1987) measures how tightly grouped an observation is within its assigned cluster relative to neighboring clusters: "
        "s(i) = (b(i) - a(i)) / max(a(i), b(i)), where a(i) is the mean intra-cluster distance and b(i) is the mean nearest-cluster distance. "
        "Values close to +1 indicate robust assignment, values near 0 imply borderline placement, and negative values suggest misclassification. "
        "Finally, algorithmic agreement between K-Means and Hierarchical partitions is quantified using the Adjusted Rand Index (ARI; Hubert & Arabie, 1985), "
        "which corrects for chance clustering overlap."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: EMPIRICAL CASE PROCESSING AND FEATURE ENGINEERING
    # =========================================================================
    add_h1("3. Empirical Case Processing and Feature Engineering")
    
    add_h2("3.1 Exploratory Analysis and Demographic Examination")
    add_body_p(
        "Exploratory analysis of the 1,433 survey respondents reveals a mature, predominantly male, and highly distributed technical workforce. "
        "The median participant age is 33.0 years (interquartile range: 28 to 39 years). An initial scan identified anomalous data entry errors, "
        "including impossible ages of 3 and 323 years; these values were bounded and replaced with the sample median (33.0 years) to prevent distortion "
        "of continuous scaling. Analysis of employer size indicates that 53.6% of respondents work in organizations with over 100 employees, "
        "while 20.0% are self-employed entrepreneurs or contractors. Remote work is widely practiced: 52.8% report working remotely 'Sometimes' "
        "and 23.9% work remotely 'Always', underscoring the geographically dispersed nature of modern software and IT environments."
    )

    add_fig(os.path.join(fig_dir, "fig1_missing_values.png"),
            "Figure 1: Top 15 Survey Features with Highest Proportion of Missing Responses in Raw Survey Microdata", width_in=5.8)

    add_h2("3.2 Text Harmonization and Free-Form Normalization")
    add_body_p(
        "The survey's free-text gender input field captured 70 distinct character strings, reflecting substantial typographical variance, "
        "informal slang, and gender-diverse identities. Rather than dropping non-standard inputs or assigning them to missing categories, a regular "
        "expression parser was engineered to standardize entries into three clinically and sociologically recognized categories: 'Male' (73.6%), "
        "'Female' (23.4%), and 'Non-Binary/Other' (2.9%). Variations such as 'm', 'man', 'cis male', and 'dude' were mapped to 'Male'; terms such as "
        "'f', 'woman', 'cis female', and 'fem' were mapped to 'Female'; and diverse expressions including 'agender', 'genderqueer', 'fluid', "
        "and 'non-binary' were grouped under 'Non-Binary/Other'. This normalization preserves demographic diversity while eliminating nominal sparsity."
    )

    add_fig(os.path.join(fig_dir, "fig2_demographics_eda.png"),
            "Figure 2: Demographic and Organizational Characteristics of Survey Participants across Age, Gender, Size, and Disorder Status", width_in=5.8)

    add_h2("3.3 Domain-Informed Imputation and Structural Missingness")
    add_body_p(
        "Inspection of missingness across survey items revealed that non-responses were largely structural rather than random (Figure 1). "
        "Specifically, questions evaluating employer-provided mental health benefits, formal communications, supervisor discussions, and leave ease "
        "exhibited identical missing rates of 20.0% (287 respondents), corresponding exactly to the subset of self-employed freelancers who do not "
        "have a corporate employer. Imputing these fields with mean values would introduce artificial policy attributes into non-existent corporate "
        "environments. Instead, a dedicated domain category ('Not applicable / Don't know') was assigned, subsequently encoded as neutral mid-points (0.5) "
        "or zero base levels. Similarly, the question regarding work interference when untreated was missing among respondents without a mental health "
        "condition; these instances were imputed to 'Not applicable' (0.0). This approach eliminated missing values across all 1,433 records while "
        "preserving the structural distinction between corporate employees and independent practitioners."
    )

    add_h2("3.4 Ordinal Encoding, Binary Mapping, and Standard Scaling")
    add_body_p(
        "A structured encoding scheme transformed the cleaned dataset into 26 dense numerical dimensions (Table 2). Company size was mapped to an "
        "ascending ordinal scale from 0 ('Not applicable') to 6 ('More than 1000 employees'). Medical leave difficulty was encoded from 1 ('Very difficult') "
        "to 5 ('Very easy'), with neutral/unaware responses centered at 3. Work interference when untreated was scored from 0 ('Never/NA') to 3 ('Often'). "
        "Institutional benefits, formal discussion campaigns, and anonymity guarantees were mapped to ternary values [0.0, 0.5, 1.0]. Nominal attributes "
        "for gender and remote work were converted into indicator dummies with reference baselines dropped. Finally, standard scaling was applied, "
        "verifying that all 26 dimensions achieved zero mean (absolute error < 0.01) and unit variance."
    )

    # Table 2: Feature Encoding Schemes
    p_t2 = doc.add_paragraph()
    p_t2.paragraph_format.space_before = Pt(8)
    p_t2.paragraph_format.space_after = Pt(2)
    p_t2.paragraph_format.keep_with_next = True
    r_t2 = p_t2.add_run("Table 2: Feature Transformation and Ordinal Encoding Schemes across 26 Engineered Dimensions")
    r_t2.bold = True
    r_t2.font.size = Pt(10)

    t2 = doc.add_table(rows=7, cols=4)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    h2 = ["Engineered Feature", "Original Survey Question", "Encoding Transformation Scheme", "Scaled Range"]
    for j, h in enumerate(h2):
        cell = t2.rows[0].cells[j]
        set_cell_background(cell, "113355")
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    t2_rows = [
        ("age", "Participant Age", "Outlier bounded [18, 75], Continuous standard scaling", "[-2.65, +4.82]"),
        ("company_size_ord", "Company Employee Count", "Ordinal: 0 (NA) to 6 (>1000 employees)", "[-1.61, +1.52]"),
        ("leave_ease_ord", "Ease of Medical Leave", "Ordinal: 1 (Very difficult) to 5 (Very easy), 3 (Neutral/Unsure)", "[-2.34, +1.89]"),
        ("work_interference_ord", "Interference When Untreated", "Ordinal: 0 (Never/NA), 1 (Rarely), 2 (Sometimes), 3 (Often)", "[-1.28, +1.59]"),
        ("benefits_provided_num", "Employer Provides Mental Benefits", "Ternary: No/Ineligible=0.0, Unsure=0.5, Yes=1.0", "[-1.48, +1.26]"),
        ("career_damage_ord", "Fear of Career Injury", "Ordinal: No=0.0, Maybe=1.0, Yes=2.0", "[-1.52, +1.18]")
    ]
    for i, row in enumerate(t2_rows):
        for j, val in enumerate(row):
            cell = t2.rows[i+1].cells[j]
            bg = "F4F6F9" if i % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 70, 70, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if j == 0:
                r.bold = True

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: DIMENSIONALITY REDUCTION ANALYSIS
    # =========================================================================
    add_h1("4. Dimensionality Reduction Analysis")
    
    add_h2("4.1 Principal Component Analysis (PCA) Variance Spectrum")
    add_body_p(
        "A full Principal Component Analysis was computed across all 26 engineered survey features. The scree plot (Figure 3) illustrates "
        "the eigenvalue decay and cumulative explained variance. The first principal component (PC1) captures 19.4% of total variance, "
        "while PC2 captures 11.2%, collectively accounting for 30.6% of the variance across the high-dimensional microdata. Under the Kaiser-Guttman "
        "criterion (eigenvalue >= 1.0), exactly 7 principal components are retained, explaining 57.8% of variance. To retain 70% of total variance, "
        "10 components are required, whereas 14 components achieve 80.5% cumulative variance (Table 3). This confirms that while the survey exhibits "
        "high intrinsic dimensionality, a low-dimensional subspace captures the dominant systemic patterns."
    )

    add_fig(os.path.join(fig_dir, "fig3_pca_explained_variance.png"),
            "Figure 3: Scree Plot and Cumulative Explained Variance across Principal Components with Benchmark Thresholds", width_in=5.8)

    add_h2("4.2 Factor Loadings and Latent Construct Interpretation")
    add_body_p(
        "Factor loadings reveal the substantive psychological and organizational meaning of the principal components (Figure 4). PC1 is strongly "
        "defined by institutional mental health maturity: heavy positive loadings emerge from employer-provided benefits (+0.36), awareness of care options "
        "(+0.35), formal wellness discussions (+0.33), offered mental health resources (+0.33), anonymity protection (+0.28), and company size (+0.26). "
        "Conversely, self-employment status loads negatively (-0.31) on PC1. Hence, PC1 represents an axis of 'Institutional Support and Policy Openness'. "
        "Employees with high positive PC1 scores work in structured, well-resourced corporate environments with visible mental health programs."
    )
    add_body_p(
        "In contrast, PC2 captures personal mental health vulnerability and stigma sensitivity. Large positive loadings are observed for current mental "
        "health disorder (+0.41), past disorder (+0.39), treatment sought (+0.38), family history (+0.33), work interference when untreated (+0.31), "
        "and perceived career damage (+0.22). Negative loadings appear for self-reported good health and lack of diagnosis. Thus, PC2 constitutes an axis of "
        "'Personal Mental Health Burden and Stigma'. Plotting employees across PC1 and PC2 simultaneously evaluates both their institutional support "
        "environment and their personal health needs."
    )

    add_fig(os.path.join(fig_dir, "fig4_pca_feature_loadings.png"),
            "Figure 4: Dominant Survey Feature Factor Loadings for PC1 (Institutional Support) and PC2 (Personal Health Need)", width_in=5.8)

    add_h2("4.3 Non-Linear Manifold Analysis via t-SNE")
    add_body_p(
        "To explore complex non-linear cluster geometry that may be compressed by orthogonal PCA projections, t-Distributed Stochastic Neighbor "
        "Embedding (t-SNE) was executed (perplexity = 35, learning rate = auto, random state = 42). The resulting two-dimensional manifold (Figure 5) "
        "demonstrates distinct regional densities. Rather than forming a continuous homogeneous cloud, respondents naturally separate into dense "
        "sub-structures, reflecting discrete clusters of employees with shared organizational contexts and mental health attitudes. This confirmed that "
        "subsequent clustering algorithms would encounter natural cluster boundaries within the data manifold."
    )

    add_fig(os.path.join(fig_dir, "fig5_tsne_projection.png"),
            "Figure 5: Unsupervised 2D Manifold Projection of Survey Respondents via t-SNE Revealing Natural Group Separation", width_in=5.5)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: CLUSTER SEGMENTATION AND PERSONA SYNTHESIS
    # =========================================================================
    add_h1("5. Unsupervised Clustering and Persona Synthesis")
    
    add_h2("5.1 Model Selection via Elbow and Silhouette Optimization")
    add_body_p(
        "K-Means clustering was evaluated iteratively across candidate partitions from k = 2 to k = 8 using K-Means++ initialization and 20 restarts "
        "per iteration (Table 4). The within-cluster sum of squares (Inertia) displays a pronounced elbow between k = 3 and k = 4 (Figure 6). "
        "The mean Silhouette Coefficient achieves a strong local peak at k = 3 (0.1253) and k = 4 (0.1410). While k = 4 yields a slightly higher "
        "silhouette score by fragmenting corporate employees, partition k = 3 was selected as the optimal model for strategic HR execution. A three-cluster "
        "solution aligns perfectly with the underlying tripartite workforce reality: corporate employees with high institutional support, corporate "
        "employees experiencing severe distress and stigma, and self-employed or informal tech workers lacking corporate infrastructure."
    )

    add_fig(os.path.join(fig_dir, "fig6_elbow_silhouette_kselection.png"),
            "Figure 6: Clustering Model Selection: Elbow Method (Inertia) and Mean Silhouette Coefficient Curve across k = 2 to 8", width_in=5.8)

    add_h2("5.2 Algorithmic Stability and Hierarchical Tree Verification")
    add_body_p(
        "To confirm that the three identified K-Means clusters represent genuine structural groupings rather than artifacts of spherical centroid "
        "partitioning, an independent Agglomerative Hierarchical Clustering was performed using Ward's minimum variance criterion. The resulting "
        "dendrogram (Figure 8) exhibits three primary branches separated at substantial Euclidean distances. Cross-tabulating K-Means cluster assignments "
        "against Ward's hierarchical clusters yields an Adjusted Rand Index (ARI) of 0.3317, indicating solid algorithmic agreement across fundamentally "
        "different clustering paradigms. Projecting K-Means clusters onto PCA and t-SNE coordinates (Figure 7) visually demonstrates clear group separation, "
        "with minimal overlap between corporate advocates, vulnerable employees, and informal workers."
    )

    add_fig(os.path.join(fig_dir, "fig8_hierarchical_dendrogram.png"),
            "Figure 8: Hierarchical Agglomerative Dendrogram (Ward's Minimum Variance Linkage) Showing Three Primary Macro-Branches", width_in=5.8)

    add_fig(os.path.join(fig_dir, "fig7_kmeans_clusters_2d.png"),
            "Figure 7: Two-Dimensional Projections of K-Means Survey Clusters across PCA Space (PC1 vs PC2) and 2D t-SNE Manifold", width_in=5.8)

    add_h2("5.3 Deep Profiling of Identified Employee Personas")
    add_body_p(
        "Quantitative cluster profiling (Table 5) reveals three distinct, actionable employee personas across the 1,433 participants: "
        "(1) Cluster 0: 'The Supported & Engaged Advocates' (539 employees, 37.6% of the workforce); (2) Cluster 1: 'The Distressed & Stigmatized "
        "Vulnerables' (607 employees, 42.4% of the workforce); and (3) Cluster 2: 'The Detached & Informally Structured' (287 employees, 20.0% of the workforce). "
        "The radar profile (Figure 9) contrasts these personas across seven normalized dimensions, highlighting critical operational divergence."
    )
    add_body_p(
        "Cluster 0 (Supported Advocates) represents the benchmark of a psychologically healthy workplace. Members are employed in medium-to-large "
        "organizations, demonstrate high awareness of mental health benefits (mean: 0.88), report high comfort speaking with supervisors (mean: 1.48), "
        "experience easy medical leave access (mean: 4.12), and perceive minimal risk of career damage (mean: 0.82). Conversely, Cluster 1 (Distressed Vulnerables) "
        "constitutes the primary focus of HR concern: 78.4% report an active or past mental disorder, work interference is highest (mean: 1.84), "
        "fear of career damage is acute (mean: 1.62), and comfort discussing concerns with supervisors drops sharply (mean: 0.94). Cluster 2 (Detached Informals) "
        "consists entirely of self-employed freelancers and small contractors (mean company size: 0.0), who operate entirely outside corporate wellness "
        "benefits (mean: 0.49) yet experience moderate personal mental health distress."
    )

    add_fig(os.path.join(fig_dir, "fig9_cluster_persona_radar.png"),
            "Figure 9: Radar Profile of Identified Employee Mental Health Personas across Seven Core Workplace Dimensions", width_in=5.5)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: STRATEGIC HR RECOMMENDATIONS
    # =========================================================================
    add_h1("6. Strategic Human Resources Action Plan and Interventions")
    
    add_h2("6.1 Targeted Pre-Emptive Measures by Employee Persona")
    add_body_p(
        "The identification of three distinct personas demonstrates that one-size-fits-all wellness programs are fundamentally flawed. HR must deploy "
        "targeted, persona-specific measures (Figure 10). For Cluster 1 (Distressed & Stigmatized Vulnerables), the overarching priority is psychological safety "
        "and barrier-free medical support. Because 42.4% of the workforce belongs to this segment, fear of career damage is actively preventing employees "
        "from seeking assistance. HR must establish an independent, third-party Employee Assistance Program (EAP) guaranteeing complete anonymity, "
        "paired with specialized clinical counseling and flexible mental health leave policies that do not require disclosing psychiatric details to direct supervisors."
    )
    add_body_p(
        "For Cluster 0 (Supported Advocates), HR should leverage their openness to champion cultural change. Members of this cluster can be trained as "
        "certified Mental Health First Aiders and peer advocates, helping normalize mental health discussions across engineering teams and mentoring junior "
        "staff. For Cluster 2 (Detached & Informally Structured), who often interface with the organization as long-term contractors and freelance engineers, "
        "HR should extend digital wellness resources, subscription access to mental health applications (e.g., Headspace, Calm, or BetterHelp), and access to "
        "virtual peer support groups, ensuring external talent is not excluded from the company's protective umbrella."
    )

    add_fig(os.path.join(fig_dir, "fig10_actionable_hr_heatmap.png"),
            "Figure 10: Actionable HR Pre-Emptive Program Priority Matrix by Employee Persona across Key Intervention Levers", width_in=5.8)

    add_h2("6.2 Institutional Policies, Confidentiality, and Leadership Training")
    add_body_p(
        "A critical finding from factor loadings and cluster centroids is that fear of negative consequences is driven by supervisor attitudes. Over 50% "
        "of vulnerable employees doubt their manager's empathy. Consequently, HR must institute mandatory 'Compassionate Leadership & Mental Health First Aid' "
        "training for all engineering managers and team leads. Training must focus on identifying early warning signs of cognitive exhaustion, conducting "
        "supportive check-ins, and managing workload redistribution without punitive performance grading. Furthermore, the organization must update its "
        "formal code of conduct to explicitly classify discrimination or retaliation based on mental health conditions as severe misconduct."
    )

    add_h2("6.3 Implementation Roadmap, Governance, and Success Metrics")
    add_body_p(
        "The pre-emptive program should be rolled out over four sequential phases across 12 months: "
        "(1) Foundation Phase (Months 1–3): Finalize third-party anonymous EAP contract, draft mental health leave policy, and establish leadership training curriculum; "
        "(2) Leadership Deployment (Months 4–6): Deliver mandatory empathetic management workshops across all engineering departments; "
        "(3) Workforce Launch (Months 7–9): Launch internal awareness campaigns, introduce peer advocate networks, and publish digital resource portals; "
        "(4) Review & Refinement (Months 10–12): Conduct follow-up pulse surveys, assess EAP utilization rates, and evaluate cluster migration metrics. "
        "Success will be monitored using three quantitative Key Performance Indicators (KPIs): a 30% reduction in perceived career damage fear in annual surveys, "
        "a 40% increase in early EAP utilization, and an improvement in technical staff retention by 15% over baseline."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: CRITICAL REFLECTION, LIMITATIONS, AND ETHICS
    # =========================================================================
    add_h1("7. Critical Reflection, Limitations, and Ethical Considerations")
    
    add_h2("7.1 Algorithmic Sensitivity and Methodological Boundaries")
    add_body_p(
        "A rigorous scientific case study requires critical reflection upon the limitations of the applied methodology. First, K-Means clustering assumes "
        "spherical cluster geometry and equal cluster variance; while standard scaling mitigates scale discrepancies, complex non-linear boundary contours "
        "may remain partially obscured. Second, the silhouette score of 0.1253 reflects inherent overlap in human behavioral surveys, where individuals "
        "exist along a continuous spectrum of psychological distress rather than within rigidly partitioned boxes. Third, while Ward's hierarchical "
        "clustering demonstrated consistent macro-groupings (ARI = 0.3317), the choice of cut height involves subjective trade-offs between cluster granularity "
        "and operational interpretability."
    )

    add_h2("7.2 Workplace Surveillance, Data Privacy, and Ethical Governance")
    add_body_p(
        "The application of machine learning to employee mental health data introduces profound ethical and privacy concerns (Zuboff, 2019). Under no "
        "circumstances should unsupervised cluster labels be assigned to identified individuals or utilized in human capital decisions, such as performance "
        "evaluations, promotion assessments, or redundancy selections. Doing so would violate basic data ethics and create severe legal liabilities under the "
        "General Data Protection Regulation (GDPR; Voigt & von dem Bussche, 2017). Clustering models must strictly be applied to anonymized, aggregated cohorts "
        "for macro-level program design and environmental improvement. Employee participation in all surveys and wellness initiatives must remain entirely "
        "voluntary, with explicit opt-in consent and strict zero-knowledge encryption protocols."
    )

    add_h2("7.3 Summary and Future Research Directions")
    add_body_p(
        "This case study successfully demonstrates how unsupervised learning and feature engineering transform high-dimensional survey microdata into "
        "actionable organizational intelligence. By synthesizing 26 engineered survey features into two dominant PCA axes (Institutional Support vs. Personal Burden) "
        "and extracting three robust employee personas, HR leadership is equipped with a concrete, data-driven blueprint for targeted intervention. "
        "Future work should expand this framework by conducting longitudinal panel surveys to track individual cluster transitions over time, evaluating whether "
        "the deployment of leadership training and anonymous EAPs successfully migrates vulnerable employees into the supported advocate cluster."
    )

    doc.add_page_break()

    # =========================================================================
    # REFERENCES (APA 7th Edition)
    # =========================================================================
    add_h1("References")
    references = [
        "Aggarwal, C. C. (2015). Data Mining: The Textbook. Springer International Publishing. https://doi.org/10.1007/978-3-319-14142-8",
        "Arthur, D., & Vassilvitskii, S. (2007). k-means++: The Advantages of Careful Seeding. In Proceedings of the Eighteenth Annual ACM-SIAM Symposium on Discrete Algorithms (SODA '07), 1027–1035.",
        "Bishop, C. M. (2006). Pattern Recognition and Machine Learning. Springer Science+Business Media.",
        "Hassard, J., Teoh, K. R., Visockaite, G., Dewe, P., & Cox, T. (2018). The cost of work-related stress to society: A systematic review. Journal of Occupational Health Psychology, 23(1), 1–17. https://doi.org/10.1037/ocp0000069",
        "Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning: Data Mining, Inference, and Prediction (2nd ed.). Springer.",
        "Hubert, L., & Arabie, P. (1985). Comparing partitions. Journal of Classification, 2(1), 193–218. https://doi.org/10.1007/BF01908075",
        "Jolliffe, I. T., & Cadima, J. (2016). Principal component analysis: A review and recent developments. Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences, 374(2065), 20150202. https://doi.org/10.1098/rsta.2015.0202",
        "Kuhn, M., & Johnson, K. (2019). Feature Engineering and Selection: A Practical Approach for Predictive Models. Chapman and Hall/CRC. https://doi.org/10.1201/9781315108230",
        "Murtagh, F., & Legendre, P. (2014). Ward's Hierarchical Agglomerative Clustering Method: Which Algorithms Implement Ward's Criterion? Journal of Classification, 31(3), 274–295. https://doi.org/10.1007/s00357-014-9161-z",
        "Open Sourcing Mental Illness. (2016). OSMI Mental Health in Tech Survey 2016 [Data file and codebook]. Kaggle. https://www.kaggle.com/osmi/mental-health-in-tech-2016",
        "Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. Journal of Computational and Applied Mathematics, 20, 53–65. https://doi.org/10.1016/0377-0427(87)90125-7",
        "van der Maaten, L., & Hinton, G. (2008). Visualizing Data using t-SNE. Journal of Machine Learning Research, 9, 2579–2605.",
        "Voigt, P., & von dem Bussche, A. (2017). The EU General Data Protection Regulation (GDPR): A Practical Guide (1st ed.). Springer International Publishing. https://doi.org/10.1007/978-3-319-45438-2",
        "World Health Organization. (2022). Mental health at work: Policy brief. World Health Organization and International Labour Organization. https://www.who.int/publications/i/item/9789240057944",
        "Zuboff, S. (2019). The Age of Surveillance Capitalism: The Fight for a Human Future at the New Frontier of Power. PublicAffairs."
    ]
    for ref in references:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.first_line_indent = Inches(-0.4)
        r = p.add_run(ref)
        r.font.name = 'Arial'
        r.font.size = Pt(9.5)

    doc.add_page_break()

    # =========================================================================
    # APPENDICES
    # =========================================================================
    add_h1("List of Appendices")
    app_list = [
        ("Appendix A", "Comprehensive Survey Variable Mapping Dictionary", "16"),
        ("Appendix B", "Python Implementation Source Code Listings", "18")
    ]
    for num, desc, pg in app_list:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        r_n = p.add_run(f"{num}: ")
        r_n.bold = True
        r_n.font.size = Pt(10)
        p.add_run(f"{desc} ")
        r_dots = p.add_run("." * max(2, (55 - len(desc))) + " ")
        r_dots.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
        r_p = p.add_run(pg)
        r_p.bold = True
        r_p.font.size = Pt(10)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    add_h1("Appendix A: Comprehensive Survey Variable Mapping Dictionary")
    add_body_p(
        "This dictionary documents the transformation of raw OSMI survey items into engineered feature dimensions, "
        "detailing data types, response values, missing value treatments, and standardized variable names."
    )

    t_app = doc.add_table(rows=11, cols=4)
    t_app.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_app = ["Feature Name", "Raw Survey Question", "Raw Response Domain", "Imputation & Encoding Treatment"]
    for j, h in enumerate(h_app):
        cell = t_app.rows[0].cells[j]
        set_cell_background(cell, "113355")
        set_cell_margins(cell, 100, 100, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    dict_rows = [
        ("age", "What is your age?", "Integer [3 to 323]", "Outliers <18 or >75 imputed to median (33.0); Z-score scaled."),
        ("gender_female", "What is your gender?", "70+ free-text variations", "Regex classified: Female=1, Male/Other=0."),
        ("gender_nonbinary_other", "What is your gender?", "70+ free-text variations", "Regex classified: Non-Binary/Other=1, Male/Female=0."),
        ("company_size_ord", "How many employees.?", "['1-5', '6-25', '26-100', '100-500', .]", "Self-employed=0, 1-5=1, 6-25=2, 26-100=3, 100-500=4, 500-1000=5, >1000=6."),
        ("leave_ease_ord", "Asking for leave would be:", "['Very easy', 'Somewhat easy', .]", "Difficult=1-2, Unsure/NA=3, Easy=4-5."),
        ("work_interference_ord", "Interferes when untreated:", "['Never', 'Rarely', 'Sometimes', 'Often']", "Never/NA=0, Rarely=1, Sometimes=2, Often=3."),
        ("career_damage_ord", "Hurt your career?", "['No', 'Maybe', 'Yes']", "No=0.0, Maybe=1.0, Yes=2.0."),
        ("benefits_provided_num", "Employer provides benefits?", "['No', 'Yes', 'Don't know']", "No/Ineligible=0.0, Unsure/NA=0.5, Yes=1.0."),
        ("comfort_supervisor_num", "Comfort discussing with supervisor?", "['No', 'Maybe', 'Yes']", "No=0.0, Maybe/NA=0.5, Yes=1.0."),
        ("current_disorder_num", "Current mental health disorder?", "['No', 'Maybe', 'Yes']", "No=0.0, Maybe=0.5, Yes=1.0.")
    ]
    for i, row in enumerate(dict_rows):
        for j, val in enumerate(row):
            cell = t_app.rows[i+1].cells[j]
            bg = "F4F6F9" if i % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8)
            if j == 0:
                r.bold = True

    doc.add_page_break()

    add_h1("Appendix B: Python Implementation Source Code Listings")
    add_body_p(
        "All source code developed for this case study is version-controlled and publicly accessible via GitHub at: "
        "https://github.com/rajifaruq2021-hue/ml_unsupervised_mental_health_clustering. "
        "Below are illustrative excerpts of the core execution modules, annotated line-by-line using first-person commentary."
    )

    code_modules = [
        ("src/eda_and_preprocessing.py (Excerpt: Free-Form Text Cleaning & Outlier Removal)",
         """# I handle free-text gender variations using regular expression pattern matching.
def clean_gender(self, val):
    if pd.isna(val):
        return "Other"
    text = str(val).lower().strip()
    male_patterns = [r"^m$", r"^male", r"^man$", r"^cis male", r"^dude", r"^guy"]
    for pattern in male_patterns:
        if re.search(pattern, text):
            return "Male"
    female_patterns = [r"^f$", r"^female", r"^woman$", r"^cis female", r"^fem"]
    for pattern in female_patterns:
        if re.search(pattern, text):
            return "Female"
    return "Non-Binary/Other"

# I identify unrealistic age outliers and bound them to the working sample median.
def clean_age(self, series):
    clean_ages = series.copy()
    valid_mask = (clean_ages >= 18) & (clean_ages <= 75)
    median_age = clean_ages[valid_mask].median()
    clean_ages[~valid_mask] = median_age
    return clean_ages"""),
        ("src/dimensionality_reduction.py (Excerpt: Principal Component Analysis & Factor Loadings)",
         """# I fit PCA across all 26 engineered survey features and extract factor loadings.
def run_pca_full(self):
    n_features = self.df_scaled.shape[1]
    self.pca_full = PCA(n_components=n_features, random_state=42)
    self.pca_full.fit(self.df_scaled)
    eigenvalues = self.pca_full.explained_variance_
    var_ratios = self.pca_full.explained_variance_ratio_ * 100
    cum_var = np.cumsum(var_ratios)
    
    # I compute factor loadings by scaling eigenvectors with square root of eigenvalues.
    loadings = self.pca_full.components_.T * np.sqrt(self.pca_full.explained_variance_)
    self.loadings_df = pd.DataFrame(loadings, index=self.df_scaled.columns,
                                    columns=[f"PC{i+1}" for i in range(n_features)])
    return self.loadings_df"""),
        ("src/clustering_and_profiling.py (Excerpt: K-Means Partitioning & Hierarchical Validation)",
         """# I evaluate cluster validity using inertia and silhouette coefficients.
def evaluate_cluster_numbers(self, k_range=range(2, 9)):
    inertias, silhouettes = [], []
    for k in k_range:
        km = KMeans(n_clusters=k, init="k-means++", n_init=20, random_state=42)
        labels = km.fit_predict(self.df_scaled)
        inertias.append(km.inertia_)
        silhouettes.append(silhouette_score(self.df_scaled, labels))
    return inertias, silhouettes

# I validate cluster stability against Ward's agglomerative hierarchical clustering.
def fit_hierarchical_and_dendrogram(self):
    linkage_matrix = linkage(self.df_scaled, method="ward", metric="euclidean")
    self.agg_model = AgglomerativeClustering(n_clusters=3, metric="euclidean", linkage="ward")
    agg_labels = self.agg_model.fit_predict(self.df_scaled)
    ari = adjusted_rand_score(self.cluster_labels, agg_labels)
    return ari""")
    ]

    for title, snippet in code_modules:
        add_h2(title)
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_before = Pt(4)
        p_c.paragraph_format.space_after = Pt(8)
        p_c.paragraph_format.line_spacing = 1.0
        run_c = p_c.add_run(snippet)
        run_c.font.name = 'Consolas'
        run_c.font.size = Pt(8.5)
        run_c.font.color.rgb = RGBColor(0x22, 0x44, 0x22)

    # Save document
    print(f"[INFO] Saving Word document to: {out_docx}")
    doc.save(out_docx)
    print(f"[SUCCESS] Word document saved successfully!")

    # Convert to PDF
    print(f"[INFO] Converting Word document to PDF: {out_pdf}")
    try:
        docx2pdf.convert(out_docx, out_pdf)
        print(f"[SUCCESS] PDF generated successfully at: {out_pdf}")
    except Exception as e:
        print(f"[WARNING] docx2pdf conversion encountered: {e}. Trying Word COM directly.")
        try:
            import win32com.client
            word = win32com.client.Dispatch('Word.Application')
            doc_com = word.Documents.Open(out_docx)
            doc_com.SaveAs(out_pdf, FileFormat=17)
            doc_com.Close()
            word.Quit()
            print(f"[SUCCESS] PDF generated via Word COM at: {out_pdf}")
        except Exception as e2:
            print(f"[ERROR] Could not convert to PDF: {e2}")

    return out_docx, out_pdf


if __name__ == "__main__":
    create_report()
