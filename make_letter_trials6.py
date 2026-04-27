import csv
import os
import random

N_TRIALS = 96
SET_SIZE = 6

PARTICIPANT_ID = 1  # change this for each participant

OUT_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    f"letter_change_trials_6items_p{PARTICIPANT_ID}.csv"
)

LETTERS = list("BCDFGHJKLM")

if N_TRIALS % 2 != 0:
    raise ValueError("N_TRIALS must be even.")

if (N_TRIALS // 2) % SET_SIZE != 0:
    raise ValueError("N_TRIALS // 2 must be divisible by SET_SIZE.")

def rand_six_letter_string_unique(rng):
    return "".join(rng.sample(LETTERS, SET_SIZE))

def safe_text(x):
    s = str(x)
    return s[1:] if s.startswith("=") else s

fixed_rng = random.Random(1)

change_list = [1] * (N_TRIALS // 2) + [0] * (N_TRIALS // 2)

positions = list(range(SET_SIZE)) * ((N_TRIALS // 2) // SET_SIZE)
fixed_rng.shuffle(positions)

trial_plan = []
pos_index = 0

for change in change_list:
    if change == 1:
        pos = positions[pos_index]
        pos_index += 1
    else:
        pos = -1

    trial_plan.append({
        "change": change,
        "pos": pos
    })

fixed_rng.shuffle(trial_plan)

rows = []

for fixed_trial_number, plan in enumerate(trial_plan, start=1):
    mem_str = rand_six_letter_string_unique(fixed_rng)
    probe_letters = list(mem_str)

    change = plan["change"]
    pos = plan["pos"]

    if change == 1:
        used_letters = set(mem_str)
        options = [l for l in LETTERS if l not in used_letters]
        probe_letters[pos] = fixed_rng.choice(options)
        correct = "d"
    else:
        correct = "s"

    probe_str = "".join(probe_letters)

    row = {
        "fixed_trial_number": fixed_trial_number,
        "mem_text": safe_text(mem_str),
        "probe_text": safe_text(probe_str),
        "d1": mem_str[0],
        "d2": mem_str[1],
        "d3": mem_str[2],
        "d4": mem_str[3],
        "d5": mem_str[4],
        "d6": mem_str[5],
        "p1": probe_str[0],
        "p2": probe_str[1],
        "p3": probe_str[2],
        "p4": probe_str[3],
        "p5": probe_str[4],
        "p6": probe_str[5],
        "correct": correct,
        "change": change,
        "pos": pos
    }

    rows.append(row)

participant_rng = random.Random(PARTICIPANT_ID)
participant_rng.shuffle(rows)

for presentation_order, row in enumerate(rows, start=1):
    row["presentation_order"] = presentation_order

with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    fieldnames = [
        "presentation_order",
        "fixed_trial_number",
        "mem_text",
        "probe_text",
        "d1", "d2", "d3", "d4", "d5", "d6",
        "p1", "p2", "p3", "p4", "p5", "p6",
        "correct",
        "change",
        "pos"
    ]

    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {N_TRIALS} trials for participant {PARTICIPANT_ID} to {OUT_CSV}")