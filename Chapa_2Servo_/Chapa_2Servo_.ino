#include <Servo.h>
#define DEBUG(a) Serial.println(a);

Servo servo1;//servo seguro
Servo servo2;// servo Puerta
//Servo servo3;
//Servo servo4;
//Servo servo5;
//Servo servo6;

int position = 0;//posicion inicial en 0

int lista[]={1,1,1,1,1,1};
Servo servos[] = {servo1, servo2};
void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(50);
  servos[0].attach(8); //Definicion del pin para el servo que abrir el seguro
  servos[1].attach(9); // Definicion del pin para el servo que abre la puerta
  servos[0].write(0);
  servos[1].write(0);
}

void loop()
{
  if (Serial.available() > 0) {
      int data = Serial.parseInt();

      if (lista[data]) {
        servos[data].write(90);
        lista[data] = 0;
        DEBUG("Se mueve a 90");
      }
      else {
        servos[data].write(0);
        lista[data] = 1;
        DEBUG("Se mueve a 10");
        }
        
      }
}


 
