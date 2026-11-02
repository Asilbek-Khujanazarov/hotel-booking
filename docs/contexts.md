# Bounded contexts · P05

## Words
Room, room number, room type, nightly price, out of service, Guest, Stay, check-in, check-out, Reservation, Confirmed, Cancelled, Deposit, Paid, Declined, Refund, Confirmation, Sent, Failed.

## Rooms
Job: catalog of physical rooms, type, nightly price and operational availability.
Room means the physical room and its descriptive data. Owns room number, type, price and out-of-service information. Public contract: IRoomCatalog and Room. In P06 catalog returns R7/Standard and R8/Deluxe; price and maintenance are design vocabulary for future changes.
Needs no other context. Other modules must not read its internal catalog.

## Reservations
Job: decide whether a guest gets a room for nights and retain all reservations.
Stay means [check-in, check-out); Reservation means id + Guest + Room + Stay + status. Confirmed means the nights are promised; Cancelled withdraws that promise, without deleting history.
Owns date validity, overlap and booking status. Uses Rooms contract and sends a Notifications-owned Confirmation. The rule against two confirmed reservations sharing a night belongs here; concurrent enforcement remains unfinished until P09.

## Payments
Job: collect a deposit and track payment/refund outcomes.
Deposit means 30% of the stay price; Paid means money was accepted, not that the room is necessarily confirmed. Declined means payment failed. Public contract: IPaymentService.TakeDeposit(stayPrice), PaymentStatus (Paid/Declined). P06 has a simulated service only; Reserve does not charge money.

## Notifications
Job: tell the guest what happened using email or SMS.
Confirmation is a message containing reservation id, guest email, room number, check-in and check-out. Sent means delivery was attempted successfully by this sender; it is not a booking status. Public contract: INotificationSender.SendConfirmation(Confirmation). Owns provider and transport selection. Does not import Reservation.

## Same word, different meaning
| Word | Meaning by context |
|---|---|
| Room | Rooms: physical catalog entry; Reservations: the room referenced by a promise for nights |
| Cancel | Reservations: withdraw the promise; Payments: refund money under payment rules; Notifications: communicate the change |
| Confirmed / Paid / Sent | Independent statuses for a booking, a payment and a message; none automatically implies the other two |

## Rule owners
| Rule card | Owner | Reason |
|---|---|---|
| Room number/type | Rooms | Catalog identity and description |
| Nightly price | Rooms | Price belongs to room offering |
| Room out of service | Rooms | Operational room availability |
| Check-out after check-in | Reservations | Defines a valid stay |
| No two Confirmed reservations sharing a night | Reservations | Has all promises and their dates |
| Deposit is 30% | Payments | Money calculation and collection policy |
| Payment/refund status | Payments | Financial lifecycle differs from booking lifecycle |
| Email/SMS delivery and failures | Notifications | Provider details must not spread into booking rules |

## Between contexts
| Caller → owner | Contract/message | Fields/result |
|---|---|---|
| Reservations → Rooms | IRoomCatalog.All() | IReadOnlyList<Room>: Number, Type (P06) |
| Reservations → Notifications | SendConfirmation(Confirmation) | ReservationId, GuestEmail, RoomNumber, CheckIn, CheckOut; may throw; R6 keeps saved booking |
| Reservations → Payments | TakeDeposit(stayPrice), future use | decimal total stay price → Paid/Declined; simulated contract exists, no Reserve integration yet |
| Payments → Rooms | Price lookup, future design | Room number → nightly price; not implemented in P06 |

Only public contracts cross module borders. Private storage is owned by the module. Diagrams label planned dependencies separately from current code. P06 adds architecture checks; P07 later replaces the reservation storage adapter.
