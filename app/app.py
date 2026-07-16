from fastapi import FastAPI, status
from app.routers import accounts


app = FastAPI()

app.include_router(
    router=accounts.users_router,
    prefix='/api/v1',
    tags=['users'],
)

app.include_router(
    router=accounts.students_router,
    prefix='/api/v1',
    tags=['students'],
)

app.include_router(
    router=accounts.teachers_router,
    prefix='/api/v1',
    tags=['teachers'],
)

@app.get(
    path = '/health_check',
    status_code=status.HTTP_200_OK,
)
def read_root():
    return {'Status': 'ok'}