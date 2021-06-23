import pygame
from pygame.locals import*
import sys
import serial, time
import serial.tools.list_ports

# Variables Globales
global Accion, CtrlGrr, arduino

# Apertura/Cierre de la garra
Garra = 0

# Tarjeta Arduino
arduino = None

def AccionDraw(x,y,x2,mov,colorAcc):
    pygame.draw.circle(Vent, (100,255,0), (x, y), 20, 10)
    pygame.draw.circle(Vent, (0,100,255), (x2, 130), 20, 10)

    pygame.draw.circle(Vent, colorAcc, (575-(mov*7), 195), 20, 10)
    pygame.draw.circle(Vent, colorAcc, (625+(mov*7), 195), 20, 10)

# ============== Tarjeta Arduino

ports = list(serial.tools.list_ports.comports())
if len(ports) == 0:
    print("\n\n Sin alguna conexión en los puertos Seriales...\n\n")
    sys.exit()
else:
    for p in ports:
        if 'Arduino' in p[1]:
            print('\n\n == Conexión con: '+p[1]+' ==') # Descripción tarjeta Arduino
            arduino = serial.Serial(p[0], 9600)
            time.sleep(2) #Tiempo de espera por el reseteo del Arduino
        elif 'CH340' in p[1]:
            # Componente de Arduino Nano
            print('\n\n == Conexión con: '+p[1]+' ==') # Descripción tarjeta Arduino
            arduino = serial.Serial(p[0], 9600)
            time.sleep(2) #Tiempo de espera por el reseteo del Arduino
        else:
            print("\n\n ¡¡ Error !! - No hay alguna Tarjeta Arduino Conectada...\n\n")
            sys.exit()


# ============== Mando de PC
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() <= 0:
    print("\n\n ¡¡ Error !! - No hay un mando conectado...\n\n")
    sys.exit()
elif pygame.joystick.get_count() > 1:
    print("\n\n ¡¡ Error !! - Hay más de un mando conectado...\n\n")
    sys.exit()
else:
    # Objeto del mando conectado...
    mando = pygame.joystick.Joystick(0) 
    mando.init()

    #Comprobamos las caracteristicas del mando 
    if mando.get_numaxes() < 2 and mando.get_numhats() < 1:  
        print ("\n\n ¡¡ Error !! - El mando conectado no es adecuado para la ejecución...\n\n")
        sys.exit()

Vent = pygame.display.set_mode((800,300))
colorAcc = (0,200,200)
x2,y2,x3 = 220, 220, 500

Text1 = pygame.font.SysFont('Comic Sans MS', 25)
Text2 = pygame.font.SysFont('Comic Sans MS', 20)
Text3 = pygame.font.SysFont('Comic Sans MS', 20)
Text4 = pygame.font.SysFont('Comic Sans MS', 20)

T1 = Text1.render('- Control de brazo robótico -', True, (200, 200, 230))
T2 = Text2.render(' Movimientos del brazo ', True, (255, 255, 255))
T3 = Text3.render(' Movimientos de la garra ', True, (255,255,255))
T4 = Text4.render(' Garra cerrada ', True, colorAcc)

# ============== Ejecución del programa
while True:
    Vent.fill((0,0,0))
    pygame.draw.rect(Vent, (100,255,0), (70, 40, 290, 200), 3, 5)
    pygame.draw.rect(Vent, (0,100,255), (470, 100, 260, 60), 3, 5)
    pygame.draw.rect(Vent, colorAcc, (470, 165, 260, 60), 3, 5)

    Vent.blit(T1,(250,0))
    Vent.blit(T2,(110,250))
    Vent.blit(T3,(490,50))
    Vent.blit(T4,(530,230))

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit()
        if event.type ==  pygame.locals.JOYAXISMOTION:# Joystick
            # ===== Joystick del Mando ===== 
            x = int(mando.get_axis(0)*10)
            y = int(mando.get_axis(1)*10)

            if (x == 0 and y == -10):
                #'===================================== ARRIBA'
                # Arriba - SUBIR BRAZO
                if(y2 > 70):
                    y2 -= 11
                    #Envio a Arduino de acción
                    arduino.write(b'w')
                    time.sleep(.1)

            if (x == 0 and y == 9):
                #'===================================== ABAJO'
                # Abajo - BAJAR BRAZO
                if(y2 < 220):
                    y2 += 11
                    arduino.write(b's')
                    time.sleep(.1)

            if (x == 9 and y == 0):
                #'===================================== DERECHA'
                # Derecha - ROTACIÓN DER BRAZO
                if(x2 < 330):
                    x2 += 16
                    #Envio a Arduino de acción
                    arduino.write(b'r')
                    time.sleep(.1)

            if (x == -10 and y == 0):
                #'===================================== IZQUIERDA'
                # Izquierda - ROTACIÓN IZQ BRAZO
                if(x2 > 100):
                    x2 -= 16
                    #Envio a Arduino de acción
                    arduino.write(b'l')
                    time.sleep(.1)
        elif event.type == pygame.locals.JOYHATMOTION: 
            # ===== Cruzeta del Mando ===== 
            if event.value[1] == -1:
                # Abajo - Cruzeta - BAJAR BRAZO
                if(y2 < 220):
                    y2 += 11
                    #Envio a Arduino de acción
                    arduino.write(b's')
                    time.sleep(.1)
            if event.value[1] == 1:
                # Arriba - Cruzeta - SUBIR BRAZO
                if(y2 > 70):
                    y2 -= 11
                    #Envio a Arduino de acción
                    arduino.write(b'w')
                    time.sleep(.1)
            if event.value[0] == -1:
                # Izquierda - Cruzeta - ROTACIÓN IZQ BRAZO
                if(x2 > 100):
                    x2 -= 16
                    #Envio a Arduino de acción
                    arduino.write(b'l')
                    time.sleep(.1)
            if event.value[0] == 1:
                # Derecha - Cruzeta - ROTACIÓN DER BRAZO
                if(x2 < 330):
                    x2 += 16
                    #Envio a Arduino de acción
                    arduino.write(b'r')
                    time.sleep(.1)

        elif event.type == pygame.locals.JOYBUTTONDOWN: #botones al dejar de presionarlo
            '''
            if e.button == 0:
                # Botón 1 del mando - "Y" ó "Triangulo"
                print("1")
            if e.button == 1:
                # Botón 2 del mando - "B" ó "Círculo"
                print("2")
            if e.button == 3:
                # Botón 4 del mando - "X" ó "Cuadrado"
                print("4")
            if event.button == 8:
                # Botón del mando - "select"
                print("9")
            '''

            if event.button == 6:
                # Botón GATILLO2 Izq del mando - GIRO IZQ GARRA
                if(x3 > 500):
                    x3 -= 13

                    #Envio a Arduino de acción
                    arduino.write(b'a')
                    time.sleep(.1)
            if event.button == 7:
                # Botón GATILLO2 del mando - GIRO DER GARRA
                if(x3 < 700):
                    x3 += 13

                    #Envio a Arduino de acción
                    arduino.write(b'd')
                    time.sleep(.1)
            if event.button == 2:
                # Botón 3 del mando - "A" ó "Equís"
                # ACCIÓN: Apertura de garra
                
                if Garra == 0:
                    Garra = 9

                    # - Abrir Garra
                    colorAcc = (255,0,100)
                    T4 = Text4.render(' Garra abierta ', True, colorAcc)

                    #Envio a Arduino de acción
                    arduino.write(b'p')
                    time.sleep(.1)
                else:
                    Garra = 0

                    # - Cerrar Garra
                    colorAcc = (0,200,200)
                    T4 = Text4.render(' Garra cerrada ', True, colorAcc)

                    #Envio a Arduino de acción
                    arduino.write(b'p')
                    time.sleep(.1)
            
            if event.button == 5:
                # Botón GATILLO Izq del mando - "Abrir Garra"
                if Garra < 8:
                    Garra +=1

                    # - Abrir Garra
                    colorAcc = (255,0,100)
                    T4 = Text4.render(' Abriendo Garra ', True, colorAcc)

                    #Envio a Arduino de acción
                    arduino.write(b'i')
                    time.sleep(.1)

            if event.button == 4:
                # Botón GATILLO Der del mando - "Cerrar Garra"
                if Garra >= 1:
                    Garra -=1

                    # - Cerrar Garra
                    colorAcc = (0,200,200)
                    T4 = Text4.render(' Cerrando Garra ', True, colorAcc)

                    #Envio a Arduino de acción
                    arduino.write(b'o')
                    time.sleep(.1)
            if event.button == 9: 
                # Botón "start" del mando
                # ACCIÓN: Finalizar ejecución

                arduino.close() # Cerrando conexión con Arduino
                sys.exit()

    AccionDraw(x2,y2,x3,Garra,colorAcc)
    pygame.display.flip()