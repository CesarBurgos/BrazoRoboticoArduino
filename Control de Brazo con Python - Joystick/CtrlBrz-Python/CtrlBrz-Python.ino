#include <Servo.h>

/* Apodos de los servomotores (Brazo robótico):
 * Rot - Rotación del brazo
 * Incl - Inclinación del brazo
 * GGrr - Giro de la garra
 * Grr - Control de garra (Abrir/Cerrar)*/

Servo Rot,Incl,GGrr,Grr;

// Varibles para controlar los ángulos de cada servomotor
int SMRot,SMIncl,SMGGrr,SMGrr;

// Variable del caracter recibio de Python
char DePy;

void setup(){
  //Frecuencia de comunicación con python
  Serial.begin(9600);

  //Activando servomotores
  /*Rot.attach(3,900,2100);  //Pin 3 (PWM)
  Incl.attach(5,900,2100); //Pin 5 (PWM)
  GGrr.attach(6,900,2100); //Pin 6 (PWM)
  Grr.attach(9,900,2100);  //Pin 9 (PWM)
  */
  
  Rot.attach(3);  //Pin 3 (PWM)
  Incl.attach(5); //Pin 5 (PWM)
  GGrr.attach(6); //Pin 6 (PWM)
  Grr.attach(9);  //Pin 9 (PWM)

  /*//Leyendo la posición actual de cada servomotor
  SMRot = Rot.read();
  SMIncl = Incl.read();
  SMGGrr = GGrr.read();
  SMGrr = Grr.read();*/
  
  //Colocando en una posición Default a los servomotores
  SMRot = 90;
  Rot.write(SMRot);
  SMIncl = 135;
  Incl.write(SMIncl);
  SMGGrr = 0;
  GGrr.write(SMGGrr);
  SMGrr = 90;
  Grr.write(SMGrr);
}

void loop() {
  while(Serial.available()) {
    if(Serial.available() > 0) {
      //Leyendo de Python
      DePy = Serial.read();
      delay(100);

      // ============== ACCIONES DE LA GARRA
      if(DePy == 'd'){
        //Rotación izq - Garra
        if(SMGGrr <= 168){
          SMGGrr+=12;
          GGrr.write(SMGGrr);
        }
      }

      if(DePy == 'a'){
        //Rotación der - Garra
        if(SMGGrr >= 12){
          SMGGrr-=12;
          GGrr.write(SMGGrr);
        }
      }


      if(DePy == 'p'){
        if(SMGrr < 90){
          //CERRAR - Garra
          SMGrr = 90;
          Grr.write(SMGrr);
        }else{
          //ABRIR - Garra
          SMGrr = 0;
          Grr.write(SMGrr);
        }
      }

      if(DePy == 'i'){
        //ABRIR - Garra
        if(SMGrr >= 10){
          SMGrr -= 10;
          Grr.write(SMGrr);
        }
      }

      if(DePy == 'o'){
        //CERRAR - Garra
        if(SMGrr <= 80){
          SMGrr += 10;
          Grr.write(SMGrr);
        }
      }
      
      
      // ============== ACCIONES DEL BRAZO
      if(DePy == 's'){
        //Rotación Abajo - Brazo
        if(SMIncl <= 126){
          SMIncl+=9;
          Incl.write(SMIncl);
        }
      }

      if(DePy == 'w'){
        //Rotación Arriba - Brazo
        if(SMIncl >= 18){
          SMIncl-=9;
          Incl.write(SMIncl);
        }
      }

      if(DePy == 'r'){
        //Rotación izq - Brazo
        if(SMRot <= 165){
          SMRot+=11;
          Rot.write(SMRot);
        }
      }

      if(DePy == 'l'){
        //Rotación Der - Brazo
        if(SMRot >= 30){
          SMRot-=11;
          Rot.write(SMRot);
        }          
      }
    }
  }
}
