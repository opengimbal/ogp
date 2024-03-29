// Moving All this to RPI side Python.  (H- BRIDGE and ACCELEROMETER MAGNETOMETER)
// OGP -- ARDUINO SIDE V3.0

// for use with any serial device over usb
// this config handles:  2 SERVOS, 1 DC MOTOR and now featuring one LSM303dlhc compass/accelerometer.

// watch out!! if you lose contact with the rpi in mid-movement, 
// your motors will run free until you pull the plug! 

#include <Servo.h>      // Libraries
#include <AFMotor.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>

char val = 'z';         // variable to receive data from the serial port ('z' means it's asleep)

Adafruit_LSM303_Mag_Unified mag = Adafruit_LSM303_Mag_Unified(12345);              // create sensor objects
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(54321);

Servo myservo;         // create servo objects
Servo myservo2; 
AF_DCMotor motor(1);     //create dc motor object

float Pi = 3.14159;
float heading = 0;
float val2 = 0;
float inclination = 0;
int ms = 200;      //  map step size
int vms = 600;
int nms = 50;      // nudge step size
int i = 0;      //  i is for 'while loops'

void displaySensor(){
    delay(500);
    sensors_event_t event;    ///* Get a new sensor event */
    mag.getEvent(&event);
    delay(500);
    heading = (atan2(event.magnetic.y,event.magnetic.x) * 180) / Pi;      // Calculate the angle of the vector y,x,  /* (magnetic vector values are in micro-Tesla (uT)) */
    if (heading < 0)                      // Normalize to 0-360
    {
      heading = 360 + heading; 
    }
    Serial.print("c_");                         //Header parsing c = compass heading
    Serial.println(heading);
    Serial.print(" ");
    accel.getEvent(&event);                  //  same as before but with the level
    Serial.print("i_"); 
    float inclination = event.acceleration.z ;
    inclination = 10 - inclination;
    inclination = inclination * 9;           // adjust into 90 degrees
    Serial.print(inclination);
    Serial.print("   ");
    val = 'z';
}


void gotoY(){              // acquire a set of co-ordinates
   delay (1000);
    sensors_event_t event;                      // obtain sensor info  -- same as above, in displaySensor
    mag.getEvent(&event);
    heading = (atan2(event.magnetic.y,event.magnetic.x) * 180) / Pi;
    if (heading < 0)
    {heading = 360 + heading;}
    accel.getEvent(&event);
    float inclination = event.acceleration.z ;
    inclination = 10 - inclination;
    inclination = inclination * 9;
//    inclination = inclination - 180;
//    inclination = inclination * -1;


   if (val2 < 90){        //  activate motors based on readings, first    -- ALTITUDE

      if (inclination > (val2 - 1))     // NOTE: make sure that you aleady have your AZUMUTH set before finding altitude
      {
      myservo2.write(80);  //up
      }
      
      if (inclination < (val2 + 1))
      {
      myservo2.write(100);   //down
      }     
      
      if (((val2 - 1) < inclination) && (inclination < (val2 + 1 )))
      {
      myservo2.write(90);  //stop
      //Serial.print("ARRIVAL");
      //displaySensor();
      val = 'z';
      }  
      }

     
   if ((val2 < 459) && (val2 > 90)){                            
      float val3 = val2 - 100;      // AZ commands have 100 added at the python level to differentiate them from ALT commands
          //Serial.print(val3);

 
      if ((heading < (val3-2)) )          //  motors are set to turn off within one degree of target
          {
          myservo.write(87);    //counterclockwise
          }                
      if ((heading > (val3+2)))
          {
          myservo.write(93);    //clockwise
          }          
      if (((val3 - 2) < heading) && (heading < (val3 + 2 )))
          {
          myservo.write(90);  //stop
          //Serial.print("ARRIVAL");
          //displaySensor();
          val = 'z';
          }   
      }
        
    
    if ((val2 > 1000)&&(val2 < 2000)){
      ms = val2 - 1000;   //change map step size
    }   
    
    if (val2 > 2000){
      nms = val2 - 2000;   //change nudge size
    }
    if (val2 > 3000){
      vms = val2 - 3000;   //change vertical size
    }
}



void setup() 
{ 
  myservo.attach(9);         // attaches the servo on pin 9 to the servo object 
  myservo2.attach(10);       

  motor.setSpeed(0);         // just to make sure the motor is stopped
  motor.run(RELEASE);

  Serial.begin(9600);    // start serial communication at 9600bps 

  mag.enableAutoRange(true);
  if(!mag.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println("Ooops, no LSM303 detected ... Check your wiring!A");
    myservo.write(90);
    myservo2.write(90);

    while(1);
  }

  /* Initialise the sensor */
  if(!accel.begin())
  {
    /* There was a problem detecting the ADXL345 ... check your connections */
    Serial.println("Ooops, no LSM303 detected ... Check your wiring!B");
    myservo.write(90);
    myservo2.write(90);
    while(1);
  }

}

void loop() { 

  if( Serial.available() )       // if data is available to read 
  { 
    val = Serial.read();         // read it and store it in 'val'   
    val2 = Serial.parseFloat();   // filters out numbers
  }


  switch( val )        //   switch handles incoming commands
  {    
    case 'x':            // x needs to precede ALT/ AZ commands and stepsize commands
    if (val2 >10){
    gotoY();}
    break;         

    case 'w':                         //  nudging directionals -- up
    myservo2.write(80);
    i = 0; 
    while (i <  ms){ 
    i=i+1; 
    delay(1);
    }
    val = 'z';
    break;
    
    case 'a':                         //  nudging directionals -- down
    myservo2.write(100);
    i = 0; 
    while (i <  ms){ 
    i=i+1; 
    delay(1);
    }
    val = 'z';
    break;
    
    case 'q':                         //  nudging directionals -- left
    myservo.write(95);
    i = 0; 
    while (i <  nms){ 
    i=i+1; 
    delay(1);
    }
    val = 'z';
    break;
    
    case 's':                         //  nudging directionals -- right
    myservo.write(85);
    i = 0; 
    while (i <  nms){ 
    i=i+1; 
    delay(1);
    }
    val = 'z';
    break;
    
    case 'o':                         //  mapping directionals  -- up
    myservo2.write(100);
    i = 0; 
    while (i <  vms){ 
    i=i+1; 
    delay(1);
    }
    val = 'z';
    break;
    
    case 'l':                          //  mapping directionals  -- down
    myservo2.write(80);
    i = 0; 
    while (i <  vms){ 
    i=i+1; 
    delay(1);
    }
    val = 'z';
    break;
    
    case 'k':                          //  mapping directionals  -- left
    myservo.write(95);
    i = 0; 
    while (i <  ms){ 
    i=i+1; 
    delay(1);
    }
    val = 'z';
    break;
    
    case 'p':                          //  mapping directionals  -- right
    myservo.write(85);
    i = 0; 
    while (i <  ms){ 
    i=i+1; 
    delay(1);
    }
    val = 'z';
    break;
    

  case 'f':                // Focus motor controls   IN  
    motor.setSpeed(255);
    motor.run(FORWARD);
    i = 0; 
    while (i <  ms){ 
    i=i+1; 
    delay(1);
    }
    val = 'z';
    motor.run(RELEASE);
    //Serial.println("focus 1");
    break;       

  case 'c':       //  STOP
    motor.run(RELEASE);
    //Serial.println("focus stop");
    break;               

  case 't':       //  OUT
    motor.setSpeed(255);
    motor.run(BACKWARD);
    i = 0; 
    while (i <  ms){ 
    i=i+1; 
    delay(1);
    }
    motor.run(RELEASE);
    val = 'z';
    break;


  case '1':                         //  directionals  X
    myservo.write(95);    
    //Serial.println("1 - CounterClockwise Fast");
    break; 

  case '2':                   
    myservo.write(93);    
    //Serial.println("2 - CounterClockwise");
    break;

  case '3':          
    myservo.write(90);
    //Serial.println("3 - Stop x");
    break;

  case '4':
    myservo.write(83);
    //Serial.println("8 - Clockwise");
    break;

  case '5':
    myservo.write(86);
    //Serial.println("9 - Clockwise Fast");
    break;        

  case '6':        
    myservo2.write(105); 
    //Serial.println("6 - down fast");
    break;     

  case '7':      
    myservo2.write(100); 
    //Serial.println("7 - down");
    break;       

  case '8':
    myservo2.write(90);
    break;

  case '9':
    myservo2.write(80);
    //Serial.println("9 - up");
    break;

  case '0':
    myservo2.write(75);
    //Serial.println("0 - up fast");
    break;

  case 'n':
    myservo2.write(90);
    myservo.write(90);
    displaySensor();
    //Serial.println("all stop");
    break;


  default :        
    myservo.write(90);
    myservo2.write(90);

    
    
  }
  
  

} 

