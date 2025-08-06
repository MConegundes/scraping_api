# venv\Scripts\activate
# uvicorn api:app --reload  

from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from bs4 import BeautifulSoup as BfS4
from mangum import Mangum 
import pandas as pd
import requests
import utils
import scraple

app = FastAPI(
    title="My FastAPI API",
    version="1.0.0",
    description="API de Exemplo com FastAPI"
)

try:
    books_df = pd.read_csv('books_data.csv', index_col='index')
except:
    raise HTTPException(status_code=404, detail="Books data not found")

@app.get("/v1/books")
async def get_books_title():
    return books_df['Title']

# class Item(BaseModel):
#     id_book: int = None     # id do item
#     title: str = None       # nome opcional
#     price: float = None     # preço opcional

@app.get("/v1/books/top-rated")
async def get_toprated():
    index_found = books_df.index[books_df['Rating'] == 'Five'].tolist()
    return books_df.loc[index_found, ['Title', 'Link']]

@app.get("/v1/books/search") 
async def get_book_title_cat(title: str, category: str):
    if (books_df['Title'].str.contains(title).any() or 
        books_df['Category'].str.contains(category).any()):
        index_found = books_df.index[(
            (books_df['Title'].str.contains(title)) | 
            (books_df['Category'].str.contains(category))
            )].tolist()
        return books_df.loc[index_found, ['Title', 'Link']]
    raise HTTPException(status_code=404, detail="Item não encontrado")

@app.get("/v1/books/price-range") 
async def get_book_by_price(min: float, max: float):
    if 0 <= min <= max:
        index_found = utils.books_by_price_range(books_df, max, min)
        return books_df.loc[index_found, ['Title', 'Link', 'Price']]
    raise HTTPException(status_code=404, detail="Entre com valores validos para preço minimo e maximo")

@app.get("/v1/books/{id_search}")
async def get_book(id_search: int):
    if 0 <= id_search < len(books_df):
        return books_df.loc[id_search,:]
    raise HTTPException(status_code=404, detail="Item não encontrado")

@app.get("/v1/categories")
async def get_categories():
    result = pd.DataFrame(utils.sorted_categories(books_df), columns=['categorys'])
    return result

@app.get("/v1/health") # não funciona
async def get_api_status():
    if len(books_df) > 0:
        raise HTTPException(status_code=202, detail="API status: OK - Books data: OK")
    else: 
        raise HTTPException(status_code=503, detail="API status: OK - Books data: Absent")

@app.get("/v1/stats/overview")
async def get_overview():
    return utils.general_overview(books_df)

@app.get("/v1/stats/categories")
async def get_categories_stats():
    return utils.categories_overview(books_df)

@app.get("/v1/scraping/trigger")
async def scraple_books():
    return scraple.scraple_books()


# Wrap app with handler for Vercel
handler = Mangum(app)