# Hello Los Santos (working title)

A **GTA V Legacy story-mode** mod inspired by Hello Neighbor: someone new has moved
into the neighbourhood, he never leaves his house, and something is in his basement.
Sneak in, dodge a homeowner who learns your routes and sets traps there, find the
keys, and open the basement. Get caught too often and he calls the cops.

- **Host game (required):** Grand Theft Auto V Legacy, story mode only. Do not use it in GTA Online.
- **Inspiration (not required):** Hello Neighbor.
- **Players:** solo.
- **Loader:** Ultimate ASI Loader (Melty installs it). No Script Hook V: the mod ships its own native-calling layer.

## Status: design only, nothing built or tested yet

The design lives in `design/*.json` sheets (one row per thing, one column per property).
They are the source of truth; the C++ ASI will be generated from them.

Run the preflight to see every unfinished cell:

    python3 tools/preflight.py

It currently fails because native hashes, coordinates, door/prop models and the
house choice have to be read from the running game on a Windows PC.
