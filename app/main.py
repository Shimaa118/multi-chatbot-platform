from fastapi import FastAPI 
from app.routes.auth import auth_router
from app.routes.chatbot import chatbot_router
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse

app = FastAPI()

# Register routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Multi-Chatbot Creation Platform"}


