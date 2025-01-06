import re
import os
import sys

try:
    from library.general.config import get_config

except (ImportError, ModuleNotFoundError):
    dir_path = (os.path.realpath(__file__)).rsplit("\\library", 1)[0]
    sys.path.append(dir_path)

    from library.general.config import get_config


config = get_config("autolyre.settings")


class Converter():
    def __init__(self):
        self.lowest, self.highest = 36, 71
        
        self.keys = [
            ["z", "x", "c", "v", "b", "n", "m"],
            ["a", "s", "d", "f", "g", "h", "j"],
            ["q", "w", "e", "r", "t", "y", "u"]
        ]
        self.frequency_bias = [0, 2, 4, 5, 7, 9, 11]

    
    def frequency_to_key(self, frequency):
        if re.sub("[+-]", "", config["Transpose"]).isdigit():
            frequency += int(config["Transpose"])
            
        frequency = self.special_frequency(frequency)
        key = ""
        
        if frequency is None:
            key = None
        
        elif self.lowest <= frequency <= self.highest:
            rol = frequency // 12 - (self.lowest // 12)
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
        
        if frequency > self.highest:
            match config["Higher"]:
                case "flat_highest": frequency = self.highest
                case "flat_12":  frequency -= ((frequency - self.highest) // 12 + 1) * 12
                
                case "skip": return None

        elif frequency < self.lowest:
            match config["Lower"]:
                case "sharp_lowest": frequency = self.lowest
                case "sharp_12": frequency += ((self.lowest - frequency) // 12 + 1) * 12
                
                case "skip": return None
                
        return frequency