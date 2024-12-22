import trace
import mido


def test():
    midi = mido.MidiFile("assets/midi/test.mid")

    #for i, message in enumerate(midi):
    #    if i >= 10:
    #        break
        
    #    if message.type == "note_on":
    #        frequency, velocity, time = message.note, message.velocity, message.time
    

tracer = trace.Trace(countfuncs=1)
tracer.run("test()")

result = tracer.results()
result.write_results(summary=True)