import json
import re
import hashlib
import random

class RasaFAQGenerator():
    def __init__(self, 
                 data_dic = None, 
                 nlu_yaml_fn = 'nlu_faq.yml', 
                 nlu_domain_fn = 'domain_faq.yml', 
                 limit_terms_to = None):
        self.request_patterns = [
            "Что означает {}",
            "Что такое {}",
            "Что значит термин {}"
        ]
        self.data_dic = data_dic
        self.nlu_yaml_fn = nlu_yaml_fn
        self.domain_yaml_fn = nlu_domain_fn
        self.limit_terms_to = limit_terms_to

        if data_dic:
            self.nlu_data = self.import_data()

    def read_json(self, input_fn):
        with open(input_fn) as f:
            self.data_dic = json.load(f)
        assert len(self.data_dic) > 0, "Faild to load data from JSON. No records loaded."
        self.nlu_data = self.import_data()

    def import_data(self, data_dic = None):
        if self.data_dic is None and data_dic is None:
            raise "No data provided"
        elif data_dic is not None:
            return self.gen_nlu_data(data_dic)
        else:
            return self.gen_nlu_data(self.data_dic)

    def gen_nlu_data(self, data_dic):
        nlu_data = []
        if self.limit_terms_to:
            data_dic = random.sample(data_dic, k=self.limit_terms_to)
        re_whatis = re.compile("Что такое (.+)")
        for item in data_dic:
            # Пропускаем термины без нормального описания:
            # - длинной менее 15 символов
            if len(item['desc_short']) < 30:
                continue
            # Составляем список примеров
            terms = []
            # Некоторые термины начинаются со слов "Что такое "
            whatis_match = re_whatis.match(item['term'])
            if whatis_match is not None:
                item['term'] = whatis_match.group(1)
            for request_pattern in self.request_patterns:
                terms.append(request_pattern.format(item['term']))
            
            # Для каждого термина генерируем hash
            term_hash = hashlib.sha1(item['term'].encode('utf-8')).hexdigest()
            # Если такого хэша ещё нет
            if term_hash not in [d['intent'] for d in nlu_data]:
                # Формируем dict
                nlu_item = {'intent': term_hash, 'examples': terms, 'text': item['desc_short']}
                # И добавляем
                nlu_data.append(nlu_item)
        return nlu_data

    def write_rasa_nlu(self, output_file = None):
        """
        #  - intent: chitchat/ask_name
        #    examples: |
        #      - What is your name?
        """
        if not output_file:
            output_file = self.nlu_yaml_fn
        ret = "nlu:\n"
        for block in self.nlu_data:
            ret += "  - intent: faq/{}\n".format(block['intent'])
            ret += "    examples: |\n"
            for example in block['examples']:
                ret += '      - "{}"\n'.format(example)
        with open(output_file, 'w') as f:
            f.writelines(ret)
        return 

    def write_rasa_domain(self, output_file = None):
        """
        #responses:
        #  utter_chitchat/ask_name:
        #  - image: "https://i.imgur.com/zTvA58i.jpeg"
        #    text: Hello, my name is Retrieval Bot.
        """
        if not output_file:
            output_file = self.domain_yaml_fn
        ret = "responses:\n"
        for block in self.nlu_data:
            ret += '  utter_faq/{}:\n'.format(block['intent'])
            ret += '  - text: "{}"\n'.format(block['text'].replace('"','\\"'))
        with open(output_file, 'w') as f:
            f.writelines(ret)
        return 