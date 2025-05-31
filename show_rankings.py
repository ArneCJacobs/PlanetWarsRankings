import pandas as pd

def main():
    df = pd.read_parquet("ratings.parquet")

    #ratings contains 3 columns: timestamp, id, rating
    # get the latest rating for each id 
    latest_ratings = df.sort_values(by='timestamp').groupby('id').last().reset_index()
    # sort by ratings 
    latest_ratings = latest_ratings.sort_values(by='rating_mu', ascending=False)
    #pretty print 
    print(latest_ratings[['bot_name', 'rating_mu']].to_string(index=False))

    latest_ratings.to_csv("latest_ratings.csv", index=False)


if __name__ == "__main__":
    main()
