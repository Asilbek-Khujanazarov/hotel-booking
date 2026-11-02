import runpy
from pathlib import Path
m=runpy.run_path('tools/create_p03_diagrams.py'); page,box,edge=m['page'],m['box'],m['edge'];E=m['E'];mx=m['mx']
r=page('Classes - after')
for i,(id,t,x,y) in enumerate([
 ('service','BookingService\nFindFreeRooms / Reserve / Cancel',350,30),
 ('store','«interface» IReservationStore\nCount / HasOverlap / Save / Find',40,240),
 ('sender','«interface» INotificationSender\nSendConfirmation',700,240),
 ('memory','InMemoryReservationStore\nlist storage',40,480),
 ('email','EmailNotificationSender\nsimulated email',600,480),
 ('sms','SmsNotificationSender\nsimulated SMS',870,480)]):box(r,id,t,x,y,250,110)
edge(r,'a','service','store','uses','dashed=1;endArrow=open;');edge(r,'b','service','sender','uses','dashed=1;endArrow=open;')
for n,a,b in [('c','memory','store'),('d','email','sender'),('e','sms','sender')]:edge(r,n,a,b,'implements','dashed=1;endArrow=block;endFill=0;')
r=page('Context map')
for id,t,x,y in [('rooms','Rooms\nRoom catalog / type / price',60,80),('reservations','Reservations\nStay / Confirmed / Cancelled\nOwns no-overlap rule',430,80),('notifications','Notifications\nConfirmation / Sent / Failed',800,80),('payments','Payments\nDeposit / Paid / Declined',430,440)]:box(r,id,t,x,y,260,140)
edge(r,'a','reservations','rooms','All() → Room list');edge(r,'b','reservations','notifications','Confirmation message');edge(r,'c','reservations','payments','Planned: TakeDeposit(price)','dashed=1;endArrow=open;');edge(r,'d','payments','rooms','Planned: price lookup','dashed=1;endArrow=open;')
r=page('Modules')
box(r,'app','One console application / one deployment',20,20,1090,650,'verticalAlign=top;fontStyle=1;')
for id,t,x,y in [('main','Program.cs\nComposition root',440,70),('rooms','Rooms\nPublic: Room, IRoomCatalog\nInternal: InMemoryRoomCatalog',50,270),('reservations','Reservations\nPublic: BookingService, domain, IReservationStore\nInternal: InMemoryReservationStore',420,270),('notifications','Notifications\nPublic: Confirmation, INotificationSender\nInternal: Email / SMS senders',790,270),('payments','Payments\nPublic: IPaymentService, PaymentStatus\nInternal: SimulatedPaymentService',420,500)]:box(r,id,t,x,y,280,130)
for n,b in enumerate(['rooms','reservations','notifications','payments']):edge(r,'wire'+str(n),'main',b,'wires','dashed=1;endArrow=open;')
edge(r,'a','reservations','rooms','IRoomCatalog only');edge(r,'b','reservations','notifications','INotificationSender only')
E.indent(mx);E.ElementTree(mx).write('docs/diagrams.drawio',encoding='utf-8',xml_declaration=True)
print('8 editable pages saved: P03 + P04 + P05 + P06')
