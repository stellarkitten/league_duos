import requests
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors

patch = "15_2"
champion = "117"  # lulu
server = "12"  # world
role = "2"  # support
title = "15.2 Lulu Support Rank Evolution"

url = f"https://stats2.u.gg/lol/1.5/rankings/{patch}/ranked_solo_5x5/{champion}/1.5.0.json"
response = requests.get(url)
data = response.json()

ranks = ["12", "7", "6", "5", "4", "15", "3", "2", "13", "1"]

win_rates = []
pick_rates = []
matches = []
for i in ranks:
    rank_data = data[server][i][role]

    win_rate = rank_data[0]/rank_data[1]
    pick_rate = rank_data[1]/rank_data[11]
    match = rank_data[1]

    win_rates.append(win_rate)
    pick_rates.append(pick_rate)
    matches.append(match)

wr = np.array(win_rates)
pr = np.array(pick_rates)

plt.axhline(0.5, color="black")
plt.scatter(pr, wr, c=matches, cmap="rainbow", norm=matplotlib.colors.LogNorm())
plt.colorbar(label="Matches")
plt.quiver(pr[:-1], wr[:-1], pr[1:]-pr[:-1], wr[1:]-wr[:-1], scale_units='xy', angles='xy', scale=1.005, width=0.005, color="C1")

ranks_string = ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Emerald", "Diamond", "Master", "Grandmaster", "Challenger"]
for i, label in enumerate(ranks_string):
    plt.annotate(label, (pick_rates[i], win_rates[i]))

plt.xlabel("Pick Rate")
plt.ylabel("Win Rate")
plt.title(title)

plt.tight_layout()
plt.show()
