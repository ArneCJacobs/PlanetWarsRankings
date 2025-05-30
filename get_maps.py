import orjson
from calculate_ratings import Match

def main():
    maps = set()
    with open("matches.jsonl", "r") as f:
        for line in f.readlines():
            match = Match.model_validate(orjson.loads(line))
            maps.add(match.map.name)

    maps = sorted(maps)
    print(f"Maps: {len(maps)}")
    for map_name in maps:
        print(map_name)

if __name__ == "__main__":
    main()
