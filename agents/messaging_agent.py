from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI

from utils.config import GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY
)

def get_messaging_agent():
    return Agent(
        role="Outreach Message Writer",
        goal=(
            "Write short, personalized outreach messages — recruiter and "
            "hiring-manager notes, networking requests, and follow-ups — that "
            "tie the candidate's background to a specific role and invite a "
            "reply, without sounding generic or pushy."
        ),
        backstory=(
            "You are a job-search and networking coach who has written thousands "
            "of outreach messages that actually get responses. You know great "
            "outreach is brief, specific, and respectful of the reader's time: "
            "it opens with a genuine hook, connects the candidate's most relevant "
            "experience to the role, and closes with a clear, low-friction ask. "
            "You never sound like a mass-blasted template, and you never invent "
            "details about the candidate."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

def create_messaging_task(agent, job_summary, agency_name, user_bio):
    return Task(
        description=(
            "Write a brief, professional outreach message from the candidate "
            f"expressing genuine interest in a role at {agency_name}. Use the "
            "job summary and the candidate's bio below to connect their most "
            "relevant experience to what the role needs. Keep it warm but "
            "professional, specific rather than generic, and do not invent any "
            "experience the candidate does not have.\n\n"
            f"Hiring organization: {agency_name}\n\n"
            f"Job Summary:\n{job_summary}\n\n"
            f"Candidate Bio:\n{user_bio}"
        ),
        expected_output=(
            "A single outreach message under 150 words, suitable to send on "
            "LinkedIn or by email. Open with a specific hook, tie one or two of "
            "the candidate's most relevant strengths to the role, and close with "
            "a clear, low-friction ask such as a short conversation. Write it "
            "ready to send — no subject line, and no unfilled placeholders."
        ),
        agent=agent,
    )