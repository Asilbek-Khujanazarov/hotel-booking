# Quality scenarios · P05

Stakeholders: guests need correct booking results; reception needs a shared booking history; hotel manager needs dependable operation and manageable cost; developers need safe changes; operations needs a simple release; email/SMS providers can fail.

These are proposed acceptance targets, not measured production results.

| ID | Stimulus and environment | Response | Measure and proof plan |
|---|---|---|---|
| S1 Performance | Guest searches during a peak of 200 searches/minute | Return available rooms | p95 < 500 ms; benchmark later in P08. No production measurement claimed. |
| S2 Correctness | Two guests concurrently request the same room and nights | Accept at most one | Exactly 1 Confirmed reservation; currently FAILED by the P03 race, database repair in P09. |
| S3 Reliability | Notification provider throws after saving | Keep booking and return Accepted | 1 saved Confirmed booking; passing failure test. |
| S4 Modifiability | Hotel switches email to SMS | Replace sender through contract | Zero BookingService edits; existing 8 behaviour tests stay green. |
| S5 Operability | Small team releases a module change | Deploy the application together | One build and one deployment; architecture checks guard boundaries. |
| S6 Sustainability | 1,000 identical searches for the same dates | Reduce unnecessary database work | Target <= 2 DB queries with cache in P08 instead of 2,000; estimate only, no DB/cache in P06. |

Priority: S2 then S3. Boundaries concentrate booking correctness in Reservations and isolate notification failure. A modular monolith reduces operational overhead while this is one small team. Architectural structure alone does not fix S2.
