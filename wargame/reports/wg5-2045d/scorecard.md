| Turn | Side | Orders | Value $B | Best response | Best $B | Regret $B | Capture | Prediction | Expectation error $B |
|---|---|---|---:|---|---:|---:|---:|---:|---:|
| T1 | boeing | no new moves | -2.40 | no new moves | -2.40 | 0.00 | 100% | 83% | -0.10 |
| T1 | airbus | launch ngsa with rr_ultrafan_nb + Poaching | +41.87 | launch ngsa with rr_ultrafan_nb + Poaching | +41.87 | 0.00 | 100% | 80% | -1.73 |
| T1 | rolls_royce | Trent 1000 upgrade | +0.81 | launch uf_nb (solo, standard) | +21.13 | 20.31 | 23% | 60% | +0.00 |
| T1 | pratt_whitney | launch gtf_next (standard) + GTF durability upgrade | -5.62 | GTF durability upgrade | -2.01 | 3.61 | 79% | 80% | -5.24 |
| T1 | cfm | LEAP durability upgrade | +16.25 | LEAP durability upgrade | +16.25 | 0.00 | 100% | 60% | +6.25 |
| T2 | boeing | launch re787 + rate increase | +0.66 | launch re787 | +0.90 | 0.24 | 97% | 100% | +0.08 |
| T2 | airbus | Poaching | +44.48 | Poaching | +44.48 | 0.00 | 100% | 40% | +1.78 |
| T2 | rolls_royce | no new moves | -1.82 | no new moves | -1.82 | 0.00 | 100% | 100% | -2.64 |
| T2 | pratt_whitney | cancel gtf_next | -2.77 | cancel gtf_next | -2.77 | 0.00 | 100% | 80% | -0.03 |
| T2 | cfm | GEnx improvement package | +18.67 | GEnx improvement package | +18.67 | 0.00 | 100% | 100% | +6.17 |
| T3 | boeing | no new moves | +1.68 | no new moves | +1.68 | 0.00 | 100% | 67% | +5.04 |
| T3 | airbus | no new moves | +44.54 | no new moves | +44.54 | 0.00 | 100% | 100% | +1.44 |
| T3 | rolls_royce | launch uf_wb (standard) | -3.68 | no new moves | -2.15 | 1.53 | 75% | 75% | -0.12 |
| T3 | pratt_whitney | no new moves | -2.77 | no new moves | -2.77 | 0.00 | 100% | 75% | +0.00 |
| T3 | cfm | no new moves | +18.99 | no new moves | +18.99 | 0.00 | 100% | 75% | +1.39 |

| Side | Mean capture | Total myopic regret $B | Prediction accuracy | Mean abs expectation error $B | Final delta PV $B | Hindsight regret $B |
|---|---:|---:|---:|---:|---:|---:|
| boeing | 99% | 0.24 | 83% | 1.74 | +1.68 | 0.24 |
| airbus | 100% | 0.00 | 73% | 1.65 | +44.54 | -11.04 |
| rolls_royce | 66% | 21.84 | 78% | 0.92 | - | - |
| pratt_whitney | 93% | 3.61 | 78% | 1.76 | - | - |
| cfm | 100% | 0.00 | 78% | 4.60 | - | - |

Assigned objectives (attainment on the final projection):

| Player | Objective | Measured | Met |
|---|---|---|---|
| Boeing | Hold the 50/50 narrowbody split | 2040: 38.4%; 2045: 32.3%; 2050: 25.0%, gap -25.0pp | no |
| Boeing | Defend incumbency: narrowbody share never below the status quo | 2030: 40.0% (sq 40.0%); 2035: 42.0% (sq 40.0%); 2040: 38.4% (sq 40.0%); 2045: 32.3% (sq 40.0%); 2050: 25.0% (sq 40.0%), gap -15.0pp | no |
| Airbus | Defend the 60/40 edge | 2040: 61.6%; 2045: 67.7%; 2050: 75.0% | yes |
| Airbus | Protect the A320 family: 60% while it carries the line | 2030: 60.0% | yes |
| Rolls-Royce | Enter the narrowbody market: Rolls-Royce narrowbody engines delivered by 2045 | 2045: 0 (sq 0); 2050: 0 (sq 0) | no |
| Rolls-Royce | Keep widebody dominance: widebody engines at or above the status quo | 2040: 144 (sq 212); 2045: 123 (sq 212); 2050: 102 (sq 212) | no |
| Pratt & Whitney | Capitalize on the GTF investment: narrowbody engines at or above the status quo | 2040: 0 (sq 960); 2045: 0 (sq 960); 2050: 0 (sq 960) | no |
| Pratt & Whitney | Restore credibility (proxy): GTF durability upgrade funded by 2031 | upgrade 2026 | yes |
| CFM International (GE side) | Dominate narrowbody engines: CFM share of narrowbody engines (LEAP derivative included) at or above the status quo | 2040: 100.0% (sq 76.0%); 2045: 100.0% (sq 76.0%); 2050: 100.0% (sq 76.0%) | yes |
| CFM International (GE side) | Introduce the open fan: an airframer flies the RISE open fan by 2045 | first EIS none | no |

| Turn | boeing:nb_share_50 | boeing:defend_incumbency | airbus:nb_share_60 | airbus:protect_a320 | rolls_royce:nb_entry | rolls_royce:wb_dominance | pratt_whitney:gtf_base | pratt_whitney:credibility | cfm:nb_dominance | cfm:open_fan |
|---|---|---|---|---|---|---|---|---|---|---|
| T1 | no | no | yes | yes | no | yes | no | yes | yes | no |
| T2 | no | no | yes | yes | no | no | no | yes | yes | no |
| T3 | no | no | yes | yes | no | no | no | yes | yes | no |
