import uvicorn
from app import app
from scripts.constants.app_configuration import AppConfig

if __name__ == "__main__":
    uvicorn.run(app, host=AppConfig.API_HOST, port=int(AppConfig.API_PORT))
