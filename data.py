import ast
import pandas
import numpy
import matplotlib.pyplot as pyplt


def build_age_categories() -> None:
    df = pandas.read_csv("titles.tsv")
    age_categories = df[df["type"] == "SHOW"]
    df2 = age_categories.groupby("age_certification")["age_certification"].count()
    labels = set(
        age_categories[age_categories["age_certification"].notnull()][
            "age_certification"
        ]
    )

    fig, ax = pyplt.subplots()
    ax.pie(df2, labels=labels, autopct="%1.1f%%", shadow=True)
    ax.set_title("Percentage of movies by age categories")
    pyplt.show()
