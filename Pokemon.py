import requests 
import simplejson


class Move(object):

    def __init__(move):
        pass

class Pokemon:
    api_url = "https://pokeapi.co/api/v2/{}/{}"
    def __init__(self, pokemon_name):
        self.name = pokemon_name
        self.__make_request(method_name="pokemon")
        self.__make_request(method_name="pokemon-species")

    def __make_request(self, method_name="pokemon", method="get", params=None):
        if not params:
            params = {}
        url  = self.api_url.format(method_name, self.name)
        if method == "get":
            response = requests.get(url)
        
        if response.status_code in range(200,300):
            self.__transform_json_to_self(response.json())


    def __transform_json_to_self(self, json):
        for key, value in json.items():
            setattr(self, key, value)




    