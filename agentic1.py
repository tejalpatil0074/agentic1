import streamlit as st
from openai import OpenAI
from datetime import datetime
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

# ---------------- IMAGE HELPERS ----------------
def image_to_base64(image_file):
    return base64.b64encode(image_file.read()).decode()

def file_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ---------------- SESSION STATE ----------------
if "sow" not in st.session_state:
    st.session_state.sow = {}

if "customer_logo" not in st.session_state:
    st.session_state.customer_logo = None

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Configuration")

    openai_api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not openai_api_key:
        st.warning("OpenAI API key not configured")
    else:
        st.success("OpenAI API key loaded")

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

    final_solution = other_solution if other_solution else sol_type
    final_industry = other_industry if other_industry else industry

    if st.button("✨ Generate SOW Content"):
        if not openai_api_key:
            st.error("OpenAI API key missing")
        else:
            with st.spinner("Generating content..."):

                st.session_state.customer_logo = customer_logo

                objective_prompt = f"""
Write EXACTLY 2 concise professional business sentences
for a Statement of Work objective.

Solution: {final_solution}
Industry: {final_industry}
Customer: {customer}

Focus on business outcomes and measurable value.
"""

                stakeholders_prompt = f"""
List EXACTLY 4 stakeholders in this format:
Name – Role – Organization

Context: {final_solution} project for {customer}
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
                    "solution": final_solution,
                    "industry": final_industry,
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
        st.info("Generate content first")
    else:
        sow = st.session_state.sow

        st.subheader("📝 Objective")
        sow["objective"] = st.text_area("", sow["objective"], height=120)

        st.subheader("➕ Add Stakeholder")
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("Name")
        with c2:
            role = st.text_input("Role")
        with c3:
            org = st.text_input("Organization")

        if st.button("Add Stakeholder"):
            if name and role and org:
                sow["stakeholders"] += f"\n{name} – {role} – {org}"
                st.success("Stakeholder added")

        st.subheader("👥 Stakeholders")
        sow["stakeholders"] = st.text_area("", sow["stakeholders"], height=160)

        st.subheader("📌 Assumptions & Dependencies")
        sow["assumptions"] = st.text_area("", sow["assumptions"], height=220)

        st.subheader("🗓 Timeline")
        sow["timeline"] = st.text_area("", sow["timeline"], height=220)

# ================= TAB 3: DOWNLOAD =================
with tabs[2]:
    if not st.session_state.sow:
        st.warning("Nothing to download yet")
    else:
        sow = st.session_state.sow

        logo1_b64 = file_to_base64("assets/common_logo_1.png")
        logo2_b64 = file_to_base64("assets/common_logo_2.png")

        customer_logo_b64 = ""
        if st.session_state.customer_logo:
            customer_logo_b64 = image_to_base64(st.session_state.customer_logo)

        html_doc = f"""
<html>
<body style="font-family:Arial; line-height:1.6;">
<div style="display:flex; justify-content:space-between;">
<img src="data:image/png;base64,{logo1_b64}" height="60"/>
<img src="data:image/png;base64,{customer_logo_b64}" height="60"/>
<img src="data:image/png;base64,{logo2_b64}" height="60"/>
</div>
<hr/>

<h1>Statement of Work</h1>
<p><b>Customer:</b> {sow['customer']}</p>
<p><b>Industry:</b> {sow['industry']}</p>
<p><b>Date:</b> {datetime.now().strftime('%d %b %Y')}</p>

<h2>Objective</h2>
<p>{sow['objective']}</p>

<h2>Stakeholders</h2>
<p>{sow['stakeholders'].replace(chr(10), '<br>')}</p>

<h2>Assumptions & Dependencies</h2>
<p>{sow['assumptions'].replace(chr(10), '<br>')}</p>

<h2>Timeline</h2>
<p>{sow['timeline'].replace(chr(10), '<br>')}</p>
</body>
</html>
"""

        st.download_button(
            "📥 Download SOW (Word)",
            data=html_doc,
            file_name="Statement_of_Work.doc",
            mime="application/msword"
        )
