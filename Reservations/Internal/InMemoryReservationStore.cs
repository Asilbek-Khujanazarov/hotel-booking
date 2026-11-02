using HotelBooking.Rooms;
using HotelBooking.Reservations;
namespace HotelBooking.Reservations.Internal;
public class InMemoryReservationStore : IReservationStore
{
    private readonly List<Reservation> rows = [];
    // Protect list operations only. HasOverlap + Save remains non-atomic on purpose.
    private readonly object gate = new();
    public int Count { get { lock (gate) return rows.Count; } }
    public bool HasOverlap(Room room, DateRange stay) { lock (gate) return rows.Any(r => r.Blocks(room, stay)); }
    public void Save(Reservation reservation) { lock (gate) rows.Add(reservation); }
    public Reservation? Find(string id) { lock (gate) return rows.Find(r => r.Id == id); }
    public int CountConfirmed(Room room, DateRange stay) { lock (gate) return rows.Count(r => r.Blocks(room, stay)); }
}
