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
    
    // Cores (0xRRGGBB)
    static constexpr long RED = 0xFF0000;
    static constexpr long GREEN = 0x00FF00;
    static constexpr long BLUE = 0x000080;
    
    // Ajuste da sensibilidade
    static constexpr int SENSI = 50;
};

