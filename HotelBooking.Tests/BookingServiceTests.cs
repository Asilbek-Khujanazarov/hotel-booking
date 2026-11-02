using HotelBooking.Rooms;
using HotelBooking.Rooms.Internal;
using HotelBooking.Reservations;
using HotelBooking.Reservations.Internal;
using HotelBooking.Notifications.Internal;
using HotelBooking.Payments.Internal;
using HotelBooking.Notifications;
using Xunit;
namespace HotelBooking.Tests;
public class BookingServiceTests
{
    private static readonly Room R7 = new("R7", "Standard"), R8 = new("R8", "Deluxe");
    private static readonly Guest Maya = new("Maya", "maya@example.com");
    private static DateRange Nov(int a, int b) => new(new(2026,11,a), new(2026,11,b));
    private readonly InMemoryReservationStore store = new();
    private BookingService Service(INotificationSender? sender = null) => new(new InMemoryRoomCatalog([R7,R8]), store, sender ?? new FakeSender());
    [Fact] public void Empty_hotel_lists_both_rooms() => Assert.Equal(new[]{R7,R8},Service().FindFreeRooms(Nov(12,14)));
    [Fact] public void Accepted_booking_can_be_viewed_by_id()
    { var s=Service();var result=s.Reserve(Maya,R7,Nov(12,14));Assert.Equal("Accepted",result.Outcome);var r=store.Find(result.ReservationId!)!;Assert.Equal(Maya,r.Guest);Assert.Equal(R7,r.Room);Assert.Equal(Nov(12,14),r.Stay);Assert.Equal(ReservationStatus.Confirmed,r.Status);Assert.DoesNotContain(R7,s.FindFreeRooms(Nov(12,14))); }
    [Fact] public void Overlapping_booking_is_refused_without_saving()
    { var s=Service();s.Reserve(Maya,R7,Nov(12,14));Assert.Equal("Unavailable",s.Reserve(Maya,R7,Nov(13,15)).Outcome);Assert.Equal(1,store.Count); }
    [Fact] public void Checkout_day_can_be_next_checkin()
    {var s=Service();s.Reserve(Maya,R7,Nov(12,14));Assert.Equal("Accepted",s.Reserve(Maya,R7,Nov(14,16)).Outcome);}
    [Fact] public void Invalid_dates_save_nothing()
    {var s=Service();Assert.Equal("InvalidDates",s.Reserve(Maya,R8,Nov(15,15)).Outcome);Assert.Equal("InvalidDates",s.Reserve(Maya,R8,Nov(16,15)).Outcome);Assert.Equal(0,store.Count);}
    [Fact] public void Cancel_retains_history_and_releases_room()
    {var s=Service();var id=s.Reserve(Maya,R7,Nov(12,14)).ReservationId!;Assert.True(s.Cancel(id));Assert.Equal(ReservationStatus.Cancelled,store.Find(id)!.Status);Assert.Contains(R7,s.FindFreeRooms(Nov(12,14)));Assert.False(s.Cancel(id));Assert.False(s.Cancel("missing"));}
    [Fact] public void Notification_failure_keeps_confirmed_booking()
    {var s=Service(new FakeSender(true));var r=s.Reserve(Maya,R7,Nov(12,14));Assert.Equal("Accepted",r.Outcome);Assert.Equal(ReservationStatus.Confirmed,store.Find(r.ReservationId!)!.Status);Assert.Equal("Unavailable",s.Reserve(Maya,R7,Nov(12,14)).Outcome);}
    [Fact] public void Sender_can_be_swapped_without_changing_booking_service()
    {var fake=new FakeSender();var s=Service(fake);var result=s.Reserve(Maya,R7,Nov(12,14));Assert.Equal(result.ReservationId,Assert.Single(fake.Sent).ReservationId);var sms=new SmsNotificationSender();Assert.Equal("Accepted",Service(sms).Reserve(Maya,R8,Nov(12,14)).Outcome);Assert.Equal(1,sms.Sent);}
    private sealed class FakeSender(bool fail=false) : INotificationSender
    {public List<Confirmation> Sent {get;}=[];public void SendConfirmation(Confirmation r){if(fail)throw new InvalidOperationException("Simulated provider failure");Sent.Add(r);}}
}
