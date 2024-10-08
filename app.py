import fastapi
import uvicorn
import api_router
from utils import get_current_port


def create_app():
    app = fastapi.FastAPI()
    app.include_router(api_router.router)
    return app


app = create_app()

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=get_current_port(), reload=True)
