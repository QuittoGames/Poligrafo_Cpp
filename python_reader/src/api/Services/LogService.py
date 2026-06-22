from src.api.model.Log import Log
from src.api.data.core.deps.deps import get_data
import json

class LogService:
    def __init__(self):
        pass

    def create_log() -> bool:
        try:
            states = get_data().latest_state
            if not states :
                raise RuntimeError("Sem dados disponíveis")
            
            log:Log = Log(data_state=states)
            data_json:dict = log.serialize_toJSON()
            data_log:str = log.serialize_toLog() 
            
            with open("poligrafo.json", "w", encoding="utf-8") as file:
                json.dump(data_json, file, indent=4, ensure_ascii=False)

            with open("poligrafo.log", "w", encoding="utf-8") as file:
                json.dump(data_log, file, indent=4, ensure_ascii=False)

            return True
        except Exception as e:
            raise RuntimeError(f"Erro inesperado ao criar log: {e}")
    