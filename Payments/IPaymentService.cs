
namespace HotelBooking.Payments;
public interface IPaymentService { PaymentStatus TakeDeposit(decimal stayPrice); }
