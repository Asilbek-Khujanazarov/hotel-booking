using HotelBooking.Rooms;
namespace HotelBooking.Rooms.Internal;
public sealed class InMemoryRoomCatalog(IReadOnlyList<Room> rooms) : IRoomCatalog { public IReadOnlyList<Room> All() => rooms.ToArray(); }
