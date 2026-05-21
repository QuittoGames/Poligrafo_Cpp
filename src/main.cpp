#include <Arduino.h>

const int RED_PIN = 11;
const int GREEN_PIN = 10;
const int BLUE_PIN = 9;
const int BUZZER_PIN = 7;

const int POT_PIN = 1;
const int SENSOR_PIN = 0;

const long RED = 0xFF0000;
const long GREEN = 0x00FF00;
const long BLUE = 0x000080;

const int SENSI = 50;
//ajuste da sensibilidade

void setup()
{
    pinMode(RED_PIN, OUTPUT);
    pinMode(GREEN_PIN, OUTPUT);
    pinMode(BLUE_PIN, OUTPUT);
    pinMode(BUZZER_PIN, OUTPUT);
}

void loop()
{
    int gsr = analogRead(SENSOR_PIN);
    int pot = analogRead(POT_PIN);
    if (gsr > pot + SENSI)
    {
        setColor(RED);
        beep();
    }
    else if (gsr < pot - SENSI)
    {
        setColor(BLUE);
    }
    else
    {
        setColor(GREEN);
    }
}

void setColor(long rgb)
{
    int red = rgb >> 16;
    int green = (rgb >> 8) & 0xFF;
    int blue = rgb & 0xFF;
    analogWrite(RED_PIN, red);
    analogWrite(GREEN_PIN, green);
    analogWrite(BLUE_PIN, blue);
}

void beep()
{
    // 5 khz para 1/5 de segundo
    for (int i = 0; i < 1000; i++)
    {
        digitalWrite(BUZZER_PIN, HIGH);
        delayMicroseconds(100);
        digitalWrite(BUZZER_PIN, LOW);
        delayMicroseconds(100);
    }
}