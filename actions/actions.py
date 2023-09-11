import os
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from swiplserver import PrologMQI


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
class ActionShowPhotos(Action):

    def name(self) -> Text:
        return "action_show_photo"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        folder_path = "C:\\Users\\jmgoi\\OneDrive\\Documentos\\Facultad\\porg exploratoria\\fotos hotel"

        photo_files = [f for f in os.listdir(folder_path) if f.endswith((".jpg", ".png", ".jpeg"))]

        # Envía cada foto como respuesta
        for photo_file in photo_files:
            photo_path = os.path.join(folder_path, photo_file)
            dispatcher.utter_message(image=photo_path)

        # Define una ranura (slot) para rastrear la respuesta del usuario
        return []
class ActionMoreInfo(Action):

    def name(self) -> Text:
        return "action_more_info"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        info = next(tracker.get_latest_entity_values("det"),None)
        foto =next(tracker.get_latest_entity_values("fot"),None)

        if foto is None and info is not None:
            dispatcher.utter_template("utter_more_info", tracker=tracker)
        elif foto is not None and info is None:
            dispatcher.utter_action_trigger("action_show_photo")
        # Define una ranura (slot) para rastrear la respuesta del usuario
        return []

class ActionProvideInfo(Action):

    def name(self) -> Text:
        return "action_provide_help"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        doubt_value = tracker.get_slot("doubt")

        # Define las respuestas basadas en el valor de 'doubt' según domain.yml
        response_messages = {
            "hospedaje": "utter_hospedaje",
            "destino": "utter_destino",
            "traslado": "utter_traslado",
            "precio": "utter_precio",
            "paquete": "utter_paquete",
            "fecha": "utter_fecha",
            "sorpresas": "utter_sorpresas",
            "reserva": "utter_reserva",
            "compra": "utter_compra"
        }

        # Verifica si el valor de 'doubt' tiene una respuesta asociada
        if doubt_value in response_messages:
            # Utiliza dispatcher para enviar la respuesta basada en 'doubt'
            dispatcher.utter_template(response_messages[doubt_value], tracker)
        else:
            dispatcher.utter_message(text="No estoy seguro de cómo puedo ayudarte en este momento.")

        return []
class ActionMoreHelp(Action):

    def name(self) -> Text:
        return "action_more_help"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        preg = tracker.get_slot("preguntar_mas_informacion")

        while preg:
            dispatcher.utter_template("utter_more_help")
            ActionListen(Action)
            ActionSaveConsulta(Action)
            
        return[]   
class ActionSendLink(Action):

    def name(self) -> Text:
        return "action_send_link"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        # Define el enlace que deseas enviar como respuesta
        enlace = "https://www.ejemplo.com"

        # Crea el mensaje que contiene el enlace
        message = f"¡Aquí tienes un enlace interesante: [{enlace}]({enlace})"

        # Envía el mensaje con el enlace
        dispatcher.utter_message(text=message)

        return []
        