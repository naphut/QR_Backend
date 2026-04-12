from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import time
import os
from .database import init_db, test_db_connection, get_db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI first
app = FastAPI(
    title="E-commerce Clothing API", 
    version="1.0.0",
    description="High-performance e-commerce API for clothing store"
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        logger.info("Starting database initialization...")
        if test_db_connection():
            init_db()
            logger.info("✅ Database initialized successfully")
        else:
            logger.error("❌ Database connection failed")
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}")

# Simple health check routes
@app.get("/")
def read_root():
    return {"message": "QR E-commerce API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/debug")
def debug_info():
    """Debug endpoint to check module loading status"""
    try:
        from . import models, database
        from .routers import products, orders, auth, admin
        return {
            "status": "modules_loaded",
            "modules": ["models", "database", "auth", "products", "orders", "admin"],
            "database_url": str(database.engine.url)
        }
    except Exception as e:
        return {
            "status": "modules_not_loaded",
            "error": str(e),
            "error_type": type(e).__name__
        }

# Try to import and setup additional components
try:
    logger.info("🔄 Starting module imports...")
    
    # Test individual imports
    try:
        from . import models
        logger.info("✅ Models imported successfully")
    except Exception as e:
        logger.error(f"❌ Models import failed: {e}")
        raise
    
    try:
        from . import database
        logger.info("✅ Database imported successfully")
    except Exception as e:
        logger.error(f"❌ Database import failed: {e}")
        raise
    
    try:
        from .routers import auth
        logger.info("✅ Auth router imported successfully")
    except Exception as e:
        logger.error(f"❌ Auth router import failed: {e}")
        raise
    
    try:
        from .routers import products
        logger.info("✅ Products router imported successfully")
    except Exception as e:
        logger.error(f"❌ Products router import failed: {e}")
        raise
    
    try:
        from .routers import orders
        logger.info("✅ Orders router imported successfully")
    except Exception as e:
        logger.error(f"❌ Orders router import failed: {e}")
        raise
    
    try:
        from .routers import admin
        logger.info("✅ Admin router imported successfully")
    except Exception as e:
        logger.error(f"❌ Admin router import failed: {e}")
        raise
    
    logger.info("✅ Successfully imported all modules")
    
    # Create database tables
    try:
        models.Base.metadata.create_all(bind=database.engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {e}")
    
    # Add GZip compression for better performance
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # CORS middleware - get allowed origins from environment
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")
    logger.info(f"🌐 CORS allowed origins: {allowed_origins}")
    
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
    
    logger.info("✅ All routers included successfully")
    print("✅ All modules loaded successfully")
    
except Exception as e:
    logger.error(f"❌ Error importing modules: {e}")
    logger.error(f"❌ Error details: {type(e).__name__}: {str(e)}")
    print(f"⚠️ Error importing some modules: {e}")
    print("🔄 Running in basic mode with health checks only")