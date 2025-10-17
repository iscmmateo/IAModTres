# Auth API (FastAPI) — Secure Module

Autenticación con **FastAPI + Pydantic + Argon2 + JWT** y **rate limiting** (SlowAPI).
Listo para correr en Docker.

## Características
- Validación con **Pydantic** (v2).
- Hash de contraseñas con **Argon2**.
- Tokens **JWT** (access y refresh).
- **Rate limiting** en rutas sensibles (login/registro).
- DB **SQLite** vía SQLAlchemy.
- Pruebas básicas con **pytest**.

## Requisitos
- Docker y Docker Compose.

## Cómo ejecutar
```bash
docker compose up --build
```

La API quedará en: http://localhost:8000 (docs: http://localhost:8000/docs)

## Variables de entorno
Copia `.env.example` a `.env` y ajusta si deseas:
- `JWT_SECRET` — secreto para firmar JWTs.
- `JWT_ALG` — algoritmo (por defecto HS256).
- `ACCESS_TOKEN_EXPIRE_MINUTES` — minutos de validez del access token.
- `REFRESH_TOKEN_EXPIRE_DAYS` — días de validez del refresh token.

## Endpoints principales
- `POST /auth/register` → Crear usuario.
- `POST /auth/login` → Obtener `access_token` y `refresh_token`.
- `POST /auth/refresh` → Refrescar `access_token` con `refresh_token`.
- `GET /users/me` → Datos del usuario autenticado (Bearer).

## Tests
```bash
docker compose run --rm api pytest -q
```
