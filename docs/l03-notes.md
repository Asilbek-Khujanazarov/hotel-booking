# L03 notes

1. Reservations owns the booking rule because it sees the room's reservations and overlapping nights.
2. Reservations must not instantiate EmailNotificationSender; it uses INotificationSender with a Notifications-owned Confirmation.
3. One team and one release rhythm favour a modular monolith; revisit if measured needs require independent releases or scaling.
