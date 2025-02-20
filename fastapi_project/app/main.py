import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, addresses
from app.database import Base, engine

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Profile Management API", version="1.0.0", description="A FastAPI-manages user profiles ")

app.add_middleware(
    CORSMiddleware,  # type:ignore
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(addresses.router, prefix="/api", tags=["Addresses"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the FastAPI User Profile Management System 🚀"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
