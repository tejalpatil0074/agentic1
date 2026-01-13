import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GenAI SOW Architect",
    page_icon="📄",
    layout="wide"
)

# ---------------- OPENAI HELPER ----------------
def call_openai(prompt, api_key):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a senior enterprise solution architect writing professional Statements of Work."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()

# ===== IMAGE HELPERS =====
def image_to_base64(image_file):
    return base64.b64encode(image_file.read()).decode()

def file_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()



# ---------------- SESSION STATE ----------------
if "sow" not in st.session_state:
    st.session_state.sow = {}

# ===== ADDED =====
if "customer_logo" not in st.session_state:
    st.session_state.customer_logo = None

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Configuration")

    # For Streamlit Cloud use secrets
    openai_api_key = st.secrets.get("OPENAI_API_KEY", "")

    if not openai_api_key:
        st.warning("OpenAI API key not configured in Secrets")
    else:
        st.success("OpenAI API key loaded")

 # ===== ADDED: CUSTOMER LOGO UPLOAD =====
    st.subheader("🏷 Branding")

    customer_logo = st.file_uploader(
        "Upload Customer Logo",
        type=["png", "jpg", "jpeg"]
    )

    if customer_logo:
        st.image(customer_logo, width=150)


# ---------------- MAIN UI ----------------
st.title("📄 GenAI SOW Architect")
st.caption("Generate → Edit → Download professional SOW documents")

tabs = st.tabs(["1️⃣ Generate", "2️⃣ Edit & Review", "3️⃣ Download"])

# ================= TAB 1: GENERATE =================
with tabs[0]:
    sol_type = st.selectbox(
    "Solution Type",
    [
        "Multi Agent Store Advisor",
        "Intelligent Search",
        "Recommendation",
        "AI Agents Demand Forecasting",
        "Banner Audit using LLM",
        "Image Enhancement",
        "Virtual Try-On",
        "Agentic AI L1 Support",
        "Product Listing Standardization",
        "AI Agents Based Pricing Module",
        "Cost, Margin Visibility & Insights using LLM",
        "AI Trend Simulator",
        "Virtual Data Analyst (Text to SQL)",
        "Multilingual Call Analysis",
        "Customer Review Analysis",
        "Sales Co-Pilot",
        "Research Co-Pilot",
        "Product Copy Generator",
        "Multi-agent e-KYC & Onboarding",
        "Document / Report Audit",
        "RBI Circular Scraping & Insights Bot",
        "Visual Inspection",
        "AIoT based CCTV Surveillance",
        "Multilingual Voice Bot",
        "SOP Creation",
        "Other (Please specify)"
    ]
)
other_solution = ""
if sol_type == "Other (Please specify)":
    other_solution = st.text_input("Please specify solution type")


    industry = st.selectbox(
    "Industry",
    [
        "Retail / E-commerce",
        "BFSI",
        "Manufacturing",
        "Telecom",
        "Healthcare",
        "Energy / Utilities",
        "Logistics",
        "Media",
        "Government",
        "Other (Specify)"
    ]
)
other_industry = ""
if industry == "Other (Specify)":
    other_industry = st.text_input("Please specify industry")

    customer = st.text_input("Customer Name", "Acme Corp")

    if st.button("✨ Generate SOW Content"):
        if not openai_api_key:
            st.error("OpenAI API key missing")
        else:
            with st.spinner("Generating content..."):
 # ===== ADDED =====
                 st.session_state.customer_logo = customer_logo

                objective_prompt = f"""
Write EXACTLY 2 concise professional business sentences
for a Statement of Work objective.

Solution: {sol_type}
Industry: {industry}
Customer: {customer}

Focus on business outcomes and measurable value.
"""

                stakeholders_prompt = f"""
List EXACTLY 4 stakeholders in this format:
Name – Role – Organization

Context: {sol_type} project for {customer}
"""

                assumptions_prompt = f"""
Provide:
Assumptions:
- 5 bullet points

Dependencies:
- 5 bullet points

Context: Enterprise AI implementation
"""

                timeline_prompt = f"""
Create a delivery timeline table.

Format:
Phase | Key Activities | Duration

Provide EXACTLY 4 phases.
"""

                st.session_state.sow = {
                    "solution": sol_type,
                    "industry": industry,
                    "customer": customer,
                    "objective": call_openai(objective_prompt, openai_api_key),
                    "stakeholders": call_openai(stakeholders_prompt, openai_api_key),
                    "assumptions": call_openai(assumptions_prompt, openai_api_key),
                    "timeline": call_openai(timeline_prompt, openai_api_key),
                }

                st.success("Content generated successfully!")

# ================= TAB 2: EDIT & REVIEW =================
with tabs[1]:
    if not st.session_state.sow:
        st.info("Generate content first in Tab 1")
    else:
        sow = st.session_state.sow

        st.subheader("📝 Objective (Editable)")
        sow["objective"] = st.text_area(
            "Edit Objective",
            sow["objective"],
            height=120
        )
# ===== ADDED: ADD STAKEHOLDER FORM =====
st.subheader("➕ Add Stakeholder")

col1, col2, col3 = st.columns(3)
with col1:
    stakeholder_name = st.text_input("Name", key="stk_name")
with col2:
    stakeholder_role = st.text_input("Role", key="stk_role")
with col3:
    stakeholder_org = st.text_input("Organization", key="stk_org")

    if st.button("Add Stakeholder"):
            if stakeholder_name and stakeholder_role and stakeholder_org:
                sow["stakeholders"] += f"\n{stakeholder_name} – {stakeholder_role} – {stakeholder_org}"
                st.success("Stakeholder added")
            else:
                st.warning("Please fill all stakeholder fields")

        st.subheader("👥 Stakeholders (Editable)")
        sow["stakeholders"] = st.text_area(
            "Edit Stakeholders",
            sow["stakeholders"],
            height=160
        )

        st.subheader("📌 Assumptions & Dependencies (Editable)")
        sow["assumptions"] = st.text_area(
            "Edit Assumptions & Dependencies",
            sow["assumptions"],
            height=220
        )

        st.subheader("🗓 Timeline (Editable)")
        sow["timeline"] = st.text_area(
            "Edit Timeline",
            sow["timeline"],
            height=220
        )

        st.success("Edits are saved automatically")


        st.subheader("👥 Stakeholders (Editable)")
        sow["stakeholders"] = st.text_area(
            "Edit Stakeholders",
            sow["stakeholders"],
            height=160
        )

        st.subheader("📌 Assumptions & Dependencies (Editable)")
        sow["assumptions"] = st.text_area(
            "Edit Assumptions & Dependencies",
            sow["assumptions"],
            height=220
        )

        st.subheader("🗓 Timeline (Editable)")
        sow["timeline"] = st.text_area(
            "Edit Timeline",
            sow["timeline"],
            height=220
        )

        st.success("Edits are saved automatically")

# ================= TAB 3: DOWNLOAD =================
with tabs[2]:
    if not st.session_state.sow:
        st.warning("Nothing to download yet")
    else:
        sow = st.session_state.sow

 # ===== ADDED: LOAD LOGOS =====
        logo1_b64 = file_to_base64("assets/common_logo_1.png")
        logo2_b64 = file_to_base64("assets/common_logo_2.png")

        html_doc = f"""
        <html>
        <body style="font-family:Arial; line-height:1.6;">
        <h1>Statement of Work</h1>

        <p><b>Customer:</b> {sow['customer']}</p>
        <p><b>Industry:</b> {sow['industry']}</p>
        <p><b>Date:</b> {datetime.now().strftime('%d %b %Y')}</p>

        <h2>1. Objective</h2>
        <p>{sow['objective']}</p>

        <h2>2. Stakeholders</h2>
        <p>{sow['stakeholders'].replace(chr(10), '<br>')}</p>

        <h2>3. Assumptions & Dependencies</h2>
        <p>{sow['assumptions'].replace(chr(10), '<br>')}</p>

        <h2>4. Delivery Timeline</h2>
        <p>{sow['timeline'].replace(chr(10), '<br>')}</p>
        </body>
        </html>
        """

        st.download_button(
            "📥 Download SOW (Word Format)",
            data=html_doc,
            file_name="Statement_of_Work.doc",
            mime="application/msword"
        )








