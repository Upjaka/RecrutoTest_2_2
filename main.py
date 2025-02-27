import random
from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    """Принимает логин и пароль, сразу возвращает 4-значный код"""
    code = f"{random.randint(1, 9999):04d}"  # Генерируем 4-значное число
    return {"code": code}


@app.get("/")
def hello():
    code = f"{random.randint(1, 9999):04d}"
    return {"code": code}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
