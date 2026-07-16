import requests
import streamlit as st
from config import API_BASE_URL

class CareerPilotAPI:

    @staticmethod
    def headers():
        # Defensive programming: Cast to string to prevent crashes if session state contains non-string types
        token = str(st.session_state.get("access_token", "")).strip()
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}

    @staticmethod
    def logout():
        keys = [
            "authenticated", "access_token", "user", 
            "resume_id", "job_id", "resume_response", 
            "parsed_resume", "resume_filename", "resume_size", 
            "resume_type", "job_response", "parsed_job", 
            "ats_report", "match", "feedback", "rewrite", 
            "cover_letter", "interview", "roadmap", 
            "career_agent_history", "redirect_after_login"
        ]
        for key in keys:
            st.session_state.pop(key, None)

    @staticmethod
    def register(name, email, password):
        return requests.post(
            f"{API_BASE_URL}/auth/register",
            json={"name": name, "email": email, "password": password},
            timeout=30,
        )

    @staticmethod
    def login(email, password):
        return requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"email": email, "password": password},
            timeout=30,
        )

    @staticmethod
    def health():
        return requests.get(
            f"{API_BASE_URL}/health/",
            timeout=10,
        )

    @staticmethod
    def upload_resume(file):
        return requests.post(
            f"{API_BASE_URL}/resume/upload",
            files={"file": file},
            headers=CareerPilotAPI.headers(),
            timeout=30,
        )

    @staticmethod
    def upload_job(file):
        return requests.post(
            f"{API_BASE_URL}/jobs/upload",
            files={"file": (file.name, file, "application/pdf")},
            headers=CareerPilotAPI.headers(),
            timeout=30,
        )

    @staticmethod
    def match(resume_id, job_id):
        return requests.post(
            f"{API_BASE_URL}/match",
            json={"resume_id": resume_id, "job_id": job_id},
            headers=CareerPilotAPI.headers(),
            timeout=30,
        )

    @staticmethod
    def feedback(resume_id, job_id):
        return requests.post(
            f"{API_BASE_URL}/ai/feedback",
            json={"resume_id": resume_id, "job_id": job_id},
            headers=CareerPilotAPI.headers(),
            timeout=30,
        )

    @staticmethod
    def rewrite(resume_id, job_id):
        return requests.post(
            f"{API_BASE_URL}/ai/rewrite",
            json={"resume_id": resume_id, "job_id": job_id},
            headers=CareerPilotAPI.headers(),
            timeout=30,
        )

    @staticmethod
    def cover_letter(resume_id, job_id):
        return requests.post(
            f"{API_BASE_URL}/ai/cover-letter",
            json={"resume_id": resume_id, "job_id": job_id},
            headers=CareerPilotAPI.headers(),
            timeout=30,
        )

    @staticmethod
    def interview(resume_id, job_id):
        return requests.post(
            f"{API_BASE_URL}/ai/interview",
            json={"resume_id": resume_id, "job_id": job_id},
            headers=CareerPilotAPI.headers(),
            timeout=30,
        )

    @staticmethod
    def roadmap(resume_id, job_id):
        return requests.post(
            f"{API_BASE_URL}/ai/roadmap",
            json={"resume_id": resume_id, "job_id": job_id},
            headers=CareerPilotAPI.headers(),
            timeout=30,
        )

    @staticmethod
    def career_agent(resume_id, job_id, message):
        return requests.post(
            f"{API_BASE_URL}/career-agent",
            json={"resume_id": resume_id, "job_id": job_id, "message": message},
            headers=CareerPilotAPI.headers(),
            timeout=30,
        )