import os
import sys
import mido

try:
    from library.auto_lyre.converter import Converter
    
except (ImportError, ModuleNotFoundError):
    dir_path = (os.path.realpath(__file__)).rsplit("\\library", 1)[0]
    sys.path.append(dir_path)
    
    from library.auto_lyre.converter import Converter


class MidiFile():
    def __init__(self, filepath):
        self.filepath = filepath
        self.converter = Converter("midi")
             
    def process(self):
        midi = mido.MidiFile(self.filepath, clip=True)
        result = []
        
        for i, message in enumerate(midi):
            if message.type == "note_on":
                note, velocity, time = message.note, message.velocity, message.time
                  
                if velocity > 0:
                    if time > 0:
                        r = [[self.converter.convert(note)], time]
                        
                    elif time == 0:
                        if len(result) > 0 and result[-1][0] != [None]:
                            lr = result.pop(-1)
                            lr[0].append(self.converter.convert(note))
                            
                            r = [lr[0], time]
                        
                        else:
                            r = [[self.converter.convert(note)], time]
                        
                    result.append(r)
                
                elif velocity == 0:
                    if time > 0:
                        r = [[None], time]
                    
                        result.append(r)
                        
            elif type == "control_change":
                time = message.time
                
                if time > 0:
                    r = [[None], time]
                    
                    result.append(r)
                    
        for i in range(len(result)):
            if (i + 1) == len(result):
                result[i][1] = 0
                
            else:
                result[i][1] = result[i + 1][1]
            
            if len(result[i][0]) > 1 and None in result[i][0]:
                result[i][0].remove(None)
                
            result[i] = tuple(result[i])
                
        return result