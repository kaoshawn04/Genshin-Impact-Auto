import os
import re
import sys
import lxml
import mido
import requests
import requests_html


try:
    from library.auto_lyre.convert import Converter

except (ImportError, ModuleNotFoundError):
    dir_path = (os.path.realpath(__file__)).rsplit("\\library", 1)[0]
    sys.path.append(dir_path)

    from library.auto_lyre.convert import Converter


class Midi():
    def __init__(self):
        self.convert = Converter().frequency_to_key
        

    def process(self, filepath):
        midi_file = mido.MidiFile(filepath)
        
        result = []

        for i, message in enumerate(midi_file):
            if message.type == "note_on":
                frequency, velocity, time = message.note, message.velocity, message.time

                if velocity > 0: # key down
                    if time > 0: # create new message
                        result.append([{self.convert(frequency)}, round(time, 3)])

                    elif time == 0: # combine with last message in result
                        if len(result) > 0:
                            result[-1][0].add(self.convert(frequency))

                        else: # result is empty, create new message
                            result.append([{self.convert(frequency)}, round(time, 3)])
                
                elif velocity == 0: # key up
                    if time > 0:
                        result.append([{None}, round(time, 3)])
                        
            elif type == "control_change":
                time = message.time
                
                if time > 0:
                    result.append([{None}, round(time, 3)])

                    
        for i in range(len(result)):
            if (i + 1) == len(result):
                result[i][1] = 0
                
            else:
                result[i][1] = result[i + 1][1]
            
            if len(result[i][0]) > 1 and None in result[i][0]:
                result[i][0].discard(None)
                
            result[i][0] = list(result[i][0])
            result[i] = tuple(result[i])
            
        result.insert(0, {
            "filepath": filepath,
            "duration": sum(message[1] for message in result),
            "message_count": len(result),
        })
                
        return result
    
    
    def search_musescore(self, query, num = 20):
        count, page = 0, 1
        result = []
        
        while count < num:
            url = f"https://musescore.com/sheetmusic?page={page}&text={query}"
            
            with requests_html.HTMLSession() as session:
                response = session.get(url=url)
                response.html.render() 
            
            tree = lxml.html.fromstring(response.html.html)
            scores = tree.xpath(
                "/html/body/div[1]/div/section/section/main/div[2]/section/article"
            )
            
            for score in scores:
                if count == num:
                    break
                
                instrument = score.xpath("./div[1]/div[2]/div[4]/a/div")[0]
                
                if instrument.text != "Solo Piano":
                    continue
                
                title = score.xpath("./div[1]/div[2]/a/h2/text() | ./div[1]/div[2]/a/h2/span/text()")
                information = score.xpath("./div[1]/div[2]/div[2]")[0]
                url = score.xpath("./div[1]/div[2]/a")[0]
                
                result.append({
                    "title": "".join(title),
                    "duration": re.search(r"\d\d:\d\d", information.text).group(),
                    "url": url.get("href")
                })
                
                count += 1
            page += 1
                
        return result
            
        
    def download_musescore(self, score_url, filepath = None):
        base_url = "https://msdl.nanomidi.net/musescore/midi"
        api_key = "BZ51A86BLM"
        
        response = requests.get(f"{base_url}?url={score_url}&api_key={api_key}").json()
        
        title = response["score_title"]
        title = re.sub(r"\W+", "_", title)
        
        if title.startswith("_"):
            title = title[1:]
        
        download_url = response["download_url"]
        
        response = requests.get(download_url)
        
        if filepath is None:
            filepath = f"midi/{title}.mid"
        
        with open(filepath, "wb") as file:
            file.write(response.content)