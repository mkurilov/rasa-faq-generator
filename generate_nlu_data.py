from rasa_faq_generator import RasaFAQGenerator

gen = RasaFAQGenerator(limit_terms_to = 100)
gen.read_json('../data/bankiru_faq.json')
gen.write_rasa_nlu('../data/nlu_faq.yml')
gen.write_rasa_domain('../domain_faq.yml')