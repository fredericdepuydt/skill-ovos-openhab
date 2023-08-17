from ovos_utils import classproperty
from ovos_utils.intents import IntentBuilder
from ovos_utils.process_utils import RuntimeRequirements
from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill

import requests
import json
from requests.auth import HTTPBasicAuth

class OpenHABSkill(OVOSSkill):
    def __init__(self, *args, **kwargs):
        """The __init__ method is called when the Skill is first constructed.
        Note that self.bus, self.skill_id, self.settings, and
        other base class settings are only available after the call to super().

        This is a good place to load and pre-process any data needed by your
        Skill, ideally after the super() call.
        """
        super().__init__(*args, **kwargs)

        self.command_headers = {"Content-type": "text/plain"}
        self.polling_headers = {"Accept": "application/json"}        
        self.url = "http://openhab.automation:8080/rest"
        self.auth = HTTPBasicAuth('frederic.depuydt@outlook.com', 'Dq40n!ZN6U54MwO33B7jbAbtnj7i9BMw')
        self.learning = True
        self.getTaggedItems()



    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(
            internet_before_load=False,
            network_before_load=False,
            gui_before_load=False,
            requires_internet=False,
            requires_network=False,
            requires_gui=False,
            no_internet_fallback=True,
            no_network_fallback=True,
            no_gui_fallback=True,
        )

    @property
    def get_my_setting(self):
        """Dynamically get the my_setting from the skill settings file.
        If it doesn't exist, return the default value.
        This will reflect live changes to settings.json files (local or from backend)
        """
        return self.settings.get("my_setting", "default_value")

    @intent_handler(IntentBuilder("ThankYouIntent").require("ThankYouKeyword"))
    def handle_thank_you_intent(self, message):
        """This is an Adapt intent handler, it is triggered by a keyword."""
        self.speak_dialog("ItemNotFoundError")


    @intent_handler(IntentBuilder("ListOpenHABItemsIntent").require("ListItemsKeyword"))
    def handle_list_openhab_items_intent(self, message):
        """This is an Adapt intent handler, it is triggered by a keyword."""
        self.speak_dialog("ConfigurationNeeded")


    @intent_handler("HowAreYou.intent")
    def handle_how_are_you_intent(self, message):
        """This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        self.speak_dialog("how.are.you")

    @intent_handler(IntentBuilder("HelloWorldIntent").require("HelloWorldKeyword"))
    def handle_hello_world_intent(self, message):
        """Skills can log useful information. These will appear in the CLI and
        the skills.log file."""
        self.log.info("There are five types of log messages: " "info, debug, warning, error, and exception.")
        self.speak_dialog("hello.world")

    def stop(self):
        """Optional action to take when "stop" is requested by the user.
        This method should return True if it stopped something or
        False (or None) otherwise.
        If not relevant to your skill, feel free to remove.
        """
        pass
    
    def getTaggedItems(self):
        #find all the items tagged Lighting and Switchable from openHAB
        #the labeled items are stored in dictionaries

        self.lightingItemsDic = {}
        self.switchableItemsDic = {}
        self.currentTempItemsDic = {}
        self.currentHumItemsDic = {}
        self.currentThermostatItemsDic = {}
        self.targetTemperatureItemsDic = {}
        self.homekitHeatingCoolingModeDic = {}

        if self.url == None:
            self.log.error("Configuration needed!")
            self.speak_dialog('ConfigurationNeeded')
        else:            
            requestUrl = self.url+"/items?recursive=false"

            try: 
                req = requests.get(requestUrl, headers=self.polling_headers, auth=self.auth)
                if req.status_code == 200:
                    json_response = req.json()
                    self.log.info("Found " + str(len(json_response)) + " items in OpenHAB")
                    for x in range(0,len(json_response)):
                        
                        if ("Lighting" in json_response[x]['tags']):
                            self.lightingItemsDic.update({json_response[x]['name']: json_response[x]['label']})
                        elif ("Switchable" in json_response[x]['tags']):
                            self.switchableItemsDic.update({json_response[x]['name']: json_response[x]['label']})
                        elif ("CurrentTemperature" in json_response[x]['tags']):
                            self.currentTempItemsDic.update({json_response[x]['name']: json_response[x]['label']})
                        elif ("CurrentHumidity" in json_response[x]['tags']):
                            self.currentHumItemsDic.update({json_response[x]['name']: json_response[x]['label']})
                        elif ("Thermostat" in json_response[x]['tags']):
                            self.currentThermostatItemsDic.update({json_response[x]['name']: json_response[x]['label']})
                        elif ("TargetTemperature" in json_response[x]['tags']):
                            self.targetTemperatureItemsDic.update({json_response[x]['name']: json_response[x]['label']})
                        elif ("homekit:HeatingCoolingMode" in json_response[x]['tags']):
                            self.homekitHeatingCoolingModeDic.update({json_response[x]['name']: json_response[x]['label']})
                        else:
                            pass
                else:
                    self.log.error("HTTP " + str(req.status_code ))
                    self.speak_dialog('GetItemsListError')
            except KeyError:
                    pass
            except Exception as ex:
                    self.log.error("Exception thrown: " + str(ex))
                    self.speak_dialog('GetItemsListError')
