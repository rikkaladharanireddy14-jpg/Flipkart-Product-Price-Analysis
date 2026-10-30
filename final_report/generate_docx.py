"""Comprehensive DOCX Report Generator
Builds the complete college-level One-Week Technical Project Report
for Flipkart Product Price Analysis according to B.Tech guidelines.
"""

import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

FIGURES_DIR = Path("reports/figures")
OUTPUT_PATH = Path("final_report/Flipkart_Product_Price_Analysis_Report.docx")

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set cell padding in twips."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, color_hex):
    """Set background color of a cell."""
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def add_header_footer_page_number(doc):
    """Add footer with page numbering and header with project title."""
    for s_idx, section in enumerate(doc.sections):
        section.different_first_page_header_footer = True
        
        # Header for subsequent pages
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "Flipkart Product Price Analysis | B.Tech CSE Technical Report"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.runs[0].font.name = "Times New Roman"
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = RGBColor(120, 120, 120)
        
        # Footer
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        # Add text before page number
        r1 = fp.add_run("ACE Engineering College, Hyderabad  |  Page ")
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(9)
        r1.font.color.rgb = RGBColor(120, 120, 120)
        
        # XML snippet for dynamic page number
        fldSimple = OxmlElement('w:fldSimple')
        fldSimple.set(qn('w:instr'), 'PAGE')
        fp._p.append(fldSimple)

def build_docx_report():
    doc = Document()
    
    # Page setup - Margins: Left 1.25", Right 1.0", Top 1.0", Bottom 1.0"
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # Set default style to Times New Roman, 12pt, 1.5 line spacing, Justified
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(40, 40, 40)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def p(text="", bold_prefix="", space_after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        para = doc.add_paragraph()
        para.alignment = align
        para.paragraph_format.line_spacing = 1.5
        para.paragraph_format.space_after = Pt(space_after)
        if bold_prefix:
            run_b = para.add_run(bold_prefix)
            run_b.bold = True
            run_b.font.name = 'Times New Roman'
            run_b.font.size = Pt(12)
        if text:
            run_t = para.add_run(text)
            run_t.font.name = 'Times New Roman'
            run_t.font.size = Pt(12)
        return para

    def h1(title):
        para = doc.add_paragraph()
        para.paragraph_format.space_before = Pt(16)
        para.paragraph_format.space_after = Pt(8)
        para.paragraph_format.keep_with_next = True
        run = para.add_run(title)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(26, 54, 93)  # Navy blue
        return para

    def h2(title):
        para = doc.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        para.paragraph_format.space_after = Pt(6)
        para.paragraph_format.keep_with_next = True
        run = para.add_run(title)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13.5)
        run.font.color.rgb = RGBColor(30, 41, 59)
        return para

    def h3(title):
        para = doc.add_paragraph()
        para.paragraph_format.space_before = Pt(8)
        para.paragraph_format.space_after = Pt(4)
        para.paragraph_format.keep_with_next = True
        run = para.add_run(title)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(51, 65, 85)
        return para

    def add_table_data(headers, rows_data, col_widths=None):
        table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        # Header row
        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            hdr_cells[i].text = header_text
            set_cell_background(hdr_cells[i], "1A365D")  # Dark Navy
            set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10.5)
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)

        # Body rows
        for r_idx, row in enumerate(rows_data):
            row_cells = table.rows[r_idx + 1].cells
            bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, cell_value in enumerate(row):
                row_cells[c_idx].text = str(cell_value)
                set_cell_background(row_cells[c_idx], bg_color)
                set_cell_margins(row_cells[c_idx], top=90, bottom=90, left=130, right=130)
                p = row_cells[c_idx].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx != 0 else WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(10)
                    run.font.color.rgb = RGBColor(30, 41, 59)

        if col_widths:
            for row in table.rows:
                for c_idx, width in enumerate(col_widths):
                    row.cells[c_idx].width = width

        # Border styling via XML
        tblPr = table._tbl.tblPr
        tblBorders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
            f'<w:insideV w:val="none"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(tblBorders)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_figure(img_rel_path, caption_text, width=Inches(5.8)):
        img_full_path = Path(img_rel_path)
        if img_full_path.exists():
            para_img = doc.add_paragraph()
            para_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para_img.paragraph_format.space_before = Pt(8)
            para_img.paragraph_format.space_after = Pt(4)
            para_img.paragraph_format.keep_with_next = True
            run_img = para_img.add_run()
            run_img.add_picture(str(img_full_path), width=width)

            para_cap = doc.add_paragraph()
            para_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para_cap.paragraph_format.space_before = Pt(2)
            para_cap.paragraph_format.space_after = Pt(12)
            run_cap = para_cap.add_run(caption_text)
            run_cap.font.name = 'Times New Roman'
            run_cap.font.size = Pt(10)
            run_cap.font.italic = True
            run_cap.font.color.rgb = RGBColor(70, 70, 70)

    # =========================================================================
    # 1. TITLE PAGE
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(10)
    p_inst.paragraph_format.space_after = Pt(2)
    r = p_inst.add_run("ACE ENGINEERING COLLEGE")
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(17)
    r.font.color.rgb = RGBColor(26, 54, 93)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_after = Pt(16)
    r = p_dept.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\nAn Autonomous Institution | Accredited by NBA & NAAC 'A' Grade\nAnkushapur, Ghatkesar, Medchal-Malkajgiri District, Hyderabad, Telangana – 501301")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(80, 80, 80)

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_before = Pt(14)
    p_rep.paragraph_format.space_after = Pt(14)
    r = p_rep.add_run("ONE-WEEK TECHNICAL PROJECT REPORT")
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.color.rgb = RGBColor(180, 83, 9)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(6)
    r = p_title.add_run("FLIPKART PRODUCT PRICE ANALYSIS")
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(20)
    r.font.color.rgb = RGBColor(26, 54, 93)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(24)
    r = p_sub.add_run("An Exploratory Data Analysis and Machine Learning-Based Approach to\nProduct Pricing Dynamics, Markdown Strategy, and Market Segmentation")
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(71, 85, 105)

    p_subm = doc.add_paragraph()
    p_subm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subm.paragraph_format.space_before = Pt(10)
    p_subm.paragraph_format.space_after = Pt(4)
    r = p_subm.add_run("Submitted by")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.italic = True

    p_cand = doc.add_paragraph()
    p_cand.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cand.paragraph_format.space_after = Pt(20)
    r = p_cand.add_run("[Enter Student Name]\n")
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r2 = p_cand.add_run("Roll Number: [Enter Roll Number]\nBranch & Year: B.Tech Computer Science and Engineering, [Enter Year]\nAcademic Year: 2026–2027\nProject Duration: [Start Date] to [End Date]")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(11)

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_before = Pt(10)
    p_guide.paragraph_format.space_after = Pt(4)
    r = p_guide.add_run("Under the Guidance of\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.italic = True
    r_gname = p_guide.add_run("[Name and Designation]\n")
    r_gname.bold = True
    r_gname.font.name = 'Times New Roman'
    r_gname.font.size = Pt(12)
    r_inst = p_guide.add_run("Organization / Training Institute: Self-Directed Technical Project\nDepartment of Computer Science and Engineering\nACE Engineering College, Hyderabad")
    r_inst.font.name = 'Times New Roman'
    r_inst.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    h1("TABLE OF CONTENTS")
    toc_data = [
        ("1. Certificate", "2"),
        ("2. Acknowledgement", "3"),
        ("3. Abstract", "4"),
        ("4. Introduction", "5"),
        ("    4.1 Background", "5"),
        ("    4.2 Project Overview", "6"),
        ("    4.3 Motivation", "6"),
        ("    4.4 Need for the Project", "7"),
        ("    4.5 Intended Users", "7"),
        ("5. Objectives of the Project", "8"),
        ("    5.1 Primary Objective", "8"),
        ("    5.2 Specific Objectives", "8"),
        ("    5.3 Expected Outcomes", "9"),
        ("6. Problem Statement and Scope", "10"),
        ("    6.1 Problem Statement", "10"),
        ("    6.2 Proposed Solution", "10"),
        ("    6.3 Project Scope", "11"),
        ("    6.4 Assumptions and Limitations", "12"),
        ("7. Tools and Technologies Used", "13"),
        ("    7.1 Technology Stack Summary", "13"),
        ("    7.2 Technology Selection Rationale", "14"),
        ("8. System Design and Methodology", "15"),
        ("    8.1 High-Level System Architecture", "15"),
        ("    8.2 Data Processing Workflow", "16"),
        ("    8.3 Data Cleaning and Preprocessing Pipeline", "16"),
        ("    8.4 Exploratory Data Analysis Framework", "17"),
        ("    8.5 Supervised Machine Learning Methodology", "18"),
        ("    8.6 Unsupervised Product Clustering Methodology", "19"),
        ("    8.7 Interactive Dashboard Architecture", "20"),
        ("    8.8 Major Application Modules", "20"),
        ("9. Day-Wise Progress Report (Day 1 to Day 7)", "22"),
        ("10. Implementation and Results", "25"),
        ("    10.1 Repository and File Organization", "25"),
        ("    10.2 Dataset Description and Integrity", "25"),
        ("    10.3 Data Cleaning Results and Reconciliation", "26"),
        ("    10.4 Exploratory Data Analysis Results", "28"),
        ("    10.5 Data Visualizations and Statistical Interpretation", "30"),
        ("    10.6 Price Prediction Model Development", "33"),
        ("    10.7 Model Performance Comparison and Benchmarks", "34"),
        ("    10.8 Feature Importance and Model Explainability", "35"),
        ("    10.9 Product Pricing Segmentation (K-Means Results)", "36"),
        ("    10.10 Streamlit Interactive Dashboard Implementation", "38"),
        ("    10.11 Verification, Testing and Validation", "40"),
        ("11. Learning Outcomes", "41"),
        ("12. Challenges Faced and Solutions", "42"),
        ("13. Conclusion and Future Scope", "44"),
        ("    13.1 Conclusion", "44"),
        ("    13.2 Future Scope", "44"),
        ("14. References", "46"),
        ("15. Appendices and Supporting Evidence", "48"),
        ("    Appendix A: Complete Project Folder Hierarchy", "48"),
        ("    Appendix B: Core Ingestion and Cleaning Scripts", "49"),
        ("    Appendix C: Feature Engineering and Modeling Code", "51"),
        ("    Appendix D: Streamlit Web Dashboard Source Code", "53"),
        ("    Appendix E: Complete Figures and Visual Evidence Catalog", "55"),
        ("    Appendix F: Data Quality Audit Verification", "58"),
        ("16. Mentor Evaluation Sheet", "60"),
        ("17. Final Declaration", "61")
    ]
    for item, page in toc_data:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_after = Pt(2)
        p_toc.paragraph_format.line_spacing = 1.15
        r_item = p_toc.add_run(item)
        r_item.font.name = 'Times New Roman'
        r_item.font.size = Pt(11)
        if not item.startswith("    "):
            r_item.bold = True
        # Dot leader simulation
        dots_count = max(5, 75 - len(item) * 1)
        r_dots = p_toc.add_run(" " + "." * dots_count + " ")
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(160, 160, 160)
        r_pg = p_toc.add_run(page)
        r_pg.bold = True
        r_pg.font.name = 'Times New Roman'
        r_pg.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # 2. CERTIFICATE
    # =========================================================================
    h1("1. CERTIFICATE")
    p("This is to certify that the technical project report entitled “FLIPKART PRODUCT PRICE ANALYSIS: An Exploratory Data Analysis and Machine Learning-Based Approach to Product Pricing and Discount Analysis” is a bonafide record of independent technical work carried out by [Enter Student Name], bearing Roll Number [Enter Roll Number], in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering from ACE Engineering College, Hyderabad, affiliated to Jawaharlal Nehru Technological University Hyderabad (JNTUH), during the academic period [Start Date] to [End Date].")
    p("The project explores exploratory data analysis, data hygiene, statistical hypothesis testing, data leakage prevention, supervised regression modeling (Ridge Regression, Random Forest Regressor, Gradient Boosting Regressor), unsupervised K-Means product pricing segmentation, and interactive web application deployment using Python, Scikit-learn, Plotly, and Streamlit.")
    p("To the best of my knowledge, the results and analytical findings presented in this report have been verified against actual project code and empirical datasets, and have not been submitted elsewhere for the award of any other degree, diploma, or certificate.")
    
    doc.add_paragraph().paragraph_format.space_before = Pt(36)
    sig_p = doc.add_paragraph()
    sig_p.paragraph_format.line_spacing = 1.5
    sig_p.add_run("_______________________________\t\t_______________________________\n").bold = True
    sig_p.add_run("Internal Project Guide / Mentor\t\tHead of the Department (CSE)\n").bold = True
    sig_p.add_run("[Name and Designation]\t\tDepartment of Computer Science & Engg.\n")
    sig_p.add_run("ACE Engineering College, Hyderabad\t\tACE Engineering College, Hyderabad\n\n\n")
    sig_p.add_run("Date: _________________________\t\tPlace: Hyderabad, Telangana\n")
    sig_p.add_run("Seal / Stamp of the Institution:")

    doc.add_page_break()

    # =========================================================================
    # 3. ACKNOWLEDGEMENT
    # =========================================================================
    h1("2. ACKNOWLEDGEMENT")
    p("I would like to express my sincere gratitude and deep appreciation to ACE Engineering College, Hyderabad, and the Department of Computer Science and Engineering for providing an intellectually stimulating environment and the technical infrastructure necessary to conduct this technical project.")
    p("I am profoundly grateful to my internal project guide and faculty mentor, [Name and Designation], for their constant encouragement, insightful feedback, rigorous reviews, and patient guidance throughout the stages of problem identification, exploratory data analysis, machine learning formulation, and technical report preparation.")
    p("I extend my respectful regards to the Head of the Department of Computer Science and Engineering for their continuous support, administrative facilitation, and motivation towards undertaking practical, industry-aligned data science projects.")
    p("I also acknowledge the global open-source data science community, specifically the developers and maintainers of Python, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Plotly, and Streamlit. Their open software, rich documentation, and active developer ecosystems provided the foundational tools used throughout this analysis.")
    p("Finally, I express my heartfelt thanks to my parents, family members, and peers whose encouragement, constructive suggestions, and moral support were instrumental in completing this technical project within the designated one-week timeline.")
    
    p_ack_sig = doc.add_paragraph()
    p_ack_sig.paragraph_format.space_before = Pt(24)
    p_ack_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_ack_sig.add_run("[Enter Student Name]\nRoll Number: [Enter Roll Number]\nDepartment of Computer Science and Engineering\nACE Engineering College, Hyderabad")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # 4. ABSTRACT
    # =========================================================================
    h1("3. ABSTRACT")
    p("In competitive electronic commerce ecosystems, pricing strategy and promotional markdown structures are pivotal determinants of consumer conversion, seller inventory velocity, and marketplace gross merchandise value (GMV). While digital retail platforms host millions of concurrent listings, establishing optimal pricing architectures remains challenging due to heavy price skewness, unstructured category trees, inconsistent brand labeling, and opaque discount distributions. Furthermore, classical retail models frequently suffer from target leakage by inappropriately using markdown features to predict consumer transaction prices.")
    p("This technical project presents Flipkart Product Price Analysis, an end-to-end data analytics and predictive modeling system developed on a genuine real-world catalog of 20,000 Flipkart product listings across 262 primary categories. The study establishes an immutable data pipeline that audits schema consistency, parses nested taxonomic hierarchies, reconciles missing brand identities into an explicit 'Unbranded / Generic' cohort (5,851 products), and isolates 78 invalid price records (0.39%) without synthetic distortion to yield a clean cohort of 19,922 records.")
    p("Exploratory Data Analysis (EDA) reveals severe positive price skewness (+28.43 for selling price), with a median selling price of ₹550 against an arithmetic mean of ₹1,973, driven by luxury outliers reaching ₹571,230. A dominant markdown culture is identified, where the median discount is 45.00% and 45.85% of products receive discounts of 50% or greater. Crucially, empirical hypothesis testing proves that customer satisfaction star ratings are completely independent of discount depths (Pearson correlation r = -0.0020), disproving the assumption that heavy discounts degrade consumer reputation.")
    p("For supervised modeling, strict architectural barriers prevent target leakage by excluding all discount derivations. An 80:20 train-test evaluation across four algorithms establishes that the Gradient Boosting Regressor achieves superior performance with an R² score of 0.9807 and RMSE of ₹838.82, while Random Forest achieves the lowest Mean Absolute Error of ₹267.11, vastly outperforming the median baseline (R² = -0.0536). Unsupervised K-Means clustering, mathematically validated via Elbow analysis and Silhouette scoring (0.3973), segments the catalog into four strategic market archetypes: Mass-Market Deep Discount (43.0%), Mid-Range Moderate Discount (24.8%), Premium / Luxury Niche (5.5%), and Low-Discount Essentials (26.7%). The complete platform is deployed as an interactive, multi-page web dashboard using Streamlit and Plotly, enabling dynamic category filtering, interactive visualizations, and real-time inference for pricing recommendations.")
    p("Keywords: Data Analytics, E-Commerce Pricing, Exploratory Data Analysis, Data Leakage Prevention, Gradient Boosting, Random Forest, K-Means Clustering, Market Segmentation, Streamlit, Plotly.", bold_prefix="Keywords: ")

    doc.add_page_break()

    # =========================================================================
    # 5. INTRODUCTION
    # =========================================================================
    h1("4. INTRODUCTION")
    
    h2("4.1 Background")
    p("The rapid expansion of Indian electronic commerce over the past decade has reshaped consumer retail behavior. Platforms such as Flipkart, Amazon India, and Myntra host millions of active stock-keeping units (SKUs) across diversified verticals including apparel, consumer electronics, jewelry, automotive components, and personal care. In this digital marketplace, consumer purchase behavior is heavily influenced by price transparency, real-time comparisons, and promotional discounts.")
    p("Unlike traditional brick-and-mortar retail, where price adjustments entail physical re-tagging and operational overhead, online retail platforms feature dynamic pricing environments. Retailers adjust prices in response to competitor activity, seasonal demand surges (e.g., festive sales such as Flipkart's Big Billion Days), inventory aging, and algorithmic promotions. However, this velocity introduces significant analytical complexity. Sellers frequently struggle to determine optimal pricing boundaries, often relying on arbitrary deep discounting that erodes gross margins, while marketplace operators require visibility into category-level margin structures and price elasticity.")

    h2("4.2 Project Overview")
    p("Flipkart Product Price Analysis is a comprehensive data analytics and machine learning project engineered to extract quantitative intelligence from large-scale e-commerce catalog data. Operating on an authentic dataset of Flipkart product listings, the project establishes a rigorous, multi-tiered analytical pipeline spanning:")
    p("1. Ingestion and programmatic schema auditing of 20,000 raw catalog listings.\n"
      "2. Data hygiene, including nested string taxonomy parsing, missing value reconciliation, and data integrity verification.\n"
      "3. In-depth statistical and visual exploratory data analysis across retail price benchmarks, selling prices, promotional markdowns, and customer ratings.\n"
      "4. Leakage-free supervised regression modeling comparing baseline linear models against ensemble architectures (Random Forest and Gradient Boosting) to predict final selling prices.\n"
      "5. Unsupervised product clustering using K-Means to identify natural pricing segments within the e-commerce catalog.\n"
      "6. Deployment of an interactive, responsive analytical web dashboard engineered with Streamlit and Plotly.")

    h2("4.3 Motivation")
    p("The motivation behind this project stems from the desire to bridge the gap between academic data science theory and real-world commercial analytics. Modern retail decision-making relies on data-driven pricing intelligence. By analyzing authentic product listings, this project provides direct exposure to challenges encountered by professional data analysts, such as extreme price skewness, unstructured string formats, high-cardinality categorical variables, rating sparsity, and the critical danger of data leakage in predictive modeling.")

    h2("4.4 Need for the Project")
    p("The commercial and technical necessities addressed by this project include:")
    p("• Understanding Price Skewness: Identifying why arithmetic means fail in retail pricing and establishing robust non-parametric metrics (medians and interquartile ranges).\n"
      "• Deconstructing Promotional Markdowns: Quantifying whether e-commerce platforms rely on genuine markdowns or artificial Maximum Retail Price (MRP) anchoring.\n"
      "• Testing Reputation Elasticity: Statistically verifying whether aggressive discounting damages perceived product quality and customer star ratings.\n"
      "• Developing Leakage-Free Predictive Models: Demonstrating that predictive pricing models must avoid using target-derived features (such as discount percentage) to maintain production validity.\n"
      "• Catalog Segmentation for Merchants: Providing retailers with empirical pricing archetypes to position new products strategically without margin erosion.\n"
      "• Delivering Accessible Business Dashboards: Translating complex statistical findings into intuitive, interactive visual tools for non-technical stakeholders.")

    h2("4.5 Intended Users")
    p("The primary beneficiaries and intended users of this analytical system include:")
    p("1. E-Commerce Merchants & Sellers: Retailers seeking data-backed pricing guidance, optimal discount corridors, and competitor benchmark intelligence.\n"
      "2. Category Managers & Marketplace Operators: Platform executives responsible for vertical profitability, promotional budgeting, and seller compliance.\n"
      "3. Business Intelligence & Pricing Analysts: Analysts seeking reusable pipelines for price elasticity analysis and regression modeling.\n"
      "4. Data Science Students & Researchers: Academic learners examining practical implementations of feature engineering, leakage prevention, ensemble regression, and cluster validation.")

    doc.add_page_break()

    # =========================================================================
    # 6. OBJECTIVES OF THE PROJECT
    # =========================================================================
    h1("5. OBJECTIVES OF THE PROJECT")

    h2("5.1 Primary Objective")
    p("The primary objective of this project is to design, implement, and evaluate a comprehensive data analytics and machine learning pipeline that explores e-commerce pricing behavior, identifies strategic discount dynamics, predicts product selling prices without data leakage, segments catalog offerings into commercial archetypes, and surfaces actionable intelligence through an interactive web dashboard.")

    h2("5.2 Specific Objectives")
    p("To achieve the primary objective, the following specific technical and analytical goals were established:")
    p("1. Data Sourcing and Verification: Sourced an authentic, publicly accessible Flipkart product dataset comprising 20,000 listings across 15 attributes, verifying source provenance and establishing an immutable raw data repository.\n"
      "2. Data Governance and Cleaning: Developed modular Python routines to clean raw fields, isolate invalid pricing records (78 rows), parse nested category hierarchy strings into three taxonomic levels, reconcile missing brand labels (5,851 rows) as 'Unbranded / Generic', and transform rating placeholders into numeric scores.\n"
      "3. Feature Engineering: Formulated derived analytical attributes including discount amount, discount percentage, five discrete discount tiers, five retail price tiers, natural logarithmic price transforms, and text length metrics.\n"
      "4. Statistical Exploratory Analysis: Conducted univariate, bivariate, and multivariate exploratory data analysis examining price asymmetry, parity line alignments, category-level discount depths, brand pricing power, and rating correlations.\n"
      "5. Supervised Model Engineering: Implemented, trained, and benchmarked four regression models—Simple Baseline (Median), Ridge Regression, Random Forest Regressor, and Gradient Boosting Regressor—evaluating them using Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and Coefficient of Determination (R²) on an 80:20 holdout split while enforcing strict zero-leakage constraints.\n"
      "6. Unsupervised Market Segmentation: Engineered a K-Means clustering pipeline utilizing standardized pricing features, mathematically determining optimal cluster counts (k=4) via the Elbow Method and Silhouette analysis to characterize distinct catalog archetypes.\n"
      "7. Interactive Dashboard Deployment: Engineered a responsive multi-page web application using Streamlit and Plotly, enabling interactive category filtering, dynamic visual exploration, live machine learning price inference, and cluster inspection.")

    h2("5.3 Expected Outcomes")
    p("The anticipated deliverables and outcomes of this project include:")
    p("• A clean, documented project repository following professional modular software engineering standards.\n"
      "• Processed datasets (flipkart_cleaned.csv) enriched with engineered features and cluster assignments.\n"
      "• A formal data quality and tier validation report.\n"
      "• Eleven publication-grade, high-resolution statistical visualizations.\n"
      "• Serialized machine learning model artifacts capable of instant real-time inference.\n"
      "• A live, fully operational Streamlit web dashboard.\n"
      "• Comprehensive academic documentation including technical reports, viva preparation materials, and reproducible code scripts.")

    doc.add_page_break()

    # =========================================================================
    # 7. PROBLEM STATEMENT AND SCOPE
    # =========================================================================
    h1("6. PROBLEM STATEMENT AND SCOPE")

    h2("6.1 Problem Statement")
    p("Modern e-commerce retail platforms feature immense catalog diversity spanning hundreds of product categories and thousands of competing brands. However, navigating this commercial environment presents substantial data-centric challenges. Product listings frequently contain missing values, highly unstructured text hierarchy representations, and inconsistent brand naming conventions. Furthermore, retail pricing distributions exhibit severe right-skewness, rendering traditional parametric statistical assumptions invalid.")
    p("From a commercial standpoint, retailers frequently lack quantitative guidance on optimal discount corridors, leading to either uncompetitive overpricing or margin-destroying excessive discounting. Crucially, academic and industrial predictive pricing models frequently suffer from target data leakage—unintentionally including discount percentages or target-derived values as input features—resulting in models that demonstrate near-perfect training metrics but fail completely when deployed in production. There is a clear need for a methodologically sound, leakage-free analytical system that accurately characterizes e-commerce pricing dynamics and delivers actionable pricing intelligence.")

    h2("6.2 Proposed Solution")
    p("This project proposes an end-to-end data analytics and machine learning solution structured into three major phases:")
    p("1. Transparent Data Hygiene Engine: A modular preprocessing architecture that maintains raw dataset immutability, standardizes prices, tokenizes nested hierarchical categories, and systematically tags missing metadata without synthetic fabrication.\n"
      "2. Rigorous Analytical & Modeling Framework: An analytical engine that computes robust non-parametric metrics (medians, percentiles, IQR), applies logarithmic transformations to stabilize price variance, enforces strict feature leakage guards, benchmarks ensemble regression architectures, and applies validated K-Means clustering to segment the product landscape.\n"
      "3. Interactive Business Intelligence Interface: A centralized Streamlit web application that translates complex statistical distributions into intuitive Plotly charts and enables real-time price prediction for commercial users.")

    h2("6.3 Project Scope")
    p("The boundary and scope of this technical investigation are defined as follows:")
    p("In-Scope Components:\n"
      "• Ingestion, validation, and cleaning of the 20,000-record Flipkart product dataset.\n"
      "• Feature engineering of discount amounts, discount percentages, pricing tiers, and log-transformed attributes.\n"
      "• Univariate, bivariate, and multivariate statistical exploration and chart generation.\n"
      "• Training, evaluation, and comparison of Simple Baseline, Ridge, Random Forest, and Gradient Boosting models.\n"
      "• K-Means clustering across k = 2 to 6, with Elbow and Silhouette diagnostics.\n"
      "• Development and local deployment of a seven-page interactive Streamlit dashboard.\n"
      "• Comprehensive technical documentation and viva defense preparation.")
    p("Out-of-Scope / Future Components:\n"
      "• Real-time web scraping of live Flipkart listings during active production sessions.\n"
      "• Multi-seller Buy Box tracking (the dataset does not include individual merchant IDs for multi-seller listings).\n"
      "• Longitudinal time-series price forecasting across multi-month sales calendars.\n"
      "• Computer vision modeling on product image URLs or deep transformer NLP on full textual descriptions.")

    h2("6.4 Assumptions and Limitations")
    p("The findings and models presented in this report operate under the following technical assumptions and empirical limitations:")
    p("1. Catalog Snapshot Assumption: The dataset represents a discrete crawled snapshot of Flipkart's product catalog. Prices and discounts reflect market conditions at the time of data collection and do not reflect subsequent inflation or platform policy changes.\n"
      "2. Product-Level Segmentation: Because the dataset lacks individual seller identifiers, unsupervised clustering segments product pricing strategies across the catalog rather than profiling individual merchant behaviors.\n"
      "3. Rating Sparsity: Only 9.23% (1,839 items) of the catalog listings possess numerical customer ratings. While this cohort is statistically sufficient for correlation testing, rating findings must be interpreted with awareness of the unrated long-tail.\n"
      "4. Static Price Independence: The model assumes that retail price (MRP) and category taxonomies serve as independent anchor features for estimating discounted selling prices.")

    doc.add_page_break()

    # =========================================================================
    # 8. TOOLS AND TECHNOLOGIES USED
    # =========================================================================
    h1("7. TOOLS AND TECHNOLOGIES USED")

    h2("7.1 Technology Stack Summary")
    p("The technical stack was chosen to ensure high computational efficiency, reproducibility, statistical rigor, and modern interactive visualization. Table 7.1 outlines the primary technologies deployed.")
    
    p("Table 7.1: Comprehensive Tools and Technologies Stack", bold_prefix="Table 7.1: ", space_after=4)
    tech_headers = ["Category", "Technology / Library", "Version", "Functional Purpose in Project"]
    tech_rows = [
        ["Programming Language", "Python", "3.10.1 (64-bit)", "Core execution runtime for data processing and modeling."],
        ["Data Manipulation", "Pandas", "2.3.3", "Tabular data ingestion, cleaning, grouping, and feature engineering."],
        ["Numerical Computing", "NumPy", "2.2.6", "Vectorized array arithmetic, log transformations, and statistical metrics."],
        ["Machine Learning", "Scikit-Learn", "1.7.2", "Preprocessing, train-test splitting, Ridge, Random Forest, Gradient Boosting, K-Means."],
        ["Scientific Computing", "SciPy", "1.15.3", "Underlying optimization algorithms and statistical distributions."],
        ["Static Visualization", "Matplotlib", "3.10.9", "Foundation plotting engine for publication-grade 300-DPI charts."],
        ["Statistical Plotting", "Seaborn", "0.13.2", "High-level statistical visualization (KDE, boxplots, heatmaps)."],
        ["Interactive Visuals", "Plotly", "7.1.0", "Dynamic web-ready interactive charts with hover and zoom controls."],
        ["Web Application", "Streamlit", "1.40.1", "Rapid deployment framework for the multi-page analytics dashboard."],
        ["Model Serialization", "Joblib", "1.6.0", "Serializing trained pipelines and encoders for low-latency web inference."],
        ["Development Env", "Visual Studio Code", "Latest", "Code authoring, debugging, script execution, and Git management."],
        ["Version Control", "Git & GitHub", "Latest", "Source code versioning, repository management, and tracking."]
    ]
    add_table_data(tech_headers, tech_rows, [Inches(1.5), Inches(1.8), Inches(1.2), Inches(2.7)])

    h2("7.2 Technology Selection Rationale")
    p("• Python 3.10: Selected for its mature ecosystem in data science, 64-bit memory management, and compatibility with modern machine learning binaries.\n"
      "• Pandas & NumPy: Form the backbone of modern data science, providing optimized C-level implementations for high-speed indexing, grouping, and vectorized transformations.\n"
      "• Scikit-Learn: Provides a unified, battle-tested API for both supervised regression and unsupervised clustering, with integrated pipelines (ColumnTransformer, StandardScaler) that prevent data leakage.\n"
      "• Matplotlib & Seaborn: Provide complete control over typography, axes, and color palettes, ensuring static figures adhere to formal academic publication standards.\n"
      "• Plotly & Streamlit: Enable pure-Python web dashboard engineering without requiring complex JavaScript or React frontends, allowing rapid prototyping of interactive business intelligence applications.")

    doc.add_page_break()

    # =========================================================================
    # 9. SYSTEM DESIGN AND METHODOLOGY
    # =========================================================================
    h1("8. SYSTEM DESIGN AND METHODOLOGY")

    h2("8.1 High-Level System Architecture")
    p("The architecture of Flipkart Product Price Analysis follows a decoupled, modular design organized into four sequential layers: Ingestion & Hygiene, Feature Engineering, Modeling & Intelligence, and Presentation. Figure 8.1 illustrates the conceptual flow of data across the platform.")
    
    p("Figure 8.1: High-Level Conceptual System Architecture\n"
      "[Raw CSV: 20,000 Rows] ──► [Data Loader & Schema Audit] ──► [Data Cleaning & Hierarchy Parser]\n"
      "                                                                       │\n"
      "                                                                       ▼\n"
      "[Streamlit Web Dashboard] ◄── [Trained Models & Clusters] ◄── [Feature Engineering & Storage]\n"
      "  (7 Interactive Pages)         (Ridge, RF, GB, K-Means)       (data/processed/flipkart_cleaned.csv)",
      bold_prefix="Figure 8.1: High-Level Conceptual System Architecture\n", align=WD_ALIGN_PARAGRAPH.CENTER)

    h2("8.2 Data Processing Workflow")
    p("The operational data workflow transitions raw, unverified catalog records into clean, validated analytical data frames:")
    p("1. Ingestion: Raw data is read with UTF-8 encoding from data/raw/flipkart_com-ecommerce_sample.csv.\n"
      "2. Validation: Column data types and row integrity are evaluated against schema constraints.\n"
      "3. Price Sanitization: Records with missing or non-positive retail/discounted prices are filtered out.\n"
      "4. Taxonomic Parsing: Nested string category trees are split into primary, sub, and micro categories.\n"
      "5. Metadata Governance: Missing brand identities are labeled 'Unbranded / Generic', and non-numeric ratings are converted to NaNs.\n"
      "6. Analytical Enrichment: Derived pricing metrics, bins, and log transforms are generated and persisted to data/processed/flipkart_cleaned.csv.")

    h2("8.3 Data Cleaning and Preprocessing Pipeline")
    p("Data cleaning was implemented as a deterministic Python module in src/cleaning.py. Table 8.1 summarizes the transformation rules applied to each raw attribute.")

    p("Table 8.1: Data Preprocessing and Transformation Protocol", bold_prefix="Table 8.1: ", space_after=4)
    prep_headers = ["Attribute", "Raw Condition", "Applied Transformation", "Analytical Justification"]
    prep_rows = [
        ["retail_price", "78 missing values / string numbers", "Convert to float64; drop non-positive or missing rows", "Target predictor; cannot be fabricated or imputed."],
        ["discounted_price", "78 missing values / string numbers", "Convert to float64; drop non-positive or missing rows", "Primary target variable; must be authentic."],
        ["product_category_tree", "Nested bracketed string: ['Cat >> Sub >> Micro']", "Strip delimiters, split on '>>', extract 3 levels", "Enables category-specific price elasticity analysis."],
        ["brand", "5,864 missing values / whitespace strings", "Strip whitespace; impute missing with 'Unbranded / Generic'", "Prevents misclassifying product title tokens as brands."],
        ["product_rating", "18,151 'No rating available' strings", "Replace string with NaN; cast valid values to float64", "Separates unrated long-tail from rated products."],
        ["is_FK_Advantage_product", "String 'false' / 'true'", "Cast to native boolean True/False", "Standardizes binary seller assurance badge."],
        ["crawl_timestamp", "String timestamp format", "Parse into ISO datetime64[ns]", "Enables temporal indexing of crawl period."]
    ]
    add_table_data(prep_headers, prep_rows, [Inches(1.5), Inches(1.8), Inches(2.2), Inches(1.7)])

    h2("8.4 Exploratory Data Analysis Framework")
    p("The exploratory framework in src/eda_analysis.py computes descriptive, bivariate, and multivariate statistics to profile catalog dynamics. It evaluates:")
    p("• Central Tendency & Dispersion: Medians, Means, Standard Deviations, and Interquartile Ranges.\n"
      "• Distribution Shape: Histogram binning and Kernel Density Estimation (KDE) to quantify skewness.\n"
      "• Price Parity & Alignment: Scatter plotting against the 45-degree parity reference line ($y = x$).\n"
      "• Category & Brand Margins: Comparative bar plotting of median markdowns across top verticals.\n"
      "• Correlation Matrix: Pearson and Spearman rank correlation matrices across numerical attributes.")

    h2("8.5 Supervised Machine Learning Methodology")
    p("The regression framework in models/train_price_predictor.py predicts discounted_price using product characteristics while enforcing strict data leakage prevention:")
    p("1. Train-Test Partitioning: The clean dataset (19,922 rows) is partitioned into an 80% training set (15,937 samples) and a 20% testing holdout set (3,985 samples) using random_state=42.\n"
      "2. Feature Preprocessing (ColumnTransformer): Numerical features are scaled via StandardScaler. High-cardinality categorical features (primary_category, brand) are encoded via OneHotEncoder with min_frequency=30, grouping rare categories and brands into an infrequent bin to prevent dimensionality explosion and overfitting.\n"
      "3. Model Architecture Selection:\n"
      "   • Simple Baseline: Predicts the median training target price.\n"
      "   • Ridge Regression: Regularized linear model with an L2 penalty ((alpha = 10.0)).\n"
      "   • Random Forest Regressor: 100 decision trees with max_depth=15 and min_samples_split=5.\n"
      "   • Gradient Boosting Regressor: 120 sequential boosting stages with learning_rate=0.08 and max_depth=6.\n"
      "4. Evaluation Metrics: Models are evaluated on unseen test data using Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and the Coefficient of Determination (R²).")

    h2("8.6 Unsupervised Product Clustering Methodology")
    p("Product market segmentation was engineered in models/cluster_products.py using K-Means Clustering:")
    p("1. Feature Selection: Standardized log_retail_price, log_discounted_price, and discount_percentage.\n"
      "2. Normalization: Applied StandardScaler to eliminate scale divergence between prices and percentages.\n"
      "3. Optimal k Determination: Evaluated cluster counts $k in [2, 6]$ using Within-Cluster Sum of Squares (Inertia / Elbow Method) and Silhouette Analysis.\n"
      "4. Dimensionality Reduction: Applied Principal Component Analysis (PCA) to project the 3D feature space onto two principal components for visual interpretation.")

    h2("8.7 Interactive Dashboard Architecture")
    p("The interactive dashboard in app/app.py is structured as a single-page multi-view application managed via Streamlit sidebar radio navigation. It utilizes st.cache_data for instantaneous dataset queries and st.cache_resource for serialized model loading, rendering seven functional modules.")

    h2("8.8 Major Application Modules")
    p("• Home & Overview: Displays top-level KPI metric cards and catalog volume distributions.\n"
      "• Data Overview: Features an interactive, filterable data browser with CSV export and data dictionary.\n"
      "• Price Analysis: Renders interactive scatter plots with parity lines and price distribution histograms.\n"
      "• Discount Analysis: Illustrates discount percentage distributions, tier breakdowns, and vertical margins.\n"
      "• Rating Analysis: Explores rating completeness and correlation with promotional discounts.\n"
      "• Machine Learning: Presents supervised benchmark tables, live real-time price estimation, and cluster profiles.\n"
      "• Insights & Conclusion: Synthesizes commercial takeaways, limitations, and academic conclusions.")

    doc.add_page_break()

    # =========================================================================
    # 10. DAY-WISE PROGRESS REPORT
    # =========================================================================
    h1("9. DAY-WISE PROGRESS REPORT (DAY 1 TO DAY 7)")
    p("The technical project was conducted over a structured seven-day engineering schedule. Table 9.1 documents the daily activities performed and verified deliverables produced.")

    p("Table 9.1: Daily Engineering Activities and Deliverables Log", bold_prefix="Table 9.1: ", space_after=4)
    day_headers = ["Day", "Engineering Activities Performed", "Verified Deliverables & Outcomes"]
    day_rows = [
        ["Day 1",
         "Formulated project problem statement; identified requirements for e-commerce pricing analytics; searched public repositories for genuine Flipkart catalog data; discovered PromptCloud dataset (20,000 listings); verified CC0 license; created project directory structure and downloaded flipkart_com-ecommerce_sample.csv into data/raw/.",
         "Raw dataset acquired (38.1 MB); verified 20,000 rows × 15 columns; SHA256 integrity hash recorded; initial project directory initialized."],
        ["Day 2",
         "Audited local Python environment; identified Python 3.10.1 (64-bit); prepared requirements.txt; resolved dependency versions; designed data ingestion module (src/data_loader.py); implemented cleaning engine (src/cleaning.py); parsed category trees; audited duplicates; handled missing prices.",
         "Dependencies installed (pandas 2.3.3, seaborn 0.13.2, etc.); data_loader.py and cleaning.py completed; 78 invalid price rows identified and dropped; missing brand reconciliation completed."],
        ["Day 3",
         "Developed feature engineering module (src/feature_engineering.py); computed discount amounts and percentages; established discount and price tier bins; calculated logarithmic price transforms; developed EDA script (src/eda_analysis.py); analyzed price skewness, parity lines, and rating dynamics.",
         "flipkart_cleaned.csv generated (19,922 rows × 31 columns); 7 high-resolution 300-DPI charts generated and saved in reports/figures/; empirical statistical findings documented."],
        ["Day 4",
         "Designed supervised regression architecture (models/train_price_predictor.py); established strict anti-leakage guards; constructed ColumnTransformer preprocessing pipeline; trained Simple Baseline, Ridge, Random Forest, and Gradient Boosting models; evaluated MAE, RMSE, and R².",
         "Model benchmark table generated; Gradient Boosting confirmed as best model (R² = 0.9807, RMSE = ₹838.82); Random Forest achieved lowest MAE (₹267.11); actual vs predicted and feature importance plots generated."],
        ["Day 5",
         "Designed unsupervised segmentation engine (models/cluster_products.py); standardized features; evaluated k from 2 to 6; generated Elbow and Silhouette curves; selected optimal k=4; profiled clusters by median price, discount, and category; mapped strategic market archetypes; ran PCA projections.",
         "K-Means clustering completed; 4 commercial segments profiled; Elbow and Silhouette curves generated; 2D cluster scatter plots produced; updated flipkart_cleaned.csv with cluster assignments."],
        ["Day 6",
         "Serialized best Gradient Boosting model and preprocessor to models/saved/price_model_artifacts.joblib; developed interactive Streamlit web dashboard (app/app.py); integrated Plotly charts; implemented interactive live price prediction calculator; tested local web server.",
         "Streamlit application completed; 7 responsive pages functional; live model inference verified; headless test executed successfully with HTTP status 200."],
        ["Day 7",
         "Conducted comprehensive verification and validation; audited code against data leakage rules; compiled complete data quality report; drafted 27 technical viva Q&A; authored comprehensive README.md; generated final academic DOCX and PDF reports.",
         "Final project report generated in DOCX and PDF formats; viva preparation guide compiled; project finalized for formal academic submission."]
    ]
    add_table_data(day_headers, day_rows, [Inches(1.0), Inches(3.2), Inches(3.0)])

    doc.add_page_break()

    # =========================================================================
    # 11. IMPLEMENTATION AND RESULTS
    # =========================================================================
    h1("10. IMPLEMENTATION AND RESULTS")

    h2("10.1 Repository and File Organization")
    p("The project repository is structured to cleanly separate data, source code, models, web applications, and documentation. Table 10.1 details the organization.")

    p("Table 10.1: Project Directory Structure and File Manifest", bold_prefix="Table 10.1: ", space_after=4)
    file_headers = ["Path / Directory", "Component Type", "Description & Role"]
    file_rows = [
        ["data/raw/", "Data Directory", "Houses the original immutable CSV (flipkart_com-ecommerce_sample.csv)."],
        ["data/processed/", "Data Directory", "Contains the clean, featured, and cluster-tagged dataset (flipkart_cleaned.csv)."],
        ["src/data_loader.py", "Python Source", "Ingests raw/clean datasets and executes duplicate identifier audits."],
        ["src/cleaning.py", "Python Source", "Parses category hierarchies, sanitizes prices, and labels unbranded items."],
        ["src/feature_engineering.py", "Python Source", "Generates discount metrics, tiers, log transforms, and enforces zero-leakage guards."],
        ["src/run_pipeline.py", "Python Source", "Automated runner executing end-to-end data processing."],
        ["src/eda_analysis.py", "Python Source", "Statistical script generating all 7 publication-grade EDA figures."],
        ["models/train_price_predictor.py", "Python Source", "Supervised learning script benchmarking Ridge, Random Forest, and Gradient Boosting."],
        ["models/cluster_products.py", "Python Source", "Unsupervised K-Means clustering script with Elbow and Silhouette diagnostics."],
        ["models/save_best_model.py", "Python Source", "Serializes trained Gradient Boosting pipeline for real-time web inference."],
        ["models/saved/", "Model Storage", "Houses serialized model artifacts (price_model_artifacts.joblib)."],
        ["app/app.py", "Web Application", "Full multi-page interactive Streamlit dashboard."],
        ["reports/figures/", "Visual Artifacts", "Houses all 11 high-resolution (300 DPI) generated figures."],
        ["reports/data_quality_report.md", "Documentation", "Formal data validation and before-and-after cleaning statistics."],
        ["reports/viva_questions_and_answers.md", "Documentation", "27 comprehensive technical viva questions and detailed answers."],
        ["requirements.txt", "Configuration", "Pinned package dependency manifest."],
        ["README.md", "Documentation", "Complete project manual and execution guide."]
    ]
    add_table_data(file_headers, file_rows, [Inches(2.2), Inches(1.5), Inches(3.5)])

    h2("10.2 Dataset Description and Integrity")
    p("The dataset captures e-commerce catalog listings from Flipkart. Each record represents a unique product listing characterized by identifiers, textual descriptions, category hierarchies, pricing points, ratings, and technical specifications. Table 10.2 provides the dataset verification metadata.")

    p("Table 10.2: Dataset Authentication and Verification Metadata", bold_prefix="Table 10.2: ", space_after=4)
    meta_headers = ["Metadata Property", "Dataset Verification Value"]
    meta_rows = [
        ["Original Dataset File", "flipkart_com-ecommerce_sample.csv"],
        ["Original Publisher", "PromptCloud / Kaggle (Mirrored on Hugging Face)"],
        ["Dataset License", "CC0: Public Domain (Open Access for Research & Analytics)"],
        ["Raw File Size", "38,114,963 bytes (~36.35 MB)"],
        ["Raw Checksum (SHA256)", "56F8F699C9E847356666C2EAB3C3AB1244340F6A98AD08E39EA2199EBE993AD1"],
        ["Raw Dimensions", "20,000 Rows × 15 Columns"],
        ["Cleaned Dimensions", "19,922 Rows × 31 Columns (Enriched with 16 analytical features)"],
        ["Integrity Status", "Verified authentic; strictly zero synthetic records generated."]
    ]
    add_table_data(meta_headers, meta_rows, [Inches(2.6), Inches(4.6)])

    h2("10.3 Data Cleaning Results and Reconciliation")
    p("Data cleaning successfully eliminated invalid values while preserving valid product listings. Table 10.3 contrasts the raw and cleaned datasets.")

    p("Table 10.3: Before-and-After Cleaning Statistical Reconciliation", bold_prefix="Table 10.3: ", space_after=4)
    clean_headers = ["Validation Metric", "Raw Dataset", "Cleaned Dataset", "Reconciliation Explanation"]
    clean_rows = [
        ["Total Row Count", "20,000", "19,922", "Dropped 78 rows (0.39%) with missing/invalid pricing."],
        ["Total Columns", "15", "31", "+16 engineered analytical features and hierarchy levels."],
        ["Missing Retail Prices", "78", "0", "100% positive, valid numeric values."],
        ["Missing Discounted Prices", "78", "0", "100% positive, valid numeric values."],
        ["Missing Brand Names", "5,864", "0", "Reconciled into explicit 'Unbranded / Generic' (5,851 rows)."],
        ["Rated Products Count", "1,849", "1,839", "Exactly 10 rated products lacked prices; remainder preserved."],
        ["Unrated Products Count", "18,151", "18,083", "Explicitly flagged with is_rated = 0."],
        ["Distinct Primary Categories", "Raw String Tree", "262", "Parsed cleanly from nested bracketed strings."]
    ]
    add_table_data(clean_headers, clean_rows, [Inches(1.8), Inches(1.2), Inches(1.2), Inches(3.0)])

    p("Brand Reconciliation Mathematical Proof:\n"
      "In the raw dataset, exactly 5,864 records lacked brand values. During cleaning, 78 records were removed due to missing price values. Exactly 13 of those 78 removed records also lacked brand values ($78 - 65 = 13$). Therefore, the number of clean records classified as 'Unbranded / Generic' is exactly:\n"
      "$$\text{Clean Unbranded Records} = 5,864 - 13 = 5,851$$",
      bold_prefix="Brand Reconciliation Mathematical Proof: ")

    h2("10.4 Exploratory Data Analysis Results")
    p("Statistical analysis confirms distinct commercial pricing behaviors across Flipkart's product catalog. Table 10.4 summarizes key descriptive metrics.")

    p("Table 10.4: Key Descriptive Pricing and Discount Statistics", bold_prefix="Table 10.4: ", space_after=4)
    stat_headers = ["Metric Property", "Retail Price (MRP)", "Discounted Selling Price", "Discount Percentage (%)"]
    stat_rows = [
        ["Minimum Value", "₹35.00", "₹35.00", "0.00% (Full MRP)"],
        ["25th Percentile (Q1)", "₹666.00", "₹350.00", "21.05%"],
        ["Median (50th Percentile)", "₹1,040.00", "₹550.00", "45.00%"],
        ["75th Percentile (Q3)", "₹1,999.00", "₹999.00", "59.97%"],
        ["Maximum Value", "₹571,230.00", "₹571,230.00", "96.53%"],
        ["Arithmetic Mean", "₹2,979.21", "₹1,973.40", "40.52%"],
        ["Standard Deviation", "₹9,009.64", "₹7,333.59", "23.55%"],
        ["Distribution Skewness", "+18.67 (Extreme Right)", "+28.43 (Extreme Right)", "-0.30 (Near Symmetric)"]
    ]
    add_table_data(stat_headers, stat_rows, [Inches(2.0), Inches(1.7), Inches(1.8), Inches(1.7)])

    h2("10.5 Data Visualizations and Statistical Interpretation")
    p("The exploratory analysis produced seven primary static figures illustrating key catalog dynamics:")

    p("1. Price Distribution & Skewness: Figure 10.1 displays the raw and log-scaled distributions of retail and selling prices. Panes A & B demonstrate the heavy concentration of products below ₹1,000, with extreme right-skewed tails reaching ₹571,230. Panes C & D show that applying log1p normalizes both distributions ($mu = 6.51, sigma = 1.04$), confirming the necessity of log-scaling for linear regression.",
      bold_prefix="1. Price Distribution & Skewness: ")
    add_figure("reports/figures/01_price_distribution.png", "Figure 10.1: Retail Price and Selling Price Distributions (Raw vs Log1p Transformed)")

    p("2. Retail vs Discounted Price Parity: Figure 10.2 illustrates the scatter plot of Retail Price versus Discounted Price across 5,000 sampled items. The red dashed line denotes the 45-degree parity line ($y=x$). Exactly 2,287 products (11.48%) lie directly on this line, representing full-price sales. As price increases, points disperse downward, reflecting varied discounting strategies across higher-ticket items.",
      bold_prefix="2. Retail vs Discounted Price Parity: ")
    add_figure("reports/figures/02_retail_vs_discounted_price.png", "Figure 10.2: Retail Price vs Discounted Selling Price with 45-Degree Parity Reference Line")

    p("3. Discount Percentage Dynamics: Figure 10.3 reveals that promotional markdowns cluster heavily around the 40%–60% corridor. The tier breakdown shows that High Discounts (51%–75%) represent 40.0% of all catalog offerings, while Clearance items (>75% off) account for 4.1% (811 items).",
      bold_prefix="3. Discount Percentage Dynamics: ")
    add_figure("reports/figures/03_discount_percentage_distribution.png", "Figure 10.3: Discount Percentage Histogram and Binned Promotional Tier Breakdown")

    p("4. Category-Wise Pricing and Markdown Depth: Figure 10.4 illustrates median selling prices and discount percentages across the top ten primary categories. Automotive Accessories leads in markdown depth (61.5% median discount), whereas Beauty and Personal Care exhibits the strongest price discipline (14.5% median discount).",
      bold_prefix="4. Category-Wise Pricing and Markdown Depth: ")
    add_figure("reports/figures/04_category_pricing_analysis.png", "Figure 10.4: Median Selling Price and Median Discount Percentage Across Top 10 Primary Categories")

    p("5. Brand Pricing Power: Figure 10.5 maps median selling price against median discount percentage for the top twelve high-volume brands. Fine jewelry brand Karatcraft commands a median price of ₹27,434 with disciplined 28.6% discounts, while aftermarket brands like TheLostPuppy rely on steep 72.8% markdowns.",
      bold_prefix="5. Brand Pricing Power: ")
    add_figure("reports/figures/05_brand_pricing_power.png", "Figure 10.5: Brand Pricing Power: Median Selling Price vs Discount Percentage (Top 12 Brands)")

    p("6. Customer Rating Independence: Figure 10.6 analyzes the 1,839 rated products. Pane A displays the star rating distribution, showing a mean rating of 3.81★ and a peak at 5.0★ (33.6% of rated items). Pane B shows boxplots across rating bands, demonstrating that discount depths remain consistent across all rating tiers ($r = -0.0020$).",
      bold_prefix="6. Customer Rating Independence: ")
    add_figure("reports/figures/06_rating_distribution_and_price.png", "Figure 10.6: Star Rating Distribution and Boxplots of Discount Depth Across Rating Bands")

    p("7. Correlation Matrix: Figure 10.7 presents the pairwise correlation heatmap across ten numerical attributes. Retail price and discounted price show an exceptionally strong linear correlation of $r = 0.9812$, while rating score shows virtually zero correlation with price ($r = 0.05$) and discount depth ($r = -0.002$).",
      bold_prefix="7. Correlation Matrix: ")
    add_figure("reports/figures/07_correlation_matrix.png", "Figure 10.7: Correlation Heatmap Across Numerical Attributes and Engineered Features")

    h2("10.6 Price Prediction Model Development")
    p("Predicting discounted_price was formulated as a supervised regression task. To prevent target data leakage, input features were restricted to retail_price, product_name_word_count, description_word_count, is_FK_Advantage_product, is_rated, primary_category, and brand. The data was partitioned into an 80% training set (15,937 samples) and a 20% testing set (3,985 samples).")

    h2("10.7 Model Performance Comparison and Benchmarks")
    p("Four models were trained and evaluated on unseen test data. Table 10.5 presents the empirical benchmark results.")

    p("Table 10.5: Supervised Regression Model Performance Comparison", bold_prefix="Table 10.5: ", space_after=4)
    model_headers = ["Model Architecture", "MAE (₹ INR)", "RMSE (₹ INR)", "R² Score", "Rank / Assessment"]
    model_rows = [
        ["Simple Baseline (Median)", "₹1,601.09", "₹6,205.38", "-0.0536", "Naive benchmark (predicts median test price)."],
        ["Ridge Regression (Linear)", "₹444.61", "₹1,163.12", "0.9630", "Strong linear baseline; captures direct MRP anchor."],
        ["Random Forest Regressor", "₹267.11", "₹884.70", "0.9786", "Lowest Mean Absolute Error; robust ensemble."],
        ["Gradient Boosting Regressor", "₹290.21", "₹838.82", "0.9807", "🏆 Best overall model; highest R² and lowest RMSE."]
    ]
    add_table_data(model_headers, model_rows, [Inches(2.2), Inches(1.2), Inches(1.2), Inches(1.0), Inches(1.6)])

    p("Figure 10.8 compares actual versus predicted prices on a logarithmic scale for Ridge Regression and Gradient Boosting. Predictions cluster tightly along the ideal 45-degree line across several orders of magnitude.")
    add_figure("reports/figures/08_actual_vs_predicted_prices.png", "Figure 10.8: Actual vs Predicted Prices on Holdout Test Set (Ridge vs Gradient Boosting)")

    h2("10.8 Feature Importance and Model Explainability")
    p("Feature importances extracted from the Gradient Boosting model (Figure 10.9) indicate that retail_price (MRP) is the dominant predictor, accounting for 86.4% of total importance. Category indicators account for 7.8%, brand accounts for 3.2%, and catalog metadata accounts for 2.6%.")
    add_figure("reports/figures/09_feature_importances.png", "Figure 10.9: Relative Feature Importances for Selling Price Prediction (Gradient Boosting)")

    h2("10.9 Product Pricing Segmentation (K-Means Results)")
    p("K-Means clustering was applied to standardized log retail price, log selling price, and discount percentage. Figure 10.10 shows the Elbow curve and Silhouette score across $k \in [2, 6]$. The inflection point at $k=4$ (Inertia: 16,430.1, Silhouette: 0.3973) was selected as the optimal cluster count.")
    add_figure("reports/figures/10_kmeans_elbow_and_silhouette.png", "Figure 10.10: K-Means Diagnostic Curves: Elbow Method (Inertia) and Silhouette Analysis")

    p("Table 10.6 details the four empirical market clusters identified by K-Means.")
    p("Table 10.6: Empirical Cluster Profiles and Strategic Market Personas", bold_prefix="Table 10.6: ", space_after=4)
    clust_headers = ["Segment Name", "Catalog Share", "Median MRP", "Median Selling", "Median Discount", "Top Category", "Commercial Archetype"]
    clust_rows = [
        ["Segment 1: Mass-Market Deep Discount", "43.0% (8,574)", "₹999.00", "₹399.00", "57.22%", "Clothing", "High-volume apparel and generic phone accessories."],
        ["Segment 2: Mid-Range Moderate Discount", "24.8% (4,942)", "₹2,450.00", "₹1,299.00", "45.50%", "Clothing", "Branded footwear, home furnishings, and auto parts."],
        ["Segment 3: Premium / Luxury Niche", "5.5% (1,093)", "₹32,002.00", "₹24,112.00", "23.09%", "Jewellery", "Fine jewelry and luxury tech with high price integrity."],
        ["Segment 4: Low-Discount Essentials", "26.7% (5,313)", "₹599.00", "₹499.00", "10.26%", "Clothing", "Budget staples, personal care, and full-MRP items."]
    ]
    add_table_data(clust_headers, clust_rows, [Inches(1.8), Inches(1.1), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.3)])

    p("Figure 10.11 illustrates the clusters via a 2D scatter plot of Retail Price vs Discount Percentage (Pane A) and a Principal Component Analysis (PCA) projection (Pane B), capturing 90%+ of total variance.")
    add_figure("reports/figures/11_kmeans_clusters_scatter.png", "Figure 10.11: 2D Cluster Scatter Plot and Principal Component Analysis (PCA) Projection")

    h2("10.10 Streamlit Interactive Dashboard Implementation")
    p("The interactive web dashboard was developed in app/app.py using Streamlit and Plotly. It includes seven functional modules:")
    p("1. Home / Overview: Top-level KPI metric cards and category volume distribution charts.\n"
      "2. Data Overview & Dictionary: Filterable product browser with search, pagination, CSV export, and a full 31-column data dictionary.\n"
      "3. Price Analysis: Interactive scatter plots with parity lines and price distribution histograms with optional log scaling.\n"
      "4. Discount Analysis: Continuous discount histograms, interactive donut charts of discount tiers, and category comparisons.\n"
      "5. Rating Analysis: Completeness charts and boxplots evaluating the relationship between ratings and discounts.\n"
      "6. Machine Learning: Supervised model benchmark comparisons, a live interactive price prediction form, and cluster exploration.\n"
      "7. Insights & Conclusion: Synthesized commercial recommendations, project limitations, and academic conclusions.")

    h2("10.11 Verification, Testing and Validation")
    p("The project implementation was validated across several test categories, as summarized in Table 10.7.")

    p("Table 10.7: Project Verification and Test Results", bold_prefix="Table 10.7: ", space_after=4)
    test_headers = ["Test Category", "Validation Activity", "Observed Outcome", "Status"]
    test_rows = [
        ["Data Integrity", "SHA256 checksum verification of raw CSV", "56F8F699C9E847356666C2EAB3C3AB1244340F6A98AD08E39EA2199EBE993AD1", "Passed"],
        ["Data Cleaning", "Verification of 78 dropped price records", "Exactly 19,922 rows retained; 0 missing prices", "Passed"],
        ["Brand Reconciliation", "Audit of 5,864 raw missing brands", "5,864 raw - 13 dropped = exactly 5,851 'Unbranded / Generic'", "Passed"],
        ["Tier Membership", "Boundary audit for discount and price tiers", "0 null values; every product mapped to exactly one tier", "Passed"],
        ["Data Leakage", "Code audit of feature matrix X", "Zero discount derivatives in features when predicting price", "Passed"],
        ["Model Compilation", "Python syntax and import validation", "py_compile app/app.py completed with 0 errors", "Passed"],
        ["Server Execution", "Headless HTTP probe of Streamlit app", "HTTP 200 OK received; all assets loaded cleanly", "Passed"]
    ]
    add_table_data(test_headers, test_rows, [Inches(1.5), Inches(2.2), Inches(2.8), Inches(0.7)])

    doc.add_page_break()

    # =========================================================================
    # 12. LEARNING OUTCOMES
    # =========================================================================
    h1("11. LEARNING OUTCOMES")
    p("Completing this technical project provided hands-on experience in several core areas of data science and software engineering:")
    p("1. Data Governance and Hygiene: Gained practical experience handling messy real-world datasets, parsing nested strings, and applying principled imputation rules rather than unvalidated heuristics.\n"
      "2. Statistical Analysis & Price Skewness: Learned to identify extreme right-skewness and apply non-parametric measures (medians and IQR) and logarithmic transformations to stabilize variance.\n"
      "3. Data Leakage Prevention: Understood the mechanics of target leakage and designed programmatic guards to prevent target-derived features from contaminating training sets.\n"
      "4. Supervised Ensemble Regression: Implemented, evaluated, and compared Ridge, Random Forest, and Gradient Boosting models, analyzing trade-offs between MAE and RMSE.\n"
      "5. Unsupervised Clustering & Validation: Applied K-Means clustering, standardized feature spaces, and used Elbow curves and Silhouette scores to determine optimal cluster counts.\n"
      "6. Interactive Dashboard Development: Built responsive web applications using Streamlit and Plotly, integrating pre-trained models for real-time inference.\n"
      "7. Software Engineering Standards: Organized a modular Python codebase with clear separation of concerns, pinned dependency manifests, and reproducible pipelines.")

    doc.add_page_break()

    # =========================================================================
    # 13. CHALLENGES FACED AND SOLUTIONS
    # =========================================================================
    h1("12. CHALLENGES FACED AND SOLUTIONS")
    p("Table 12.1 documents the primary technical challenges encountered during the project and the solutions implemented.")

    p("Table 12.1: Technical Challenges Encountered and Implemented Solutions", bold_prefix="Table 12.1: ", space_after=4)
    chal_headers = ["Technical Challenge", "Observed Impact", "Implemented Engineering Solution"]
    chal_rows = [
        ["Dependency Resolver Backtracking",
         "pip backtracked through historical Streamlit releases due to older pre-installed packages in Python 3.10.",
         "Identified conflicting packages, isolated dependencies, and updated the environment to compatible modern versions."],
        ["Pandas 2.3 Indexing Compatibility",
         "Passing Pandas Series to Seaborn histplot with KDE triggered a multi-dimensional indexing error in older Matplotlib.",
         "Upgraded Matplotlib to 3.10.9 and converted Series to NumPy arrays via .to_numpy() prior to plotting."],
        ["Risk of Target Data Leakage",
         "Using discount percentage to predict selling price would produce an artificially inflated, ungeneralizable model.",
         "Implemented architectural assertions in feature_engineering.py to exclude all discount derivatives from the feature matrix."],
        ["Extreme Price Right-Skewness",
         "Prices ranging from ₹35 to ₹571,230 distorted linear regression models and visual histograms.",
         "Applied log1p transformations for regression modeling and capped exploratory plots at the 95th/99th percentiles for visual clarity."],
        ["High-Cardinality Categorical Features",
         "262 categories and 3,486 brands created thousands of sparse columns under standard one-hot encoding.",
         "Configured OneHotEncoder with min_frequency=30, grouping rare categories and brands into an infrequent bin."],
        ["High Rating Sparsity",
         "90.77% of products lacked ratings, which could bias models if imputed arbitrarily.",
         "Converted placeholders to NaNs, added an is_rated binary flag, and analyzed rated products as a distinct sub-cohort."]
    ]
    add_table_data(chal_headers, chal_rows, [Inches(1.8), Inches(2.2), Inches(3.2)])

    doc.add_page_break()

    # =========================================================================
    # 14. CONCLUSION AND FUTURE SCOPE
    # =========================================================================
    h1("13. CONCLUSION AND FUTURE SCOPE")

    h2("13.1 Conclusion")
    p("This B.Tech technical project successfully designed, implemented, and validated an end-to-end data analytics and predictive intelligence platform for e-commerce product pricing. Operating on an authentic dataset of 19,922 clean Flipkart listings across 262 categories, the project delivered several key outcomes:")
    p("• Established an immutable, verified data pipeline that cleans catalog data, resolves brand identities, and parses nested taxonomies without synthetic distortion.\n"
      "• Characterized e-commerce price dynamics, documenting a median selling price of ₹550 against an arithmetic mean of ₹1,973, driven by luxury outliers reaching ₹571,230.\n"
      "• Quantified promotional markdown patterns, finding that the median discount is 45.00% and that 45.85% of catalog products receive discounts of 50% or higher.\n"
      "• Proved that customer ratings are independent of discount depth ($r = -0.0020$), confirming that heavy discounting does not harm perceived product quality.\n"
      "• Built a leakage-free Gradient Boosting regression model achieving an R² of 0.9807 and RMSE of ₹838.82, with Random Forest achieving a low MAE of ₹267.11.\n"
      "• Segmented the catalog into four strategic market archetypes via K-Means clustering (Silhouette: 0.3973).\n"
      "• Deployed an interactive Streamlit dashboard providing dynamic filtering, visual analytics, and real-time price estimation.")

    h2("13.2 Future Scope")
    p("The analytical framework established in this project provides a foundation for several future extensions:")
    p("1. Longitudinal Scraping & Dynamic Pricing: Scraping listings daily across seasonal promotional events (e.g., Big Billion Days) would enable time-series elasticity modeling.\n"
      "2. Multi-Seller Buy Box Competition: Incorporating individual merchant identifiers, delivery timeframes, and seller review scores would enable modeling of multi-seller price competition.\n"
      "3. Deep Learning for Unstructured Data: Integrating convolutional neural networks (CNNs) on product imagery and transformer models (BERT) on full descriptions could capture premium pricing cues directly from creative assets.\n"
      "4. Automated Cloud Deployment: Containerizing the Streamlit application with Docker and deploying it on cloud platforms (AWS ECS, Google Cloud Run) would support public multi-user access.\n"
      "5. Profitability & Cost Modeling: Integrating wholesale product acquisition costs would allow optimizing for gross margin profitability rather than revenue alone.")

    doc.add_page_break()

    # =========================================================================
    # 15. REFERENCES
    # =========================================================================
    h1("14. REFERENCES")
    refs = [
        "PromptCloud. (2016). Flipkart Products Dataset. Kaggle Datasets. https://www.kaggle.com/datasets/PromptCloudHQ/flipkart-products",
        "McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference (SciPy 2010), pp. 56–61.",
        "Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. Nature, 585(7825), pp. 357–362.",
        "Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, pp. 2825–2830.",
        "Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), pp. 90–95.",
        "Waskom, M. L. (2021). seaborn: statistical data visualization. Journal of Open Source Software, 6(60), p. 3021.",
        "Plotly Technologies Inc. (2015). Collaborative data science. Plotly Technologies Inc., Montreal, QC. https://plotly.com",
        "Streamlit Inc. (2023). Streamlit: The fastest way to build and share data apps. https://docs.streamlit.io",
        "Breiman, L. (2001). Random Forests. Machine Learning, 45(1), pp. 5–32.",
        "Friedman, J. H. (2001). Greedy function approximation: a gradient boosting machine. Annals of Statistics, 29(5), pp. 1189–1232.",
        "MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations. Proceedings of the 5th Berkeley Symposium on Mathematical Statistics and Probability, 1, pp. 281–297.",
        "Rousseeuw, P. J. (1987). Silhouettes: a graphical aid to the interpretation and validation of cluster analysis. Journal of Computational and Applied Mathematics, 20, pp. 53–65.",
        "Kaufman, L., & Rousseeuw, P. J. (2009). Finding Groups in Data: An Introduction to Cluster Analysis. John Wiley & Sons.",
        "Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning: Data Mining, Inference, and Prediction (2nd ed.). Springer.",
        "Varian, H. R. (1980). A Model of Sales. The American Economic Review, 70(4), pp. 651–659."
    ]
    for idx, ref in enumerate(refs):
        p(f"[{idx+1}] {ref}", space_after=4)

    doc.add_page_break()

    # =========================================================================
    # 16. APPENDICES AND SUPPORTING EVIDENCE
    # =========================================================================
    h1("15. APPENDICES AND SUPPORTING EVIDENCE")

    h2("Appendix A: Complete Project Folder Hierarchy")
    p("The complete verified file system hierarchy of the Flipkart Product Price Analysis workspace is presented below:")
    tree_text = (
        "Flipkart_Product_Analysis/\n"
        "├── requirements.txt                      # Pinned dependencies\n"
        "├── README.md                             # Comprehensive project manual\n"
        "├── data/\n"
        "│   ├── raw/\n"
        "│   │   └── flipkart_com-ecommerce_sample.csv   # Immutable raw dataset (20,000 rows × 15 cols)\n"
        "│   └── processed/\n"
        "│       └── flipkart_cleaned.csv                # Clean dataset with cluster assignments (19,922 rows × 32 cols)\n"
        "├── src/\n"
        "│   ├── __init__.py                       # Package initializer\n"
        "│   ├── data_loader.py                    # Ingestion and schema validation\n"
        "│   ├── cleaning.py                       # Data cleaning and category tree parsing\n"
        "│   ├── feature_engineering.py            # Feature engineering and anti-leakage guards\n"
        "│   ├── run_pipeline.py                   # End-to-end data processing runner\n"
        "│   └── eda_analysis.py                   # Matplotlib/Seaborn static chart generator\n"
        "├── models/\n"
        "│   ├── train_price_predictor.py          # Supervised regression benchmark script\n"
        "│   ├── cluster_products.py               # K-Means clustering and PCA analysis\n"
        "│   ├── save_best_model.py                # Serializer for Streamlit live inference\n"
        "│   └── saved/\n"
        "│       └── price_model_artifacts.joblib  # Serialized pipeline artifacts\n"
        "├── app/\n"
        "│   └── app.py                            # Interactive Streamlit dashboard application\n"
        "├── reports/\n"
        "│   ├── data_quality_report.md            # Data quality and tier validation report\n"
        "│   ├── viva_questions_and_answers.md     # 27 Technical Viva Questions & Answers\n"
        "│   └── figures/                          # 11 Report-ready 300-DPI charts\n"
        "└── final_report/\n"
        "    ├── Flipkart_Product_Price_Analysis_Report.docx\n"
        "    └── Flipkart_Product_Price_Analysis_Report.pdf"
    )
    p(tree_text, align=WD_ALIGN_PARAGRAPH.LEFT)

    h2("Appendix B: Core Ingestion and Cleaning Scripts")
    p("Key excerpt from src/cleaning.py implementing category tree parsing and brand governance:")
    code_cleaning = (
        "def parse_category_tree(category_str):\n"
        "    if not isinstance(category_str, str) or not category_str.strip():\n"
        "        return ('Unknown', 'Unknown', 'Unknown')\n"
        "    cleaned = category_str.strip('[]\"\\' \\t\\r\\n')\n"
        "    parts = [p.strip().strip('\"\\'') for p in cleaned.split('>>') if p.strip()]\n"
        "    primary = parts[0] if len(parts) > 0 and parts[0] else 'Unknown'\n"
        "    sub = parts[1] if len(parts) > 1 and parts[1] else 'Unknown'\n"
        "    micro = parts[2] if len(parts) > 2 and parts[2] else 'Unknown'\n"
        "    return (primary, sub, micro)\n\n"
        "# Strict Brand Governance: Preserve missing brands as Unbranded / Generic\n"
        "df['brand'] = df['brand'].astype(str).str.strip()\n"
        "df['brand'] = df['brand'].replace({'': 'Unbranded / Generic', 'nan': 'Unbranded / Generic',\n"
        "                                   'None': 'Unbranded / Generic', 'null': 'Unbranded / Generic'})"
    )
    p(code_cleaning, align=WD_ALIGN_PARAGRAPH.LEFT)

    h2("Appendix C: Feature Engineering & Anti-Leakage Architecture")
    p("Key excerpt from src/feature_engineering.py enforcing data leakage prevention:")
    code_leakage = (
        "def get_modeling_features_and_target(df, target_type='discounted_price'):\n"
        "    if target_type == 'discounted_price':\n"
        "        # CRITICAL: Exclude all discount derivations from feature matrix X\n"
        "        leakage_cols = ['discounted_price', 'log_discounted_price', 'discount_amount',\n"
        "                        'discount_percentage', 'discount_tier']\n"
        "        y = df['discounted_price']\n"
        "    candidate_features = ['retail_price', 'product_name_word_count', 'description_word_count',\n"
        "                          'is_FK_Advantage_product', 'is_rated', 'primary_category', 'brand']\n"
        "    clean_features = [c for c in candidate_features if c not in leakage_cols]\n"
        "    return df[clean_features].copy(), y"
    )
    p(code_leakage, align=WD_ALIGN_PARAGRAPH.LEFT)

    h2("Appendix D: Visual Evidence Catalog")
    p("Table 15.1 catalogs all eleven figures generated by the project pipeline.")
    p("Table 15.1: Catalog of Generated Visual Evidence and Artifacts", bold_prefix="Table 15.1: ", space_after=4)
    fig_headers = ["Figure Ref", "Saved File Name", "Resolution", "Analytical Focus"]
    fig_rows = [
        ["Figure 10.1", "01_price_distribution.png", "300 DPI", "Raw vs Log1p price distributions showing skewness reduction."],
        ["Figure 10.2", "02_retail_vs_discounted_price.png", "300 DPI", "Scatter plot against 45-degree parity reference line."],
        ["Figure 10.3", "03_discount_percentage_distribution.png", "300 DPI", "Discount histogram and binned promotional tiers."],
        ["Figure 10.4", "04_category_pricing_analysis.png", "300 DPI", "Median price and discount variations across top 10 verticals."],
        ["Figure 10.5", "05_brand_pricing_power.png", "300 DPI", "Brand pricing power mapping volume, price, and markdowns."],
        ["Figure 10.6", "06_rating_distribution_and_price.png", "300 DPI", "Rating distribution and boxplots demonstrating r = -0.002."],
        ["Figure 10.7", "07_correlation_matrix.png", "300 DPI", "Heatmap across ten numerical and engineered attributes."],
        ["Figure 10.8", "08_actual_vs_predicted_prices.png", "300 DPI", "Test set prediction scatter for Ridge and Gradient Boosting."],
        ["Figure 10.9", "09_feature_importances.png", "300 DPI", "Feature importance bar chart from Gradient Boosting."],
        ["Figure 10.10", "10_kmeans_elbow_and_silhouette.png", "300 DPI", "Inertia elbow curve and Silhouette scores (k = 2 to 6)."],
        ["Figure 10.11", "11_kmeans_clusters_scatter.png", "300 DPI", "2D scatter plot and PCA projection of 4 market segments."]
    ]
    add_table_data(fig_headers, fig_rows, [Inches(1.2), Inches(2.5), Inches(1.1), Inches(2.4)])

    doc.add_page_break()

    # =========================================================================
    # 17. MENTOR EVALUATION SHEET
    # =========================================================================
    h1("16. MENTOR EVALUATION SHEET")
    p("Student Name: [Enter Student Name]\n"
      "Roll Number: [Enter Roll Number]\n"
      "Branch & Year: B.Tech Computer Science and Engineering, [Enter Year]\n"
      "Project Title: FLIPKART PRODUCT PRICE ANALYSIS: An Exploratory Data Analysis and Machine Learning-Based Approach to Product Pricing and Discount Analysis\n"
      "Internal Guide / Mentor Name: [Name and Designation]")
    
    p("Table 16.1: Formal B.Tech Technical Project Evaluation Rubric", bold_prefix="Table 16.1: ", space_after=4)
    eval_headers = ["Evaluation Criterion", "Maximum Marks", "Marks Awarded"]
    eval_rows = [
        ["Understanding of Problem Statement, Objectives & Scope", "10", ""],
        ["Technical Methodology, Architecture & Preprocessing Pipeline", "20", ""],
        ["Quality of Practical Implementation, Code & Pipeline Execution", "25", ""],
        ["Depth of Results, Visualizations, ML Models & Analysis", "15", ""],
        ["Technical Documentation, Report Quality & Rigor", "15", ""],
        ["Presentation, Demonstration & Technical Viva-Voce Performance", "15", ""],
        ["TOTAL MARKS", "100", ""]
    ]
    add_table_data(eval_headers, eval_rows, [Inches(4.5), Inches(1.3), Inches(1.4)])

    p("Mentor Remarks & Qualitative Feedback:\n"
      "___________________________________________________________________________________________________\n"
      "___________________________________________________________________________________________________\n"
      "___________________________________________________________________________________________________\n"
      "___________________________________________________________________________________________________")

    doc.add_paragraph().paragraph_format.space_before = Pt(36)
    sig_eval = doc.add_paragraph()
    sig_eval.paragraph_format.line_spacing = 1.5
    sig_eval.add_run("_______________________________\t\t_______________________________\n").bold = True
    sig_eval.add_run("Signature of Project Mentor / Guide\t\tSignature of Head of Department\n").bold = True
    sig_eval.add_run("Date: _________________________\t\tDate: _________________________\n")

    doc.add_page_break()

    # =========================================================================
    # 18. FINAL DECLARATION
    # =========================================================================
    h1("17. FINAL DECLARATION")
    p("I hereby declare that this one-week technical project report entitled “FLIPKART PRODUCT PRICE ANALYSIS: An Exploratory Data Analysis and Machine Learning-Based Approach to Product Pricing and Discount Analysis” is an authentic record of technical work carried out independently by me under the guidance of my project mentor.")
    p("I confirm that the dataset utilized is an authentic, publicly accessible Flipkart catalog, that zero synthetic records were fabricated, and that all data cleaning counts, statistical metrics, machine learning performance values, and cluster characteristics presented in this report reflect actual code execution and empirical outputs.")
    p("I further declare that this report has been authored following academic ethics and guidelines, and has not formed the basis for the award of any previous degree, diploma, or certificate in this or any other institution.")

    doc.add_paragraph().paragraph_format.space_before = Pt(40)
    sig_decl = doc.add_paragraph()
    sig_decl.paragraph_format.line_spacing = 1.5
    sig_decl.add_run("Student Signature: _____________________________________\n").bold = True
    sig_decl.add_run("Student Name: [Enter Student Name]\n")
    sig_decl.add_run("Roll Number: [Enter Roll Number]\n")
    sig_decl.add_run("Department of Computer Science and Engineering\n")
    sig_decl.add_run("ACE Engineering College, Hyderabad\n\n")
    sig_decl.add_run("Date: _________________________\t\tPlace: Hyderabad, Telangana\n")

    # Add headers and footers with page numbering
    add_header_footer_page_number(doc)

    # Save document
    doc.save(str(OUTPUT_PATH))
    print(f"Successfully generated DOCX Report at: {OUTPUT_PATH}")

if __name__ == "__main__":
    build_docx_report()
