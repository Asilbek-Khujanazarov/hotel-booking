using HotelBooking.Rooms;
using HotelBooking.Notifications;
namespace HotelBooking.Reservations;
public record BookingResult(string Outcome, string? ReservationId = null)
{
    public override string ToString() => ReservationId is null ? Outcome : $"{Outcome} {ReservationId}";
}
