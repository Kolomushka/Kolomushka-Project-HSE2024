import random
import nltk
from nltk.corpus import wordnet

class WordAction:
    nltk.download('wordnet')

    def __init__(self) -> None:
        pass

    def replace_with_synonyms(self, text):
        original_text = text
        words = nltk.word_tokenize(text)

        words_to_replace = random.sample(words, min(2, len(words)))

        for word in words_to_replace:
            cleaned_word = word.replace('_', '')
            cleaned_word = cleaned_word.replace('-', '')
            synonyms = wordnet.synsets(cleaned_word)
            
            if synonyms:
                synonym = random.choice(synonyms).lemmas()[0].name().replace('_', ' ')
                text = text.replace(word, synonym)

        # Проверка, изменилась ли строка после замены
        if original_text.lower() != text.lower():
            return text
        else:
            text = original_text
            words = nltk.word_tokenize(text)

            words_to_replace = random.sample(words, min(5, len(words)))

            for word in words_to_replace:
                cleaned_word = word.replace('_', '')
                cleaned_word = cleaned_word.replace('-', '')  # Дополнительно удаляем символ '-'
                synonyms = wordnet.synsets(cleaned_word)
                
                if synonyms:
                    synonym = random.choice(synonyms).lemmas()[0].name().replace('_', ' ')
                    text = text.replace(word, synonym)

            # Проверка, изменилась ли строка после второй замены
            if original_text.lower() != text.lower():
                return text
            else:
                return self.swap_random_words(text)

    def swap_random_words(self, text):
        words = text.split()

        if len(words) >= 2:
            index1, index2 = random.sample(range(len(words)), 2)
            words[index1], words[index2] = words[index2], words[index1]
            return ' '.join(words)
        else:
            return text

    # Делаем случайным выбор строки, надеясь избежать повторений
    def find_random_line_number_by_value(self, target_value):
        matching_line_numbers = []

        with open(r'Dialog\dialogues_topic.txt', 'r') as file:
            for i, line in enumerate(file, 1):
                if str(target_value) in line:
                    matching_line_numbers.append(i)

        if matching_line_numbers:
            random_line_number = random.choice(matching_line_numbers)
            return random_line_number
        else:
            return -1
 # Возвращает волшебный -1, если значение не найдено

    def read_data_by_line_number(self, line_number):
        with open(r'Dialog\dialogues_text.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if 1 <= line_number <= len(lines):
                return lines[line_number - 1]
            else:
                return None