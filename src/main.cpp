#include <Arduino.h>
#include <math.h>

#include "interfaces/utils.h"
#include "interfaces/Config.h"
#include "enum/State.hpp"

utils util(Config::RED_PIN, Config::GREEN_PIN, Config::YELLOW_PIN, Config::BUZZER_PIN);

void setup(){
    pinMode(Config::RED_PIN, OUTPUT);
    pinMode(Config::GREEN_PIN, OUTPUT);
    pinMode(Config::YELLOW_PIN, OUTPUT);
    pinMode(Config::BUZZER_PIN, OUTPUT);

    Serial.begin(Config::SERIAL_BAUD);

    util.setColor(Config::GREEN);
    Serial.println();
    Serial.println(":: POLIGRAFO ::");
    Serial.println("Inicializando interface GSR...");
    Serial.println("Mantenha os dedos no sensor...");
    Serial.println("Calibrando baseline...");
    Serial.println();
    delay(3000); // estabiliza antes de calibrar
    util.calibrateBaseline();

    Serial.print("[INFO] Baseline: ");
    Serial.println(util.getBaseline(), 2);
    delay(1000);
}


void loop(){
    const double gsr = util.readGsrFiltered();

    const double diff = fabs(gsr - util.getBaseline());

    State state = State::NONE;

    if (diff > 200.0) {
        util.setColor(Config::RED);
        util.beep(120, 500U);
        state = State::NOT_CONNECTED;

        delay(1000);
        return;
    }

    if (diff > Config::SENSI)
    {
        util.setColor(Config::RED);
        util.beep(200, 500U);
        state = State::PICO_DETECTADO;
    }
    else if (diff > Config::SENSI / 2.5)
    {
        util.setColor(Config::YELLOW);
        state = State::VARIACAO_LEVE;
    }
    else
    {
        util.setColor(Config::GREEN);
        state = State::ESTAVEL;
    }

    Serial.print("---------------------------------------");
    Serial.print("[DATA] ");
    Serial.print("GSR=");
    Serial.print(gsr, 2);
    Serial.print(" | BASELINE=");
    Serial.print(util.getBaseline(), 2);
    Serial.print(" | DIFF=");
    Serial.print(diff, 2);
    Serial.print(" | STATE=");
    const State* finalstate = &state;
    Serial.println(stateToString(finalstate));

    delay(1200);
}
