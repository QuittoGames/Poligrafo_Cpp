#include <Arduino.h>

#include "interfaces/utils.h"
#include "interfaces/Config.h"

utils util(Config::RED_PIN, Config::GREEN_PIN, Config::BLUE_PIN, Config::BUZZER_PIN);


//get value for grs with security 
namespace
{
    int baseline = 0;
    unsigned long warmupStartMs = 0;

    int readGsrFiltered()
    {
        long sum = 0;

        for (int i = 0; i < Config::READ_SAMPLES; i++)
        {
            sum += analogRead(Config::SENSOR_PIN);
            delay(Config::READ_DELAY_MS);
        }

        return static_cast<int>(sum / Config::READ_SAMPLES);
    }

    // Create media for values of grs
    void calibrateBaseline()
    {
        long sum = 0;

        for (int i = 0; i < Config::CALIBRATION_SAMPLES; i++)
        {
            sum += analogRead(Config::SENSOR_PIN);
            delay(Config::CALIBRATION_DELAY_MS);
        }

        baseline = static_cast<int>(sum / Config::CALIBRATION_SAMPLES);
    }
}

void setup()
{
    pinMode(Config::RED_PIN, OUTPUT);
    pinMode(Config::GREEN_PIN, OUTPUT);
    pinMode(Config::BLUE_PIN, OUTPUT);
    pinMode(Config::BUZZER_PIN, OUTPUT);

    Serial.begin(Config::SERIAL_BAUD);

    util.setColor(Config::GREEN);
    Serial.println("[INFO] Calibrando baseline do GSR...");
    delay(3000); // estabiliza antes de calibrar
    calibrateBaseline();
    warmupStartMs = millis();

    Serial.print("[INFO] Baseline: ");
    Serial.println(baseline);
    delay(1000);
}


void loop()
{    
    const int gsr = readGsrFiltered();

    Serial.print("[INFO] GSR: ");
    Serial.print(gsr);
    Serial.print(" BASELINE: ");
    Serial.println(baseline);

    int diff = abs(gsr - baseline);

    Serial.print("DIFF: ");
    Serial.println(diff);

    if (diff < 2 || diff > 200) {
        util.setColor(Config::BLUE);
        Serial.println("SEM CONTATO");
        return;
    }

    if (diff > Config::SENSI)
    {
        util.setColor(Config::RED);
        Serial.println("PICO DETECTADO");
    }
    else if (diff > Config::SENSI / 2)
    {
        util.setColor(Config::BLUE);
        Serial.println("VARIACAO LEVE");
    }
    else
    {
        util.setColor(Config::GREEN);
        Serial.println("ESTAVEL");
    }

    delay(100);
}
