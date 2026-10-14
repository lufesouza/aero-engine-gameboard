# Why Boeing did not launch the fps (run dash-2050-sd)

Analysis of the 2030 fps decision and of later rounds, behind the explanation given in the session of 14 October 2026.
Run from any folder with `python3 <script>`; each writes its JSON next to itself.

- `why_fps.py` -> `why_fps.json`: sequential waterfall from the dashboard to the game for the 2030 10-year fps (new sites),
  deliveries and profit by period, Boeing's unsold MAX slots under Do Nothing. Its lever section uses a crude fast-ramp
  mapping and is superseded by `why2.py`.
- `order_check.py` -> `order_check.json`: alternative orderings of the waterfall.
- `f7.py` -> `f7.json`: bridge of the 7-year and 10-year decisions, with and without the supply-and-demand layer.
- `why2.py` -> `why2.json`: Shapley attribution over the 16 on/off combinations of demand, firm backlog, Airbus
  capacity and Boeing capacity (10-year and 7-year); the fps by round on the dashboard alone and with the layer;
  levers with a true k-times time compression of the fps ramp and full rate from entry into service under the cap;
  Airbus's ceiling and transition dip taken out one at a time; the value of the fps's extra capacity.

All values are Boeing's ΔPV (PV at 2026, $B) of the fps option minus Do Nothing, everyone else's orders as played,
nobody moving after the round, on corrected demand.
