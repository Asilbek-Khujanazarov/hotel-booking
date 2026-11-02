using HotelBooking.Rooms;
using HotelBooking.Rooms.Internal;
using HotelBooking.Reservations;
using HotelBooking.Reservations.Internal;
using HotelBooking.Notifications.Internal;
using HotelBooking.Payments.Internal;
// P06: only the composition root names implementations from other modules.
_ = new SimulatedPaymentService();
var r7 = new Room("R7", "Standard");
var r8 = new Room("R8", "Deluxe");
var maya = new Guest("Maya", "maya@example.com");
var omar = new Guest("Omar", "omar@example.com");
var nora = new Guest("Nora", "nora@example.com");
var store = new InMemoryReservationStore();
var email = new EmailNotificationSender();
var service = new BookingService(new InMemoryRoomCatalog([r7, r8]), store, email, args.Contains("--race") ? 500 : 0);
if (args.Contains("--race"))
{
    Console.WriteLine("Maya and Omar both book R7 for 12-14 Nov at the same moment...");
    var first = Task.Run(() => service.Reserve(maya, r7, Nov(12, 14)));
    await Task.Delay(100);
    var second = Task.Run(() => service.Reserve(omar, r7, Nov(12, 14)));
    await Task.WhenAll(first, second);
    Console.WriteLine($"Maya: {first.Result}");
    Console.WriteLine($"Omar: {second.Result}");
    var count = store.CountConfirmed(r7, Nov(12, 14));
    Console.WriteLine($"Confirmed reservations for R7 on 12-14 Nov: {count}");
    Console.WriteLine(count > 1 ? "Double booking! Both requests checked before either one saved." : "Only one guest has R7.");
}
else
{
    Console.WriteLine($"Free rooms 12-14 Nov: {Names(service.FindFreeRooms(Nov(12, 14)))}");
    Console.WriteLine($"Maya books R7 12-14 Nov: {service.Reserve(maya, r7, Nov(12, 14))}");
    Console.WriteLine($"Omar books R7 13-15 Nov: {service.Reserve(omar, r7, Nov(13, 15))}");
    Console.WriteLine($"Nora books R7 14-16 Nov: {service.Reserve(nora, r7, Nov(14, 16))}");
    Console.WriteLine($"Omar books R8 15-15 Nov: {service.Reserve(omar, r8, Nov(15, 15))}");
    Console.WriteLine($"Free rooms 12-14 Nov: {Names(service.FindFreeRooms(Nov(12, 14)))}");
    Console.WriteLine($"Maya cancels R101: {service.Cancel("R101")}");
    Console.WriteLine($"Free rooms 12-14 Nov: {Names(service.FindFreeRooms(Nov(12, 14)))}");
    Console.WriteLine($"Confirmation emails sent: {email.Sent}");
}
if (args.Contains("--verify"))
{
    static void Check(bool condition, string message)
    {
        if (!condition) throw new InvalidOperationException(message);
        Console.Error.WriteLine($"PASS: {message}");
    }
    var proofStore = new InMemoryReservationStore();
    var proofEmail = new EmailNotificationSender();
    var proofService = new BookingService(new InMemoryRoomCatalog([r7, r8]), proofStore, proofEmail);
    proofService.Reserve(maya, r7, Nov(12, 14));
    var found = proofStore.Find("R101");
    Check(found is not null && found.Guest == maya && found.Room == r7 && found.Stay == Nov(12, 14) && found.Status == ReservationStatus.Confirmed, "R5: R101 -> Maya, R7, 12-14 November, Confirmed");
    Check(proofStore.Find("missing") is null, "Unknown id returns null");
    Check(proofService.Cancel("R101") && proofStore.Find("R101")!.Status == ReservationStatus.Cancelled, "R4: cancellation retains the record as Cancelled");
    Check(!proofService.Cancel("R101") && !proofService.Cancel("missing"), "Repeated or unknown cancellation returns False");
    Check(proofService.Reserve(omar, r8, Nov(16, 15)).Outcome == "InvalidDates", "R3: reversed dates refused");
    proofService.Reserve(maya, r8, Nov(20, 22));
    Check(proofService.Reserve(omar, r8, Nov(21, 23)).Outcome == "Unavailable", "R3: R8 shared night 21 refused");
    Check(proofService.Reserve(nora, r8, Nov(22, 24)).Outcome == "Accepted", "R3: R8 adjacent stay accepted");
}
static DateRange Nov(int start, int end) => new(new(2026, 11, start), new(2026, 11, end));
static string Names(IReadOnlyList<Room> rooms) => string.Join(", ", rooms.Select(r => r.Number));

