from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List 
import uvicorn 

app = FastAPI()

class Item(BaseModel):
    text: str
    is_done: bool = False

class ItemPatch(BaseModel):
    text: Optional[str] = None
    is_done: Optional[bool] = None

items = []

 # @app.get("/")
# def root():
   # return {"Hello" : "World"}

@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items

@app.get("/items", response_model=List[Item])
def list_items(limit: int = 10):
    return items[0:limit]

@app.get("/items/{item_id}", response_model=Item)
def get_test(item_id: int) -> Item:
    if 0 <= item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail =f"Item {item_id} not found")

@app.post("/items/bulk", response_model=List[Item], status_code=status.HTTP_201_CREATED)
def create_items_bulk(payload: List[Item]):
    items.extend(payload)
    return items

@app.put("/items/{item_id}", response_model=Item)
def replace_item(item_id: int, payload: Item):
    if 0 <= item_id < len(items):
        items[item_id] = payload
        return payload 
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

@app.put("/items/{item_id}/done", response_model=Item)
def put_mark_done(item_id: int):
    if 0 <= item_id < len(items):
        items[item_id].is_done = True
        return items[item_id]
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

@app.patch("/items/{item_id}", response_model=Item)
def patch_item(item_id: int, payload: ItemPatch):
    if 0 <= item_id < len(items):
        if payload.text is not None:
            items[item_id].text = payload.text 
        if payload.is_done is not None:
            items[item_id].is_done = payload.is_done 
        return items[item_id]
    raise HTTPException(status_code=404, detail = f"Item {item_id} not found")

@app.patch("/items/{item_id}/toggle", response_model=Item)
def toggle_item(item_id: int):
    if 0 <= item_id < len(items):
        items[item_id].is_done = not items[item_id].is_done
        return items[item_id]
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    if 0 <= item_id < len(items):
        items.pop(item_id)
        return 
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

@app.delete("/items", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_items():
    items.clear()
    return

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
