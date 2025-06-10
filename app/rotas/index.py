from fastapi import APIRouter

router_index = APIRouter(prefix="/index", tags=['Index'])

@router_index.get('/')
async def introducao():
    return {"mesage": "Hello World!"}