# Hotel booking · P06 (.NET 10)

P03 → P04 → P05 → P06 completed in order. Console application, in-memory storage and simulated notifications/payments. The booking race is intentionally retained for P09.

```powershell
dotnet run --project hotel-booking.csproj --no-launch-profile
dotnet run --project hotel-booking.csproj --no-launch-profile -- --race
dotnet run --project hotel-booking.csproj --no-launch-profile -- --verify
dotnet test HotelBooking.Tests/HotelBooking.Tests.csproj
```

Rooms, Reservations, Payments and Notifications have public contracts and Internal implementations. Program.cs composes them. 8 behaviour tests and 3 NetArchTest architecture checks guard behaviour and boundaries.

Open docs/diagrams.drawio in diagrams.net: five P03 pages plus Classes - after, Context map and Modules. Requirements, context definitions, quality targets, ADR-001 and actual execution evidence are in docs. docs/p03-program.cs.txt preserves the original P03 implementation for comparison.

P07 (HTTP/PostgreSQL) has not started. Payment and email/SMS implementations are simulations; no network messages or payments are made. Quality targets in the design documents are not production benchmarks.

If testhost cannot connect in a restricted environment, run the same 11 xUnit Facts in one process:

```powershell
dotnet build tools/TestRunner/TestRunner.csproj -m:1 -p:BuildInParallel=false
dotnet tools/TestRunner/bin/Debug/net10.0/TestRunner.dll
```

The runner invokes the existing Fact methods and uses their real xUnit assertions and NetArchTest checks; it does not replace them with duplicate tests. The final evidence uses this runner because standard testhost could not connect here. NuGet audit retrieval was intermittently unavailable (NU1900); this is separate from the successful code checks.
