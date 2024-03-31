import pandas as pd


class Greetings:
    @staticmethod
    def say_hello():
        languages = ['English', 'French', 'Spanish', 'German']
        greetings_dict = {
            'English': 'Hello World',
            'French': 'Bonjour le monde',
            'Spanish': 'Hola Mundo',
            'German': 'Hallo Welt',
            # Add more languages and greetings as needed
        }
        greetings = [greetings_dict.get(
            lang, 'Unknown language') for lang in languages]
        data = {'Language': languages, 'Greeting': greetings}
        return pd.DataFrame(data)
