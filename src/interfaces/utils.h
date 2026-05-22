#pragma once

#include <Arduino.h>

class utils
{
public:
    utils(int redPin, int greenPin, int bluePin, int buzzerPin);

    void setColor(long rgb) const;
    void beep(unsigned int cycles = 1000, unsigned int halfPeriodMicros = 100) const;

private:
    int redPin_;
    int greenPin_;
    int bluePin_;
    int buzzerPin_;
};
