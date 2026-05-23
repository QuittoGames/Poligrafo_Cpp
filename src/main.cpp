#include <Arduino.h>
#include <math.h>

#include "interfaces/utils.h"
#include "interfaces/Config.h"

utils util(Config::RED_PIN, Config::GREEN_PIN, Config::YELLOW_PIN, Config::BUZZER_PIN);

void setup()
{
    pinMode(Config::RED_PIN, OUTPUT);
    pinMode(Config::GREEN_PIN, OUTPUT);
    pinMode(Config::YELLOW_PIN, OUTPUT);
    pinMode(Config::BUZZER_PIN, OUTPUT);

    Serial.begin(Config::SERIAL_BAUD);

    util.setColor(Config::GREEN);
    Serial.println("[INFO] Calibrando baseline do GSR...");
    delay(3000); // estabiliza antes de calibrar
    util.calibrateBaseline();

    Serial.print("[INFO] Baseline: ");
    Serial.println(util.getBaseline(), 2);
    delay(1000);
}


void loop()
{    
    const double gsr = util.readGsrFiltered();

    Serial.print("[INFO] GSR: ");
    Serial.print(gsr);
    Serial.print(" BASELINE: ");
    Serial.println(util.getBaseline(), 2);

    const double diff = fabs(gsr - util.getBaseline());

    Serial.print("DIFF: ");
    Serial.println(diff, 2);

    if (diff > 200.0) {
        util.setColor(Config::GREEN);
        util.beep(120, 500U);
        Serial.println("State: SEM CONTATO");
        delay(1000);
        return;
    }

    if (diff > Config::SENSI)
    {
        util.setColor(Config::RED);
        util.beep(250, 500U);
        Serial.println("[ALERT] State: PICO DETECTADO");
    }
    else if (diff > Config::SENSI / 2.5)
    {
        util.setColor(Config::YELLOW);
        util.beep(160, 500U);
        Serial.println("[WARN] State: VARIACAO LEVE");
    }
    else
    {
        util.setColor(Config::GREEN);
        Serial.println("[OK] State: ESTAVEL");
    }

    delay(1000);
}
