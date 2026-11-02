# Requirements: hotel booking app, version 1

Source: https://teaching.ultimerinc.com/#/P03/welcome
Dates are half-open: check-in included, check-out excluded. All examples use November 2026.

## R1 · Search
A guest or receptionist can list the rooms that are free for given dates.
Check: empty hotel, 12–14 November → R7, R8.
Proof: `Free rooms 12-14 Nov: R7, R8`

## R2 · Book
A guest or receptionist can book a free room. The app answers with a reservation id.
Check: Maya books R7 for 12–14 November → Accepted R101.
Proof: `Maya books R7 12-14 Nov: Accepted R101`

## R3 · No clash
A room never has two Confirmed bookings on the same night. Check-out must be after check-in.
Check: Omar asks for R7 on 13–15 → Unavailable. 15–15 → InvalidDates.
More examples:
- Maya R7 12–14 → Confirmed; occupies nights 12 and 13.
- Omar R7 13–15 → Unavailable; shares night 13 with Maya.
- Nora R7 14–16 → Accepted; check-out day is free.
- R8 already booked 20–22; request 22–24 → Accepted; no shared night.
- R8 already booked 20–22; request 21–23 → Unavailable; shares night 21.
Proof: `Omar books R7 13-15 Nov: Unavailable`
Proof: `Nora books R7 14-16 Nov: Accepted R102`
Proof: `Omar books R8 15-15 Nov: InvalidDates`
Limitation: sequential requests meet R3. `--race` intentionally demonstrates that overlapping requests break it. P09 provides the database fix.

## R4 · Cancel
A booking can be cancelled. It is kept as Cancelled and no longer blocks the room.
Check: Maya cancels R101 → R7 is free again for 12–14.
Proof: `Maya cancels R101: True`, followed by `Free rooms 12-14 Nov: R7, R8`.
The record remains accessible through ReservationStore.Find; Cancel never deletes it.

## R5 · View
A booking can be looked up by its id.
Check: R101 → Maya, R7, 12–14 November, Confirmed (before cancellation).
Proof: ReservationStore.Find("R101") returns that saved object; see `docs/verification.txt` for the executed R5 check.

## Scope
In-memory console app only. Prices, payments, invoices, logins, housekeeping, HTTP and PostgreSQL are outside P03.

## R6 · Notification failure
If confirmation delivery fails after saving, the booking stays Confirmed and the caller still gets Accepted.
Check: injected sender throws; booking can be found and another overlapping request is refused.
Proof: BookingServiceTests.Notification_failure_keeps_confirmed_booking.
