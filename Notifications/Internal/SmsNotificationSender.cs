using HotelBooking.Notifications;
namespace HotelBooking.Notifications.Internal;
public class SmsNotificationSender : INotificationSender { public int Sent {get; private set;} public void SendConfirmation(Confirmation confirmation) => Sent++; }
