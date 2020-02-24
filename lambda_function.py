# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
#import request
import logging
import json
import requests
import decimal
import time
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

locations = {
    "De Neve": ["Flex Bar", "The Front Burner", "The Kitchen", "The Pizzeria", "The Grill"],
    "Covel": ["Exhibition Kitchen","Euro Kitchen", "Pizza Oven", "Grill"],
    "Bruin Plate": ["Freshly Bowled","Harvest","Stone Oven","Simply Grilled"]
}

def read_Menu (dining_hall):
    response = requests.get('http://44.232.86.238/dining/menu/overviewMenu')
    json_response= response.json()
    items = []
    for sublocation in locations[dining_hall]:
        for meal in json_response['menus'][0]['overviewMenu']['dinner'][dining_hall][sublocation]:
            items.append(meal['name'])
            
    return (', '.join(items))

def avg_nutrition(json_response, dining_hall, nutrition_type):
    total = 0
    count = 0
    truncate=2
    divisor=1000
    if nutrition_type!="Sodium":
        truncate=1
        divisor=1
    for sublocation in locations[dining_hall]:
        for meal in json_response['menus'][0]['overviewMenu']['dinner'][dining_hall][sublocation]:
            total += float(meal['nutrition'][nutrition_type][0][:-truncate]) / divisor
            count += 1
    
    return total / count

def all_avg(nutrition_type):
    response = requests.get('http://44.232.86.238/dining/menu/overviewMenu')
    json_response= response.json();
    avg_sodium=[0.0,0.0,0.0]
    avg_sodium[0] = avg_nutrition(json_response, "Covel", nutrition_type)
    avg_sodium[1] = avg_nutrition(json_response, "De Neve", nutrition_type)
    avg_sodium[2] = avg_nutrition(json_response, "Bruin Plate", nutrition_type)
    return avg_sodium


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, you can say ask about carbs, sodium,or sugar"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class NameIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NameIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response = requests.get('http://44.232.86.238/dining/menu/overviewMenu')
        json_response= response.json()
        
        #const dininghall = handlerInput.requestEnvelope.request.intent.slots.dininghall
        #dininghallName= dininghall.value
        #dininghallName= "Covel"
        
        speak_output = ""+str(read_Menu("Covel"))
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class SugarIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SugarIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #speak_output = "Hello World test!"
        avg_sugar=all_avg("Sugars")
        speak_output= "Covel: "+str(round(avg_sugar[0],1))+ ". De Neve: "+str(round(avg_sugar[1],1))+" . Bruin Plate: "+str(round(avg_sugar[2],1))


        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class CarbIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CarbIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #speak_output = "Hello World test!"
        avg_carbs=all_avg("Total_Carbohydrate")
        speak_output= "Covel: "+str(round(avg_carbs[0],1))+ ". De Neve: "+str(round(avg_carbs[1],1))+" . Bruin Plate: "+str(round(avg_carbs[2],1))


        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class SodiumIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SodiumIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #speak_output = "Hello World test!"
        avg_sodium=all_avg("Sodium")
        speak_output= "Covel: "+str(round(avg_sodium[0],1))+ ". De Neve: "+str(round(avg_sodium[1],1))+" . Bruin Plate: "+str(round(avg_sodium[2],1))


        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


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
sb.add_request_handler(SugarIntentHandler())
sb.add_request_handler(SodiumIntentHandler())
sb.add_request_handler(CarbIntentHandler())
sb.add_request_handler(NameIntentHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
