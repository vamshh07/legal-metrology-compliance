import streamlit as st
from PIL import Image

from ocr_engine import extract_text
from extractor import extract_product_details
from compliance_engine import check_compliance
from report_generator import generate_report
from history_manager import save_scan, get_history


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="LegalMet AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

/* MAIN CONTAINER */
.block-container {
    padding-top: 4rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px;
}


/* NAVIGATION BUTTONS */
.stButton > button {
    border-radius: 12px;
    height: 48px;
    font-size: 16px;
    font-weight: 600;
}


/* HERO SECTION */
.hero {
    background: linear-gradient(135deg, #102a43, #1f4e78);
    padding: 65px 40px;
    border-radius: 25px;
    text-align: center;
    color: white;
    margin-top: 15px;
    margin-bottom: 35px;
}

.hero h1 {
    color: white;
    font-size: 52px;
    margin-bottom: 15px;
}

.hero h2 {
    color: #dbeafe;
    font-size: 28px;
    margin-bottom: 25px;
}

.hero p {
    color: #e5edf5;
    font-size: 18px;
    line-height: 1.7;
    max-width: 850px;
    margin: auto;
}


/* SECTION TITLES */
.section-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    color: #1f2937;
    margin-top: 45px;
    margin-bottom: 10px;
}

.section-subtitle {
    text-align: center;
    color: #6b7280;
    font-size: 17px;
    margin-bottom: 30px;
}


/* FEATURE CARDS */
.feature-card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    min-height: 190px;
    margin-bottom: 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
}

.feature-card h2 {
    font-size: 35px;
    margin-bottom: 10px;
}

.feature-card h3 {
    color: #1f4e78;
    font-size: 20px;
}

.feature-card p {
    color: #6b7280;
    line-height: 1.6;
}


/* WORKFLOW CARDS */
.workflow-card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    min-height: 170px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
}

.workflow-card h2 {
    font-size: 35px;
}

.workflow-card h3 {
    color: #1f4e78;
}


/* PAGE HEADER */
.page-header {
    background: linear-gradient(135deg, #1f4e78, #2563eb);
    padding: 35px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
}

.page-header h1 {
    color: white;
}

.page-header p {
    color: #eaf2ff;
    font-size: 17px;
}


/* ABOUT CARDS */
.about-card {
    background-color: white;
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}


/* FOOTER */
.footer {
    text-align: center;
    color: #6b7280;
    padding: 25px;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# NAVIGATION BAR
# =========================================================

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

nav1, nav2, nav3, nav4 = st.columns(4, gap="medium")

with nav1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()

with nav2:
    if st.button("🔍 AI Scanner", use_container_width=True):
        st.session_state.page = "Scanner"
        st.rerun()

with nav3:
    if st.button("📊 Scan History", use_container_width=True):
        st.session_state.page = "History"
        st.rerun()

with nav4:
    if st.button("ℹ️ About", use_container_width=True):
        st.session_state.page = "About"
        st.rerun()

st.markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)


# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>⚖️ LegalMet AI</h1>
        <h2>AI-Powered Packaged Commodity Compliance System</h2>
        <p>
            An intelligent system that analyzes product packaging using OCR
            and automatically checks mandatory declarations for preliminary
            Legal Metrology compliance assessment.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button(
            "🚀 Start Compliance Check",
            type="primary",
            use_container_width=True
        ):
            st.session_state.page = "Scanner"
            st.rerun()


    # FEATURES

    st.markdown(
        '<div class="section-title">✨ Intelligent Features</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Everything required for automated product package analysis'
        '</div>',
        unsafe_allow_html=True
    )


    row1_col1, row1_col2, row1_col3 = st.columns(3)

    with row1_col1:
        st.markdown("""
        <div class="feature-card">
            <h2>📷</h2>
            <h3>OCR Package Scanning</h3>
            <p>
                Extract important text and declarations directly
                from product package images.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with row1_col2:
        st.markdown("""
        <div class="feature-card">
            <h2>⚖️</h2>
            <h3>Compliance Verification</h3>
            <p>
                Automatically check important mandatory declarations
                on packaged commodities.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with row1_col3:
        st.markdown("""
        <div class="feature-card">
            <h2>📊</h2>
            <h3>Compliance Score</h3>
            <p>
                Get an instant percentage-based preliminary
                compliance assessment.
            </p>
        </div>
        """, unsafe_allow_html=True)


    row2_col1, row2_col2, row2_col3 = st.columns(3)

    with row2_col1:
        st.markdown("""
        <div class="feature-card">
            <h2>💡</h2>
            <h3>Smart Suggestions</h3>
            <p>
                Receive useful recommendations for declarations
                that require attention.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with row2_col2:
        st.markdown("""
        <div class="feature-card">
            <h2>📄</h2>
            <h3>Automated Reports</h3>
            <p>
                Generate downloadable compliance reports
                for further review.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with row2_col3:
        st.markdown("""
        <div class="feature-card">
            <h2>📜</h2>
            <h3>Scan History</h3>
            <p>
                Keep track of previous product compliance
                assessments.
            </p>
        </div>
        """, unsafe_allow_html=True)


    # HOW IT WORKS

    st.markdown(
        '<div class="section-title">🔄 How It Works</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Simple AI-powered workflow for product package verification'
        '</div>',
        unsafe_allow_html=True
    )

    work1, arrow1, work2, arrow2, work3 = st.columns(
        [3, 1, 3, 1, 3]
    )

    with work1:
        st.markdown("""
        <div class="workflow-card">
            <h2>📷</h2>
            <h3>1. Upload Product</h3>
            <p>Upload clear images of the product package.</p>
        </div>
        """, unsafe_allow_html=True)

    with arrow1:
        st.markdown(
            "<h1 style='text-align:center; padding-top:50px;'>→</h1>",
            unsafe_allow_html=True
        )

    with work2:
        st.markdown("""
        <div class="workflow-card">
            <h2>🔎</h2>
            <h3>2. AI OCR Analysis</h3>
            <p>Extract important product information automatically.</p>
        </div>
        """, unsafe_allow_html=True)

    with arrow2:
        st.markdown(
            "<h1 style='text-align:center; padding-top:50px;'>→</h1>",
            unsafe_allow_html=True
        )

    with work3:
        st.markdown("""
        <div class="workflow-card">
            <h2>⚖️</h2>
            <h3>3. Compliance Result</h3>
            <p>Get compliance score and declaration analysis.</p>
        </div>
        """, unsafe_allow_html=True)


    # FINAL CTA

    st.markdown(
        '<div class="section-title">Ready to Analyze Your Product?</div>',
        unsafe_allow_html=True
    )

    cta1, cta2, cta3 = st.columns([1, 2, 1])

    with cta2:
        if st.button(
            "🔍 Open AI Compliance Scanner",
            type="primary",
            use_container_width=True
        ):
            st.session_state.page = "Scanner"
            st.rerun()


# =========================================================
# SCANNER PAGE
# =========================================================

elif st.session_state.page == "Scanner":

    st.markdown("""
    <div class="page-header">
        <h1>🔍 AI Compliance Scanner</h1>
        <p>
            Upload product package images and analyze mandatory
            declarations using OCR and rule-based compliance checks.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "📷 For better accuracy, upload clear images of the "
        "front, back, and side of the product package."
    )

    uploaded_files = st.file_uploader(
        "Upload Product Package Images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.subheader("📷 Uploaded Images")

        images = []
        columns = st.columns(min(len(uploaded_files), 3))

        for index, uploaded_file in enumerate(uploaded_files):

            image = Image.open(uploaded_file).convert("RGB")
            images.append(image)

            with columns[index % len(columns)]:
                st.image(
                    image,
                    caption=f"Product Image {index + 1}",
                    use_container_width=True
                )

        st.divider()

        if st.button(
            "🚀 Scan All Images & Check Compliance",
            type="primary",
            use_container_width=True
        ):

            with st.spinner("🔍 AI is analyzing the product package..."):

                all_text = ""

                for index, image in enumerate(images):

                    extracted_text = extract_text(image)

                    all_text += (
                        f"\n\n========== IMAGE {index + 1} ==========\n"
                    )

                    all_text += extracted_text

                details = extract_product_details(all_text)

                results, score, final_status = check_compliance(details)


            # SAVE HISTORY

            missing_for_history = []

            for field, result in results.items():

                if result.get("status") == "MISSING":
                    missing_for_history.append(field)

            try:
                save_scan(
                    score,
                    final_status,
                    missing_for_history
                )
            except Exception:
                pass

            st.success("✅ Product analysis completed successfully!")

            st.divider()

            st.subheader("📊 Compliance Assessment Dashboard")

            metric1, metric2, metric3 = st.columns(3)

            with metric1:
                st.metric(
                    "Compliance Score",
                    f"{score:.0f}%"
                )

            with metric2:

                total = len(results)

                compliant = sum(
                    1 for result in results.values()
                    if result.get("status") == "COMPLIANT"
                )

                st.metric(
                    "Requirements Found",
                    f"{compliant}/{total}"
                )

            with metric3:

                if final_status == "COMPLIANT":
                    st.success("🟢 COMPLIANT")
                else:
                    st.warning(f"🟠 {final_status}")

            st.progress(int(min(max(score, 0), 100)))

            st.divider()


            # EXTRACTED DETAILS

            st.subheader("📋 Extracted Product Information")

            items = list(details.items())

            left_col, right_col = st.columns(2)

            midpoint = (len(items) + 1) // 2

            with left_col:

                for key, value in items[:midpoint]:

                    if value:
                        st.success(f"✅ {key}: {value}")
                    else:
                        st.error(f"❌ {key}: Not Detected")

            with right_col:

                for key, value in items[midpoint:]:

                    if value:
                        st.success(f"✅ {key}: {value}")
                    else:
                        st.error(f"❌ {key}: Not Detected")


            # COMPLIANCE CHECK

            st.divider()
            st.subheader("⚖️ Declaration Compliance Check")

            missing_fields = []

            for field, result in results.items():

                status = result.get("status", "")
                message = result.get("message", "")

                if status == "COMPLIANT":

                    st.success(f"✅ {field} — {message}")

                elif status == "MISSING":

                    st.error(f"❌ {field} — {message}")
                    missing_fields.append(field)

                else:

                    st.info(f"ℹ️ {field} — {message}")


            # MISSING REQUIREMENTS

            st.divider()
            st.subheader("⚠️ Missing Requirements")

            if missing_fields:

                for field in missing_fields:
                    st.warning(f"⚠️ {field}")

            else:
                st.success("🎉 No missing core declarations detected!")


            # SMART SUGGESTIONS

            st.divider()
            st.subheader("💡 Smart Compliance Suggestions")

            suggestions = {
                "Product Name": "Clearly mention the name or description of the commodity.",
                "MRP": "Clearly declare the Maximum Retail Price inclusive of applicable taxes.",
                "Net Quantity": "Clearly mention net quantity using an appropriate standard unit.",
                "Packed Date": "Clearly declare the packing or manufacturing date.",
                "Manufacturer": "Clearly mention manufacturer, packer, or importer details.",
                "Consumer Care": "Provide consumer care contact details for complaints.",
                "Unit Sale Price": "Mention unit sale price where applicable."
            }

            if missing_fields:

                for field in missing_fields:

                    suggestion = suggestions.get(
                        field,
                        "Ensure this declaration is clearly visible on the package."
                    )

                    st.info(f"💡 {field}: {suggestion}")

            else:
                st.success("Great! All major declarations were detected.")


            # DOWNLOAD REPORT

            st.divider()
            st.subheader("📄 Download Compliance Report")

            try:

                report_html = generate_report(
                    details,
                    results,
                    score,
                    final_status
                )

                st.download_button(
                    label="📥 Download Compliance Report",
                    data=report_html,
                    file_name="legalmet_compliance_report.html",
                    mime="text/html",
                    use_container_width=True
                )

            except Exception as e:
                st.warning(f"Report generation needs attention: {e}")


            # RAW OCR TEXT

            st.divider()

            with st.expander("🔎 View Raw OCR Extracted Text"):
                st.text_area(
                    "OCR Output",
                    all_text,
                    height=350
                )


# =========================================================
# HISTORY PAGE
# =========================================================

elif st.session_state.page == "History":

    st.markdown("""
    <div class="page-header">
        <h1>📊 Scan History</h1>
        <p>View previously recorded compliance assessments.</p>
    </div>
    """, unsafe_allow_html=True)

    try:

        history = get_history()

        if history is not None and len(history) > 0:

            st.success(f"📁 Total Scans Recorded: {len(history)}")

            st.dataframe(
                history,
                use_container_width=True
            )

        else:
            st.info(
                "No scan history available yet. "
                "Scan a product to see results here."
            )

    except Exception:
        st.info("No scan history available yet.")


# =========================================================
# ABOUT PAGE
# =========================================================

elif st.session_state.page == "About":

    st.markdown("""
    <div class="page-header">
        <h1>ℹ️ About LegalMet AI</h1>
        <p>
            AI-powered preliminary packaged commodity
            compliance assessment system.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-card">
        <h2>🎯 Project Objective</h2>
        <p>
            LegalMet AI helps automate the preliminary analysis of
            packaged commodity labels. The system uses OCR technology
            to extract visible product declarations and a rule-based
            engine to assess their presence.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-card">
        <h2>🤖 Technologies Used</h2>
        <ul>
            <li>Python</li>
            <li>Streamlit</li>
            <li>Tesseract OCR</li>
            <li>OpenCV</li>
            <li>Rule-Based Compliance Engine</li>
            <li>Automated Report Generation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-card">
        <h2>🔄 System Workflow</h2>
        <p>
            Product Image → OCR Text Extraction → Product Information
            Detection → Compliance Rule Engine → Compliance Score →
            Smart Suggestions → Downloadable Report
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-card">
        <h2>⚠️ Disclaimer</h2>
        <p>
            This application provides a preliminary automated assessment
            based on OCR and programmed rules. Final legal compliance
            verification should be performed by authorized professionals
            or relevant authorities.
        </p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown("""
<div class="footer">
    <h3>⚖️ LegalMet AI</h3>
    <p>AI-Based Packaged Commodity Compliance Assessment System</p>
    <p>Smart India Hackathon Prototype 🚀</p>
</div>
""", unsafe_allow_html=True)
