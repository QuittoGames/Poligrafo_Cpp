#include "../interfaces/utils.h"
#include "../interfaces/Config.h"


utils::utils(int redPin, int greenPin, int yellowPin, int buzzerPin)
    : redPin_(redPin),
      greenPin_(greenPin),
    yellowPin_(yellowPin),
      buzzerPin_(buzzerPin)
{
}

void utils::setColor(long color) const{
    digitalWrite(redPin_, LOW);
    digitalWrite(greenPin_, LOW);
    digitalWrite(yellowPin_, LOW);

    if (color == Config::RED)
        digitalWrite(redPin_, HIGH);

    else if (color == Config::GREEN)
        digitalWrite(greenPin_, HIGH);

    else if (color == Config::YELLOW)
        digitalWrite(yellowPin_, HIGH);
}

void utils::beep(unsigned int cycles, unsigned int halfPeriodMicros) const{
    for (unsigned int i = 0; i < cycles; i++){
        digitalWrite(buzzerPin_, HIGH);
        delayMicroseconds(halfPeriodMicros);
        digitalWrite(buzzerPin_, LOW);
        delayMicroseconds(halfPeriodMicros);
    }
}

double utils::readGsrFiltered() const{
    long sum = 0;

    for (int i = 0; i < Config::READ_SAMPLES; i++){
        sum += analogRead(Config::SENSOR_PIN);
        delay(Config::READ_DELAY_MS);
    }

    return static_cast<double>(sum) / static_cast<double>(Config::READ_SAMPLES);
}

void utils::calibrateBaseline(){
    long sum = 0;

    for (int i = 0; i < Config::CALIBRATION_SAMPLES; i++){
        sum += analogRead(Config::SENSOR_PIN);
        delay(Config::CALIBRATION_DELAY_MS);
    }

    baseline_ = static_cast<double>(sum) / static_cast<double>(Config::CALIBRATION_SAMPLES);
}

double utils::getBaseline() const{
    return baseline_;
}
