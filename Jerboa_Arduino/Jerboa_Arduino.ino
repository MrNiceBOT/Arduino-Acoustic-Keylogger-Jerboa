#include <SD.h>
#include <SPI.h>

#define PRESS_CUTOFF 550 // Trigger voltage (analog)
#define PRESS_SAMPLES 200
#define RELEASE_CUTOFF 280
#define RELEASE_SAMPLES 200

const int MIC_PIN = A0;
short count = 0;

// Define file
File file;

void setup() {
  Serial.begin(9600);
  pinMode(MIC_PIN, INPUT);

  if (!SD.begin(4)){
    Serial.println("Failed to initialise SD card.");
    while(true);
  }
  
  file = SD.open("data.txt", FILE_WRITE);

  file.close();
}

void loop() {  
      if (analogRead(MIC_PIN) > PRESS_CUTOFF){   
        count++;
        Serial.println(count);
        Serial.println("Triggered");
        String collect_string = "";

        for(int i = 0; i < PRESS_SAMPLES; i++){
          collect_string.concat(analogRead(MIC_PIN));
          collect_string.concat(" ");
          delayMicroseconds(10);
        }

        file = SD.open("data.txt", FILE_WRITE);
        file.print(collect_string);
        
        delay(32);

        collect_string = "";

        long int start = millis();

        while(analogRead(MIC_PIN) < RELEASE_CUTOFF && millis() - start < 150){}
        Serial.println("Released");

        for(int i = 0; i < RELEASE_SAMPLES; i++){
          collect_string.concat(analogRead(MIC_PIN));
          collect_string.concat(" ");
          delayMicroseconds(24);
        }

        file.println(collect_string);
        delay(200);
        file.close();
      }
}
