#include "../interfaces/utils.h"
#include "../interfaces/Config.h"


utils::utils(int redPin, int greenPin, int bluePin, int buzzerPin)
    : redPin_(redPin),
      greenPin_(greenPin),
      bluePin_(bluePin),
      buzzerPin_(buzzerPin)
{
}

void utils::setColor(long color) const
{
    digitalWrite(redPin_, LOW);
    digitalWrite(greenPin_, LOW);
    digitalWrite(bluePin_, LOW);

    if (color == Config::RED)
        digitalWrite(redPin_, HIGH);

    else if (color == Config::GREEN)
        digitalWrite(greenPin_, HIGH);

    else if (color == Config::BLUE)
        digitalWrite(bluePin_, HIGH);
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
