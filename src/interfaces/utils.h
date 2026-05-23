#pragma once

#include <Arduino.h>

class utils
{
public:
    utils(int redPin, int greenPin, int yellowPin, int buzzerPin);

    void setColor(long rgb) const;
    void beep(unsigned int cycles = 1000, unsigned int halfPeriodMicros = 100) const;
    double readGsrFiltered() const;
    void calibrateBaseline();
    double getBaseline() const;

private:
    int redPin_;
    int greenPin_;
    int yellowPin_;
    int buzzerPin_;
    double baseline_ = 0.0;
};
