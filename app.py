from fastapi import FastAPI
from scripts.services.service import router

app = FastAPI(root_path="/gateway/plugin/project-139/ems-plug/api")
app.include_router(router)
