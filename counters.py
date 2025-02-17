import requests
import matplotlib.pyplot as plt

patch = "15_2"
champion = "117"  # lulu
server = "12"  # world
rank = "17"  # emerald+
role = "2"  # support
min_pick_rate = 0.005
sigma = 3  # standard deviation
title = "15.2 Emerald+ Lulu Support Counters"

url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-summary.json"
response = requests.get(url)
data = response.json()

champions = {i["id"]: i["name"] for i in data}

url = f"https://stats2.u.gg/lol/1.5/matchups/{patch}/ranked_solo_5x5/{champion}/1.5.0.json"
response = requests.get(url)
data = response.json()

data = data[server][rank][role][0]
data = {champions[i[0]]: {"wins": i[1], "games": i[2]} for i in data}

total_games = sum([data[i]["games"] for i in data])
threshold = min_pick_rate*total_games
data = {i: j for i, j in data.items() if j["games"] >= threshold}

champions = data.keys()
wins = [data[i]["wins"] for i in data]
games = [data[i]["games"] for i in data]

length = range(len(champions))

win_rates = [wins[i]/games[i] for i in length]
pick_rates = [i/total_games for i in games]

standard_errors = [(win_rates[i]*(1-win_rates[i])/games[i])**(1/2) for i in length]
confidence_intervals = [win_rates[i]-sigma*standard_errors[i] for i in length]

c1 = min(confidence_intervals)
c2 = max(confidence_intervals)

scores = [10*(i-c1)/(c2-c1) for i in confidence_intervals]  # Idea: leaguephd.com

results = sorted(zip(scores, champions), reverse=True)
for i, j in results:
    print(f"{j}: {round(i, 1)}")

plt.axhline(0.5, color="black")
plt.scatter(pick_rates, win_rates, c=scores, cmap="rainbow")
plt.colorbar(label="Score")

for i, label in enumerate(champions):
    plt.annotate(label, (pick_rates[i], win_rates[i]))

plt.xlabel("Pick Rate")
plt.ylabel("Win Rate")
plt.title(title)

plt.tight_layout()
plt.show()
