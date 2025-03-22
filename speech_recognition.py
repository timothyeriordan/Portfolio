
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha
import os
# Speech Engine initialization
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) #male
activationWord = 'jarvis'

#Configure web browser
#set the path for chrome
chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

#Wolfram ALpha Client
appId = 'XH3QVH-5XR2GWLWV7'
wolframClient = wolframalpha.Client(appId)


def speak(text, rate = 120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def parseCommand():
    listener = sr.Recognizer()
    print('Listening for a command')
    
    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)
        
    try:
        print('Recognizing Speech...')
        query = listener.recognize_google(input_speech, language='en_gb')
        print(f'The input speech was: {query}')
    except Exception as exception:
        print('I did not quite catch that')
        speak('I did not quite catch that')
        print(exception)
        return 'None'
    
    return query


def search_wikipedia(query =''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('No results recieved')
        return 'No results recieved'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary


def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']


def search_wolframAlpha(query = ''):
    response = wolframClient.query(query)
    
    if response['@success'] == 'false':
        return 'Could not calculate'
    
    #Query resolved
    else:
        result = ''
        #Question
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]
        #May contain the answer, has highest confidence value
        #if its primary or has title of result or definition, then its the official result
        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            #get the result
            result = listOrDict(pod1['subpod'])
            #remove bracketed section 
            return result.split('(')[0]
        else:
            question = listOrDict(pod0['subpod'])
            #remove bracketed section 
            return question.split('(')[0]
            #if it can't find it, query wikipedia
            speak('Computation Failed, searching my universal knowledge')
            return search_wikipedia(question)


#main lop
if __name__ == '__main__':
    speak('Welcome back sir, initiating Jarvis 2.0')
    
    while True:
        #parse commands
        query = parseCommand().lower().split()
        
        if query[0] == activationWord:
            query.pop(0)
            
            #List commands
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings sir')
                else:
                    query.pop(0)
                    speech = ' '.join(query)
                    speak(speech)
                    
            #Navigation
            if query[0] == 'go' and query[1] == 'to':
                speak('Opening...')
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)
                
            #wikipedia
            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak('Querying my infinite knowledge...')
                speak(search_wikipedia(query))
            
            #wolfram alpha
            if query[0] == 'compute' or query[0] == 'computer':
                query = ' '.join(query[1:])
                speak('Calculating')
                try:
                    result = search_wolframAlpha(query)
                    speak(result)
                except:
                    speak('Unable to calculate')
            
            #note taking method
            if query[0] == 'log':
                speak('Ready to record your note')
                newNote = parseCommand().lower()
                now = datetime.now().strftime('%Y=%m-%d-%H-%M-%S')
                os.chdir(r"C:\Users\Timmy\Documents\Work\PythonProjects\AIComputerProgram")
                with open('note_%s.txt' % now, 'w') as newFile:
                    newFile.write(newNote)
                speak('Note written')
                
            if query[0] == 'exit':
                speak('Goodbye sir')
                break
            