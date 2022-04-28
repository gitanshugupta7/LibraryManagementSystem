import pandas as pd
from .models import *


def populating():
    data = pd.read_csv("./TitlesandBooks.csv")

    uidc = 500000
    acc = 11000
    j = 0
    while(j <= 862):
        title = Title(
            uid = uidc,
            title = data['Title'][j],
            author = data['Author'][j],
            total_book_count = 10,
        )
        title.save()
        k = 1
        while(k <= 10):
            book = Books(
                uid = title,
                acc_no = acc,
            )
            book.save()
            acc = acc + 1
            k = k + 1

        uidc = uidc + 1
        j = j + 1




    
    