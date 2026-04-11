from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import time
import os

# Initialize FastAPI first
app = FastAPI(
    title="E-commerce Clothing API", 
    version="1.0.0",
    description="High-performance e-commerce API for clothing store"
)

# Simple health check routes
@app.get("/")
def read_root():
    return {"message": "QR E-commerce API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

# Try to import and setup additional components
try:
    from . import models, database
    from .routers import products, orders, auth, admin, init, payment
    from .db_init import initialize_database
    
    # Create database tables
    models.Base.metadata.create_all(bind=database.engine)
    
    # Initialize database with required data
    initialize_database()
    
    # Add GZip compression for better performance
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # CORS middleware - get allowed origins from environment
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Performance monitoring middleware
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    
    # Include routers
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(products.router, prefix="/api/products", tags=["products"])
    app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
    app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
    app.include_router(init.router)
    app.include_router(payment.router)
    
    print("✅ All modules loaded successfully")
    
except Exception as e:
    print(f"⚠️ Error importing some modules: {e}")
    print("🔄 Running in basic mode with health checks only")