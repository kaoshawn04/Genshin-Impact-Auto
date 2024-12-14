import os
import sys
import mido

try:
    from library.auto_lyre.convert import Converter

except (ImportError, ModuleNotFoundError):
    dir_path = (os.path.realpath(__file__)).rsplit("\\library", 1)[0]
    sys.path.append(dir_path)

    from library.auto_lyre.convert import Converter


class Midi():
    def __init__(self, filepath):
        self.filepath = filepath
        self.convert = Converter().frequency_to_key


    def get_information(self, messages):
        return {
            "duration": sum(message[1] for message in messages)
        }


    def process(self):
        midi = mido.MidiFile(self.filepath, clip=True)
        result = []

        for i, message in enumerate(midi):
            if message.type == "note_on":
                frequency, velocity, time = message.note, message.velocity, message.time

                if velocity > 0: # key down
                    if time > 0: # create new message
                        r = [[self.convert(frequency)], time]

                    elif time == 0: # combine with last message in result
                        if len(result) > 0: #and result[-1][0] != [None]:
                            result[-1][0].append(self.convert(frequency))

                        else: # result is empty, then create new message
                            r = [[self.convert(frequency)], time]

                    result.append(r)
                
                elif velocity == 0: # key up
                    if time > 0:
                        result.append([[None], time])
                        
            elif type == "control_change":
                time = message.time
                
                if time > 0:
                    result.append([[None], time])
                    
        for i in range(len(result)):
            if (i + 1) == len(result):
                result[i][1] = 0
                
            else:
                result[i][1] = result[i + 1][1]
            
            if len(result[i][0]) > 1 and None in result[i][0]:
                result[i][0].remove(None)
                
            result[i] = tuple(result[i])
            
        result.insert(0, self.get_information(result))
                
        return result
    
    
if __name__ == "__main__":
    midi = Midi("assets/midi/test.mid")
    print(midi.process())