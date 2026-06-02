from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI

from utils.config import GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)

def get_resume_cl_agent():
    return Agent(
        role="Resume and cover letter writer",
        goal=(
            "Using the analyzed job description, write a tailored cover letter "
            "and a set of resume highlights that map the candidate's background "
            "to the role's key requirements, making a clear and honest case for "
            "why they are a strong fit."
        ),
        backstory=(
            "You are a seasoned career coach and professional resume writer who "
            "has helped hundreds of candidates land interviews. You excel at "
            "translating a person's experience into the language of a specific "
            "posting, foregrounding the most relevant skills, and writing cover "
            "letters that feel specific and persuasive rather than generic and "
            "templated. You never invent experience the candidate does not have."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

def  create_resume_cl_task(agent, job_summary, resume_text):
    return Task(
        description=(
            "You are helping a candidate apply for a U.S. government job. Using "
            "the job summary and the candidate's current resume below, do two "
            "things:\n\n"
            "1. Tailor the candidate's resume summary so it aligns with the role's "
            "key requirements, foregrounding the most relevant experience. Do NOT "
            "invent experience the candidate does not have.\n"
            "2. Write a personalized cover letter appropriate for a government "
            "position: professional and formal in tone, specific to this role, "
            "and clearly connecting the candidate's background to the job's needs.\n\n"
            f"Job Summary:\n{job_summary}\n\n"
            f"Candidate Resume:\n{resume_text}"
        ),
         expected_output=(
            "The response MUST contain both sections, each introduced by its exact "
            "marker on its own line, so they can be parsed programmatically:\n\n"
            "<<RESUME_SUMMARY>>\n"
            "A tailored 3-5 sentence resume summary here.\n\n"
            "<<COVER_LETTER>>\n"
            "A complete, personalized cover letter here.\n\n"
            "Emit the markers exactly as written, with nothing before "
            "<<RESUME_SUMMARY>>."
        ),
        agent=agent,
        output_file="/data/resume_agent_output.txt",
    )