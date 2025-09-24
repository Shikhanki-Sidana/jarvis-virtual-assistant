from assistant import speak, take_command, tell_time, tell_date, search_wikipedia, open_website, play_music_from_folder, take_screenshot
import time

def welcome():
    speak('Hello, I am Jarvis. How can I help you today?')

def main_loop():
    welcome()
    while True:
        speak('Listening...')
        query = take_command()
        if not query:
            query = input('You (type): ').lower()

        if 'time' in query:
            tell_time()
        elif 'date' in query:
            tell_date()
        elif 'wikipedia' in query:
            topic = query.replace('wikipedia', '').strip()
            if topic:
                search_wikipedia(topic)
            else:
                speak('What should I search on Wikipedia?')
                topic = take_command()
                if topic:
                    search_wikipedia(topic)
        elif 'open' in query and 'website' in query:
            parts = query.split()
            target = ' '.join(parts[parts.index('website')+1:])
            open_website(target)
        elif 'play music' in query:
            play_music_from_folder('resources/example_music')
        elif 'screenshot' in query:
            take_screenshot()
        elif 'stop' in query or 'exit' in query or 'sleep' in query:
            speak('Going offline. Goodbye!')
            break
        else:
            speak('I will search the web for that.')
            open_website(query)
        time.sleep(1)

if __name__ == '__main__':
    main_loop()
