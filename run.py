import uvicorn
from app import create_app
from config.settings import settings

app = create_app()

if __name__ == '__main__':
    uvicorn.run("run:app", host=settings.HOST, port=settings.PORT, reload=True, log_level="info")
