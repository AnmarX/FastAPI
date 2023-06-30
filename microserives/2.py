import requests
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

# USER_MICROSERVICE_URL = "http://localhost:8000/users/{user_id}"

# Endpoint to retrieve order details with associated user information
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    # Fetch order details from the database or any other data source
    order = {
        "id": order_id,
        "product": "ABC",
        "quantity": 5,
        # Assuming the user_id is stored in the order or retrieved from another source
        "user_id": 123
    }
    
    if order is None:
        # Redirect to a different URL when order is not found
        return RedirectResponse(url="http://example.com/order-not-found")
    
    # user_microservice_url = USER_MICROSERVICE_URL.format(user_id=order["user_id"])
    response = requests.get(f"http://localhost:8000/users/{order['user_id']}")
    
    if response.status_code == 200:
        user = response.json()
        order["user"] = user
    else:
        order["user"] = None
    
    return order


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)