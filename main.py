from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import List, Optional

from docx import Document
from docx.shared import Pt
import io

app = FastAPI()

# Sections
class PersonalInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

class Education(BaseModel):
    university: Optional[str] = None
    degree: Optional[str] = None
    gpa: Optional[str] = None
    grad_date: Optional[str] = None

class ProfessionalExperience(BaseModel):
    company: Optional[str] = None
    job_title: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    bullet_points: List[str] = []

class ResumeData(BaseModel):
    personal_info: PersonalInfo = PersonalInfo()
    education: List[Education] = []
    professional_experience: List[ProfessionalExperience] = []
    skills: List[str] = []
    interests: List[str] = []

class ConversationState(BaseModel):
    resume_data: ResumeData = ResumeData()
    current_section: str = "personal_info"
    current_experience_index: int = -1  # -1 = not in experience entry

class ConversationRequest(BaseModel):
    state: ConversationState
    user_input: str

def get_next_question(state: ConversationState) -> str:
    if state.current_section == "personal_info":
        if not state.resume_data.personal_info.name:
            return "What is your full name?"
        elif not state.resume_data.personal_info.email:
            return "What is your email address?"
        elif not state.resume_data.personal_info.phone:
            return "What is your phone number (XXX-XXX-XXXX)?"
        elif not state.resume_data.personal_info.location:
            return "Where are you located (e.g., City, State)?"
        else:
            state.current_section = "education"

    if state.current_section == "education":
        if not state.resume_data.education:
            # init first education entry
            state.resume_data.education.append(Education())

        # latest education entry
        current_edu = state.resume_data.education[-1]

        if not current_edu.university:
            return "What university did you attend?"
        elif not current_edu.degree:
            return "What degree are you pursuing (Bachelor's/Master's in xxx)?"
        elif not current_edu.gpa:
            return "What is your GPA (X/4.0)?"
        elif not current_edu.grad_date:
            return "What is your expected graduation date (Month Year)?"
        else:
            state.current_section = "professional_experience"

    if state.current_section == "professional_experience":
        if state.current_experience_index == -1:
            return "Would you like to add a professional experience? (y/n)"
        else:
            exp = state.resume_data.professional_experience[state.current_experience_index]
            if not exp.company:
                return "Company name?"
            elif not exp.job_title:
                return "Job title?"
            elif not exp.start_date:
                return "Start date (Month Year)?"
            elif not exp.end_date:
                return "End date (Month Year)?"
            else:
                return "Add a bullet point (or type 'done' to finish this job):"

    if state.current_section == "skills":
        return "List your skills (comma-separated):"
    if state.current_section == "interests":
        return "List your interests (comma-separated):"

    return "Thank you! Resume is ready to generate."

@app.post("/conversation")
async def converse(request: ConversationRequest):
    # fixed it!!!!
    state = request.state
    user_input = request.user_input
    
    if state.current_section == "personal_info":
        if not state.resume_data.personal_info.name:
            state.resume_data.personal_info.name = user_input
        elif not state.resume_data.personal_info.email:
            state.resume_data.personal_info.email = user_input
        elif not state.resume_data.personal_info.phone:
            state.resume_data.personal_info.phone = user_input
        elif not state.resume_data.personal_info.location:
            state.resume_data.personal_info.location = user_input
        if (
            state.resume_data.personal_info.name
            and state.resume_data.personal_info.email
            and state.resume_data.personal_info.phone
            and state.resume_data.personal_info.location
        ):
            state.current_section = "education"

    elif state.current_section == "education":
        if not state.resume_data.education:
            # init first education entry with the university
            state.resume_data.education.append(Education(university=user_input))
        else:
            # get  latest education entry
            current_edu = state.resume_data.education[-1]

            if not current_edu.university:
                current_edu.university = user_input
            elif not current_edu.degree:
                current_edu.degree = user_input
            elif not current_edu.gpa:
                current_edu.gpa = user_input
            elif not current_edu.grad_date:
                current_edu.grad_date = user_input
            else:
                state.current_section = "professional_experience"

    elif state.current_section == "professional_experience":
        if state.current_experience_index == -1:
            if user_input.lower() == "yes":
                state.resume_data.professional_experience.append(ProfessionalExperience())
                state.current_experience_index = len(state.resume_data.professional_experience) - 1
            else:
                state.current_section = "skills"
        else:
            exp = state.resume_data.professional_experience[state.current_experience_index]
            if not exp.company:
                exp.company = user_input
            elif not exp.job_title:
                exp.job_title = user_input
            elif not exp.start_date:
                exp.start_date = user_input
            elif not exp.end_date:
                exp.end_date = user_input
            elif user_input.lower() != "done":
                exp.bullet_points.append(user_input)
            else:
                state.current_experience_index = -1  # Reset for next job

    next_q = get_next_question(state)
    return {"question": next_q, "state": state.model_dump()}

def generate_resume_docx(resume_data: ResumeData):
    
    return None

@app.post("/generate")
async def generate_resume(state: ConversationState):
    doc = generate_resume_docx(state.resume_data)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return Response(
        content=buffer.read(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=resume.docx"}
    )