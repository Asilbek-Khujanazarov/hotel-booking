using HotelBooking.Reservations;
using NetArchTest.Rules;
using Xunit;
namespace HotelBooking.Tests;
public class ArchitectureTests
{
    private static Types App => Types.InAssembly(typeof(BookingService).Assembly);
    [Fact] public void Reservations_uses_only_public_contracts()
    {
        var result = App.That().ResideInNamespace("HotelBooking.Reservations")
            .ShouldNot().HaveDependencyOnAny("HotelBooking.Rooms.Internal", "HotelBooking.Payments.Internal", "HotelBooking.Notifications.Internal").GetResult();
        Assert.True(result.IsSuccessful, string.Join(", ", result.FailingTypeNames ?? []));
    }
    [Fact] public void Rooms_depends_on_no_other_module()
    {
        var result = App.That().ResideInNamespace("HotelBooking.Rooms")
            .ShouldNot().HaveDependencyOnAny("HotelBooking.Reservations", "HotelBooking.Payments", "HotelBooking.Notifications").GetResult();
        Assert.True(result.IsSuccessful, string.Join(", ", result.FailingTypeNames ?? []));
    }
    [Fact] public void Payments_and_Notifications_do_not_depend_on_Reservations()
    {
        var result = App.That().ResideInNamespace("HotelBooking.Payments").Or().ResideInNamespace("HotelBooking.Notifications")
            .ShouldNot().HaveDependencyOn("HotelBooking.Reservations").GetResult();
        Assert.True(result.IsSuccessful, string.Join(", ", result.FailingTypeNames ?? []));
    }
}
