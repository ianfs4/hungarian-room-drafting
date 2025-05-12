import pandas as pd
from scipy.optimize import linear_sum_assignment
from itertools import permutations
import numpy as np
import re

PRICES = {"B Small": 1250,
          "B Medium": 1300,
          "B Large": 1600,
          "1st Small": 1150,
          "1st Large": 1200,
          "2nd Large": 1700,
          "2nd Small 1": 1450,
          "2nd Small 2": 1450,
          "Master": 1900
          }

ROOMS = list(PRICES.keys())
N = len(ROOMS)


# helper function for reformatting "1,200", "$1200", etc. to int(1200)
def extract_price(text):
    text = str(text).replace(',', '')  # Remove comma first
    match = re.search(r'\$?(\d+)', text)
    if match:
        return int(match.group(1))
    return 9999 # if no budget specified, assume infinite


prefs = pd.read_csv("./input_data/2103 Housing Form Results - Sample2.csv")

cost_matrix = np.full((N, N), fill_value=100)   # default high cost

# Step 1: Create cost matrix using each person's scoring. Low score = better.
for i, row in prefs.iterrows():

    rankings = row[2:-1]

    max_budget = extract_price(str(row.iloc[11]))

    for j, rank in enumerate(rankings):

        col_name = prefs.columns[j+2]
        room_name = re.search(r'\[(.*?)\]', col_name).group(1)

        # stays at default high cost if out of budget
        if (PRICES[room_name] <= max_budget):
            cost_matrix[i][j] = rank

# Step 2: Find the optimal total cost
row_ind, col_ind = linear_sum_assignment(cost_matrix) # Hungarian Algorithm
# https://en.wikipedia.org/wiki/Hungarian_algorithm
optimal_cost = cost_matrix[row_ind, col_ind].sum()
average_rating = f"{(optimal_cost / N):.2f}"
print(
    f"Optimal Total Cost: {optimal_cost}\t"
    f"(on average, everyone received their {average_rating}th pick)\n"
)

# Step 3: Generate all permutations and filter optimal ones
print("All Optimal Assignments:")

count = 0
for perm in permutations(range(N)):
    total_cost = sum(cost_matrix[i, perm[i]] for i in range(N))
    if total_cost == optimal_cost:
        count += 1
        print(f"\n--- Option {count} ---")

        max_name_len = max(len(str(prefs.iloc[i]['Name'])) for i in range(N))
        max_room_len = max(len(room) for room in ROOMS)

        for i, j in enumerate(perm):
            person = prefs.iloc[i]['Name']
            room = ROOMS[j]
            rent = PRICES[room]

            rankings = prefs.iloc[i, 2:-1].values
            rank = rankings[j]

            print(f"{person:<{max_name_len}}  →  {room:<{max_room_len}}  (${rent:>6.2f})  (Rank: {rank})")

