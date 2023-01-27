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



def extract_top_titles(types: list, n: int = 1000) -> pandas.DataFrame:

    movies_df = pandas.read_csv("titles.tsv")
    movies = movies_df.loc[movies_df["type"].isin(types)]

    top_n_titles = movies.sort_values(by=["imdb_score"], ascending=False).iloc[:n]
    return top_n_titles



def build_plot_best_movies_year() -> None:
    df = pandas.read_csv("titles.tsv")
    df = df[(df["type"] == "MOVIE") & (df["release_year"] >= 2000)]
    df["Movie Count"] = df.groupby("release_year")["id"].transform("count")
    df["IMDB 8+ Count"] = (
        df[df["imdb_score"] > 8.0].groupby("release_year")["id"].transform("count")
    )

    result = (
        df.groupby(["release_year"])[["Movie Count", "IMDB 8+ Count"]]
        .count()
        .reset_index()
    )
    result["Percentage"] = round(
        100 * result["IMDB 8+ Count"] / result["Movie Count"], 2
    )

    years = list(result["release_year"])
    percentage = list(result["Percentage"])

    best_year = result.loc[result["Percentage"].idxmax()]
    last_year = max(years)

    print(f'The best IMDB year is {int(best_year["release_year"])}')

    pyplt.plot(years, percentage)
    pyplt.ylabel("IMDB percentage greater than 8, %")
    pyplt.xlabel("Year")
    pyplt.title("Percentage of films with IMDB gte 8")
    pyplt.xticks(range(2000, last_year, 2))
    pyplt.show()

