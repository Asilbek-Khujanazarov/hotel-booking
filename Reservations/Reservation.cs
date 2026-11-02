using HotelBooking.Rooms;
using HotelBooking.Notifications;
namespace HotelBooking.Reservations;
public class Reservation(string id, Guest guest, Room room, DateRange stay)
{
    public string Id { get; } = id;
    public Guest Guest { get; } = guest;
    public Room Room { get; } = room;
    public DateRange Stay { get; } = stay;
    public ReservationStatus Status { get; private set; } = ReservationStatus.Confirmed;
    public bool Blocks(Room requestedRoom, DateRange requestedStay) => Status == ReservationStatus.Confirmed && Room == requestedRoom && Stay.Overlaps(requestedStay);
    public bool Cancel()
    {
        if (Status == ReservationStatus.Cancelled) return false;
        Status = ReservationStatus.Cancelled;
        return true;
    }
}
