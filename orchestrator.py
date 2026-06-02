from crewai import Crew, Process

from agents.jd_analyst import get_jd_analyst_agent, create_jd_analysis_task
from agents.resume_cl_agent import get_resume_cl_agent, create_resume_cl_task
from agents.messaging_agent import get_messaging_agent, create_messaging_task
from utils.tracking import log_application, save_cover_letter_file
from usajobs_api import fetch_usajobs


def load_resume():
    with open("data/sample_resume.txt", "r", encoding="utf-8") as f:
        return f.read()

def extract_between_markers(text, start, end=None):
    try:
        start_idx = text.index(start) + len(start)
        end_idx = text.index(end, start_idx)
        if end_idx == -1:
            end_idx = len(text)
        return text[start_idx:end_idx].strip()
    except ValueError:
        return "Not found"

def run_pipeline(job_data, resume_text, user_bio):
    descriptor = job_data["MatchedObjectDescriptor"]
    job_summary = (
        descriptor.get("QualificationSummary", "")
        or descriptor.get("UserArea", {}).get("Details", {}).get("JobSummary", "")
    )
    agency_name = descriptor.get("OrganizationName", "Unknown Agency")

    jd_agent = get_jd_analyst_agent()
    resume_agent = get_resume_cl_agent()
    message_agent = get_messaging_agent()

    jd_task = create_jd_analysis_task(jd_agent, job_summary)
    resume_task = create_resume_cl_task(resume_agent, job_summary, resume_text)
    message_task = create_messaging_task(message_agent, job_summary, agency_name, user_bio)

    crew = Crew(
        agents=[jd_agent, resume_agent, message_agent],
        tasks=[jd_task, resume_task, message_task],
        process=Process.sequential,
        verbose=True,
    )
    return crew.kickoff()

    resume_output = str(resume_task.output)
    resume_summary = extract_between_markers(resume_output, "<<RESUME_SUMMARY>>", "<<COVER_LETTER>>")
    cover_letter = extract_between_markers(resume_output, "<<COVER_LETTER>>")

    # Log and save
    log_application(job_title, agency_name, resume_summary)
    save_cover_letter_file(job_title, cover_letter)

if __name__ == "__main__":
    sample = fetch_usajobs("data scientist", location="")[0]
    print(run_pipeline(sample, load_resume(), "I'm a data professional."))