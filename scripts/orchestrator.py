import random
import sys

participants = ["aurora-turn", "boreal-turn", "cyra-turn"]

# Optional: avoid same speaker twice
if len(sys.argv) > 1:
    last = sys.argv[1]
    filtered = [p for p in participants if p != last]
    if filtered:
        participants = filtered

print(random.choice(participants))
