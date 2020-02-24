 # -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
#import request
import logging
import json
import requests
#import commands
#from commands import getstatusoutput

import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, you can say Hello or Help. Which would you like to try?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

locations = {
    "De Neve": ["Flex Bar", "The Front Burner", "The Kitchen", "The Pizzeria", "The Grill"],
    "Covel": ["Exhibition Kitchen","Euro Kitchen", "Pizza Oven", "Grill"],
    "Bruin Plate": ["Freshly Bowled","Harvest","Stone Oven","Simply Grilled"]
}

def avg_nutrition(json_response, dining_hall, nutrition_type):
    total = 0
    count = 0
    
    for sublocation in locations[dining_hall]:
        for meal in json_response['menus'][0]['overviewMenu']['dinner'][dining_hall][sublocation]:
            total += float(meal['nutrition'][nutrition_type][0][:-2]) / 1000
            count += 1
    
    return total / count

class sodiumHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Sodium")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #speak_output = "Hello World test!"
        response = requests.get('http://44.232.86.238/dining/menu/overviewMenu')
        json_response= response.json();
        """
        dining_halls=["Covel","De Neve","Bruin Plate"]
        covel_locations=["Exhibition Kitchen","Euro Kitchen", "Pizza Oven", "Grill"]
        deNeve_locations=["Flex Bar", "The Front Burner", "The Kitchen", "The Pizzeria", "The Grill"]
        bplate_locations=["Freshly Bowled","Harvest","Stone Oven","Simply Grilled"]
        dining_hall_locations=[covel_locations,deNeve_locations,bplate_locations]
        meal_time=["dinner"]
        """
        avg_sodium=[0.0,0.0,0.0]
        
        #covel
        covel_count=0
        avg_sodium[0] = avg_nutrition(json_response, "Covel", "Sodium")
        speak_output=str(avg_sodium[0])

        return (
            handler_input.response_builder
            .speak(speak_output)
             # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )

    def handle_local(self):
        response = requests.get('http://44.232.86.238/dining/menu/overviewMenu')
        json_response= response.json();
        avg_sodium=[0.0,0.0,0.0]
        #covel
        covel_count=0
        avg_sodium[0] = avg_nutrition(json_response, "Covel", "Sodium")
        speak_output=str(avg_sodium[0])
        return speak_output


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(sodiumHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

obj = sodiumHandler()
print(obj.handle_local())