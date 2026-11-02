using HotelBooking.Notifications;
namespace HotelBooking.Notifications.Internal;
public class EmailNotificationSender : INotificationSender
{
    private int sent;
    public int Sent => sent;
    // Simulation: no real emails or network requests.
    public void SendConfirmation(Confirmation confirmation) => Interlocked.Increment(ref sent);
}
