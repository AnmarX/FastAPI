from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile,Body

app = FastAPI()


@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }



@app.post("/upload/{id}")
async def upload_files(p: str ,id:int):
    return {"files": p,"id":id}

