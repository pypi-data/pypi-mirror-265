from .features import Service

class bookmyshow(Service):

    @property
    def service(self):
        return "BookMyShow"
    
    @property
    def content(self):
        return "As you a movie finder assistant, your task is to return the list of movies and their respective URLS from the output of list of movie names and their respective URLs in a natural language always. if input have language, description, publish date, url, duration , return them in a natural language always in multiple lines with lot of new lines"
    
    @property
    def tools(self):
        return  {
            "name": "find_movie",
            "description": "Find a movie",
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_language": {
                        "type": "string",
                        "description": "The language of the movie"
                    },
                    "city": {
                        "type": "string",
                        "description": "The city to find the movie",
                        "default": "Bengaluru"
                    },
                    "movie_name": {
                        "type": "string",
                        "description": "The name of the movie",
                        "default": "dummy"
                        }
                }
            },
            "required": ["movie_language","city"]
            
        }