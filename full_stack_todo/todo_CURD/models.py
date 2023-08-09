from fastapi import APIRouter

router = APIRouter()



@router.post("add-todo")
async def add_todo():
    pass


# 6
@router.post("delete-todo")
async def delete_todo():
    pass


@router.post("complete-todo")
async def delete_todo():
    pass