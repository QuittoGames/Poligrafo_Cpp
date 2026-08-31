# pragma once

enum class State{
    NONE,
    NOT_CONNECTED,
    ESTAVEL,
    VARIACAO_LEVE,
    PICO_DETECTADO
};

inline const char* stateToString(const State* state) {
    switch (*state) {
        case State::ESTAVEL:
            return "ESTAVEL";

        case State::VARIACAO_LEVE:
            return "VARIACAO_LEVE";

        case State::PICO_DETECTADO:
            return "PICO_DETECTADO";

        case State::NOT_CONNECTED:
            return "NOT_CONNECTED";

        default:
            return "NONE";
    }
}
