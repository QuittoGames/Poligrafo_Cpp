#pragma once

#include <Arduino.h>

struct Config
{
    // Pinos
    static constexpr int RED_PIN = 11;
    static constexpr int GREEN_PIN = 10;
    static constexpr int BLUE_PIN = 9;
    static constexpr int BUZZER_PIN = 7;
    
    static constexpr int POT_PIN = 1;
    static constexpr int SENSOR_PIN = 0;

    // Serial
    static constexpr unsigned long SERIAL_BAUD = 9600;
    
    // Cores (0xRRGGBB)
    static constexpr int RED = 1;
    static constexpr int GREEN = 2;
    static constexpr int BLUE = 3;
    
    // Ajuste da sensibilidade
    static constexpr int SENSI = 10;

    // GSR: calibração/filtragem/estabilização
    static constexpr int CALIBRATION_SAMPLES = 300;
    static constexpr int CALIBRATION_DELAY_MS = 10;
    static constexpr int READ_SAMPLES = 10;
    static constexpr int READ_DELAY_MS = 5;
    static constexpr unsigned long WARMUP_MS = 5000;
};

