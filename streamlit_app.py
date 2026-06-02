import streamlit as st
from orchestrator import run_pipeline
from usajobs_api import fetch_usajobs

st.set_page_config(page_title="AI Job Hunt Assistant", layout="centered")

st.title("AI Job Hunt Assistant")
st.markdown(
    "Enter a job keyword, location, your resume, and a short bio. The assistant "
    "pulls real federal job postings, lets you pick which ones to apply to, and "
    "drafts tailored application materials for each using a team of AI agents."
)

keyword = st.text_input("Job keyword", value="data scientist")
location = st.text_input("Location", value="remote")
resume_text = st.text_area("Resume text", height=200)
user_bio = st.text_area(
    "Short bio",
    value="I'm a data professional passionate about public service.",
    height=80,
)

# Step 1: search and store the top 5 jobs in session state.
if st.button("Search Jobs"):
    with st.spinner("Fetching postings…"):
        jobs = fetch_usajobs(keyword, location=location, results_per_page=5)
        st.write(f"DEBUG: fetched {len(jobs)} jobs")   # remove later
    if not jobs:
        st.error("No jobs found — try a broader keyword or clear the location.")
    else:
        st.session_state["jobs"] = jobs        # store the LIST under a key
        st.success(f"Found {len(jobs)} postings.")

# Step 2: render a checkbox for each stored job.
if "jobs" in st.session_state:
    st.markdown("### Select jobs to apply for:")
    selected_indexes = []
    for i, job in enumerate(st.session_state["jobs"]):
        d = job["MatchedObjectDescriptor"]
        title = d.get("PositionTitle", "Unknown Title")
        org = d.get("OrganizationName", "Unknown Agency")
        if st.checkbox(f"{title} — {org}", key=f"job_{i}"):
            selected_indexes.append(i)

    # Step 3: apply to each selected job.
    if st.button("Apply to Selected Jobs"):
        if not selected_indexes:
            st.warning("Please select at least one job.")
        elif not resume_text.strip():
            st.warning("Please paste your resume before applying.")
        else:
            for i in selected_indexes:
                job = st.session_state["jobs"][i]
                d = job["MatchedObjectDescriptor"]
                st.markdown(f"## {d.get('PositionTitle', 'Role')} — {d.get('OrganizationName', '')}")
                with st.spinner(f"Applying to {d.get('PositionTitle', 'role')}…"):
                    result = run_pipeline(job, resume_text, user_bio)
                st.markdown(str(result))