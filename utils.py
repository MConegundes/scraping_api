import pandas as pd

def sorted_categories(books_df):
    categories = books_df['Category'].unique()
    categories.sort()
    return categories

def general_overview(books_df):

    total_books = len(books_df)
    average_price = books_df['Price'].str[1:].astype(float).mean()

    books_df['Rating'] = books_df['Rating'].replace(['One', 'Two', 'Three', 'Four', 'Five'],
                                                    ['1 star', '2 star', '3 star', '4 star', '5 star'])
    rating_dist = books_df.groupby('Rating').count()['Title']/len(books_df)
    rating_dist = rating_dist.to_frame()
    rating_dist['Rating'] = rating_dist.index
    rating_dist = rating_dist.reset_index(drop=True)
    rating_dist['Title'] = rating_dist['Title']*100
    rating_dist['Title'] = rating_dist['Title'].map('{:,.2f}%'.format)
    rating_dist = rating_dist[['Rating', 'Title']].rename(columns={"Title": "Distribution"})

    result = {
        "total_books": total_books,
        "average_price": average_price,
        "rating_distribution": rating_dist
        }
    return result

def categories_overview(books_df):
    books_df['Price'] = books_df['Price'].str[1:].astype(float)
    stats_category = books_df.groupby('Category').agg(
        books_total=('Title', 'count'),
        price_average=('Price', 'mean')
    ).reset_index()

    return stats_category

def books_by_price_range(books_df, max: float, min: float):
    books_df['Price'] = books_df['Price'].str[1:].astype(float)
    index_found = books_df.index[(
        (books_df['Price'] <= max) & 
        (books_df['Price'] >= min)
        )].tolist()
    return index_found


