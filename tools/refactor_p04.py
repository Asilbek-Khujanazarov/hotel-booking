from pathlib import Path
import re
p=Path('Program.cs');t=p.read_text();Path('docs/p03-program.cs.txt').write_text(t)
start=t.index('record DateRange'); code=t[start:]; main=t[:start]
parts=re.split(r'(?m)^(?=(?:record|enum|class) )',code)
for part in parts:
 if not part.strip():continue
 name=re.match(r'(?:record|enum|class) (\w+)',part)[1]
 part=re.sub(r'(?m)^(record|enum|class) ',r'public \1 ',part)
 part=part.replace('class ReservationStore','class InMemoryReservationStore').replace('class EmailSender','class EmailNotificationSender')
 if name=='BookingService':
  part=part.replace('ReservationStore store, EmailSender email','IReservationStore store, INotificationSender email')
  part=part.replace('email.SendConfirmation(reservation);','try { email.SendConfirmation(reservation); }\n        catch (Exception) { /* R6: saved booking remains confirmed. */ }')
 if name=='ReservationStore':part=part.replace('class InMemoryReservationStore\n','class InMemoryReservationStore : IReservationStore\n')
 if name=='EmailSender':part=part.replace('class EmailNotificationSender\n','class EmailNotificationSender : INotificationSender\n')
 Path(('InMemoryReservationStore' if name=='ReservationStore' else 'EmailNotificationSender' if name=='EmailSender' else name)+'.cs').write_text('namespace HotelBooking;\n'+part)
main=main.replace('// P03: one file, concrete dependencies, in-memory data. Refactoring starts in P04.','using HotelBooking;\n// P04: composition root wires the concrete implementations.').replace('new ReservationStore()','new InMemoryReservationStore()').replace('new EmailSender()','new EmailNotificationSender()')
p.write_text(main)
Path('IReservationStore.cs').write_text('namespace HotelBooking;\npublic interface IReservationStore { int Count { get; } bool HasOverlap(Room room, DateRange stay); void Save(Reservation reservation); Reservation? Find(string id); int CountConfirmed(Room room, DateRange stay); }\n')
Path('INotificationSender.cs').write_text('namespace HotelBooking;\npublic interface INotificationSender { void SendConfirmation(Reservation reservation); }\n')
Path('SmsNotificationSender.cs').write_text('namespace HotelBooking;\npublic class SmsNotificationSender : INotificationSender { public int Sent {get; private set;} public void SendConfirmation(Reservation reservation) => Sent++; }\n')
