from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
import pandas as pd

app = FastAPI(
    title="My FastAPI API",
    version="1.0.0",
    description="API de Exemplo com FastAPI"
)

books_df = pd.read_csv('books_data.csv', index_col='index')

@app.get("/v1/books")
async def get_books_title():
    return books_df['Title']

class Item(BaseModel):
    id_book: int = None     # id do item
    title: str = None       # nome opcional
    price: float = None     # preço opcional

@app.get("/v1/books/{id_search}")
async def get_book(id_search: int):
    if 0 <= id_search < len(books_df):
        return books_df.loc[id_search,:]
    raise HTTPException(status_code=404, detail="Item não encontrado")

@app.get("/v1/books/search?title={title}&category={category}")
async def get_book_title_cat(title: str, category: str):
    if (books_df['Title'].str.contains(title).any() or 
        books_df['Category'].str.contains(category)):
        index_found = books_df.index[(
            (books_df['Title'].str.contains(title)) | 
            (books_df['Category'].str.contains(category))
            )].tolist()
    raise HTTPException(status_code=404, detail="Item não encontrado")

@app.get("/v1/categories")
async def get_categories():
    categories = books_df['Category'].unique()
    categories.sort()
    return categories