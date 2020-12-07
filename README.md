# rasa-faq-generator
RasaFAQGenerator is a python class for generating NLU data suitable for training Rasa engine. It is most suitable if you have JSON-formated data and need to convert it to a set of YAML files that Rasa unerstands.

## Usage
You can find an example of how to use this class in generate_nlu_data.py script within this project.

## JSON file format
The RasaFAQGenerator can read a file formated the following way:
[
{"term": "The term you are describing (your question)", "desc_short": "Description of the term. This would be an answer which Rasa will be using when user requests for describe the term"},
...
]
