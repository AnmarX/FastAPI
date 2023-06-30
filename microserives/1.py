from fastapi import FastAPI

app = FastAPI()

# Endpoint to retrieve user information
@app.get("/users/{user_id}")
def get_user(user_id: int):
    # Retrieve user information from the database or any other data source
    user = {
        "id": user_id,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
