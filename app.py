import streamlit as st
from PIL import Image

from ocr_engine import extract_text
from extractor import extract_product_details
from compliance_engine import check_compliance
from report_generator import generate_report
from history_manager import save_scan, get_history

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Legal Metrology Compliance Checker",
    page_icon="⚖️",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.title-box {
    background: linear-gradient(90deg, #1f4e78, #2e75b6);
    padding: 30px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
}

.result-card {
    padding: 20px;
    border-radius: 12px;
    background-color: white;
    border: 1px solid #e0e0e0;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# HEADER
# ==================================================

st.markdown("""
<div class="title-box">
    <h1>⚖️ Packaged Commodity Compliance Checker</h1>
    <p>
        AI-powered system for checking packaged commodity labels
        under Legal Metrology (Packaged Commodities) Rules
    </p>
</div>
""", unsafe_allow_html=True)


# ==================================================
# INFORMATION
# ==================================================

st.info(
    "📷 Upload one or multiple images of a product package. "
    "Upload Front, Back and Side labels for better compliance analysis."
)


# ==================================================
# MULTIPLE IMAGE UPLOAD
# ==================================================

uploaded_files = st.file_uploader(
    "📤 Upload Product Package Images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)


# ==================================================
# IF IMAGES ARE UPLOADED
# ==================================================

if uploaded_files:

    st.subheader("📷 Uploaded Product Images")

    # Create maximum 3 columns
    columns = st.columns(
        min(len(uploaded_files), 3)
    )

    images = []


    # ==================================================
    # DISPLAY UPLOADED IMAGES
    # ==================================================

    for index, uploaded_file in enumerate(uploaded_files):

        image = Image.open(uploaded_file)

        images.append(image)

        with columns[index % 3]:

            st.image(
                image,
                caption=f"Image {index + 1}",
                use_container_width=True
            )


    st.divider()


    # ==================================================
    # AI SCANNER SECTION
    # ==================================================

    st.subheader("🔍 AI Compliance Scanner")

    st.write("""
    The system will:

    1. Scan all uploaded product images
    2. Extract text using OCR
    3. Combine information from all sides
    4. Identify mandatory declarations
    5. Check Legal Metrology compliance
    """)


    scan_button = st.button(
        "🚀 Scan All Images & Check Compliance",
        use_container_width=True
    )


    # ==================================================
    # PROCESS PRODUCT IMAGES
    # ==================================================

    if scan_button:

        with st.spinner(
            "🔍 AI is scanning all product package images..."
        ):

            all_text = ""


            # ==================================================
            # OCR EACH IMAGE
            # ==================================================

            for index, image in enumerate(images):

                extracted_text = extract_text(image)

                all_text += (
                    f"\n\n----- IMAGE {index + 1} -----\n"
                )

                all_text += extracted_text


            # ==================================================
            # EXTRACT PRODUCT INFORMATION
            # ==================================================

            details = extract_product_details(
                all_text
            )


            # ==================================================
            # CHECK COMPLIANCE
            # ==================================================

            results, score, final_status = check_compliance(
                details
            )
        # Save scan to history
        missing_for_history = []

        for field, result in results.items():

            if result["status"] == "MISSING":
                missing_for_history.append(field)


        save_scan(
            score,
            final_status,
            missing_for_history
        )


        st.success(
            "✅ Scanning completed successfully!"
        )


        st.divider()


        # ==================================================
        # COMPLIANCE DASHBOARD
        # ==================================================

        st.subheader(
            "📊 Automated Preliminary Compliance Assessment"
        )


        metric1, metric2, metric3 = st.columns(3)


        # --------------------------------------------------
        # COMPLIANCE SCORE
        # --------------------------------------------------

        with metric1:

            st.metric(
                "Compliance Score",
                f"{score:.0f}%"
            )


        # --------------------------------------------------
        # REQUIREMENTS DETECTED
        # --------------------------------------------------

        with metric2:

            total_fields = 0
            found_fields = 0

            for result in results.values():

                if result["status"] in [
                    "COMPLIANT",
                    "MISSING"
                ]:

                    total_fields += 1

                    if result["status"] == "COMPLIANT":

                        found_fields += 1


            st.metric(
                "Requirements Detected",
                f"{found_fields}/{total_fields}"
            )


        # --------------------------------------------------
        # FINAL STATUS
        # --------------------------------------------------

        with metric3:

            if final_status == "COMPLIANT":

                st.success(
                    "🟢 COMPLIANT"
                )

            else:

                st.error(
                    "🔴 NEEDS REVIEW"
                )


        # ==================================================
        # PROGRESS BAR
        # ==================================================

        st.progress(int(score))


        st.divider()


        # ==================================================
        # EXTRACTED PRODUCT INFORMATION
        # ==================================================

        st.subheader(
            "📋 Extracted Product Information"
        )


        detail_col1, detail_col2 = st.columns(2)

        items = list(details.items())

        midpoint = (
            len(items) + 1
        ) // 2


        # --------------------------------------------------
        # LEFT COLUMN
        # --------------------------------------------------

        with detail_col1:

            for key, value in items[:midpoint]:

                if value:

                    st.success(
                        f"✅ **{key}**: {value}"
                    )

                else:

                    st.error(
                        f"❌ **{key}**: Not Detected"
                    )


        # --------------------------------------------------
        # RIGHT COLUMN
        # --------------------------------------------------

        with detail_col2:

            for key, value in items[midpoint:]:

                if value:

                    st.success(
                        f"✅ **{key}**: {value}"
                    )

                else:

                    st.info(
                        f"ℹ️ **{key}**: "
                        f"Not Detected / Conditional"
                    )


        st.divider()


        # ==================================================
        # COMPLIANCE REQUIREMENT CHECK
        # ==================================================

        st.subheader(
            "⚖️ Declaration Compliance Check"
        )


        missing_fields = []


        for field, result in results.items():

            status = result["status"]

            message = result["message"]


            # --------------------------------------------------
            # COMPLIANT
            # --------------------------------------------------

            if status == "COMPLIANT":

                st.success(
                    f"✅ **{field}** — {message}"
                )


            # --------------------------------------------------
            # MISSING
            # --------------------------------------------------

            elif status == "MISSING":

                st.error(
                    f"❌ **{field}** — {message}"
                )

                missing_fields.append(field)


            # --------------------------------------------------
            # CONDITIONAL / INFORMATION
            # --------------------------------------------------

            else:

                st.info(
                    f"ℹ️ **{field}** — {message}"
                )


        st.divider()


        # ==================================================
        # MISSING REQUIREMENTS
        # ==================================================

        st.subheader(
            "⚠️ Missing Requirements"
        )


        if not missing_fields:

            st.success(
                "🎉 No core mandatory declarations "
                "are missing based on OCR detection."
            )

        else:

            st.warning(
                f"{len(missing_fields)} declaration(s) "
                "need attention."
            )

            for field in missing_fields:

                st.error(
                    f"❌ {field}"
                )


        st.divider()


        # ==================================================
        # SMART COMPLIANCE SUGGESTIONS
        # ==================================================

        st.subheader(
            "💡 Smart Compliance Suggestions"
        )


        suggestions = {

            "Product Name":
                "Clearly mention the name or description of the commodity.",

            "MRP":
                "Add Maximum Retail Price (MRP) inclusive of all taxes.",

            "Net Quantity":
                "Clearly declare the Net Quantity using a valid unit such as g, kg, ml or L.",

            "Packed Date":
                "Clearly mention the month/year or date of packing/manufacturing.",

            "Manufacturer":
                "Add the name and address of the manufacturer, packer or importer.",

            "Consumer Care":
                "Provide consumer care/contact details for complaints.",

            "Unit Sale Price":
                "Clearly mention the unit sale price where applicable."
        }


        if not missing_fields:

            st.success(
                "🎉 All core declarations were detected. "
                "The package appears ready for further review."
            )

        else:

            for field in missing_fields:

                suggestion = suggestions.get(
                    field,
                    "Ensure this declaration is clearly visible."
                )

                st.warning(
                    f"💡 **{field}:** {suggestion}"
                )


        st.divider()


        # ==================================================
        # DOWNLOAD COMPLIANCE REPORT
        # ==================================================

        st.subheader(
            "📄 Generate Compliance Report"
        )


        report_html = generate_report(
            details,
            results,
            score,
            final_status
        )


        st.download_button(
            label="📥 Download Compliance Report",
            data=report_html,
            file_name="compliance_report.html",
            mime="text/html",
            use_container_width=True
        )


        st.divider()


        # ==================================================
        # RAW OCR OUTPUT
        # ==================================================

        with st.expander(
            "🔎 View Combined OCR Extracted Text"
        ):

            st.text_area(
                "OCR Output",
                all_text,
                height=400
            )

# ==================================================
# SCAN HISTORY DASHBOARD
# ==================================================

st.divider()

st.subheader("📊 Recent Scan History")

history = get_history()


if history:

    st.dataframe(
        history,
        use_container_width=True
    )

else:

    st.info(
        "No scans available yet. "
        "Scan a product to create history."
    )
    
# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "Smart India Hackathon Prototype | "
    "AI-Based Legal Metrology Compliance Assessment System"
)