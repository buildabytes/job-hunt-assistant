# AI Job Hunt Assistant

AI Job Hunt Assistant is a Streamlit app that helps job seekers find real federal job postings and generate tailored application materials with a small team of AI agents.

The app searches USAJOBS, lets you choose the roles you want to apply for, then uses CrewAI agents powered by Gemini to analyze the posting, tailor resume highlights, draft a cover letter, and write a short outreach message.

## Features

- Search live federal job postings from the USAJOBS API.
- Filter results by job keyword and location.
- Paste your resume and a short personal bio directly into the app.
- Select one or more job postings from the search results.
- Run a sequential CrewAI workflow for each selected job.
- Generate structured job analysis, tailored resume summary, cover letter content, and outreach messaging.
- Save generated application artifacts and application history in the `data/` folder.

## How It Works

The assistant is organized around a simple Streamlit interface and a three-agent CrewAI pipeline.

1. `streamlit_app.py` collects the job keyword, location, resume text, and bio.
2. `usajobs_api.py` calls the USAJOBS search API and returns matching federal postings.
3. `orchestrator.py` builds and runs the CrewAI workflow.
4. The agents in `agents/` generate the application materials:
   - `jd_analyst.py` extracts the important details from the job description.
   - `resume_cl_agent.py` creates a tailored resume summary and cover letter.
   - `messaging_agent.py` writes a concise outreach message.
5. `utils/tracking.py` can save cover letters and log application metadata.

## Tech Stack

- Python
- Streamlit
- CrewAI
- LangChain Google GenAI
- Gemini 2.5 Flash
- USAJOBS API
- python-dotenv
- requests

## Project Structure

```text
.
├── agents/
│   ├── jd_analyst.py
│   ├── messaging_agent.py
│   └── resume_cl_agent.py
├── data/
│   ├── sample_resume.txt
│   ├── applications_log.csv
│   ├── report.md
│   └── resume_agent_output.txt
├── utils/
│   ├── config.py
│   └── tracking.py
├── orchestrator.py
├── streamlit_app.py
├── usajobs_api.py
├── LICENSE
└── README.md
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/buildabytes/job-hunt-assistant.git
cd job-hunt-assistant
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

This repository does not currently include a pinned `requirements.txt`, so install the app dependencies directly:

```bash
pip install streamlit crewai langchain-google-genai python-dotenv requests
```

### 4. Configure Environment Variables

Create a `.env` file and add your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key
USAJOBS_API_KEY=your_usajobs_api_key
```

The app loads environment variables through `utils/config.py`.

You can request a USAJOBS API key from the official USAJOBS developer site. The Gemini key is used by the CrewAI agents through `langchain-google-genai`.

### 5. Run the App

```bash
streamlit run streamlit_app.py
```

Then open the local Streamlit URL shown in your terminal.

## Usage

1. Enter a job keyword, such as `data scientist`.
2. Enter a location, such as `remote`, or leave it broad for more results.
3. Paste your resume text.
4. Add a short bio that describes your background and goals.
5. Click **Search Jobs**.
6. Select the postings you want to apply for.
7. Click **Apply to Selected Jobs**.
8. Review the generated analysis, resume summary, cover letter, and outreach message.

## Generated Files

The project can write generated application materials to the `data/` directory:

- `data/report.md` for job analysis output.
- `data/resume_agent_output.txt` for resume and cover letter output.
- `data/applications_log.csv` for application tracking.
- `data/cover_letters/` for saved cover letter text files.

Review generated content before using it in a real application.

## Notes

- The assistant is designed to support the job application process, not fully automate it.
- Generated materials should be edited and fact-checked before submission.
- The resume and outreach agents are instructed not to invent experience.
- API keys should stay local and should not be committed to GitHub.

## License

This project is licensed under the MIT License.
