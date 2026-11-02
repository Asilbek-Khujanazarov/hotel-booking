// Runs the same synchronous xUnit Facts without testhost's local socket dependency.
using System.Reflection;
using HotelBooking.Tests;
int passed = 0, failed = 0;
foreach (var type in typeof(BookingServiceTests).Assembly.GetTypes().Where(t => t.IsPublic && t.Namespace == "HotelBooking.Tests"))
foreach (var method in type.GetMethods().Where(m => m.GetCustomAttributes().Any(a => a.GetType().FullName == "Xunit.FactAttribute")))
{
    try
    {
        method.Invoke(Activator.CreateInstance(type), null);
        Console.WriteLine($"PASS {type.Name}.{method.Name}");
        passed++;
    }
    catch (Exception error)
    {
        Console.WriteLine($"FAIL {type.Name}.{method.Name}: {(error.InnerException ?? error).Message}");
        failed++;
    }
}
Console.WriteLine($"Passed: {passed}; Failed: {failed}; Total: {passed + failed}");
return failed == 0 && passed == 11 ? 0 : 1;
