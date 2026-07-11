from app.core.config import settings

print("Model:", settings.GEMINI_MODEL)

if settings.GEMINI_API_KEY:
    print("API Key Loaded ✅")
    print("Starts with:", settings.GEMINI_API_KEY[:6])
else:
    print("API Key Missing ❌")