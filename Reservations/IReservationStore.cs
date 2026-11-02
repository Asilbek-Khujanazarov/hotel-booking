using HotelBooking.Rooms;
using HotelBooking.Notifications;
namespace HotelBooking.Reservations;
public interface IReservationStore { int Count { get; } bool HasOverlap(Room room, DateRange stay); void Save(Reservation reservation); Reservation? Find(string id); int CountConfirmed(Room room, DateRange stay); }
