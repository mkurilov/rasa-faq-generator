# rasa-faq-generator
RasaFAQGenerator is a python class for generating NLU data suitable for training Rasa engine. It is most suitable if you have JSON-formated data and need to convert it to a set of YAML files that Rasa unerstands.

## Usage
There are two ways to provide data to generator.
1. You can eigher create class instance followed by `import_data` methon call or by creating instance with `data_dic` attribute. In both cases you must provide python dict variable with keys and values, described within the JSON file format section
1. You can call `read_json` method to load json-formated file.

You can find an example of using the generator in generate_nlu_data.py script within this project.

## JSON file format
The RasaFAQGenerator can read a file formated the following way:
```json
[
{"term": "The term you are describing (your question)", "desc_short": "Description of the term. This would be an answer which Rasa will be using when user requests for describe the term"},
...
]
```
