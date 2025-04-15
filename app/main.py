from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models.user import Base
from app.routes import auth, users, admin,  complaints, campaign , ws  ,content
from app.services.language import LanguageProcessor
from app.services.voice import VoiceProcessor

# Initialize FastAPI app
app = FastAPI(title="Wajibika API", version="0.1.0")
async def startup():
    # Initialize services
    app.state.language_processor = LanguageProcessor()
    app.state.voice_processor = VoiceProcessor()
    
# CORS Middleware (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(complaints.router) 
app.include_router(campaign.router) 
app.include_router(ws.router)
app.include_router(content.router)


# Create database tables (for development only)
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to Wajibika API!"}