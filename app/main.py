from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from .database import Base, engine
from .config import settings
from .rate_limit import limiter
from .routers import auth, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth API (FastAPI)")

# CORS (ajusta orígenes si es necesario)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SlowAPI
app.state.rate_login_limit = settings.RATE_LIMIT_LOGIN
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
def _rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return exc.get_response(request)

# Routers
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "auth-api"}
