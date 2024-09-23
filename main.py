from fastapi import FastAPI, Request, Query, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from data_base import select_random_records, select_game_name_for_url, select_all_games, select_all_games_filter
import threading
from telegram_bot import start_telegram_bot
from typing import Optional

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def on_startup():
    threading.Thread(target=start_telegram_bot).start()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    games_random = select_random_records()
    return templates.TemplateResponse("home.html", {"request": request, "games": games_random})


@app.get("/about_us/", response_class=HTMLResponse)
async def about_us(request: Request):
    return templates.TemplateResponse("about_us.html", {"request": request})


@app.get("/buy_game/{game_name}/", response_class=HTMLResponse)
async def buy_game(request: Request, game_name: str):
    game = select_game_name_for_url(game_name)
    return templates.TemplateResponse("buy_game.html", {"request": request, "game": game})


@app.get("/all_games/", response_class=HTMLResponse)
async def all_games(
        request: Request,
        sort_by: Optional[str] = Query(None, title="Sort By", description="The field to sort by"),
        filter_text: Optional[str] = Query(None, title="Filter Text", description="Text to filter games by")
):
    games = select_all_games_filter(sort_by, filter_text)
    return templates.TemplateResponse("all_games.html", {"request": request, "games": games})


@app.get("/payment", response_class=HTMLResponse)
async def payment_page(request: Request):
    return templates.TemplateResponse("payment.html", {"request": request})


@app.post("/process_payment")
async def process_payment(request: Request, name: str = Form(...), card_number: str = Form(...),
                          expiry_date: str = Form(...), cvv: str = Form(...)):
    return RedirectResponse(url="/payment_success", status_code=303)


@app.get("/payment_success", response_class=HTMLResponse)
async def payment_success(request: Request):
    return templates.TemplateResponse("payment_success.html", {"request": request})
