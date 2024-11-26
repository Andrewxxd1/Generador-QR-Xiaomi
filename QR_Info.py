import pandas as pd 
import subprocess as sp
import time
import platform
import os
import qrcode
import glob

contador = 0

#DEFINICIÓN DE FUNCIONES
def delay(n):
    time.sleep(n)

def adb_connect():
    #COMPRUEBA LA CORRECTA CONEXIÓN A ADB 
    cont_msj=0

    print('Comprobando la conexion adb... \n')

    while(True):
        delay(1)
        adb=sp.check_output(['adb','devices'],text=True)

        try:
            adb.index("device",adb.index("device")+1) #me toma la segunda aparición de device
            print('Equipo conectado correctamente \n')
            print(adb)
            print('---------------------------------------------------------------- \n')
            break
        
        except ValueError:
            if adb.find("offline") != -1:
                kill_server=sp.check_output('adb kill-server',text=True,shell=True)
                print('EQUIPO OFFLINE INTENTANDO CONECTAR')
                print(kill_server+'\n')
            
            else:
                cont_msj+=1
                if cont_msj<2:
                    print('NO SE ENCUENTRA EL EQUIPO POR FAVOR REVISE LA CONEXIÓN \n')

def sistema_operativo():
    #DEFINE LAS FUNCIONES SEGUN EL SISTEMA OPERATIVO
        
    sistema_operativo=platform.system()
    if sistema_operativo == 'Windows':
        sp.run('cmd /c cls')
    elif sistema_operativo == 'Linux':
        sp.run('clear')
    else:
        print('Este programa aún no se encuentra disponible para tu sistema operativo')
        print('Por favor intenta ejecutarlo con Windows o Linux')
        delay(5)
        exit

#RUTINA

sistema_operativo()

input('Presione ENTER para comenzar: ')
print('\n')



# Patrón para buscar archivos .png en la carpeta 'QR'
patron = 'QR/*.png'

# Obtener la lista de archivos que coinciden con el patrón
archivos_png = glob.glob(patron)

# Iterar sobre cada archivo y eliminarlo
for archivo in archivos_png:
    os.remove(archivo)
    print(f"Se eliminó el archivo: {archivo}")

print("Todos los archivos PNG en la carpeta 'QR' han sido eliminados.")


# Verificar si el archivo 'Datos.txt' existe
if os.path.exists('Datos.txt'):
    # Si existe, eliminarlo
    os.remove('Datos.txt')
    print("Se eliminó el archivo 'Datos.txt' existente.")

# Crear un nuevo archivo 'Datos.txt'
with open('Datos.txt', 'w') as file:
    file.write("Este es un nuevo archivo 'Datos.txt'\n")
    # Puedes escribir más contenido aquí si es necesario
    print("Se creó un nuevo archivo 'Datos.txt'.")

comand = ['adb shell getprop ro.product.model', 'adb shell getprop ro.ril.oem.imei1', 'adb shell getprop ro.ril.oem.imei2',
          'adb shell getprop ro.product.marketname', 'adb shell getprop ro.product.device',]

while True:
    contador += 1

    phone=[]

    adb_connect()

    num=input('MT_Abreviado: ')
    num1=input('FCC ID: ')
    num2=input('SAR: ')
    num3=input('A quien pertenece: ')


    cadena = 'adb shell'

    for i in comand:
        
        if i.find(cadena) != -1:

            info= sp.check_output(i,text=True,shell=True).strip()

            if info =='' and i == comand[1]:
                info= sp.check_output('adb shell getprop ro.ril.miui.imei0',text=True,shell=True).strip()
            if info == '' and i == comand[2] and num3 != 'CLARO':
                info= sp.check_output('adb shell getprop ro.ril.miui.imei1',text=True,shell=True).strip()



            phone.append(info)
        else:
            phone.append(i)

   

    data_phone = num.upper()+'-'+phone[0]+'\n'+phone[3]+'\n'+phone[1]+'\n'+phone[2]+'\n'+'2AFZZ'+num1.upper()+'-'+num2+'\n'+phone[4].upper()+'-'+num3.upper()+'\n\n'
    data_phone2 = num.upper()+'|'+phone[0]+'|'+phone[3]+'|'+phone[1]+'|'+phone[2]+'|'+'2AFZZ'+num1.upper()+'|'+num2+'|'+phone[4].upper()+'|'+num3.upper()+'|'

    dat = open("Datos.txt",'a')
    dat.write(data_phone)
    print(data_phone)

    img = qrcode.make(data_phone2)


    img.save('QR/'+str(contador)+'.png')  



    while True:
        respuesta=input('\n¿Desea realizar otra operación? S/n: ').lower()
        print('')
        if respuesta=='s':
            break
        if respuesta=='n':
            input("Presiona Enter para salir...")
            exit()
        else:
            print('Debe ingresar S/n ')
    