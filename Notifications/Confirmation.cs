
namespace HotelBooking.Notifications;
public sealed record Confirmation(string ReservationId, string GuestEmail, string RoomNumber, DateOnly CheckIn, DateOnly CheckOut);
