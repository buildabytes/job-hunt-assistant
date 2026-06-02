
from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI

from utils.config import GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
)

def get_jd_analyst_agent():
    return Agent(
        role="Job Description Analyst",
        goal=(
            "Read a job posting and distill it into the details a candidate "
            "actually needs: requirements, responsibilities, and qualifications."
        ),
        backstory=(
            "You are a seasoned technical recuriter who has read thousands of "
            "job descriptions. You cut through boilerplate and surface what "
            "matters to an application deciding whether to apply."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

def create_jd_analysis_task(agent, job_description):
    return Task(
        description=(
            "Analyze the job description below and extract its key details. \n\n"
            f"Job Description:\n{job_description}\n\n"
            "Identify the role title, hiring organization, location and remote "
            "options, required skills and qualification, preferred/nice-to-have "
            "skills, core responsibilities, and salary or pay grade if present."
        ),
        expected_output=(
            "A structured markdown summary using these sections, each with "
            "bultter points:\n"
            "## Role Title\n"
            "## Organization\n"
             "## Location & Remote Options\n"
            "## Required Skills & Qualifications\n"
            "## Preferred Skills\n"
            "## Key Responsibilities\n"
            "## Salary / Grade\n\n"
            "If a detail is not stated in the posting, write 'Not specified' "
            "rather than guessing."
        ),
        agent=agent,
        output_file="/data/report.md",
    )