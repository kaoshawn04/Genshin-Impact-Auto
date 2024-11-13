import os
import sys

try:
    from library.general.get_config import get_config
    
except (ImportError, ModuleNotFoundError):
    dir_path = (os.path.realpath(__file__)).rsplit("\\library", 1)[0]
    sys.path.append(dir_path)
    
    from library.general.get_config import get_config


class Converter():
    def __init__(self, type):
        self.type = type
        
        self.config = get_config("autolyre.settings", ["Higher", "Lower", "Accidental"])

        self.frequency_to_key_index = [0, 2, 4, 5, 7, 9, 11]
        self.key_list = [
            ["q", "w", "e", "r", "t", "y", "u"],
            ["a", "s", "d", "f", "g", "h", "j"],
            ["z", "x", "c", "v", "b", "n", "m"]
        ]
    
    def midi_frequency_to_key(self, frequency):
        key = ""
        
        if frequency % 12 not in self.frequency_to_key_index:
            match self.config["Accidental"]:
                case "skip": frequency = None
                case "sharp": frequency += 1
                case "flat": frequency -= 1
                
                case _: frequency = None
        
        if frequency > 83:
            match self.config["Higher"]:
                case "skip": frequency = None
                case "flat_to_b5": frequency = 83                
                
                case _: frequency = None
                
        if frequency < 48:
            match self.config["Lower"]:
                case "skip": frequency = None
                case "sharp_to_c3": frequency
                
                case _: frequency = None
        
        key = self.key_list[(frequency // 12) - 4][self.frequency_to_key_index(frequency % 12)]
        
        return key
        
    
    def convert(self, note):
        if self.type == "json_sheet":
            result = self.note_to_key(note)
            
        elif self.type == "midi":
            result = self.midi_frequency_to_key(note)
            
        return result