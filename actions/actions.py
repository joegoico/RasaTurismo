# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
    
class ActionSaveName(Action):

    def name(self) -> Text:
      return "action_save_name"

    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

      nombre = next(tracker.get_latest_entity_values("nombre"),None)
      
      message = "¡Gracias, {nombre}!. Contame, ¿en que puedo ayudarte?".format(nombre)
      dispatcher.utter_message(text = message)
        
      return [SlotSet("name", nombre)]

class ActionSaveConsulta(Action):

    def name(self) -> Text:
        return "action_save_consulta"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        consulta = next(tracker.get_latest_entity_values("consulta"),None)
        n = tracker.get_slot("name")
        
        message = "Perfecto {n} , decime que necesitas acerca de {}".format(n,consulta)
        
        dispatcher.utter_message(text = message)
    
        return [SlotSet("doubt", consulta)]

