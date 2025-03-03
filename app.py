from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from uuid import uuid4
import random

app = FastAPI()

# Простейшее in-memory хранилище сессий
sessions = {}

# Фиксированные учетные данные (для примера)
USERNAME = "admin"
PASSWORD = "1111"


@app.get("/", response_class=HTMLResponse)
async def login_form():
    return """
    <html>
      <head>
        <title>Авторизация</title>
      </head>
      <body>
        <h2>Войдите в систему</h2>
        <form action="/login" method="post">
          <label>Имя пользователя:</label>
          <input type="text" name="username" /><br/>
          <label>Пароль:</label>
          <input type="password" name="password" /><br/><br/>
          <input type="submit" value="Войти"/>
        </form>
      </body>
    </html>
    """


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == USERNAME and password == PASSWORD:
        # Генерируем уникальный идентификатор сессии и 4-значный код
        session_id = str(uuid4())
        code = random.randint(1000, 9999)
        sessions[session_id] = code

        # Перенаправляем на страницу с кодом, устанавливая cookie с session_id
        response = RedirectResponse(url="/code", status_code=302)
        response.set_cookie(key="session", value=session_id)
        return response
    else:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")


@app.get("/code", response_class=HTMLResponse)
async def get_code(request: Request):
    session_id = request.cookies.get("session")
    if session_id and session_id in sessions:

        code = f"{random.randint(1, 9999):04d}"
        response = HTMLResponse(f"""
            <html>
              <head>
                <title>Сгенерированный код</title>
              </head>
              <body>
                <h1>Ваш код: {code}</h1>
                <p>Обновление страницы приведёт к выходу из системы.</p>
              </body>
            </html>
        """)
        response.delete_cookie("session")
        return response
    else:
        # Если сессия недействительна, перенаправляем на форму авторизации
        return RedirectResponse(url="/")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)