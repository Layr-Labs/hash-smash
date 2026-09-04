# Organizer paired-judge calibration fixtures

These examples belong to no challenge target and never produce Yukon scores.
They isolate judge protocol behavior with transparent toy maps and small finite
experiments. The positive example has an exact elementary proof. The false example
changes a high-bit difference into a low-bit difference: its pair hashes to 0 and
1 and is objectively not a collision. The heuristic example reports reproducible
finite observations but openly lacks evidence establishing its probability bound.

The heuristic case's desired exploratory/rigorous disagreement is a rubric
diagnostic, not a truth label for the unestablished numerical claim. A model can
discover additional valid mathematics; a surprising verdict requires inspecting
its reasoning and citations. Three examples cannot estimate false-positive or
false-negative rates.

`scripts/calibrate_paired_judges.py --dry-run --case all` constructs and checks the
fixtures offline. Live runs use process environment credentials, a maximum of six
stage requests per case, and one transport attempt per request. Reports are written
only under ignored `.yukon/reports/paired-calibration/`. No candidate is read,
modified, executed, scored, or promoted.
