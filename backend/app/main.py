import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
import app.models  # Register models
from app.api.v1.endpoints.edital import router as edital_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.export import router as export_router

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Backend API do AprovAI - Sistema Estratégico de Estudos para Concursos com Inteligência Artificial."
)

# Configuração de CORS (Cross-Origin Resource Sharing)
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Registro de Rotas
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["Autenticação"])
app.include_router(edital_router, prefix=f"{settings.API_V1_STR}/edital", tags=["Edital"])
app.include_router(export_router, prefix=f"{settings.API_V1_STR}/export", tags=["Exportação"])

@app.get("/")
def read_root():
    return {
        "message": "Bem-vindo à API do AprovAI!",
        "docs_url": "/docs",
        "health_check": f"{settings.API_V1_STR}/edital/health"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
