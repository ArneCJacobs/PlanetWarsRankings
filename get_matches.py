from datetime import datetime
import json
import requests
def main():
    # make request to https://planetwars.zeus.gent/api/matches

    has_next = True
    params = {
        'count': 1000,
    }
    url = "https://planetwars.zeus.gent/api/matches"
    matches = []
    i = 0
    last_index_written = 0

    with open("matches.json", "w") as f:
        f.write("")

    while has_next:
        print(f"before: {params.get('before', 'None')}, matches: {len(matches)}, iteration: {i}")
        response = requests.get(url, params)
        if response.status_code == 200:
            data = response.json()
            matches_new = data["matches"]
            matches.extend(matches_new)
            print(f"new matches: {len(matches_new)}")
            has_next = data["has_next"]
            before = min(datetime.fromisoformat(match["timestamp"]) for match in matches_new)
            params = {
                "before": before.isoformat(),
                "count": 1000,
            }
            if before < datetime(2022, 1, 1):
                has_next = False
        else:
            has_next = False
            print(f"Error: {response.status_code}")

        if i % 20 == 0:
            with open("matches.json", "a") as f:
                stringified = [json.dumps(match) for match in matches[last_index_written:]]
                f.write("\n".join(stringified) + "\n")

            last_index_written = len(matches)

        i += 1

if __name__ == "__main__":
    main()
