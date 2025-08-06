# 📚 Biblioteca de livros

Esta API implementada em Python com FastAPI extrai informações de livros do site [Books to Scrape](https://books.toscrape.com/), armazena os dados no arquivo "books_data.csv" localmente e disponibiliza endpoints para consulta dos dados.


## 📦 Requisitos

- Python 3.8+
- pip


## 🗂️ Estrutura do Projeto

```
biblioteca/
├── app/
│   ├── scraple.py         # Scraping 
│   ├── models.py          # Modelos ML (implementação futura)
│   └── utils.py           # Funções auxiliares
├── data/
│   └── books_data.csv     # Arquivo .csv com os dados dos livros
├── main.py                # Inicializador do pipeline e da API
├── requirements.txt       # Dependências do projeto com as bibliotecas utilizada
└── README.md
```



## ⚙️ Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone <https://github.com/MConegundes/scraping_api>
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Inicie o FlastAPI

```bash
uvicorn api:app --reload
```

### 5. Swagger - Verificar todas as rotas criadas funcionalidades disponiveis

No swagger você poderá verificar e executar todas as rotas criadas.
```bash
http://127.0.0.1:8000/docs
```

### 6. Execute o Web Scraping executando a rota (opcional, se já houver CSV)

```bash
/api/v1/extrair/{pages}

```
Esse método extrai e salva os dados dos livros no arquivo `data/books_data.csv`

---


## 📡 Principais Endpoints

| Método | Rota                                    | Descrição |
|--------|-----------------------------------------|-----------|
| GET    | /v1/scraping/trigger                    | Extrai e salva os dados dos livros |
| GET    | /v1/health                              | Verifica status da API |
| GET    | /v1/books                               | Lista todos os livros |
| GET    | /v1/books/{id}                          | Detalha um livro |
| GET    | /v1/books/search                        | Busca por título/categoria |
| GET    | /v1/categories                          | Lista categorias únicas |


## 📡 Endpoints de Insights

| Método | Rota                                    | Descrição |
|--------|-----------------------------------------|-----------|
| GET    | /api/v1/stats/overview                  | Estatísticas gerais da coleção |
| GET    | /api/v1/stats/categories                | Estatísticas gerais por categoria |
| GET    | /api/v1/books/top-rated                 | Lista os livros com melhor avaliação |
| GET    | /api/v1/books/price-range               | Filtra livros dentro de uma faixa de preço específica |




## 🧠 scraple.py: Extração dos livros
- Realiza a extração de dados (web scraping) do site "https://books.toscrape.com/". Coleta informações sobre os livros disponíveis na página, como título, preço, disponibilidade, avaliação, categoria, URL da imagem e detalhes específicos de cada livro.


## 🛠 utils.py: Funções auxiliares
- Os métodos do arquivo utils.py são funções auxiliares que ajudam a manipular e consultar uma base de dados de livros armazenada em um arquivo CSV.

#### 1. sorted_categories(books_df): 
- Ordena categorias em ordem alfabética.

#### 2. general_overview(books_df): 
- Retorna as estatísticas gerais da coleção de livros.

#### 3. categories_overview(books_df):
- Retorna as estatísticas gerais da coleção de livros por categoria.

#### 4. books_by_price_range(books_df, max: float, min: float): 
- Filtra os livros por uma faixa de preço informada.



## 🚀 api.py: Rotas da API
- Os métodos do arquivo api.py são responsáveis por criar e gerenciar a API da sua biblioteca.

---
## 🧭 Plano Arquitetural (Pipeline e Escalabilidade)

### 🔄 Pipeline da Solução

```
      ┌─────────────┐
      │ books.toscrape.com
      └──────┬──────┘
             │  (requests + BS4)
             ▼
      ┌────────────────┐
      │ Scraper Python │
      │ scraple.py     │
      └──────┬─────────┘
             │  (CSV: pandas)
             ▼  
      ┌──────────────────────┐
      │  data/books_data.csv │
      └──────┬───────────────┘
             ▼
      ┌────────────────────┐
      │   FastAPI backend  │
      │   api.py + models  │
      └──────┬─────────────┘
             ▼
      ┌────────────────────┐
      │  REST Endpoints    │
      └──────┬─────────────┘
             ▼
     ┌────────────────────────┐
     │   Cientistas de Dados  │
     │   Frontend / ML / BI   │
     └────────────────────────┘
```



## 🧠 Caso de Uso para Cientistas de Dados / ML

### 🎯 Cenário
Objetivo: Cientistas de dados querem explorar livros para entender preferências por categorias, preços, disponibilidade e sugerir livros por interesse.

💼 Aplicações:
🔍 Análise exploratória de dados (EDA)

📊 Dashboard com Power BI

🤖 Treinamento de modelos de recomendação ou classificação de livros por categoria


## 🧠 Integração com Modelos de Machine Learning

### 🧩 Plano de Integração
| Etapa             | Detalhes                                                                       |
| ----------------- | ------------------------------------------------------------------------------ |
| Dados             | `books.csv` como entrada para pré-processamento                                |
| Pré-processamento | Limpeza, encoding de `rating`, one-hot de `category`, transformação de `price` |
| Treinamento       | Classificadores, clusterização de livros, sistemas de recomendação             |
| API ML            | Servir modelo via FastAPI                                                      |
| Integração        | Nova rota `/api/v1/predict` que recebe dados de entrada e retorna previsão     |


## 🔄 Exemplo de Rota Futuro:

```bash
@app.post("/api/v1/predict")
def predict(data: Book):
    # Preprocessar dados
    # Carregar modelo treinado
    # Retornar resultado
    return {"categoria_prevista": "Fiction"}
```


## 📈 Sugestão para Pipeline de ML

```bash
data/books.csv ──> Jupyter Notebook ──> Modelo treinado (.pkl/.joblib)
                                           │
FastAPI ── /predict ────────> Carrega modelo e retorna inferência
```