import sys
import os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

class GlobalData:
    def __init__(self) -> None:
        pass
    #------------------------------- ТЕМЫ --------------------------------------------
    
    # Словарь тем
    theme_dict = {1: "Ordinary Life", 2: "School Life", 3: "Culture & Education",
                        4: "Attitude & Emotion", 5: "Relationship", 6: "Tourism",
                        7: "Health", 8: "Work", 9: "Politics", 10: "Finance"}

    # Из имени темы получаем ее порядковый номер  
    def theme_to_num(self, theme_val):
        for key, theme in self.theme_dict.items():
            if theme == theme_val:
                return key
        return None 
            
    # Из порядкового номера темы получаем наименование темы
    def num_to_theme(self, key_val):
        for key, theme in self.theme_dict.items():
            if key == key_val:
                return theme
        return None 