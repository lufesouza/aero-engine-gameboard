| Turn | Side | Orders | Value $B | Best response | Best $B | Regret $B | Capture | Prediction | Expectation error $B |
|---|---|---|---:|---|---:|---:|---:|---:|---:|
| T1 | boeing | no new moves | -2.30 | launch fps (solo, 10y ramp-up) + rate increase | +1.14 | 3.43 | 57% | 83% | -0.30 |
| T1 | airbus | launch ngsa with rr_ultrafan_nb + Poaching | +41.37 | launch ngsa with rr_ultrafan_nb + Poaching | +41.37 | 0.00 | 100% | 60% | +6.37 |
| T1 | rolls_royce | Trent 1000 upgrade | +0.81 | launch uf_nb (solo, standard) | +20.98 | 20.16 | 23% | 60% | +0.01 |
| T1 | pratt_whitney | launch gtf_next (standard) + GTF durability upgrade | -5.62 | GTF durability upgrade | -2.01 | 3.61 | 79% | 80% | -5.12 |
| T1 | cfm | LEAP durability upgrade | +16.25 | LEAP durability upgrade | +16.25 | 0.00 | 100% | 80% | +6.75 |
| T2 | boeing | launch fps (solo, 10y ramp-up) with pw_gtf2 + rate increase | +4.34 | launch fps (solo, 10y ramp-up) + rate increase | +4.34 | 0.00 | 100% | 83% | +0.04 |
| T2 | airbus | launch rea350 + Poaching | +35.73 | launch rea350 + Poaching | +35.73 | 0.00 | 100% | 100% | -4.57 |
| T2 | rolls_royce | launch uf_nb (solo, standard) | -7.94 | launch uf_wb (standard) | -1.96 | 5.99 | 25% | 80% | -7.34 |
| T2 | pratt_whitney | cancel gtf_next | -2.77 | no new moves | -2.54 | 0.22 | 96% | 80% | -0.02 |
| T2 | cfm | GEnx improvement package | +18.39 | GEnx improvement package | +18.39 | 0.00 | 100% | 80% | +13.38 |
| T3 | boeing | no new moves | +3.87 | no new moves | +3.87 | 0.00 | 100% | 100% | +0.90 |
| T3 | airbus | Poaching | +36.53 | Delay Tactics + Poaching | +37.27 | 0.74 | 82% | 100% | +0.14 |
| T3 | rolls_royce | cancel uf_nb | -7.05 | cancel uf_nb | -7.05 | 0.00 | 100% | 100% | +0.07 |
| T3 | pratt_whitney | no new moves | -2.77 | no new moves | -2.77 | 0.00 | 100% | 100% | +0.00 |
| T3 | cfm | no new moves | +18.75 | no new moves | +18.75 | 0.00 | 100% | 100% | +0.35 |

| Side | Mean capture | Total myopic regret $B | Prediction accuracy | Mean abs expectation error $B | Final delta PV $B | Hindsight regret $B |
|---|---:|---:|---:|---:|---:|---:|
| boeing | 86% | 3.43 | 89% | 0.41 | +3.87 | -1.38 |
| airbus | 94% | 0.74 | 87% | 3.69 | +36.53 | -9.67 |
| rolls_royce | 49% | 26.15 | 80% | 2.47 | - | - |
| pratt_whitney | 92% | 3.83 | 87% | 1.72 | - | - |
| cfm | 100% | 0.00 | 87% | 6.83 | - | - |

Assigned objectives (attainment on the final projection):

| Player | Objective | Measured | Met |
|---|---|---|---|
| Boeing | Hold the 50/50 narrowbody split | 2040: 40.2%; 2045: 40.2%; 2050: 40.2%, gap -9.8pp | no |
| Boeing | Defend incumbency: narrowbody share never below the status quo | 2030: 40.0% (sq 40.0%); 2035: 42.0% (sq 40.0%); 2040: 40.2% (sq 40.0%); 2045: 40.2% (sq 40.0%); 2050: 40.2% (sq 40.0%) | yes |
| Airbus | Defend the 60/40 edge | 2040: 59.8%; 2045: 59.8%; 2050: 59.8%, gap -0.2pp | no |
| Airbus | Protect the A320 family: 60% while it carries the line | 2030: 60.0% | yes |
| Rolls-Royce | Enter the narrowbody market: Rolls-Royce narrowbody engines delivered by 2045 | 2045: 0 (sq 0); 2050: 0 (sq 0) | no |
| Rolls-Royce | Keep widebody dominance: widebody engines at or above the status quo | 2040: 62 (sq 212); 2045: 57 (sq 212); 2050: 52 (sq 212) | no |
| Pratt & Whitney | Capitalize on the GTF investment: narrowbody engines at or above the status quo | 2040: 0 (sq 960); 2045: 0 (sq 960); 2050: 0 (sq 960) | no |
| Pratt & Whitney | Restore credibility (proxy): GTF durability upgrade funded by 2031 | upgrade 2026 | yes |
| CFM International (GE side) | Dominate narrowbody engines: CFM share of narrowbody engines (LEAP derivative included) at or above the status quo | 2040: 100.0% (sq 76.0%); 2045: 100.0% (sq 76.0%); 2050: 100.0% (sq 76.0%) | yes |
| CFM International (GE side) | Introduce the open fan: an airframer flies the RISE open fan by 2045 | first EIS none | no |

| Turn | boeing:nb_share_50 | boeing:defend_incumbency | airbus:nb_share_60 | airbus:protect_a320 | rolls_royce:nb_entry | rolls_royce:wb_dominance | pratt_whitney:gtf_base | pratt_whitney:credibility | cfm:nb_dominance | cfm:open_fan |
|---|---|---|---|---|---|---|---|---|---|---|
| T1 | no | no | yes | yes | no | yes | no | yes | yes | no |
| T2 | no | yes | no | yes | no | no | no | yes | yes | no |
| T3 | no | yes | no | yes | no | no | no | yes | yes | no |
