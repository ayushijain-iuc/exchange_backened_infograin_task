from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.db import create_tables
from .routers import user_router, order_router

app = FastAPI(
    title="Trading Engine API",
    description="A simple trading exchange backend with order matching",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(order_router.router)

@app.on_event("startup")
def startup_event():
    create_tables()

@app.get("/")
def root():
    return {
        "message": "Trading Engine API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
