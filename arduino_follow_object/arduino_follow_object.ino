#include<Servo.h>

Servo servoX; //Vertical Servo
Servo servoY; //Horizontal Servo

float x_mid, x;
float y_mid, y;

float width = 32, height = 24;  // total resolution of the video divided by 10 in python
float xpos = 90;
float ypos = 60;  // initial positions of both Servos

float angle = 0.7;  //movement value of each motors

void setup()
{
  Serial.begin(9600);
  servoY.attach(11); //Attach Vertical Servo to Pin 11
  servoX.attach(9); //Attach Horizontal Servo to Pin 9
  
  servoY.write(ypos); 
  servoX.write(xpos);
}

void Pos()  //servo following object coordinates
{
    if (x_mid < ((width / 2) - 3 )){ //-+3 tolerance 
      xpos = xpos - angle;
    }
    else if (x_mid > ((width / 2) + 3 )){
      xpos = xpos + angle;
    }
    
    if (y_mid > ((height / 2) + 2)){ //-+2 tolerance 
      ypos = ypos + angle;
    }
    else if (y_mid < ((height / 2) - 2)){
      ypos = ypos - angle;
    }


    // if the servo degree is outside its range
    if (xpos >= 160){
      xpos = 160;
    }
    if (xpos <= 20){
      xpos = 20;
    }
    
    if (ypos >= 110){
      ypos = 110;
    }
    if (ypos <= 0){
      ypos = 0;
    }

    x = xpos - 90;
    y = 60 - ypos;

    servoX.write(xpos);
    Serial.print(x);
    Serial.print("A");
    servoY.write(ypos);
    Serial.print(y);
    Serial.println("B");
}

void loop()
{
  if(Serial.available() > 0)
  {   
    if(Serial.read() == 'X')
    {
      x_mid = Serial.parseInt();

      if(Serial.read() == 'Y')
      {
      if(Serial.read() == '#') 
      {
      servoX.write(90);
      servoY.write(60);
      } 
       y_mid = Serial.parseInt();
       Pos();
       
//       delay(5);
      }
    }


  }
}
