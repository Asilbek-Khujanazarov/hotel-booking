# P03 design notes

## Why design before code
Low-level design decides which classes exist, what data and methods they keep, and which classes call each other. One overlap rule in DateRange avoids inconsistent website and reception rules.

## Where the methods live
- DateRange.IsValid and Overlaps own the date calculations.
- Reservation.Blocks combines room, Confirmed status and overlapping nights; Cancel changes its own status.
- ReservationStore.HasOverlap searches saved reservations; Save and Find keep and retrieve them.
- BookingService.FindFreeRooms, Reserve and Cancel coordinate a request.
- EmailSender.SendConfirmation simulates confirmation delivery.
Guest and Receptionist are both actors. When Nora phones, Receptionist operates the app; Nora is the stored guest.
Reservation refers to an independently existing Room and Guest, and owns its stay DateRange. The store keeps zero or many reservations.

## Activity traces
- Omar, R7, 13–15 while Maya has 12–14: valid dates Yes; overlap Yes (night 13); Unavailable, nothing saved.
- Nora, R7, 14–16: valid dates Yes; overlap No; save Confirmed, send confirmation, Accepted R102.
- Omar, R8, 15–15: valid dates No; InvalidDates, no overlap check, no save or email.

## Prediction
Nora gets Accepted R102: Maya checks out on the 14th and Nora checks in on the 14th, so they share no night. The normal run matched this prediction.

## The race
Prediction: two Confirmed reservations for R7 on 12–14.
Both requests call HasOverlap before either saves, so both receive false and both are accepted. The gap is between ReservationStore.HasOverlap and ReservationStore.Save in Reserve; a safe list operation does not make the combined business operation atomic.
The race is intentionally retained for P09. The 500 ms delay is a teaching simulation, not a measured production latency.

## P03 checklist
- R1–R5 have Check and Proof lines; R3 has five examples.
- Five editable draw.io pages: Use cases, Classes, Sequence - book, Sequence - cancel, Activity - book.
- Normal console run: nine expected lines. Race run: double booking reproduced.
- This existing project stays at the repository root; run commands name its actual csproj.

# P04 design notes

BookingService previously depended on concrete list storage and EmailSender (DIP violation), and provider changes required editing the booking use case (OCP). Interfaces IReservationStore and INotificationSender now describe the small promises it needs. SRP separates booking coordination, date rules, storage and message delivery. LSP requires every sender to obey the same success/failure promise; ISP avoids combining storage and notification operations in one broad interface.

R6 is an intentional new rule: a sender exception after Save does not undo the reservation. The fake sender makes this reproducible without network access. SMS can replace email through composition, without BookingService changes. Cancel retains history.

The six original behaviour examples cover search, book/view, overlap, adjacent stays, invalid dates and cancel; two further checks cover failed notification and replaceable sender. The normal nine lines remain the same. Refactoring alone does not make HasOverlap + Save atomic; race remains.

# P06 design notes

Rooms owns Room and IRoomCatalog; internal InMemoryRoomCatalog stores the list. Reservations owns date rules, reservations, the booking service and reservation store contract. Notifications owns Confirmation so its senders no longer import Reservation. Payments has IPaymentService, Paid/Declined and a simulated implementation; it is not wired into the booking workflow.

Program.cs is the composition root. Tests may instantiate implementations. The three architecture checks forbid Reservations from reaching other internals, Rooms from depending on the other modules, and Payments/Notifications from depending on Reservations.

Break-on-purpose exercise: temporarily add a concrete EmailNotificationSender dependency to BookingService, run the architecture test, capture the failure, then restore the code and run all checks again. See architecture-red.txt and p06-tests.txt for actual results.

The normal nine lines are compared against P04 output. The race remains demonstrable because HasOverlap and Save are still separate. Module boundaries improve change safety; they do not provide transactional correctness. Future P07 replaces the storage adapter and adds HTTP, when requested.

## Final execution evidence
P04: standard dotnet test ran 8 tests successfully. P06: all 11 existing xUnit Facts passed via tools/TestRunner because standard testhost could not connect in this environment. NetArchTest found the deliberately injected concrete notification dependency (10 pass / 1 fail); after undoing it, all 11 passed. This demonstrates that the boundary checks execute rather than merely compiling. P04 and P06 normal demo output files compare identically. The final race still has 2 Confirmed reservations as required by this stage.
