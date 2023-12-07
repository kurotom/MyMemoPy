'''
'''

import locale

# from mimic_useragent import mimic_user_agent

from utils.languages_support import langs
from utils.parsers import calculate_remain_time
from text_wrapper import TextWrapper
from request_api import RequestApi

from users import (
    User,
    Anonymous,
    UserValid
)

from exceptions import (
    ApiGenericException,
    # ApiLimitUsageException,
    ApiEmailUserException,
    ApiLimitUsageException,
    EmptyTextException,
    ParameterErrorException,
    TimeOutUsage
)

from typing import Union


class MyMemoryTranslate:

    api_url = 'https://api.mymemory.translated.net'
    bytes_limit = 500
    line = '-' * 47

    def __init__(self, email: str = None):
        '''
        Constructor
        '''
        self.api = RequestApi(self.api_url)
        self.local_lang = locale.getlocale()[0].split('_')[0]
        self.code_langs = list(langs.values())
        self.textwrapper = TextWrapper()
        self.user = self.__select_user(email)

    def __select_user(
        self,
        email: str = None
    ) -> User:
        if email is None:
            user = Anonymous()
        else:
            user = UserValid(email=email)
        user.load_data()
        return user

    def show_languages(
        self,
        all: bool = False
    ) -> None:
        '''
        Print all languages and languages codes supported.
        '''
        s = 0
        e = 10
        items = list(langs.items())

        title = f'\n{"| Language".ljust(38)} | {"Code".ljust(4)} |\n'
        title += self.line
        print(title)

        while True:
            it = items[s:e]
            if it == []:
                break

            for i in it:
                print(f'| {i[0].ljust(36)} | {i[1].ljust(4)} |')

            if all and len(it) % 10 == 0:
                input(self.line)

            s += 10
            e += 10
        print(self.line + '\n')

    def search(
        self,
        lang: str
    ) -> None:
        '''
        Search for matching language.
        '''
        r = []
        for k, v in langs.items():
            if lang.lower() in k.lower():
                r.append([k, v])
        text = ''
        text += self.line + '\n'
        for i in r:
            text += f'| {i[0].ljust(36)} | {i[1].ljust(4)} |\n'
        text += self.line
        print(text)

    def __help(self) -> str:
        '''
        Show help.
        '''
        return '\t    Use `show_languages()` to list all language codes.\n'

    def __send_to_api(
        self,
        data_dict: dict
    ) -> dict:
        '''
        Send data to MyMemory API.

        Returns: dict
            quotaFinished: bool - indicates if it has reached the limit of use.
            result: list - list of string translated.
        '''
        result = []
        source = data_dict['source']
        target = data_dict['target']
        list_translate = data_dict['translate']
        quotaFinished = False

        for chunk_text in list_translate:
            response = self.api.get(
                    text=chunk_text,
                    source_lang=source,
                    target_lang=target,
                    email_user=self.user.email
                )
            if response['quotaFinished']:
                quotaFinished = True

            result.append(response)

        return {
            'quotaFinished': quotaFinished,
            'result': result
        }

    def translate(
        self,
        text: str,
        source_lang: str = 'auto',
        target_lang: str = 'en'
    ) -> Union[list, None]:
        '''
        Send the given text to api.
        '''
        if self.user.timeout is not None:
            remain_time = calculate_remain_time(self.user.timeout)
            if remain_time is None:
                self.user.timeout = None
            else:
                self.user.to_write(self.user.to_dict())
                raise TimeOutUsage(remain_time)
        if self.user.statusQuota():
            raise ApiLimitUsageException()

        if len(text) <= 0:
            raise EmptyTextException()
        else:
            if source_lang == 'auto':
                source_lang = self.local_lang
            else:
                source_lang = source_lang.lower()

            target_lang = target_lang.lower()

            correct_langs = [
                        source_lang in self.code_langs,
                        target_lang in self.code_langs
                    ]
            if not all(correct_langs):
                if correct_langs[0] is False and correct_langs[1] is False:
                    raise ParameterErrorException(
                        f'source_lang="{source_lang}"',
                        f'target_lang="{target_lang}"'
                    )
                elif correct_langs[0] is False:
                    raise ParameterErrorException(
                                f'source_lang="{source_lang}"'
                            )
                elif correct_langs[1] is False:
                    raise ParameterErrorException(
                                f'target_lang="{target_lang}"'
                            )
            else:
                text_wrapper_dict = self.textwrapper.wrap(text)

                data_translate = {
                    'source': source_lang,
                    'target': target_lang,
                    'translate': text_wrapper_dict['result']
                }

                try:
                    response_translate = self.__send_to_api(data_translate)
                    if response_translate['quotaFinished']:
                        self.user.set_quota(self.user.quota_chars_day)
                        return None
                    else:
                        self.user.set_quota(text_wrapper_dict['text_size'])
                        return self.__build_text(response_translate['result'])
                except ApiLimitUsageException:
                    self.user.timeout = str(self.api.timeout)
                    self.user.to_write(self.user.to_dict())
                    return None
                except ApiEmailUserException:
                    self.user.to_write(self.user.to_dict())
                    return None
                except ApiGenericException:
                    self.user.to_write(self.user.to_dict())
                    return None

    def __build_text(
        self,
        list_data: list
    ) -> dict:
        '''
        Build the text and calculate its average score.
        '''
        scores = []
        text = ''
        for item in list_data:
            text += item['translatedText']
            scores.append(float(item['score']))
        if text[-1] != '.':
            text += '.'
        return {
            'text': text,
            'mean_score': round(sum(scores) / len(scores), 2)
        }

    def get_status(self):
        '''
        '''
        return 'User: {0}, Current quota: {1} Quota limit: {2}'.format(
            self.user.type,
            self.user.current_quota,
            self.user.quota_chars_day,
        )

    def get_quota(self):
        '''
        '''
        return self.user.get_quota()

    def __str__(self):
        '''
        '''
        return f'{self.user}'


text = '''
**Inteligencia Artificial: Transformando el Futuro**

La inteligencia artificial (IA) ha emergido como una fuerza impulsora que transforma nuestro mundo en formas que apenas podríamos haber imaginado. En la intersección de la ciencia de la computación, la estadística y la ingeniería, la IA busca crear sistemas capaces de realizar tareas que, históricamente, requerían inteligencia humana. Este campo fascinante abarca desde algoritmos de aprendizaje automático hasta robots autónomos, y su impacto ya se siente en diversas industrias y aspectos de la vida cotidiana.

*Avances en el Aprendizaje Profundo*

Uno de los hitos más notables en la evolución de la IA es el desarrollo del aprendizaje profundo. Esta técnica, inspirada en la estructura y funcionamiento del cerebro humano, utiliza redes neuronales profundas para procesar datos de manera jerárquica y aprender representaciones complejas. El aprendizaje profundo ha revolucionado campos como la visión por computadora y el procesamiento del lenguaje natural, permitiendo que las máquinas comprendan imágenes, voz y texto con una precisión asombrosa.

*IA en la Medicina: Diagnóstico Preciso y Personalizado*

En el ámbito de la medicina, la IA está desempeñando un papel crucial en la mejora de diagnósticos y tratamientos. Algoritmos de aprendizaje automático analizan grandes conjuntos de datos médicos para identificar patrones y predecir enfermedades. Esto no solo acelera el proceso de diagnóstico, sino que también facilita tratamientos personalizados basados en la información genética de cada paciente. La IA se convierte así en una aliada invaluable para los profesionales de la salud en la lucha contra enfermedades.

**Desafíos Éticos y Consideraciones**

A medida que la IA avanza, también surgen desafíos éticos y preocupaciones sobre su impacto en la sociedad. La toma de decisiones automatizada plantea preguntas cruciales sobre la transparencia y la equidad, ya que los algoritmos pueden heredar sesgos presentes en los datos de entrenamiento. Es esencial abordar estos problemas de manera proactiva para garantizar que la IA se utilice de manera ética y beneficiosa para todos.

En resumen, la inteligencia artificial se encuentra en el centro de una revolución tecnológica que está dando forma al futuro. Desde diagnósticos médicos precisos hasta asistentes virtuales, la IA está cambiando la forma en que vivimos y trabajamos. A medida que exploramos las posibilidades de este campo, es imperativo considerar sus implicaciones éticas y garantizar que su desarrollo se guíe por principios que promuevan el bienestar y la equidad en la sociedad. La inteligencia artificial no solo es una herramienta poderosa, sino también una responsabilidad que debemos abordar con sabiduría y consideración.
'''
text = 'hola'

# m = MyMemoryTranslate(email='algo@algo.com')
m = MyMemoryTranslate(email='example@example.com')
# m = MyMemoryTranslate()
text = 'hola!'
print(m)
print(m.get_quota())

# r = m.translate(text * 2, 'es', 'en')

r = m.translate(text, 'es', 'en')
print(m)

# r = m.translate(text, 'ex', 'en')
# r = m.translate(text, 'es', 'nn')
# r = m.translate(text, 'ex', 'ññ')
# for i in r:
#     print(i)
