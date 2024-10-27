from fastapi import FastAPI, Request
from pydantic import BaseModel
from textblob import TextBlob
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Пам'ять для збереження імені та лічильник взаємодій
memory = {"name": None, "interactions": 0}

# Налаштування шаблонів
templates = Jinja2Templates(directory="templates")

# Статичні файли
app.mount("/static", StaticFiles(directory="static"), name="static")

# Схема для повідомлення користувача
class ChatRequest(BaseModel):
    message: str

# Відповіді на основі настрою
def generate_response(user_input):
    blob = TextBlob(user_input)
    sentiment = blob.sentiment.polarity

    # Привітання та прощання
    if any(word in user_input.lower() for word in ["hello", "hi", "hey"]):
        return "Hi! How can I assist you today?"
    elif any(word in user_input.lower() for word in ["bye", "goodbye", "see you"]):
        return "Goodbye! Feel free to reach out anytime."

    # Аналіз настрою
    if sentiment > 0:
        return "I'm glad to hear that! 😊"
    elif sentiment < 0:
        return "I'm sorry you're facing issues. 😔"
    else:
        return "Alright! How can I assist you further?"

@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
async def chat(request: ChatRequest):
    user_input = request.message
    response = generate_response(user_input)

    # Оновлення лічильника взаємодій
    memory["interactions"] += 1

    # Зворотний зв'язок після трьох взаємодій
    if memory["interactions"] >= 3:
        response += " By the way, could you give some feedback on this conversation?"
        memory["interactions"] = 0  # Оновлення лічильника

    return {"response": response}
