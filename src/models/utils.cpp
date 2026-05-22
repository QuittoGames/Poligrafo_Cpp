#include "../interfaces/utils.h"

utils::utils(int redPin, int greenPin, int bluePin, int buzzerPin)
    : redPin_(redPin),
      greenPin_(greenPin),
      bluePin_(bluePin),
      buzzerPin_(buzzerPin)
{
}

void utils::setColor(long rgb) const
{
    // unit8 = inteiro sem sinal de 8 bits.
    // static_cast = traformação de de tipos em C++ moderno 
    const uint8_t red = static_cast<uint8_t>((rgb >> 16) & 0xFF);
    const uint8_t green = static_cast<uint8_t>((rgb >> 8) & 0xFF);
    const uint8_t blue = static_cast<uint8_t>(rgb & 0xFF);

    analogWrite(redPin_, red);
    analogWrite(greenPin_, green);
    analogWrite(bluePin_, blue);
}

void utils::beep(unsigned int cycles, unsigned int halfPeriodMicros) const
{
    for (unsigned int i = 0; i < cycles; i++)
    {
        digitalWrite(buzzerPin_, HIGH);
        delayMicroseconds(halfPeriodMicros);
        digitalWrite(buzzerPin_, LOW);
        delayMicroseconds(halfPeriodMicros);
    }
}
