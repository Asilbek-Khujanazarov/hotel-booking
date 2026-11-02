using HotelBooking.Rooms;
using HotelBooking.Notifications;
namespace HotelBooking.Reservations;
public class BookingService(IRoomCatalog rooms, IReservationStore store, INotificationSender email, int slowStepMs = 0)
{
    public IReadOnlyList<Room> FindFreeRooms(DateRange stay) => rooms.All().Where(room => !store.HasOverlap(room, stay)).ToArray();
    public BookingResult Reserve(Guest guest, Room room, DateRange stay)
    {
        if (!stay.IsValid()) return new("InvalidDates");
        if (store.HasOverlap(room, stay)) return new("Unavailable");
        Thread.Sleep(slowStepMs); // P03 race: another request can check before we save.
        var reservation = new Reservation($"R{101 + store.Count}", guest, room, stay);
        store.Save(reservation);
        try { email.SendConfirmation(new Confirmation(reservation.Id, guest.Email, room.Number, stay.CheckIn, stay.CheckOut)); }
        catch (Exception) { /* R6: saved booking remains confirmed. */ }
        return new("Accepted", reservation.Id);
    }
    public bool Cancel(string id) => store.Find(id)?.Cancel() ?? false;
}


