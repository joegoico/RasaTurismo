import time
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from swiplserver import PrologMQI, PrologThread

class ActionTraslados(Action):
    def name(self) -> Text:
        return "action_traslados"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        doubt = tracker.get_slot("doubt")
        
        with PrologMQI() as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query("consult('prolog.pl').")
                if doubt == "destino":
                    response = prolog_thread.query("consultar_destinos(Codigo, Tipo, Nombre)")
                elif doubt == "hospedaje":
                    response = prolog_thread.query("consultar_hoteles(Codigo, Nombre, Estrellas, Camas, Ubicacion, Precio)")
                elif doubt == "traslado":
                    response = prolog_thread.query("consultar_traslados(Codigo, Nombre, Enlace)")
                else:
                    response = "no se encontraron resultados"
                
                # Obtener los resultados de Prolog
                results = list(response)
                
                print(results)
                dispatcher.utter_message(text=results)
        
        return []






        