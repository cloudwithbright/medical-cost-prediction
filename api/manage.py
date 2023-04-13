
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes import router
app = FastAPI()

origins = ["*"]

# Configure middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router=router)