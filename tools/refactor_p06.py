from pathlib import Path
mapping={
'Rooms':['Room','IRoomCatalog'], 'Rooms/Internal':['InMemoryRoomCatalog'],
'Notifications':['Confirmation','INotificationSender'], 'Notifications/Internal':['EmailNotificationSender','SmsNotificationSender'],
'Payments':['IPaymentService','PaymentStatus'], 'Payments/Internal':['SimulatedPaymentService'],
'Reservations':['BookingService','BookingResult','DateRange','Guest','Reservation','ReservationStatus','IReservationStore'], 'Reservations/Internal':['InMemoryReservationStore']}
Path('IRoomCatalog.cs').write_text('namespace HotelBooking;\npublic interface IRoomCatalog { IReadOnlyList<Room> All(); }\n')
Path('InMemoryRoomCatalog.cs').write_text('namespace HotelBooking;\npublic sealed class InMemoryRoomCatalog(IReadOnlyList<Room> rooms) : IRoomCatalog { public IReadOnlyList<Room> All() => rooms.ToArray(); }\n')
Path('Confirmation.cs').write_text('namespace HotelBooking;\npublic sealed record Confirmation(string ReservationId, string GuestEmail, string RoomNumber, DateOnly CheckIn, DateOnly CheckOut);\n')
Path('IPaymentService.cs').write_text('namespace HotelBooking;\npublic interface IPaymentService { PaymentStatus TakeDeposit(decimal stayPrice); }\n')
Path('PaymentStatus.cs').write_text('namespace HotelBooking;\npublic enum PaymentStatus { Paid, Declined }\n')
Path('SimulatedPaymentService.cs').write_text('namespace HotelBooking;\n// P06 simulation only: no money moves, not called by Reserve.\npublic sealed class SimulatedPaymentService(bool approve = true) : IPaymentService { public PaymentStatus TakeDeposit(decimal stayPrice) { if(stayPrice < 0) throw new ArgumentOutOfRangeException(nameof(stayPrice)); return approve ? PaymentStatus.Paid : PaymentStatus.Declined; } }\n')
for folder,names in mapping.items():
 Path(folder).mkdir(parents=True,exist_ok=True)
 for name in names:
  p=Path(name+'.cs');t=p.read_text();ns='HotelBooking.'+folder.replace('/','.')
  uses=[]
  if folder=='Reservations': uses=['HotelBooking.Rooms','HotelBooking.Notifications']
  if folder=='Reservations/Internal':uses=['HotelBooking.Rooms','HotelBooking.Reservations']
  if folder.endswith('/Internal'):uses.append('HotelBooking.'+folder.split('/')[0])
  t=t.replace('namespace HotelBooking;','\n'.join('using '+u+';' for u in uses)+'\nnamespace '+ns+';')
  if name=='BookingService':
   t=t.replace('IReadOnlyList<Room> rooms','IRoomCatalog rooms').replace('rooms.Where','rooms.All().Where')
   t=t.replace('email.SendConfirmation(reservation);','email.SendConfirmation(new Confirmation(reservation.Id, guest.Email, room.Number, stay.CheckIn, stay.CheckOut));')
  if name in ['INotificationSender','EmailNotificationSender','SmsNotificationSender']: t=t.replace('Reservation reservation','Confirmation confirmation')
  Path(folder,name+'.cs').write_text(t);p.unlink()
imports='using HotelBooking.Rooms;\nusing HotelBooking.Rooms.Internal;\nusing HotelBooking.Reservations;\nusing HotelBooking.Reservations.Internal;\nusing HotelBooking.Notifications.Internal;\nusing HotelBooking.Payments.Internal;'
p=Path('Program.cs');t=p.read_text().replace('using HotelBooking;',imports).replace('new BookingService([r7, r8],','new BookingService(new InMemoryRoomCatalog([r7, r8]),').replace('// P04: composition root wires the concrete implementations.','// P06: only the composition root names implementations from other modules.\n_ = new SimulatedPaymentService();');p.write_text(t)
p=Path('HotelBooking.Tests/BookingServiceTests.cs');t=p.read_text().replace('using HotelBooking;',imports+'\nusing HotelBooking.Notifications;').replace('new([R7,R8], store','new(new InMemoryRoomCatalog([R7,R8]), store').replace('List<Reservation> Sent','List<Confirmation> Sent').replace('SendConfirmation(Reservation r)','SendConfirmation(Confirmation r)').replace('Assert.Single(fake.Sent).Id','Assert.Single(fake.Sent).ReservationId');p.write_text(t)
