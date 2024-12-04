from library.config_parser import get_config


transpose, higher, lower, middle, notes_list = get_config("transpose", "higher", "lower", "middle", "notes_list")
notes_list = notes_list.split("\n")

class Converter():
    def __init__(self, type):
        self.type = type
    
    def frequent_to_key(self, note):
        note = self.process_special_notes(note)
        key = ""
        
        match note:
            case 48: key = "z"
            case 50: key = "x"
            case 52: key = "c"
            case 53: key = "v"
            case 55: key = "b"
            case 57: key = "n"
            case 59: key = "m"

            case 60: key = "a"
            case 62: key = "s"
            case 64: key = "d"
            case 65: key = "f"
            case 67: key = "g"
            case 69: key = "h"
            case 71: key = "j"

            case 72: key = "q"
            case 74: key = "w"
            case 76: key = "e"
            case 77: key = "r"
            case 79: key = "t"
            case 81: key = "y"
            case 83: key = "u"
        
            case "none": key = "none"
            case default: key = note
        
        return key
        
    def note_to_key(self, note):
        note = self.process_special_notes(note)
        key = []
        
        match note:
            case ".do": key = "q"
            case ".re": key = "w"
            case ".mi": key = "e"
            case ".fa": key = "r"
            case ".sol": key = "t"
            case ".la": key = "y"
            case ".si": key = "u"

            case "do": key = "a"
            case "re": key = "s"
            case "mi": key = "d"
            case "fa": key = "f"
            case "sol": key = "g"
            case "la": key = "h"
            case "si": key = "j"

            case "do.": key = "z"
            case "re.": key = "x"
            case "mi.": key = "c"
            case "fa.": key = "v"
            case "sol.": key = "b"
            case "la.": key = "n"
            case "si.": key = "m"
        
            case "none": key = "none"
            case default: key = note
        
        return key
    
    def process_special_notes(self, note):
        if self.type == "json_sheet" and note != "none":
            if notes_list.index(note) > 27:
                match higher:
                    case "skip": note = "none"
                    case "fall_to_si": note = ".si"
                    
            elif notes_list.index(note) < 7:
                match lower:
                    case "skip": note = "none"
                    case "rise_to_do": note = "do."
                
        elif self.type == "midi" and note != "none":
            if note % 12 in [1, 3, 6, 8, 10]:
                match middle:
                    case "rise": note += 1
                    case "fall": note -= 1
                    
            if transpose == "false":
                while note > 83 or note < 48:
                    if note > 83:
                        match higher:
                            case "skip": note = "none"
                            case "fall_to_si": note = 83
                            case "fall_8": note -= 12

                    elif note < 48:
                        match lower:
                            case "skip": note = "none"
                            case "rise_to_do": note = 48
                            case "rise_8": note += 12
        
        return note
    
    def convert(self, note):
        if self.type == "json_sheet":
            result = self.note_to_key(note)
            
        elif self.type == "midi":
            result = self.frequent_to_key(note)
            
        return result