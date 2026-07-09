from google_play_scraper import search, app
import pandas as pd
import time

keywords = [
    "action game",
    "adventure game",
    "arcade game",
    "board game",
    "card game",
    "casino game",
    "casual game",
    "educational game",
    "music game",
    "puzzle game",
    "racing game",
    "role playing game",
    "simulation game",
    "sports game",
    "strategy game",
    "trivia game",
    "word game",
    "offline game",
    "online game",
    "multiplayer game",
    "battle game",
    "war game",
    "football game",
    "cricket game",
    "car game",
    "bike game",
    "zombie game"
]

app_ids = set()
TARGET_LIMIT = 1000  

print("--- Step 1: 1000 Unique Game IDs Collecting ---")
for keyword in keywords:
    if len(app_ids) >= TARGET_LIMIT:
        break  
        
    try:
        results = search(
            keyword,
            lang="en",
            country="us",
            n_hits=200  
        )

        for game in results:
            if len(app_ids) < TARGET_LIMIT:
                app_ids.add(game["appId"])
            else:
                break

        print(f"After Keyword '{keyword}' total Unique IDs: {len(app_ids)}")
        time.sleep(1) 

    except Exception as e:
        print(f"Error searching for {keyword}: {e}")

print(f"\nTarget achieved! Total Unique Games to scrape: {len(app_ids)}")

print("\n--- Step 2: Detailed Data Extraction (Safe Mode Active) ---")
data = []
start_time = time.time()

app_id_list = list(app_ids)

for i, app_id in enumerate(app_id_list):
    try:
        info = app(app_id)

        data.append({
            "Game Name": info.get("title"),
            "Developer": info.get("developer"),
            "Genre": info.get("genre"),
            "Rating": info.get("score"),
            "Ratings Count": info.get("ratings"),
            "Reviews": info.get("reviews"),
            "Installs": info.get("installs"),
            "Real Installs": info.get("realInstalls"),
            "Price": info.get("price"),
            "Free": info.get("free"),
            "Content Rating": info.get("contentRating"),
            "Released": info.get("released"),
            "Updated": info.get("updated"),
            "Version": info.get("version"),
            "Developer Website": info.get("developerWebsite")
        })

        print(f"Progress: {i+1}/{TARGET_LIMIT} Done | Game: {info.get('title')}...")


        if (i + 1) % 50 == 0:
            pd.DataFrame(data).to_csv("google_play_games_dataset.csv", index=False)
            print(">>> Backup Saved! (Data safe in CSV) <<<")

        time.sleep(2)

    except Exception as e:
        print(f"Error fetching data for: {app_id} (Skipping...)")
        time.sleep(2) 

# Final Save
df = pd.DataFrame(data)
df.to_csv("google_play_games_dataset1.csv")

end_time = time.time()
total_minutes = round((end_time - start_time) / 60, 2)

print("\n--- Scraping Complete ---")
print(f"File Saved As: google_play_games_dataset.csv")
print(f"Total Games Successfully Scraped: {len(df)}")
print(f"Total Time Taken: {total_minutes} minutes")
