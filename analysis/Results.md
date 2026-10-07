# Exact synthetic pilot results

These are enumerated model expectations, not measured attack frequencies or independent live trials. Lower modeled loss is better. NASim fixtures are not used in these calculations.

| Case | Naive | Dedup | Lineage + age | Standard VOI | Oracle |
| --- | ---: | ---: | ---: | ---: | ---: |
| certain | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| independent_disagreement | 4.800 | 4.800 | 4.800 | 2.900 | 2.400 |
| duplicates | 6.400 | 5.000 | 5.000 | 3.700 | 3.200 |
| deduplicated_control | 5.000 | 5.000 | 5.000 | 3.700 | 3.200 |
| stale_observation | 4.800 | 4.800 | 2.600 | 1.738 | 1.248 |
| incorrect_lineage | 6.400 | 6.400 | 6.400 | 6.400 | 3.200 |
| cheap_verification | 4.000 | 4.000 | 4.000 | 2.500 | 2.000 |
| expensive_verification | 4.000 | 4.000 | 4.000 | 4.000 | 2.000 |
| verification_sacrifices_patch | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

No novel algorithm is implemented: standard VOI is a baseline. Perfect patch efficacy, a two-path graph, a known observation model and only one optional verification are strong simplifications. Source-label errors are modeled explicitly; uncertainty about error parameters and larger graphs remain untested.
