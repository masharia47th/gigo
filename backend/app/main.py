from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import welcome, auth, admin

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust if needed for your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers for different endpoints
app.include_router(welcome.router)
app.include_router(auth.router)
app.include_router(admin.router, prefix="/admin")

# Define a root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI React App!"}
