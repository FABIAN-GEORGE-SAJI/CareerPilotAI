# CareerPilot AI 🚀
**Next-Gen AI-Powered Career Intelligence Platform**

CareerPilot AI is an end-to-end intelligent career suite designed to bridge the gap between your professional profile and market demands. Using advanced semantic analysis and multi-agent AI workflows, CareerPilot helps you beat the ATS, optimize your resume, and prepare for high-stakes technical interviews.

## 🛠 Core Intelligence Modules
*   **Semantic Resume Engine:** Deep parsing to extract impact metrics and skills.
*   **Precision ATS Diagnostics:** Rule-based and AI-driven scoring with actionable gap analysis.
*   **Agentic Career Coach:** A context-aware Gemini-powered assistant for salary negotiation, strategy, and resume feedback.
*   **Technical Mock Interviews:** Calibrated one-on-one technical screening sessions.
*   **Custom Growth Roadmaps:** Personalized 30/60/90-day upskilling plans.

## 🚀 The Conversion Pipeline
1.  **Ingest:** Upload your resume (PDF/DOCX) for structural parsing.
2.  **Target:** Input job descriptions for semantic keyword mapping.
3.  **Diagnose:** Receive instant gap analysis and recruiter-grade feedback.
4.  **Optimize:** Generate ATS-optimized rewrites using the Google X-Y-Z formula.
5.  **Train:** Conduct mock interviews and follow structured learning roadmaps.

## ⚙️ Tech Stack
*   **Frontend:** Streamlit (High-performance, reactive UI)
*   **Backend:** FastAPI (Async-first, production-ready)
*   **AI Engine:** Google Gemini (Generative models via LangChain)
*   **Vector Search:** ChromaDB (Semantic resume & job matching)
*   **Persistence:** SQLAlchemy & Alembic (Secure user and document management)

## 📦 Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/career-pilot-ai.git](https://github.com/FABIAN-GEORGE-SAJI/career-pilot-ai.git)
    cd career-pilot-ai
    ```

2.  **Setup Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    3.1 3. Install Backend Dependencies:

        ```bash
        cd backend
        pip install -r requirements.txt
        cd ..
    
    3.2 Install Frontend Dependencies:

        cd frontend
        pip install -r requirements.txt
        cd ..

4.  **Environment Configuration:**
    Create a `.env` file in the `backend/` directory based on the `.env.example`:
    ```env
    GEMINI_API_KEY=your_actual_key_here
    GEMINI_MODEL=gemini-2.5-flash
    ```

5.  **Launch the Application:**
    5.1 Start the Backend
    Open a terminal:
    ```bash
    cd backend
    uvicorn app.main:app --reload
    ```

    5.2 Start the frontend
    Open a second terminal:
    ```bash
    cd frontend
    streamlit run app.py
    ```

## 🛡️ Security Note
Ensure your `.env` file is **never** committed to version control. Use the provided `.env.example` as a template for new installations.

## 🚀 Deployment
This project is built for production-ready deployment via platforms like **Railway**, **Render**, or **AWS**. 
1. Push your code to a GitHub repository.
2. Connect your repository to your chosen hosting provider.
3. Configure your Environment Variables in the hosting dashboard.