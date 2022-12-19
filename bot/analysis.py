from typing import List

from purchase_info import PurchaseInfo
import pandas as pd
import plotly.express as px


def graphic_analysis(purchases: List[PurchaseInfo], id_: int):
    df = pd.DataFrame([purchase.__dict__ for purchase in purchases])
    df = df.groupby('date')['price'].agg(func=sum).reset_index()
    df = df.sort_values(by="date")
    fig = px.line(df, x="date", y="price", width=800, height=400)
    fig.update_layout(title='График трат',
                      xaxis_title='День',
                      yaxis_title='Сумма')

    fig.write_image(f"data/graphics/{id_}.png", width=800, height=400)


def pie_analysis(purchases: List[PurchaseInfo], id_: int):
    df = pd.DataFrame([purchase.__dict__ for purchase in purchases])
    df = df.groupby('type_')['price'].agg(func=sum).reset_index()
    df = df.sort_values(by="type_")
    print(df)
    fig = px.pie(df, values='price', names='type_', width=800, height=400)
    fig.update_layout(title='Траты по категориям')
    fig.write_image(f"data/pies/{id_}.png")
