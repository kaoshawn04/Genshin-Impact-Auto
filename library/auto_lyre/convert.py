import os
import sys

try:
    from library.general.config import get_config

except (ImportError, ModuleNotFoundError):
    dir_path = (os.path.realpath(__file__)).rsplit("\\library", 1)[0]
    sys.path.append(dir_path)

    from library.general.config import get_config


config = get_config("autolyre.settings", ["Higher", "Lower", "Accidental"])


class Converter():
    def __init__(self):
        self.keys = [
            ["z", "x", "c", "v", "b", "n", "m"],
            ["a", "s", "d", "f", "g", "h", "j"],
            ["q", "w", "e", "r", "t", "y", "u"]
        ]
        self.frequency_bias = [0, 2, 4, 5, 7, 9, 11]

    
    def frequency_to_key(self, frequency):
        frequency = self.special_frequency(frequency)
        key = ""
        
        if frequency is None:
            key = None
        
        elif 48 <= frequency <= 83:
            rol = frequency // 12 - 4
            col = self.frequency_bias.index(frequency % 12)
            
            key = self.keys[rol][col]
        
        return key
        
    
    def special_frequency(self, frequency):
        if frequency is None:
            return None
        
        if frequency % 12 not in self.frequency_bias:
            match config["Accidental"]:
                case "sharp": frequency += 1
                case "flat": frequency -= 1
                
                case "skip": return None
        
        if frequency > 83:
            match config["Higher"]:
                case "flat_b6": frequency = 83
                case "flat_8":  frequency -= ((frequency - 83) // 12 + 1) * 12
                
                case "skip": return None

        elif frequency < 48:
            match config["Lower"]:
                case "sharp_c4": frequency = 48
                case "sharp_8": frequency += ((48 - frequency) // 12 + 1) * 12
                
                case "skip": return None
                
        return frequency