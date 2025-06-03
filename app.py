from fastapi import FastAPI
from scripts.services.service import router

app = FastAPI(root_path="/plugin/project-139/ems-plugin/api")
app.include_router(router)
