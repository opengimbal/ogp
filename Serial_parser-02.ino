


String inPut = "";

float val_02 = 0;

String command; // strig data to pull in the serial buffer





void setup() 
{
  
  Serial.begin(9600); // sets serial
  pinMode(LED_BUILTIN, OUTPUT);
  inPut.reserve(200); // limits the input for commands, will be modified later
}


void parseCommand(String com)
{

  // TEMP CODE all of this code will be retuned to the main Arduino controller
   String part1;
   String part2; 
   int sendBytes;

   part1 = com.substring(0,com.indexOf(" ")); //substring takes a subpart of a string in 2 arrguments the start part and up till. This one is start 0 up until the index of the space
   part2 = com.substring(com.indexOf(" ") +1);// take anything after the space pluse one character, so it's selecting the character after the space
  
   if(part1.equalsIgnoreCase("a001")) // if the string is a001 ignoring the case of the characters
   {
     int pin = part2.toInt();// sends 
     digitalWrite(LED_BUILTIN,HIGH);
     Serial.print(part1);   
    
   }
  if(part1.equalsIgnoreCase("a002")) // if the string is a001 ignoring the case of the characters
   {
     int pin = part2.toInt(); //converts part 2 to int for  an interger to part2 
     digitalWrite(LED_BUILTIN,LOW);
     Serial.print(part1);   
    
   }
}


boolean isUp; // switch for connection
boolean go() //setup state
{

  if(isUp == false)
  {
    Serial.println("inside stop loop");
    isUp = true;
    serialup();
  }
 delay(1000);


 return isUp;
}

void serialup()
{  

while (isUp == true)
  {
  if(Serial.available()) //if the serial is clear
  {
    char c = Serial.read(); // c is set for reading the serial
     
    if (c == '\n' ) // if there is an end of a line, clear command
    {
      Serial.print("Sent"); 
      parseCommand(command);// pass command to the the parsing function string com
      command = "";
    }

    else // append c to the command 
    {
      command += c;
      Serial.print("00"); 
    }
    }
  }
}


void loop() 
{
  isUp = go();
 
}






