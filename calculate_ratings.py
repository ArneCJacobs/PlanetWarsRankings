from collections import defaultdict
import datetime
from trueskill import Rating, TrueSkill
import pandas as pd
import orjson
import pydantic
from tqdm import tqdm

class Player(pydantic.BaseModel):
    bot_version_id: int
    bot_id: int
    bot_name: str
    owner_id: int | None
    had_errors: bool

    @property 
    def id(self):
        return f"{self.owner_id}-{self.bot_name}"


class Map(pydantic.BaseModel):
    name: str

class Match(pydantic.BaseModel):
    id: int
    timestamp: datetime.datetime 
    state: str
    players: list[Player]
    winner: int | None
    map: Map

def main():
    with open("matches.jsonl", "r") as f:
        matches: list[Match] = [Match.model_validate(orjson.loads(line)) for line in f if line.strip()]

    matches.sort(key=lambda x: x.timestamp)

    draw_count = sum(1 for match in matches if match.winner == None)
    draw_propability = draw_count / len(matches) if matches else 0
    print(f"Draws: {draw_count} ({draw_propability:.2%})")

    ts_env = TrueSkill(draw_probability=draw_propability)

    rows = []
    skill_ratings: dict[str, Rating] = defaultdict(lambda: ts_env.create_rating())

    for match in tqdm(matches):
        if match.state != "Finished":
            continue

        player_ratings = [(skill_ratings[player.id],) for player in match.players]

        if match.winner is None:
            ranks = [0] * len(player_ratings)
        else:
            ranks = [] 
            for index, player in enumerate(match.players):
                if index == match.winner:
                    ranks.append(0)
                else:
                    ranks.append(1)

        player_ratings_new = ts_env.rate(player_ratings, ranks=ranks)

        for player, rating in zip(match.players, player_ratings_new):
            skill_ratings[player.id] = rating[0]
            rows.append({
                "timestamp": match.timestamp,
                "bot_name": player.bot_name,
                "owner_id": player.owner_id,
                "id": player.id,
                "bot_version_id": player.bot_version_id,
                "rating_mu": rating[0].mu,
                "rating_sigma": rating[0].sigma,
            })

    df = pd.DataFrame(rows)
    # df.to_csv("ratings.csv", index=False)
    df.to_parquet("ratings.parquet", index=False)



if __name__ == "__main__":
    main()
