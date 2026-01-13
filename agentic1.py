import streamlit as st
from openai import OpenAI
from datetime import datetime
import os 

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GenAI SOW Architect",
    page_icon="📄",
    layout="wide"
)

# ---------------- OPENAI HELPER ----------------
import openai

def generate_text(prompt):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text

output = generate_text("Write a one-line SOW objective.")
print(output)


# ---------------- SESSION STATE ----------------
if "sow" not in st.session_state:
    st.session_state.sow = {}

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Configuration")

    # For Streamlit Cloud use secrets
    openai_api_key = st.secrets.get("OPENAI_API_KEY", "")

    if not openai_api_key:
        st.warning("OpenAI API key not configured in Secrets")
    else:
        st.success("OpenAI API key loaded")

# ---------------- MAIN UI ----------------
st.title("📄 GenAI SOW Architect")
st.caption("Generate → Edit → Download professional SOW documents")

tabs = st.tabs(["1️⃣ Generate", "2️⃣ Edit & Review", "3️⃣ Download"])

# ================= TAB 1: GENERATE =================
with tabs[0]:
    sol_type = st.selectbox(
        "Solution Type",
        [
            "Intelligent Search",
            "Recommendation System",
            "Customer Review Analysis",
            "Virtual Assistant",
            "AI Agents",
            "Other"
        ]
    )

    industry = st.text_input("Industry", "Retail / E-commerce")
    customer = st.text_input("Customer Name", "Acme Corp")

    if st.button("✨ Generate SOW Content"):
        if not openai_api_key:
            st.error("OpenAI API key missing")
        else:
            with st.spinner("Generating content..."):

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





