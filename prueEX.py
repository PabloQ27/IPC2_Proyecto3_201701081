import re
from evento import Evento
lista_event=[]
eve1 = Evento('25/04/2021', 'barni@ing.usac.edu.gt', 'homero@ing.usac.edu.gt, lisa@ing.usac.edu.gt, moe@ing.usac.edu.gt, bart@ing.usac.edu.gt', '20003 - Sobrecarga de informacion')
eve2 = Evento('24/04/2021', 'barni@ing.usac.edu.gt', 'homero@ing.usac.edu.gt, lisa@ing.usac.edu.gt, moe@ing.usac.edu.gt, bart@ing.usac.edu.gt', '20003 - Sobrecarga de informacion')
eve3 = Evento('23/04/2021', 'barni@ing.usac.edu.gt', 'homero@ing.usac.edu.gt, lisa@ing.usac.edu.gt, moe@ing.usac.edu.gt, bart@ing.usac.edu.gt', '20003 - Sobrecarga de informacion')
lista_event.append(eve1)
lista_event.append(eve2)
lista_event.append(eve3)

for x in lista_event:
    
    print(x.fecha)



correo = ['Reportado por: bart@ing.usa.edu.gt',

            'Reportado por: lisa@ing.usac.edu.Gt',
            'Reportado por: home6548@ing.usac.du.gt',
            'Reportado por: homero@ing.usaC.edu.gt']

for rep in correo:
    if re.findall('^reportado por: ', rep.lower()):
        if re.findall('@ing.usac.edu.gt$', rep.lower()):
            print('si ta')
        else:
            print('no ta segundo')
    else:
        print('no ta primer if')
