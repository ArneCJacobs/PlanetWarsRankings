import seaborn as sns 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

def main():
    # matplotlib.use("nbagg")
    matplotlib.use("WebAgg")
    df = pd.read_parquet("ratings.parquet")

    sns.lineplot(
        data=df,
        x="timestamp",
        y="rating_mu",
        hue="id",
    )

    plt.show()


if __name__ == "__main__":
    main()
