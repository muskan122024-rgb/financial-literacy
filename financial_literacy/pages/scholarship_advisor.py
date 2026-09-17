"""
pages/scholarship_advisor.py

Scholarship guidance — helps students understand what to look for.
Uses the AI assistant to generate tailored guidance text.
"""
from __future__ import annotations

import streamlit as st

from services.financial_assistant import FinancialAssistant
from utils.exceptions import AIServiceError


_SCHOLARSHIP_DISCLAIMER = (
    "⚠️ **Important:** This tool provides general educational guidance only. "
    "It does not verify your eligibility for any specific scholarship. "
    "Scholarship criteria, deadlines, and availability change frequently. "
    "Always verify information from official sources such as your college, "
    "the National Scholarship Portal (scholarships.gov.in), or the relevant "
    "government/institution website."
)

_COMMON_DOCUMENTS = [
    "Marksheets / Grade transcripts (current and previous years)",
    "Income certificate / Family income proof",
    "Caste or community certificate (if applicable)",
    "Domicile or residence certificate",
    "Aadhaar card or other government-issued photo ID",
    "Bank account details (for direct benefit transfer)",
    "College/university bonafide certificate",
    "Fee receipts or admission letter",
    "Disability certificate (if applicable)",
    "Passport-size photographs",
]


def show() -> None:
    st.title("🎓 Scholarship Advisor")
    st.markdown(
        "Answer a few questions and get general guidance about what scholarship "
        "criteria and documents you should look into."
    )
    st.warning(_SCHOLARSHIP_DISCLAIMER)

    # ------------------------------------------------------------------
    # Student information form
    # ------------------------------------------------------------------
    st.markdown("---")
    st.subheader("Tell us about yourself")
    st.caption(
        "This information is only used within the app to generate guidance. "
        "Nothing is stored or shared."
    )

    with st.form("scholarship_form"):
        education_level = st.selectbox(
            "Education Level",
            [
                "Undergraduate (UG) — 1st Year",
                "Undergraduate (UG) — 2nd Year",
                "Undergraduate (UG) — 3rd Year",
                "Postgraduate (PG) — 1st Year",
                "Postgraduate (PG) — 2nd Year",
                "Diploma",
                "PhD / Research",
            ],
        )

        course = st.text_input(
            "Course / Field of Study",
            placeholder="e.g. B.Tech Computer Science, B.Com, MBBS",
            max_chars=100,
        )

        state = st.text_input(
            "State / Region",
            placeholder="e.g. Maharashtra, Karnataka",
            max_chars=50,
        )

        academic_performance = st.selectbox(
            "Approximate Academic Performance",
            [
                "Above 90% / 9+ CGPA",
                "75–90% / 7.5–9 CGPA",
                "60–75% / 6–7.5 CGPA",
                "Below 60% / Below 6 CGPA",
                "Prefer not to say",
            ],
        )

        income_category = st.selectbox(
            "Family Annual Income (approximate)",
            [
                "Below ₹1 lakh",
                "₹1–2.5 lakh",
                "₹2.5–5 lakh",
                "₹5–8 lakh",
                "Above ₹8 lakh",
                "Prefer not to say",
            ],
        )

        special_category = st.multiselect(
            "Do any of these apply to you? (Optional)",
            [
                "SC / ST category",
                "OBC category",
                "Person with disability (PwD)",
                "Single parent / orphan",
                "Girl student",
                "Minority community",
                "None / Prefer not to say",
            ],
        )

        submitted = st.form_submit_button(
            "🔍 Get Scholarship Guidance", type="primary"
        )

    if submitted:
        if not course.strip():
            st.error("❌ Please enter your course/field of study.")
            return

        _show_guidance(
            education_level,
            course,
            state,
            academic_performance,
            income_category,
            special_category,
        )


def _show_guidance(
    education_level: str,
    course: str,
    state: str,
    academic_performance: str,
    income_category: str,
    special_category: list,
) -> None:
    """Display scholarship guidance based on the student's inputs."""

    st.markdown("---")
    st.subheader("📋 Scholarship Criteria to Look For")

    # ------------------------------------------------------------------
    # General eligibility criteria checklist
    # ------------------------------------------------------------------
    criteria_items = []

    # Merit-based
    if "Above 90%" in academic_performance or "75–90%" in academic_performance:
        criteria_items.append(
            "**Merit-based scholarships** — Your academic performance may qualify "
            "you for merit scholarships. Look for schemes requiring 75%+ marks."
        )

    # Income-based
    if income_category in [
        "Below ₹1 lakh",
        "₹1–2.5 lakh",
        "₹2.5–5 lakh",
    ]:
        criteria_items.append(
            "**Need-based / means-tested scholarships** — Many central and state "
            "government scholarships target families with annual income below "
            "₹2.5 lakh or ₹5 lakh. Check the National Scholarship Portal."
        )

    # Category-based
    if any(c in special_category for c in ["SC / ST category", "OBC category"]):
        criteria_items.append(
            "**SC/ST/OBC scholarships** — The government offers several dedicated "
            "scholarship schemes for SC, ST, and OBC students. "
            "Check with your college welfare office and scholarships.gov.in."
        )
    if "Girl student" in special_category:
        criteria_items.append(
            "**Girl student scholarships** — Several state and central schemes "
            "specifically support female students in higher education."
        )
    if "Person with disability (PwD)" in special_category:
        criteria_items.append(
            "**PwD scholarships** — The Department of Empowerment of Persons with "
            "Disabilities (DEPwD) offers scholarships. Verify through official channels."
        )
    if "Minority community" in special_category:
        criteria_items.append(
            "**Minority scholarships** — The Ministry of Minority Affairs offers "
            "pre-matric, post-matric, and merit-cum-means scholarships."
        )

    # State-specific
    if state.strip():
        criteria_items.append(
            f"**State scholarships for {state.strip()}** — Your state government "
            "likely has dedicated scholarship schemes. Check the state higher "
            "education department's website."
        )

    # Education loan interest subsidy
    criteria_items.append(
        "**Central Sector Scheme of Scholarships** — For students from families "
        "with income below ₹8 lakh. Covers both UG and PG students at recognised "
        "institutions. Check scholarships.gov.in."
    )

    if not criteria_items:
        criteria_items.append(
            "Based on the information provided, check general merit and "
            "institution-based scholarships on scholarships.gov.in."
        )

    for item in criteria_items:
        st.markdown(f"- {item}")

    # ------------------------------------------------------------------
    # Documents checklist
    # ------------------------------------------------------------------
    st.markdown("---")
    st.subheader("📄 Common Documents You May Need")
    for doc in _COMMON_DOCUMENTS:
        st.markdown(f"- {doc}")

    st.caption(
        "Document requirements vary by scholarship. Always check the specific "
        "scholarship's official notification for the exact list."
    )

    # ------------------------------------------------------------------
    # AI-generated guidance
    # ------------------------------------------------------------------
    st.markdown("---")
    st.subheader("🤖 AI Guidance (IBM Bob)")

    assistant = FinancialAssistant()
    if assistant.is_stub():
        st.info(
            "AI assistant is in offline mode. Configure your API credentials "
            "in .env to get AI-generated scholarship guidance."
        )
        _show_static_scholarship_tips()
        return

    context = (
        f"Student profile: {education_level}, studying {course}, "
        f"from {state if state.strip() else 'not specified'}, "
        f"academic performance: {academic_performance}, "
        f"family income: {income_category}, "
        f"special categories: {', '.join(special_category) if special_category else 'none'}."
    )
    question = (
        "What scholarship eligibility criteria should this student look for? "
        "What questions should they verify from official sources? "
        "Do not claim they are definitely eligible — just explain what to check."
    )

    with st.spinner("Getting AI guidance…"):
        try:
            response = assistant.ask(question, context=context)
            st.markdown(response)
        except AIServiceError as e:
            st.error(f"AI service unavailable: {e}")
            _show_static_scholarship_tips()

    st.warning(_SCHOLARSHIP_DISCLAIMER)


def _show_static_scholarship_tips() -> None:
    st.markdown(
        """
        **General tips for finding scholarships:**
        - Visit **scholarships.gov.in** (National Scholarship Portal) — the single
          largest source for central government scholarships in India.
        - Check your **college's scholarship/welfare office** — many institutions
          have their own scholarships or can guide you to state schemes.
        - Ask about **education loan interest subsidies** if you have taken or
          are planning to take an education loan.
        - Look for **private scholarships** from organisations like Tata Trusts,
          Infosys Foundation, and Reliance Foundation — eligibility varies.
        - Apply early — many scholarships have limited seats and strict deadlines.
        - Always read the official scholarship notification carefully before applying.

        *Verify all information from official sources before applying.*
        """
    )
