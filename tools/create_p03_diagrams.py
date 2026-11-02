import xml.etree.ElementTree as E
from pathlib import Path
mx=E.Element('mxfile',host='app.diagrams.net')
def page(name):
 d=E.SubElement(mx,'diagram',name=name,id=name.replace(' ','-')); m=E.SubElement(d,'mxGraphModel',page='1',pageWidth='1169',pageHeight='827',grid='1',gridSize='10'); r=E.SubElement(m,'root'); E.SubElement(r,'mxCell',id='0');E.SubElement(r,'mxCell',id='1',parent='0');return r
base='whiteSpace=wrap;html=0;fontSize=13;'
def box(r,id,text,x,y,w=180,h=90,style='rounded=0;'):
 c=E.SubElement(r,'mxCell',id=id,value=text,style=base+style,vertex='1',parent='1');E.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),**{'as':'geometry'})
def edge(r,id,a,b,text='',style='endArrow=block;',p=None):
 c=E.SubElement(r,'mxCell',id=id,value=text,source=a,target=b,style=base+style,edge='1',parent='1');g=E.SubElement(c,'mxGeometry',relative='1',**{'as':'geometry'})
 if p:
  for tag,x,y in p:E.SubElement(g,'mxPoint',x=str(x),y=str(y),**{'as':tag})
r=page('Use cases');box(r,'system','Hotel booking app',290,40,520,630,'verticalAlign=top;fontStyle=1;');
for i,name in enumerate(['Guest','Receptionist']):box(r,'actor'+str(i),name,50,130+i*300,80,100,'shape=umlActor;')
for i,name in enumerate(['Search free rooms','Book a room','View a booking','Cancel a booking']):
 box(r,'goal'+str(i),name,430,110+i*130,230,70,'ellipse;')
 for a in range(2):edge(r,f'e{a}{i}','actor'+str(a),'goal'+str(i),style='endArrow=none;')
r=page('Classes')
items=[('service','BookingService\n────────────\nrooms\n────────────\nFindFreeRooms(stay)\nReserve(guest, room, stay)\nCancel(id)',390,20),('store','ReservationStore\n────────────\nrows\n────────────\nHasOverlap(room, stay)\nSave(reservation), Find(id)\nCountConfirmed(room, stay)',50,240),('email','EmailSender\n────────────\nSent\n────────────\nSendConfirmation(reservation)',730,240),('status','«enumeration»\nReservationStatus\n────────────\nConfirmed\nCancelled',390,240),('guest','Guest\n────────────\nName, Email',30,540),('reservation','Reservation\n────────────\nId, Status\n────────────\nBlocks(room, stay)\nCancel()',300,540),('room','Room\n────────────\nNumber, Type',570,540),('dates','DateRange\n────────────\nCheckIn, CheckOut\n────────────\nIsValid(), Overlaps(other)',820,540)]
for id,t,x,y in items:box(r,id,t,x,y,230,160)
for i,(a,b,label,st) in enumerate([('service','store','uses','dashed=1;endArrow=open;'),('service','email','uses','dashed=1;endArrow=open;'),('reservation','status','has 1','endArrow=none;'),('store','reservation','1 keeps 0..*','endArrow=none;'),('guest','reservation','1 makes 0..*','endArrow=none;'),('reservation','room','0..* reserves 1','endArrow=none;'),('reservation','dates','1 owns stay dates 1','startArrow=diamond;startFill=1;endArrow=none;')]):edge(r,'e'+str(i),a,b,label,st)
for name,last,msgs in [('Sequence - book','EmailSender',[(0,1,'Reserve(Maya, R7, 12–14 Nov)',0),(1,2,'HasOverlap(R7, 12–14 Nov)',0),(2,1,'false',1),(1,2,'Save(R101, Confirmed)',0),(1,3,'SendConfirmation(R101)',0),(1,0,'Accepted R101',1)]),('Sequence - cancel','R101',[(0,1,'Cancel("R101")',0),(1,2,'Find("R101")',0),(2,1,'R101',1),(1,3,'Cancel()',0),(3,1,'true: now Cancelled',1),(1,0,'true',1)])]:
 r=page(name)
 for i,t in enumerate(['Maya','BookingService','ReservationStore',last]):
  box(r,'p'+str(i),t,40+i*270,30,210,50)
  c=E.SubElement(r,'mxCell',id='life'+str(i),style='dashed=1;endArrow=none;',edge='1',parent='1');g=E.SubElement(c,'mxGeometry',relative='1',**{'as':'geometry'});E.SubElement(g,'mxPoint',x=str(145+i*270),y='80',**{'as':'sourcePoint'});E.SubElement(g,'mxPoint',x=str(145+i*270),y='650',**{'as':'targetPoint'})
 for n,(a,b,t,reply) in enumerate(msgs,1):
  y=140+n*70;c=E.SubElement(r,'mxCell',id='msg'+str(n),value=f'{n}. {t}',style=base+('dashed=1;endArrow=open;' if reply else 'endArrow=block;'),edge='1',parent='1');g=E.SubElement(c,'mxGeometry',relative='1',**{'as':'geometry'});E.SubElement(g,'mxPoint',x=str(145+a*270),y=str(y),**{'as':'sourcePoint'});E.SubElement(g,'mxPoint',x=str(145+b*270),y=str(y),**{'as':'targetPoint'})
r=page('Activity - book')
box(r,'start','',390,20,30,30,'ellipse;fillColor=#222222;');box(r,'valid','Check-out after\ncheck-in?',310,90,190,110,'rhombus;');box(r,'invalid','InvalidDates\nsave nothing',660,110,220,60,'rounded=1;');box(r,'overlap','Confirmed booking\nshares a night?',310,260,190,110,'rhombus;');box(r,'unavailable','Unavailable\nsave nothing',660,280,220,60,'rounded=1;');box(r,'save','Save reservation as Confirmed',280,420,250,60,'rounded=1;');box(r,'send','Send confirmation email',280,530,250,60,'rounded=1;');box(r,'accepted','Accepted + reservation id',280,640,250,50,'rounded=1;');box(r,'end','',390,740,30,30,'ellipse;shape=doubleEllipse;fillColor=#222222;')
for n,(a,b,t) in enumerate([('start','valid',''),('valid','invalid','No'),('valid','overlap','Yes'),('overlap','unavailable','Yes'),('overlap','save','No'),('save','send',''),('send','accepted',''),('accepted','end','')]):edge(r,'e'+str(n),a,b,t)
E.indent(mx);E.ElementTree(mx).write('docs/diagrams.drawio',encoding='utf-8',xml_declaration=True)
print('Created 5 editable draw.io pages.')
