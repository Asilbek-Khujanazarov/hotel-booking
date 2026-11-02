using HotelBooking.Rooms;
using HotelBooking.Notifications;
namespace HotelBooking.Reservations;
public record DateRange(DateOnly CheckIn, DateOnly CheckOut)
{
    public bool IsValid() => CheckOut > CheckIn;
    public bool Overlaps(DateRange other) => CheckIn < other.CheckOut && other.CheckIn < CheckOut;
}
