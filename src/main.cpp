#include <Arduino.h>

#include "interfaces/utils.h"
#include "interfaces/Config.h"

utils util(Config::RED_PIN, Config::GREEN_PIN, Config::BLUE_PIN, Config::BUZZER_PIN);

void setup()
{
    pinMode(Config::RED_PIN, OUTPUT);
    pinMode(Config::GREEN_PIN, OUTPUT);
    pinMode(Config::BLUE_PIN, OUTPUT);
    pinMode(Config::BUZZER_PIN, OUTPUT);
}

void loop()
{
    int gsr = analogRead(Config::SENSOR_PIN);
    int pot = analogRead(Config::POT_PIN);
    if (gsr > pot + Config::SENSI)
    {
        util.setColor(Config::RED);
        util.beep();
    }
    else if (gsr < pot - Config::SENSI)
    {
        util.setColor(Config::BLUE);
    }
    else
    {
        util.setColor(Config::GREEN);
    }
}
