using HotelBooking.Payments;
namespace HotelBooking.Payments.Internal;
// P06 simulation only: no money moves, not called by Reserve.
public sealed class SimulatedPaymentService(bool approve = true) : IPaymentService { public PaymentStatus TakeDeposit(decimal stayPrice) { if(stayPrice < 0) throw new ArgumentOutOfRangeException(nameof(stayPrice)); return approve ? PaymentStatus.Paid : PaymentStatus.Declined; } }
