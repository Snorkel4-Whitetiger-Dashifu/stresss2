# Pager-Policy Rollout Review Log
Mercury Payments Ops — change-advisory archive for the failed pager-policy rollout (2026-Q1 through 2026-Q2).

## Executive Summary
The outage routing compiler has produced unsafe responder queues since the February rollout. How the compile is *meant* to behave — normalization, dedupe and its tie-breaks, interval and overlap semantics, domain ordering, policy resolution, attenuation, the responder debt ledger, unit and threshold math, scoring, priority and queue ordering — was settled incrementally by the change-advisory board, and those decisions live in the review entries below, not in any single summary. The February draft proposals were revisited during the 2026-05 review cycle and several were reversed; where a draft proposal and a later CAB decision disagree, the later decision governs. `/app/docs/routing_contract.json` is the output contract only: it fixes file paths, schemas, exact key sets, identifier payloads and checksum encodings, not how the values are derived.

## February Draft Proposals (2026-02 — partly reversed)
The initial rollout draft circulated a set of compile-behavior proposals through CAB tickets in the 1900 range. Several did not survive review. They are archived in place below and marked superseded; do not implement them as written.

## Change-Review Archive (2025-Q4 through 2026-Q2)
Routine entries are context only. CAB-ticketed proposal and decision quotes embedded in the entries are the authoritative record for compile behavior.

### Review entry 0001 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0001. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0002 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0002. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0003 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0003. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0004 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0004. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0005 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0005. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0006 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0006. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0007 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0007. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0008 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0008. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0009 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0009. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0010 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0010. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0011 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0011. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0012 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0012. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.
> **Rollout draft proposal (2026-02-09 - CAB-1903)** Dana: service labels are stable upstream; preserve their exact casing and do not fold aliases together *(Superseded — reversed in the 2026-05 change review; see the matching decision entry.)*

### Review entry 0013 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0013. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0014 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0014. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0015 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0015. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0016 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0016. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0017 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0017. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0018 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0018. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0019 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0019. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0020 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0020. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0021 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0021. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0022 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0022. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0023 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0023. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0024 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0024. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.
> **Rollout draft proposal (2026-02-11 - CAB-1907)** Dana: rows whose start_ms or end_ms will not parse as an integer should be dropped from the compile entirely *(Superseded — reversed in the 2026-05 change review; see the matching decision entry.)*

### Review entry 0025 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0025. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0026 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0026. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0027 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0027. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0028 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0028. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0029 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0029. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0030 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0030. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0031 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0031. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0032 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0032. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0033 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0033. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0034 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0034. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0035 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0035. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0036 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0036. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.
> **Rollout draft proposal (2026-02-13 - CAB-1911)** Tomas: treat any non-empty `planned` string as true, including `false` and `no` *(Superseded — reversed in the 2026-05 change review; see the matching decision entry.)*

### Review entry 0037 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0037. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0038 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0038. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0039 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0039. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0040 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0040. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0041 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0041. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0042 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0042. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0043 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0043. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0044 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0044. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0045 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0045. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0046 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0046. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0047 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0047. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0048 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0048. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.
> **Rollout draft proposal (2026-02-16 - CAB-1914)** Tomas: when an incident_id repeats, keep the first row encountered and discard the rest *(Superseded — reversed in the 2026-05 change review; see the matching decision entry.)*

### Review entry 0049 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0049. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0050 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0050. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0051 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0051. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0052 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0052. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0053 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0053. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0054 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0054. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0055 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0055. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0056 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0056. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0057 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0057. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0058 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0058. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0059 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0059. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0060 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0060. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.
> **Rollout draft proposal (2026-02-18 - CAB-1917)** Dana: treat all intervals as closed [start_ms, end_ms], so endpoint contact counts as overlap *(Superseded — reversed in the 2026-05 change review; see the matching decision entry.)*

### Review entry 0061 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0061. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0062 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0062. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0063 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0063. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0064 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0064. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0065 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0065. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0066 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0066. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0067 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0067. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0068 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0068. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0069 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0069. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0070 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0070. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0071 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0071. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0072 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0072. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.
> **Rollout draft proposal (2026-02-20 - CAB-1921)** Tomas: when suppress and boost spans intersect, the intersection stays with suppress — suppression is safety-critical *(Superseded — reversed in the 2026-05 change review; see the matching decision entry.)*

> **Rollout draft proposal (2026-02-21 - CAB-1922)** Dana: for scoped attenuation (handoff, blackout, degrade), clip the all-scope compacted intervals and the matching-severity compacted intervals to the window separately, add the two clipped durations to get overlap_ms, and set segment_count to the total count of clips across both scopes — do not merge the two scopes together *(Superseded — reversed in the 2026-05 change review; see the matching decision entry.)*

### Review entry 0073 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0073. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0074 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0074. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0075 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0075. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0076 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0076. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0077 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0077. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0078 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0078. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0079 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0079. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0080 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0080. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0081 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0081. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0082 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0082. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0083 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0083. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0084 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0084. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.
> **Rollout draft proposal (2026-02-23 - CAB-1924)** Dana: subtract the full handoff, blackout and degrade overlaps from billable time with no divisor *(Superseded — reversed in the 2026-05 change review; see the matching decision entry.)*

> **Rollout draft proposal (2026-02-24 - CAB-1925)** Tomas: exception and attenuation unit counts should all round the same way — floor-divide every overlap (suppress, boost, handoff, blackout, degrade) by its unit size so the conversions stay consistent *(Superseded — reversed in the 2026-05 change review; see the matching decision entry.)*

### Review entry 0085 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0085. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0086 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0086. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0087 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0087. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0088 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0088. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0089 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0089. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0090 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0090. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0091 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0091. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0092 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0092. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0093 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0093. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0094 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0094. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0095 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0095. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0096 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0096. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.
> **Rollout draft proposal (2026-02-25 - CAB-1928)** Tomas: carry responder debt forward without any cap; long weekends should accumulate naturally *(Superseded — reversed in the 2026-05 change review; see the matching decision entry.)*

> **Rollout draft proposal (2026-02-25 - CAB-1926)** Dana: responder-debt bookkeeping between a service's windows — decay carried debt by half the idle gap (`debt_in_ms = max(previous.debt_out_ms - idle_gap_ms//2, 0)`), credit `debt_adjusted_dispatchable_ms` with `debt_in_ms//4`, and on carry-out add `handoff_segment_count*15 + blackout_segment_count*20 + degrade_segment_count*10` with no separate maintenance-span credit *(Superseded — reversed in the 2026-05 change review; see the matching decision entry.)*

> **Rollout draft proposal (2026-02-26 - CAB-1930)** Dana: the pressure probes should look back a flat 200ms — probe [end_ms-200, end_ms) for handoff, blackout and degrade alike — and each pressure score is (all_probe_ms // 40) + (severity_probe_ms // 25) + segment_count, uniform across the three domains *(Superseded — reversed in the 2026-05 change review; see the matching decision entry.)*

> **Rollout draft proposal (2026-02-27 - CAB-1932)** Tomas: escalation_score should weight debt_adjusted_dispatchable_ms // 50, incident_count once, critical_incident_count twice, and count each pressure score a single time rather than doubling any of them *(Superseded — reversed in the 2026-05 change review; see the matching decision entry.)*

> **Rollout draft proposal (2026-02-28 - CAB-1934)** Tomas: queue admission thresholds — compute `effective_queue_min_ms = queue_min_effective_ms + suppress_units*suppress_penalty_ms - boost_units*boost_credit_ms` with no floor at that step, add the handoff, blackout and degrade unit penalties in turn, and apply the `min_queue_floor_ms` floor once at the very end to the final `dispatch_queue_min_ms` *(Superseded — reversed in the 2026-05 change review; see the matching decision entry.)*

### Review entry 0097 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0097. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0098 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0098. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0099 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0099. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0100 — inventory lane
> **Change-review decision (2026-04-02 - CAB-2102)** Dana: attenuation divides overlaps as handoff // 3, blackout // 4, degrade // 5. *(Revised — see the 2026-05 change review.)*
Shift lead logged routine rollout observation for inventory (east) during review window 0100. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0101 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0101. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0102 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0102. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0103 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0103. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0104 — auth lane
> **Change-review decision (2026-04-06 - CAB-2106)** Dana: responder debt decays by half the idle gap, caps at 2200, and credits segments at 15/20/10 for handoff/blackout/degrade. *(Revised — see the 2026-05 change review.)*
Shift lead logged routine rollout observation for auth (east) during review window 0104. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0105 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0105. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0106 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0106. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0107 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0107. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0108 — inventory lane
> **Change-review decision (2026-04-10 - CAB-2110)** Tomas: every unit conversion rounds down, including suppress units. *(Revised — see the 2026-05 change review.)*
Shift lead logged routine rollout observation for inventory (east) during review window 0108. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0109 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0109. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0110 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0110. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0111 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0111. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0112 — auth lane
> **Change-review decision (2026-04-14 - CAB-2114)** Tomas: queue admission compares debt-adjusted dispatchability against effective_queue_min_ms alone; no further threshold escalation applies. *(Revised — see the 2026-05 change review.)*
Shift lead logged routine rollout observation for auth (east) during review window 0112. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0113 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0113. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0114 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0114. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0115 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0115. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0116 — inventory lane
> **Change-review decision (2026-04-18 - CAB-2118)** Dana: incident windows merge only when the next incident starts at or before the current window's end, with no grace interval. *(Revised — see the 2026-05 change review.)*
Shift lead logged routine rollout observation for inventory (east) during review window 0116. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0117 — edge lane
> **Change-review decision (2026-04-20 - CAB-2127)** Dana: duplicate incidents are grouped by `incident_id` and the kept row is chosen by highest severity rank first, then max end_ms, then max start_ms; the planned flag does not enter the tie-break. *(Revised — see the 2026-05 change review.)*
> **Change-review decision (2026-04-22 - CAB-2131)** Tomas: scoped handoff/blackout/degrade overlap_ms is the SUM of the (service, all) clipped duration and the (service, max_severity) clipped duration, and segment_count is the total count of clips across both scopes; the two scopes are not unioned. *(Revised — see the 2026-05 change review.)*
> **Change-review decision (2026-04-24 - CAB-2133)** Tomas: where a suppress span and a boost span intersect, the shared duration counts toward suppression_overlap_ms and is excluded from boost_overlap_ms; suppress wins the intersection. *(Revised — see the 2026-05 change review.)*
Shift lead logged routine rollout observation for edge (west) during review window 0117. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0118 — notifications lane
> **Change-review decision (2026-04-26 - CAB-2135)** Dana: pressure divisors — `handoff_pressure_score` = (all_probe_ms // 25) + (severity_probe_ms // 15) + handoff_segment_count; `blackout_pressure_score` uses // 30 and // 20; `degrade_pressure_score` uses // 28 and // 18. *(Revised — see the 2026-05 change review.)*
> **Change-review decision (2026-04-28 - CAB-2137)** Tomas: `escalation_score` = (debt_adjusted_dispatchable_ms // 60) + incident_count*2 + critical_incident_count*3 + severity_weight[max_severity]; the exception-balance, handoff, blackout and debt pressure terms are not part of it. *(Revised — see the 2026-05 change review.)*
> **Change-review decision (2026-04-30 - CAB-2139)** Dana: interval semantics are closed [start_ms, end_ms]; endpoint-only contact contributes 1ms of overlap. *(Revised — see the 2026-05 change review.)*
Shift lead logged routine rollout observation for notifications (north) during review window 0118. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0119 — ledger lane
> **Change-review decision (2026-05-01 - CAB-2141)** Tomas: `planned` coercion treats any non-empty string as true, including `false` and `no`, and treats a numeric planned value of 2 as true. *(Revised — see the 2026-05 change review.)*
> **Change-review decision (2026-05-01 - CAB-2143)** Dana: `debt_adjusted_dispatchable_ms` = dispatchable_billable_duration_ms + (debt_in_ms // 4). *(Revised — see the 2026-05 change review.)*
Shift lead logged routine rollout observation for ledger (central) during review window 0119. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0120 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0120. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.
> **Change-review decision (2026-05-02 - CAB-2201)** Ilya: canonical service labels are trimmed and lowercased, then folded through the alias table: `authentication` -> `auth`, `payments` -> `billing`, `search-api` -> `search`. This supersedes CAB-1903.

### Review entry 0812 — debt bench
> **Change-review decision (2026-05-16 - CAB-2242)** Ilya: the debt credit applied to the dispatchable duration was losing every partial step, so a debt carry smaller than one full step credited nothing. That credit now ROUNDS UP: `debt_adjusted_dispatchable_ms = dispatchable_billable_duration_ms + ceil(debt_in_ms / 5)`. In integer arithmetic ceil(x/5) is -(-x // 5). The `// 3` idle decay and the debt_out cap recorded earlier are unchanged and still round down. This revises the floored credit in CAB-2236.

### Review entry 0816 — probe bench
> **Change-review decision (2026-05-17 - CAB-2246)** Dana: the blackout probe takes the same correction and no other: `blackout_pressure_score = (blackout_all_probe_ms // 36) + ceil(blackout_severity_probe_ms / 24) + blackout_segment_count`. The degrade probe was reviewed in the same session and is deliberately left floored on both halves, so the two must not be assumed symmetric.

### Review entry 0818 — debt bench
> **Change-review decision (2026-05-17 - CAB-2248)** Ilya: the debt-in half of the debt pressure score ROUNDS UP while the debt-out half does not: `debt_pressure_score = (debt_out_ms // 80) + ceil(debt_in_ms / 120)`. The 80 debt-out divisor is unchanged.

### Review entry 0821 — canonicalization bench
> **Change-review decision (2026-05-18 - CAB-2258)** Marta: duplicate-severity precedence is REVERSED. Incident reports that duplicate an existing `incident_id` frequently arrive from an automated escalator that inflates severity before a human has confirmed it, so taking the maximum severity was systematically over-escalating the queue. Where two rows share an `incident_id` and tie on `end_ms`, the row with the LOWER severity rank is now the one kept — minor beats major, major beats critical. The remaining keys of the CAB-2207 chain are unchanged and still run in the same order after this one: then prefer `planned == false`, then max `start_ms`, then max `service` lexicographically. Only the severity comparison direction changes. This reverses that step of CAB-2207.

### Review entry 0822 — routing bench
> **Change-review decision (2026-05-19 - CAB-2252)** Dana: handoff attenuation review found a scoped handoff overlap shorter than one full step was being absorbed without cost, so the handoff subtraction ROUNDS UP: `adjusted_billable_duration_ms = max(billable_duration_ms - ceil(handoff_overlap_ms / 2), 0)`. In integer arithmetic ceil(x/2) is -(-x // 2). This revises the floored form recorded in CAB-2208.

### Review entry 0824 — routing bench
> **Change-review decision (2026-05-19 - CAB-2254)** Dana: the blackout attenuation takes the same correction: `routed_billable_duration_ms = max(adjusted_billable_duration_ms - ceil(blackout_overlap_ms / 3), 0)`. The degrade attenuation that follows it was reviewed in the same session and is deliberately left FLOORED at `degrade_overlap_ms // 4`, so the three attenuation layers must not be assumed to round alike.

### Review entry 0826 — exception bench
> **Change-review decision (2026-05-20 - CAB-2256)** Ilya: boost units are counted the same way suppression units already are — `boost_units = ceil(boost_overlap_ms / boost_unit_ms)` — because a partial boost window was previously granting no credit at all. The handoff, blackout and degrade unit counts keep their floors and are not affected by this entry.

### Review entry 0820 — audit bench
> **Change-review decision (2026-05-18 - CAB-2250)** Ilya: recording the rounding map settled across CAB-2224, CAB-2242, CAB-2246, CAB-2248, CAB-2252, CAB-2254 and CAB-2256 for the avoidance of doubt. Rounding in this compiler is NOT uniform and no divisor's direction may be inferred from any other, including between siblings in the same family: the suppression unit count and the four probe/unit families each carry their own direction, and the degrade and handoff probes stay floored where the blackout probe rounds up. Read each divisor's direction from its own governing decision. *(Revised on the degrade probe point — see CAB-2264.)*

### Review entry 0121 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0121. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0122 — search lane
> **Change-review decision (2026-04-16 - CAB-2116)** Dana: final queue ordering is priority tier, then dispatchable_billable_duration_ms descending, then service ascending — a short, coarse key that avoids the pressure-score comparisons. *(Revised — see the 2026-05 change review.)*
Shift lead logged routine rollout observation for search (north) during review window 0122. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0123 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0123. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0124 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0124. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0125 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0125. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0126 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0126. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0127 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0127. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0128 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0128. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0129 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0129. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0130 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0130. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0131 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0131. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0132 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0132. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0133 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0133. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0134 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0134. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0135 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0135. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0136 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0136. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0137 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0137. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.
> **Change-review decision (2026-05-02 - CAB-2202)** Ilya: allowed severities are critical, major, minor; anything else (or a missing value) becomes `minor`. Severity rank for comparisons is critical > major > minor.

### Review entry 0138 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0138. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0139 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0139. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0140 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0140. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0141 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0141. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0142 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0142. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0143 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0143. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0144 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0144. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0145 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0145. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0146 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0146. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0147 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0147. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0148 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0148. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0149 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0149. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0150 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0150. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0151 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0151. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0152 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0152. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0153 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0153. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0154 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0154. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.
> **Change-review decision (2026-05-03 - CAB-2204)** Priya: every millisecond field is coerced with int(str(value).strip()) with fallback 0. Unparseable rows are KEPT with the fallback value — they are not dropped. This supersedes CAB-1907.

### Review entry 0155 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0155. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0156 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0156. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0157 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0157. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0158 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0158. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0159 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0159. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0160 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0160. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0161 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0161. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0162 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0162. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0163 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0163. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0164 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0164. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0165 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0165. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0166 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0166. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0167 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0167. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0168 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0168. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0169 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0169. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0170 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0170. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0171 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0171. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.
> **Change-review decision (2026-05-03 - CAB-2205)** Priya: `planned` coercion: booleans — preserve the boolean value; strings — strip and lowercase; true, 1, and yes become true; every other string becomes false; other types — use Python bool(value): null and numeric 0 become false; nonzero numbers and other truthy values become true. For the summary, count canonical deduplicated rows whose normalized planned value is true; for example planned=2 is excluded and planned=null is not. This supersedes CAB-1911.

### Review entry 0172 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0172. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0173 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0173. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0174 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0174. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0175 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0175. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0176 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0176. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0177 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0177. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0178 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0178. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0179 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0179. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0180 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0180. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0181 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0181. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0182 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0182. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0183 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0183. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0184 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0184. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0185 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0185. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0186 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0186. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0187 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0187. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0188 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0188. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.
> **Change-review decision (2026-05-04 - CAB-2207)** Marta: duplicate incidents are grouped by `incident_id` and one row is kept per group. Tie-break chain, in order: max end_ms; then max severity rank; then prefer planned == false; then max start_ms; then max service lexicographically. This supersedes CAB-1914.

### Review entry 0189 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0189. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0190 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0190. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0191 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0191. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0192 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0192. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0193 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0193. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0194 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0194. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0195 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0195. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0196 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0196. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0197 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0197. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0198 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0198. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0199 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0199. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0200 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0200. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0201 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0201. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0202 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0202. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0203 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0203. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0204 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0204. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0205 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0205. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.
> **Change-review decision (2026-05-04 - CAB-2208)** Marta: interval semantics: all source and overlap intervals are half-open [start_ms,end_ms); rows with end_ms <= start_ms are discarded. Overlap is max(0, min(end_a, end_b) - max(start_a, start_b)); endpoint-only contact contributes 0ms. This supersedes CAB-1917.

### Review entry 0206 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0206. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0207 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0207. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0208 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0208. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0209 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0209. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0210 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0210. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0211 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0211. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0212 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0212. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0213 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0213. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0214 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0214. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0215 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0215. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0216 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0216. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0217 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0217. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0218 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0218. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0219 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0219. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0220 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0220. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0221 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0221. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0222 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0222. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.
> **Change-review decision (2026-05-05 - CAB-2210)** Ilya: window construction uses unplanned incidents only; stitch rule: merge if next.start_ms <= current.end_ms + 30 — the 30ms grace interval is final and revises CAB-2118. Maintenance compaction: per service, merge touching intervals if next.start_ms <= current.end_ms. Exceptions compaction: per (service, action), merge touching intervals if next.start_ms <= current.end_ms. Scoped compaction: per (service, severity_scope), merge touching intervals if next.start_ms <= current.end_ms.

### Review entry 0223 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0223. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0224 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0224. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0225 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0225. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0226 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0226. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0227 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0227. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0228 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0228. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0229 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0229. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0230 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0230. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0231 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0231. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0232 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0232. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0233 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0233. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0234 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0234. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0235 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0235. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0236 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0236. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0237 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0237. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0238 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0238. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0239 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0239. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.
> **Change-review decision (2026-05-05 - CAB-2211)** Ilya: routing domains apply in the fixed order maintenance -> exceptions -> handoff -> blackout -> degrade. Exception actions are limited to suppress and boost; severity scopes are all, major, critical.

### Review entry 0240 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0240. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0241 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0241. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0242 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0242. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0243 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0243. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0244 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0244. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0245 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0245. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0246 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0246. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0247 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0247. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0248 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0248. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0249 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0249. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0250 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0250. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0251 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0251. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0252 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0252. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0253 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0253. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0254 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0254. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0255 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0255. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0256 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0256. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.
> **Change-review decision (2026-05-06 - CAB-2213)** Nadia: scoped overlap for handoff, blackout and degrade: for handoff, blackout, and degrade, select compacted intervals for (service, all) and (service, window.max_severity), clip both sets to the outage window, discard zero-duration clips, union and compact the combined clips using the touching merge rule, then set overlap_ms to the union duration and segment_count to the number of combined union segments. Thus an all-scope clip ending at 240 and a matching-severity clip starting at 240 form one segment, not two.

### Review entry 0257 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0257. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0258 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0258. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0259 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0259. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0260 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0260. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0261 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0261. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0262 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0262. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0263 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0263. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0264 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0264. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0265 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0265. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0266 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0266. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0267 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0267. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0268 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0268. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0269 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0269. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0270 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0270. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0271 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0271. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0272 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0272. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0273 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0273. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.
> **Change-review decision (2026-05-06 - CAB-2214)** Nadia: suppress/boost precedence: compute half-open suppress and boost overlap spans, union each action's spans independently, assign all boost union duration to boost_overlap_ms, and subtract the duration of the suppress/boost intersection from suppression_overlap_ms; boost therefore wins intersection time. This supersedes CAB-1921.

### Review entry 0274 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0274. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0275 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0275. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0276 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0276. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0277 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0277. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0278 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0278. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0279 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0279. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0280 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0280. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0281 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0281. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0282 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0282. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0283 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0283. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0284 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0284. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0285 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0285. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0286 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0286. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0287 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0287. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0288 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0288. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0289 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0289. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0290 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0290. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.
> **Change-review decision (2026-05-07 - CAB-2216)** Priya: attenuation chain: `billable_duration_ms` = max(duration_ms - maintenance_overlap_ms, 0); `adjusted_billable_duration_ms` = max(billable_duration_ms - (handoff_overlap_ms // 2), 0); `routed_billable_duration_ms` = max(adjusted_billable_duration_ms - (blackout_overlap_ms // 3), 0); `dispatchable_billable_duration_ms` = max(routed_billable_duration_ms - (degrade_overlap_ms // 4), 0). The 2/3/4 divisors are final and revise CAB-2102. This supersedes CAB-1924.

### Review entry 0291 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0291. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0292 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0292. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0293 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0293. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0294 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0294. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0295 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0295. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0296 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0296. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0297 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0297. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0298 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0298. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0299 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0299. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0300 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0300. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0301 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0301. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0302 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0302. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0303 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0303. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0304 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0304. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0305 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0305. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0306 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0306. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0307 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0307. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.
> **Change-review decision (2026-05-07 - CAB-2217)** Priya: field dependency review: billable_duration_ms depends only on duration_ms and maintenance_overlap_ms suppression_overlap_ms and boost_overlap_ms are tracked separately and do not directly change billable_duration_ms adjusted_billable_duration_ms depends only on billable_duration_ms and handoff_overlap_ms routed_billable_duration_ms depends only on adjusted_billable_duration_ms and blackout_overlap_ms dispatchable_billable_duration_ms depends only on routed_billable_duration_ms and degrade_overlap_ms.

### Review entry 0308 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0308. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0309 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0309. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0310 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0310. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0311 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0311. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0312 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0312. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0313 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0313. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0314 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0314. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0315 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0315. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0316 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0316. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0317 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0317. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0318 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0318. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0319 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0319. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0320 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0320. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0321 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0321. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0322 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0322. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0323 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0323. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0324 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0324. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.
> **Change-review decision (2026-05-08 - CAB-2219)** Marta: debt ledger: state is independent per normalized service; process each service's merged windows in start_ms ascending order after all attenuation fields are finalized. First window: idle_gap_ms=0, debt_in_ms=0. `idle_gap_ms`: for later windows max(current.start_ms-previous.end_ms,0). `debt_in_ms` = max(previous.debt_out_ms-(idle_gap_ms//3),0). `debt_adjusted_dispatchable_ms` = dispatchable_billable_duration_ms + (debt_in_ms//5). `debt_out_ms` = min(debt_in_ms + dispatchable_billable_duration_ms + handoff_segment_count*20 + blackout_segment_count*25 + degrade_segment_count*15, 2500). finalize debt_out_ms for one window before evaluating the next window in the same service. The one-third idle decay, the 2500 cap, and the 20/25/15 segment credits are final and revise CAB-2106. This supersedes CAB-1928.

### Review entry 0325 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0325. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0326 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0326. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0327 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0327. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0328 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0328. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0329 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0329. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0330 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0330. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0331 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0331. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0332 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0332. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0333 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0333. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0334 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0334. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0335 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0335. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0336 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0336. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0337 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0337. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0338 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0338. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0339 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0339. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0340 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0340. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0341 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0341. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.
> **Change-review decision (2026-05-09 - CAB-2221)** Nadia: approved policy baseline (integers, defaults for every field): `queue_min_effective_ms` = 234; `critical_p1_min_ms` = 280; `critical_threshold_ms` = 650; `high_threshold_ms` = 320; `no_overlap_high_duration_ms` = 450; `critical_count_for_critical` = 2; `no_overlap_bonus` = 4; `segment_bonus` = 1; `score_threshold_critical` = 38; `score_threshold_high` = 24; `suppress_penalty_ms` = 40; `boost_credit_ms` = 30; `suppress_unit_ms` = 50; `boost_unit_ms` = 50; `min_queue_floor_ms` = 120; `boost_force_critical_ms` = 140; `boost_high_relief_ms` = 40; `handoff_penalty_ms` = 35; `handoff_unit_ms` = 60; `handoff_force_critical_ms` = 59; `handoff_high_relief_ms` = 50; `blackout_penalty_ms` = 45; `blackout_unit_ms` = 70; `blackout_force_critical_ms` = 200; `blackout_high_relief_ms` = 55; `degrade_penalty_ms` = 30; `degrade_unit_ms` = 80; `degrade_force_critical_ms` = 170; `degrade_high_relief_ms` = 45. Severity weights default to critical=5, major=3, minor=1.

### Review entry 0342 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0342. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0343 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0343. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0344 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0344. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0345 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0345. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0346 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0346. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0347 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0347. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0348 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0348. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0349 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0349. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0350 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0350. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0351 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0351. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0352 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0352. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0353 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0353. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0354 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0354. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0355 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0355. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0356 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0356. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0357 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0357. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0358 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0358. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.
> **Change-review decision (2026-05-09 - CAB-2222)** Nadia: policy file resolution: normalize the source default object by starting from policies.defaults and replacing each present integer field after int coercion with fallback 0; merge severity_weight by replacing only present critical/major/minor entries. Overrides: resolve every service profile to a complete policy: start from the normalized default profile, apply the matching service_overrides[canonical_service] fields, and merge a partial severity_weight map by key; omitted fields must remain available and must never raise KeyError. Sparse sources: the default object and every service override may omit any field; all omitted fields fall back through the complete defaults above.

### Review entry 0359 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0359. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0360 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0360. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0361 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0361. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0362 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0362. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0363 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0363. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0364 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0364. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0365 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0365. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0366 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0366. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0367 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0367. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0368 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0368. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0369 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0369. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0370 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0370. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0371 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0371. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0372 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0372. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0373 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0373. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0374 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0374. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0375 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0375. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.
> **Change-review decision (2026-05-10 - CAB-2224)** Ilya: unit conversions: `suppress_units` = 0 when suppression_overlap_ms == 0 else ceil(suppression_overlap_ms / max(suppress_unit_ms, 1)); `boost_units` = boost_overlap_ms // max(boost_unit_ms, 1); `handoff_units` = handoff_overlap_ms // max(handoff_unit_ms, 1); `blackout_units` = blackout_overlap_ms // max(blackout_unit_ms, 1); `degrade_units` = degrade_overlap_ms // max(degrade_unit_ms, 1). Note suppress rounds up; every other unit rounds down — this revises the all-floor rule in CAB-2110.

### Review entry 0376 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0376. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0377 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0377. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0378 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0378. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0379 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0379. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0380 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0380. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0381 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0381. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0382 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0382. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0383 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0383. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0384 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0384. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0385 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0385. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0386 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0386. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0387 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0387. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0388 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0388. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0389 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0389. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0390 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0390. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0391 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0391. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0392 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0392. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.
> **Change-review decision (2026-05-10 - CAB-2225)** Ilya: queue admission thresholds build in four steps: `effective_queue_min_ms` = max(queue_min_effective_ms + suppress_units*suppress_penalty_ms - boost_units*boost_credit_ms, min_queue_floor_ms); `adjusted_queue_min_ms` = effective_queue_min_ms + handoff_units*handoff_penalty_ms; `routed_queue_min_ms` = adjusted_queue_min_ms + blackout_units*blackout_penalty_ms; `dispatch_queue_min_ms` = routed_queue_min_ms + degrade_units*degrade_penalty_ms. A window enters the queue only when debt_adjusted_dispatchable_ms >= dispatch_queue_min_ms — the full four-step chain is final and revises CAB-2114.

### Review entry 0393 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0393. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0394 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0394. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0395 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0395. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0396 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0396. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0397 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0397. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0398 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0398. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0399 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0399. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0400 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0400. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0401 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0401. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0402 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0402. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0403 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0403. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0404 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0404. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0405 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0405. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0406 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0406. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0407 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0407. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0408 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0408. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0409 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0409. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.
> **Change-review decision (2026-05-11 - CAB-2227)** Marta: pressure probes and scores: `exception_balance_score` = boost_units - suppress_units. Handoff probe [end_ms-180, end_ms+1), blackout probe [end_ms-240, end_ms+1), degrade probe [end_ms-210, end_ms+1). `handoff_pressure_score` = (all_probe_ms // 30) + (severity_probe_ms // 20) + handoff_segment_count; `blackout_pressure_score` = (all_probe_ms // 36) + (severity_probe_ms // 24) + blackout_segment_count; `degrade_pressure_score` = (all_probe_ms // 34) + (severity_probe_ms // 23) + degrade_segment_count; `debt_pressure_score` = (debt_out_ms // 80) + (debt_in_ms // 120).

### Review entry 0410 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0410. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0411 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0411. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0412 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0412. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0413 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0413. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0414 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0414. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0415 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0415. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0416 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0416. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0417 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0417. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0418 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0418. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0419 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0419. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0420 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0420. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0421 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0421. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0422 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0422. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0423 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0423. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0424 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0424. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0425 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0425. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0426 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0426. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.
> **Change-review decision (2026-05-11 - CAB-2228)** Marta: `escalation_score` = (debt_adjusted_dispatchable_ms // 60) + incident_count*2 + critical_incident_count*3 + (maintenance_overlap_ms==0 ? no_overlap_bonus : 0) + maintenance_span_count*segment_bonus + severity_weight[max_severity] + exception_balance_score*2 + handoff_pressure_score*2 + blackout_pressure_score*2 + debt_pressure_score*2. `risk_vector` = escalation_score + blackout_pressure_score + (degrade_pressure_score * 2) + debt_pressure_score.

### Review entry 0427 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0427. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0428 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0428. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0429 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0429. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0430 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0430. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0431 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0431. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0432 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0432. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0433 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0433. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0434 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0434. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0435 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0435. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0436 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0436. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0437 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0437. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0438 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0438. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0439 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0439. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0440 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0440. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0441 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0441. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0442 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0442. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0443 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0443. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.
> **Change-review decision (2026-05-12 - CAB-2230)** Nadia: a window is priority critical when ANY of the following holds: max_severity == critical and debt_adjusted_dispatchable_ms >= critical_p1_min_ms; OR debt_adjusted_dispatchable_ms >= critical_threshold_ms; OR critical_incident_count >= critical_count_for_critical; OR escalation_score >= score_threshold_critical; OR boost_overlap_ms >= boost_force_critical_ms; OR handoff_overlap_ms >= handoff_force_critical_ms; OR blackout_overlap_ms >= blackout_force_critical_ms; OR degrade_overlap_ms >= degrade_force_critical_ms; OR debt_out_ms >= 900; OR risk_vector >= score_threshold_critical + 4.

### Review entry 0444 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0444. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0445 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0445. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0446 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0446. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0447 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0447. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0448 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0448. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0449 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0449. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0450 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0450. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0451 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0451. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0452 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0452. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0453 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0453. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0454 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0454. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0455 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0455. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0456 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0456. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0457 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0457. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0458 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0458. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0459 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0459. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0460 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0460. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.
> **Change-review decision (2026-05-12 - CAB-2231)** Nadia: when not critical, a window is priority high when ANY of the following holds: debt_adjusted_dispatchable_ms >= high_threshold_ms; OR incident_count >= 3 and max_severity in {major, critical}; OR maintenance_overlap_ms == 0 and duration_ms >= no_overlap_high_duration_ms; OR escalation_score >= score_threshold_high; OR exception_balance_score > 0 and debt_adjusted_dispatchable_ms >= max(high_threshold_ms - boost_high_relief_ms, 0); OR handoff_pressure_score > 0 and debt_adjusted_dispatchable_ms >= max(high_threshold_ms - handoff_high_relief_ms, 0); OR blackout_pressure_score > 0 and debt_adjusted_dispatchable_ms >= max(high_threshold_ms - blackout_high_relief_ms, 0); OR degrade_pressure_score > 0 and debt_adjusted_dispatchable_ms >= max(high_threshold_ms - degrade_high_relief_ms, 0); OR debt_pressure_score > 0 and debt_adjusted_dispatchable_ms >= max(high_threshold_ms - 35, 0); OR risk_vector >= score_threshold_high + 2. Otherwise priority falls back to medium.

### Review entry 0461 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0461. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0462 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0462. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0463 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0463. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0464 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0464. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0465 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0465. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0466 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0466. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0467 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0467. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0468 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0468. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0469 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0469. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0470 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0470. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0471 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0471. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0472 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0472. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0473 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0473. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0474 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0474. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0475 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0475. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0476 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0476. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0477 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0477. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.
> **Change-review decision (2026-05-13 - CAB-2233)** Ilya: final queue ordering, applied strictly in sequence — this full 16-key order is final and revises the coarse 3-key ordering in CAB-2116: priority (critical > high > medium); then escalation_score desc; then handoff_pressure_score desc; then blackout_pressure_score desc; then degrade_pressure_score desc; then debt_pressure_score desc; then risk_vector desc; then exception_balance_score desc; then dispatchable_billable_duration_ms desc; then routed_billable_duration_ms desc; then adjusted_billable_duration_ms desc; then critical_incident_count desc; then maintenance_span_count desc; then incident_count desc; then service asc; then start_ms asc.

### Review entry 0478 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0478. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0479 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0479. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0480 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0480. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0481 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0481. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0482 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0482. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0483 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0483. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0484 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0484. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0485 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0485. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0486 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0486. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0487 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0487. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0488 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0488. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0489 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0489. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0490 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0490. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0491 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0491. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.
> **Change-review decision (2026-05-16 - CAB-2236)** Marta: closing the extended-quiet thread from the 0491 review — proportional decay leaves stale debt on the books when a service goes quiet for a long stretch, so the ledger now resets outright past a threshold: when `idle_gap_ms` is 600 or greater, `debt_in_ms` is 0 for that window instead of `max(previous.debt_out_ms - (idle_gap_ms // 3), 0)`. Below 600 the one-third decay stands exactly as written. This reset revises CAB-2219; the 2500 cap and the 20/25/15 segment credits there are unaffected.

### Review entry 0492 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0492. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0493 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0493. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.
> **Change-review decision (2026-05-18 - CAB-2251)** Marta: the maintenance-window review closed on this lane with one ledger change — a window that overlapped planned maintenance still leaves residual responder debt, and carrying nothing for it understated the next window's position. Each maintenance span now carries a credit alongside the existing ones: `debt_out_ms = min(debt_in_ms + dispatchable_billable_duration_ms + maintenance_span_count*12 + handoff_segment_count*20 + blackout_segment_count*25 + degrade_segment_count*15, 2500)`. The 12-point maintenance credit revises CAB-2219; the 20/25/15 credits, the one-third idle decay and the 2500 cap recorded there are unchanged, as is the extended-idle reset in CAB-2236.

### Review entry 0494 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0494. Vendor paging webhook retried twice before delivery; within contractual retry budget.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0495 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0495. Synthetic incident injection verified pager delivery for secondary responders in this region.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0496 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0496. Rotation swap requested and approved; no change to escalation policy parameters.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0497 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0497. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0498 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0498. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0499 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0499. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0500 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0500. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0501 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0501. Dashboard tiles for responder load lagged during the sync window; attributed to cache refresh, not the compiler.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0502 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0502. Escalation bridge reviewed stale runbook links; owners pinged to refresh links before the next drill.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0503 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0503. On-call handoff rehearsal ran clean; no gaps observed in the rotation calendar for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0504 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0504. Vendor paging webhook retried twice before delivery; within contractual retry budget.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0505 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0505. Synthetic incident injection verified pager delivery for secondary responders in this region.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0506 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0506. Rotation swap requested and approved; no change to escalation policy parameters.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0507 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0507. Quarterly audit sampled acknowledgment records; no compiler-relevant findings for this lane.
Thread archived; see the CAB decision log entries for anything affecting compile behavior.

### Review entry 0508 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0508. Noise review: duplicate page storm traced to a flapping health check, muted at the source.
Historical CSV escalation exports remain archived and non-authoritative for the JSON compile acceptance.

### Review entry 0509 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0509. Capacity review noted rising page volume; no threshold changes approved outside the CAB process.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0510 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0510. Paging drill completed within SLO; acknowledgment latency p95 held under the rollout target.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.


## Communications Retro — Rollout Incident (filed 2026-05-29)
The comms retro examined how decisions traveled during the rollout incident, because two early misimplementations traced to engineers acting on chat summaries rather than ticketed CAB decisions. The board's decisions were consistently correct at the ticket level, but paraphrases posted to the incident channel dropped qualifiers — most notably scope restrictions — and those paraphrases were what several implementers read. Three practices were adopted. First, decision announcements in chat must link the ticket and quote its operative sentence verbatim, with paraphrase labeled non-authoritative. Second, the weekly digest pilots a superseded-by column so anyone skimming can see which February drafts and later-revised interim positions were overturned without reconstructing the chain by hand. Third, the incident channel's pinned post now states the reading rule that governs this archive: where an earlier proposal and a later decision disagree, the later decision governs, and the ticketed record — not chat — is the source of truth. The retro reaffirmed that no communications practice changes compile semantics; the tickets remain the only mechanism by which behavior changes.


> **Change-review decision (2026-05-25 - CAB-2240)** Priya: responder dashboards retain ninety days of window history; older windows are served from the artifact archive on demand. Dashboard retention is an operational setting and carries no weight in compile output.

> **Change-review decision (2026-05-28 - CAB-2243)** Marta: artifact bundles must record output signatures at export time and again at archive ingest; a mismatch quarantines the bundle for manual review. Evidence handling only; artifact contents are unaffected.


### Review entry 0511 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0511. Quarterly access recertification for the routing dashboards closed with one dormant reviewer account disabled; no service principals were touched. The wrapper-script drill completed inside its budget; the runbook timing stands with no change requested.
Historical CSV exports remain archived and non-authoritative for the JSON compiler acceptance.

### Review entry 0512 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0512. A typo fix in the contract reference doc was merged; reviewers confirmed it altered prose only, not any key set.
Thread archived; see the CAB decision entries for anything affecting compile behavior.

### Review entry 0513 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0513. The ops channel piloted a weekly digest of CAB decisions; the pilot continues through quarter end.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0514 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0514. The board reconfirmed that lane-local experiments must not write to the shared evidence store. Log-retention verification confirmed the ninety-day tier is intact; nothing in the compile path reads beyond thirty days.
Filed for context only; the authoritative record for compile behavior stays with the CAB tickets.

### Review entry 0515 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0515. Capacity review noted outage-record volume trending up week over week; the board declined to adjust anything outside the CAB process.
Nothing in this window altered thresholds, priority, or ordering; those remain governed by the ticketed decisions.

### Review entry 0516 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0516. An audit pass matched queue artifacts against their recorded signatures; no mismatches were observed.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0517 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0517. Two junior reviewers completed shadowing rotations and joined the secondary review pool. The wrapper-script drill completed inside its budget; the runbook timing stands with no change requested.
Historical CSV exports remain archived and non-authoritative for the JSON compiler acceptance.

### Review entry 0518 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0518. The wrapper-script drill completed inside its budget; the runbook timing stands with no change requested.
Thread archived; see the CAB decision entries for anything affecting compile behavior.

### Review entry 0519 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0519. Backlog grooming closed five informational tickets referencing the pre-rollout compiler; none carried behavior decisions.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0520 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0520. A staleness monitor was tuned to stop double-paging when a dashboard refresh overlaps a deploy. Log-retention verification confirmed the ninety-day tier is intact; nothing in the compile path reads beyond thirty days.
Filed for context only; the authoritative record for compile behavior stays with the CAB tickets.

### Review entry 0521 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0521. Change-window grooming returned three stale exception approvals to their owners for re-justification before the next cycle.
Nothing in this window altered thresholds, priority, or ordering; those remain governed by the ticketed decisions.

### Review entry 0522 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0522. A drill prep note asked lanes to verify their escalation trees before the Q2 exercise; four lanes confirmed same day.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0523 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0523. The drill scribe rotated per the roster; minutes were filed the same business day. The wrapper-script drill completed inside its budget; the runbook timing stands with no change requested.
Historical CSV exports remain archived and non-authoritative for the JSON compiler acceptance.

### Review entry 0524 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0524. A status-page webhook flapped once during the window; the retry queue absorbed it and no routing decision was involved.
Thread archived; see the CAB decision entries for anything affecting compile behavior.

### Review entry 0525 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0525. Pager noise stayed within the SLO; the single page during the window was acknowledged inside four minutes.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0526 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0526. A stale wiki bookmark still pointed at deprecated compiler notes; the link was retired. Log-retention verification confirmed the ninety-day tier is intact; nothing in the compile path reads beyond thirty days.
Filed for context only; the authoritative record for compile behavior stays with the CAB tickets.

### Review entry 0527 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0527. The on-call handoff template gained a checklist row for confirming the responder dashboard is live before accepting the rotation.
Nothing in this window altered thresholds, priority, or ordering; those remain governed by the ticketed decisions.

### Review entry 0528 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0528. The dashboard TLS certificate was rotated ahead of expiry; tiles rendered stale for one refresh and recovered without intervention.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.


## Q2 Tabletop Exercise — Minutes (2026-06-04)
The quarterly tabletop walked the outage-to-responder path end to end with the compiler treated as a black box: a synthetic outage burst was injected into a staging replica and each lane's on-call narrated their actions from the artifacts alone. Facilitators stopped the clock four times. The first stop tested whether responders could distinguish a suppressed window from a queued one using only the queue artifact and the runbook; every lane answered correctly, though two took over five minutes, and the board asked for a one-page reading guide rather than any change to the artifacts. The second stop simulated a stale dashboard during an active page; the on-call correctly fell back to the queue file on disk, noted as intended behavior since the dashboard is a projection, never the record. The third stop was a deliberately misrouted escalation where the paged lane did not own the affected service; the handoff completed in under two minutes using the escalation tree verified in prep. The final stop rehearsed evidence preservation: responders exported the queue and summary artifacts, recorded their signatures in the incident channel, and confirmed the frozen snapshot remained untouched. Action items: publish the reading guide, add the signature-recording step to the runbook appendix, and repeat with the secondary pool as primary. The board minuted explicitly that no action item touches compile behavior; all semantics remain exactly as ticketed.


> **Change-review decision (2026-06-03 - CAB-2262)** Dana: quarterly access recertification for the routing path samples service-to-service grants at twice the standard rate through year end. Access policy; no compiler impact.
> **Change-review decision (2026-05-30 - CAB-2264)** Marta: degrade probe rounding, and the rounding map of record. The SEVERITY-scoped half of the degrade probe now ROUNDS UP (ceiling) while the all-scoped half keeps its floor: `degrade_pressure_score = (degrade_all_probe_ms // 34) + ceil(degrade_severity_probe_ms / 23) + degrade_segment_count`. In integer arithmetic ceil(x/23) is -(-x // 23). This revises the floored `degrade_severity_probe_ms // 23` written in CAB-2227, which is superseded on this point only: the probe range [end_ms-210, end_ms+1), the divisors 34 and 23, the all-scoped floor and the segment term are unchanged. This entry also supersedes CAB-2250 as the rounding map of record: rounding remains NON-uniform and no divisor's direction may be inferred from any other, but the degrade probe no longer stays floored on both halves — only the handoff probe does. Read each divisor's direction from its own governing decision.


### Review entry 0529 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0529. Log-retention verification confirmed the ninety-day tier is intact; nothing in the compile path reads beyond thirty days. The wrapper-script drill completed inside its budget; the runbook timing stands with no change requested.
Historical CSV exports remain archived and non-authoritative for the JSON compiler acceptance.

### Review entry 0530 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0530. Metrics ingest lagged for nine minutes during the collector restart; window math was unaffected because the compiler reads recorded outage times, not ingest times.
Thread archived; see the CAB decision entries for anything affecting compile behavior.

### Review entry 0531 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0531. Retention sampling of archived queue artifacts passed spot audit; one bundle was re-indexed for slow retrieval.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0532 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0532. A reviewer flagged two chat excerpts that contradicted a ticketed decision; the thread was annotated to point at the ticket as authoritative. Log-retention verification confirmed the ninety-day tier is intact; nothing in the compile path reads beyond thirty days.
Filed for context only; the authoritative record for compile behavior stays with the CAB tickets.

### Review entry 0533 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0533. Quarterly access recertification for the routing dashboards closed with one dormant reviewer account disabled; no service principals were touched.
Nothing in this window altered thresholds, priority, or ordering; those remain governed by the ticketed decisions.

### Review entry 0534 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0534. A typo fix in the contract reference doc was merged; reviewers confirmed it altered prose only, not any key set.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0535 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0535. The ops channel piloted a weekly digest of CAB decisions; the pilot continues through quarter end. The wrapper-script drill completed inside its budget; the runbook timing stands with no change requested.
Historical CSV exports remain archived and non-authoritative for the JSON compiler acceptance.

### Review entry 0536 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0536. The board reconfirmed that lane-local experiments must not write to the shared evidence store.
Thread archived; see the CAB decision entries for anything affecting compile behavior.

### Review entry 0537 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0537. Capacity review noted outage-record volume trending up week over week; the board declined to adjust anything outside the CAB process.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0538 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0538. An audit pass matched queue artifacts against their recorded signatures; no mismatches were observed. Log-retention verification confirmed the ninety-day tier is intact; nothing in the compile path reads beyond thirty days.
Filed for context only; the authoritative record for compile behavior stays with the CAB tickets.

### Review entry 0539 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0539. Two junior reviewers completed shadowing rotations and joined the secondary review pool.
Nothing in this window altered thresholds, priority, or ordering; those remain governed by the ticketed decisions.

### Review entry 0540 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0540. The wrapper-script drill completed inside its budget; the runbook timing stands with no change requested.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0541 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0541. Backlog grooming closed five informational tickets referencing the pre-rollout compiler; none carried behavior decisions. The wrapper-script drill completed inside its budget; the runbook timing stands with no change requested.
Historical CSV exports remain archived and non-authoritative for the JSON compiler acceptance.

### Review entry 0542 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0542. A staleness monitor was tuned to stop double-paging when a dashboard refresh overlaps a deploy.
Thread archived; see the CAB decision entries for anything affecting compile behavior.

### Review entry 0543 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0543. Change-window grooming returned three stale exception approvals to their owners for re-justification before the next cycle.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0544 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0544. A drill prep note asked lanes to verify their escalation trees before the Q2 exercise; four lanes confirmed same day. Log-retention verification confirmed the ninety-day tier is intact; nothing in the compile path reads beyond thirty days.
Filed for context only; the authoritative record for compile behavior stays with the CAB tickets.

### Review entry 0545 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0545. The drill scribe rotated per the roster; minutes were filed the same business day.
Nothing in this window altered thresholds, priority, or ordering; those remain governed by the ticketed decisions.

### Review entry 0546 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0546. A status-page webhook flapped once during the window; the retry queue absorbed it and no routing decision was involved.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.


## Access Review Appendix — 2026-06 Cycle
The June access review covered every principal with write access to the routing path. The rollout-era automation account remained disabled with credentials expired and no login attempts since containment; the artifact bucket's writer list matched the roster after one contractor account was removed at engagement end; the dashboard service account retained read-only scopes with token rotation verified against the ninety-day policy; and the break-glass account passed its quarterly seal check, countersigned by two leads. One follow-up: a legacy CI role carried a stale policy attachment referencing the pre-rollout compiler path — no active trust relationships, removed same day through the standard change process. Ten sampled permission grants from the quarter all carried ticket references and approver signatures. The board accepted the appendix without dissent and doubled the service-to-service sampling rate for next cycle as a precaution following the rollout incident. Nothing in this appendix modifies how the compiler computes, admits, or orders responder work.


> **Change-review decision (2026-06-06 - CAB-2249)** Ilya: the weekly CAB digest becomes a standing publication with a superseded-by column. Communications practice only; the ticketed decisions remain the sole authority on compile behavior.


### Review entry 0547 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0547. Pager noise stayed within the SLO; the single page during the window was acknowledged inside four minutes. The wrapper-script drill completed inside its budget; the runbook timing stands with no change requested.
Historical CSV exports remain archived and non-authoritative for the JSON compiler acceptance.

### Review entry 0548 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0548. A stale wiki bookmark still pointed at deprecated compiler notes; the link was retired.
Thread archived; see the CAB decision entries for anything affecting compile behavior.

### Review entry 0549 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0549. The on-call handoff template gained a checklist row for confirming the responder dashboard is live before accepting the rotation.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0550 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0550. The dashboard TLS certificate was rotated ahead of expiry; tiles rendered stale for one refresh and recovered without intervention. Log-retention verification confirmed the ninety-day tier is intact; nothing in the compile path reads beyond thirty days.
Filed for context only; the authoritative record for compile behavior stays with the CAB tickets.

### Review entry 0551 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0551. Log-retention verification confirmed the ninety-day tier is intact; nothing in the compile path reads beyond thirty days.
Nothing in this window altered thresholds, priority, or ordering; those remain governed by the ticketed decisions.

### Review entry 0552 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0552. Metrics ingest lagged for nine minutes during the collector restart; window math was unaffected because the compiler reads recorded outage times, not ingest times.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0553 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0553. Retention sampling of archived queue artifacts passed spot audit; one bundle was re-indexed for slow retrieval. The wrapper-script drill completed inside its budget; the runbook timing stands with no change requested.
Historical CSV exports remain archived and non-authoritative for the JSON compiler acceptance.

### Review entry 0554 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0554. A reviewer flagged two chat excerpts that contradicted a ticketed decision; the thread was annotated to point at the ticket as authoritative.
Thread archived; see the CAB decision entries for anything affecting compile behavior.

### Review entry 0555 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0555. Quarterly access recertification for the routing dashboards closed with one dormant reviewer account disabled; no service principals were touched.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0556 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0556. A typo fix in the contract reference doc was merged; reviewers confirmed it altered prose only, not any key set. Log-retention verification confirmed the ninety-day tier is intact; nothing in the compile path reads beyond thirty days.
Filed for context only; the authoritative record for compile behavior stays with the CAB tickets.

### Review entry 0557 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0557. The ops channel piloted a weekly digest of CAB decisions; the pilot continues through quarter end.
Nothing in this window altered thresholds, priority, or ordering; those remain governed by the ticketed decisions.

### Review entry 0558 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0558. The board reconfirmed that lane-local experiments must not write to the shared evidence store.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0559 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0559. Capacity review noted outage-record volume trending up week over week; the board declined to adjust anything outside the CAB process. The wrapper-script drill completed inside its budget; the runbook timing stands with no change requested.
Historical CSV exports remain archived and non-authoritative for the JSON compiler acceptance.

### Review entry 0560 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0560. An audit pass matched queue artifacts against their recorded signatures; no mismatches were observed.
Thread archived; see the CAB decision entries for anything affecting compile behavior.

### Review entry 0561 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0561. Two junior reviewers completed shadowing rotations and joined the secondary review pool.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0562 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0562. The wrapper-script drill completed inside its budget; the runbook timing stands with no change requested. Log-retention verification confirmed the ninety-day tier is intact; nothing in the compile path reads beyond thirty days.
Filed for context only; the authoritative record for compile behavior stays with the CAB tickets.

### Review entry 0563 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0563. Backlog grooming closed five informational tickets referencing the pre-rollout compiler; none carried behavior decisions.
Nothing in this window altered thresholds, priority, or ordering; those remain governed by the ticketed decisions.

### Review entry 0564 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0564. A staleness monitor was tuned to stop double-paging when a dashboard refresh overlaps a deploy.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.


### Review entry 0565 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0565. Change-window grooming returned three stale exception approvals to their owners for re-justification before the next cycle. The wrapper-script drill completed inside its budget; the runbook timing stands with no change requested.
Historical CSV exports remain archived and non-authoritative for the JSON compiler acceptance.

### Review entry 0566 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0566. A drill prep note asked lanes to verify their escalation trees before the Q2 exercise; four lanes confirmed same day.
Thread archived; see the CAB decision entries for anything affecting compile behavior.

### Review entry 0567 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0567. The drill scribe rotated per the roster; minutes were filed the same business day.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0568 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0568. A status-page webhook flapped once during the window; the retry queue absorbed it and no routing decision was involved. Log-retention verification confirmed the ninety-day tier is intact; nothing in the compile path reads beyond thirty days.
Filed for context only; the authoritative record for compile behavior stays with the CAB tickets.

### Review entry 0569 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0569. Pager noise stayed within the SLO; the single page during the window was acknowledged inside four minutes.
Nothing in this window altered thresholds, priority, or ordering; those remain governed by the ticketed decisions.

### Review entry 0570 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0570. A stale wiki bookmark still pointed at deprecated compiler notes; the link was retired.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0571 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0571. The on-call handoff template gained a checklist row for confirming the responder dashboard is live before accepting the rotation. The wrapper-script drill completed inside its budget; the runbook timing stands with no change requested.
Historical CSV exports remain archived and non-authoritative for the JSON compiler acceptance.

### Review entry 0572 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0572. The dashboard TLS certificate was rotated ahead of expiry; tiles rendered stale for one refresh and recovered without intervention.
Thread archived; see the CAB decision entries for anything affecting compile behavior.

### Review entry 0573 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0573. Log-retention verification confirmed the ninety-day tier is intact; nothing in the compile path reads beyond thirty days.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0574 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0574. Metrics ingest lagged for nine minutes during the collector restart; window math was unaffected because the compiler reads recorded outage times, not ingest times. Log-retention verification confirmed the ninety-day tier is intact; nothing in the compile path reads beyond thirty days.
Filed for context only; the authoritative record for compile behavior stays with the CAB tickets.

### Review entry 0575 — auth lane
Shift lead logged routine rollout observation for auth (east) during review window 0575. Retention sampling of archived queue artifacts passed spot audit; one bundle was re-indexed for slow retrieval.
Nothing in this window altered thresholds, priority, or ordering; those remain governed by the ticketed decisions.

### Review entry 0576 — billing lane
Shift lead logged routine rollout observation for billing (west) during review window 0576. A reviewer flagged two chat excerpts that contradicted a ticketed decision; the thread was annotated to point at the ticket as authoritative.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.

### Review entry 0577 — checkout lane
Shift lead logged routine rollout observation for checkout (central) during review window 0577. Quarterly access recertification for the routing dashboards closed with one dormant reviewer account disabled; no service principals were touched. The wrapper-script drill completed inside its budget; the runbook timing stands with no change requested.
Historical CSV exports remain archived and non-authoritative for the JSON compiler acceptance.

### Review entry 0578 — edge lane
Shift lead logged routine rollout observation for edge (west) during review window 0578. A typo fix in the contract reference doc was merged; reviewers confirmed it altered prose only, not any key set.
Thread archived; see the CAB decision entries for anything affecting compile behavior.

### Review entry 0579 — inventory lane
Shift lead logged routine rollout observation for inventory (east) during review window 0579. The ops channel piloted a weekly digest of CAB decisions; the pilot continues through quarter end.
No compiler semantics were changed in this entry; parameters remain as approved by the change board.

### Review entry 0580 — ledger lane
Shift lead logged routine rollout observation for ledger (central) during review window 0580. The board reconfirmed that lane-local experiments must not write to the shared evidence store. Log-retention verification confirmed the ninety-day tier is intact; nothing in the compile path reads beyond thirty days.
Filed for context only; the authoritative record for compile behavior stays with the CAB tickets.

### Review entry 0581 — notifications lane
Shift lead logged routine rollout observation for notifications (north) during review window 0581. Capacity review noted outage-record volume trending up week over week; the board declined to adjust anything outside the CAB process.
Nothing in this window altered thresholds, priority, or ordering; those remain governed by the ticketed decisions.

### Review entry 0582 — search lane
Shift lead logged routine rollout observation for search (north) during review window 0582. An audit pass matched queue artifacts against their recorded signatures; no mismatches were observed.
Reviewers should reconcile behavior questions against the CAB decision entries rather than chat excerpts.
