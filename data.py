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


def build_histogram() -> None:
    top1000 = extract_top_titles(types=["MOVIE", "SHOW"])

    df = top1000[top1000["genres"] != "[]"]

    df = pandas.DataFrame(df)
    df["genres"] = df["genres"].apply(ast.literal_eval)

    genres_counts = (
        df.explode(column="genres").groupby(["genres"]).size().reset_index(name="Count")
    )

    genres = list(genres_counts["genres"])
    counts = list(genres_counts["Count"])

    pyplt.bar(genres, counts)
    pyplt.xticks(rotation=90)
    pyplt.xlabel("Genre")
    pyplt.ylabel("Count of movies/shows")

    pyplt.title("Count by genre")

    pyplt.show()
