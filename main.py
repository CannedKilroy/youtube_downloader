#main

from Youtube_Downloader import *
import configparser
import os
import sys


config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))
api_key = config['api']['api_key']


def main():
    
    looping = True
    
    while looping:
        looping= False
        
        wrapper(header)
        
        header()
        
        #api_key = input("Please enter your Youtube API key: ")
        api_key = 'AIzaSyA4145IxhNBuIyyGFg5F7r6YgjAJ-CruaA'
        
        fileName = get_filename()
        input()
        
        header()
        
        url_list = file_contents(fileName)
        
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory,'Youtube_Vids')
        
        # Tries making new directory
        try:
            os.mkdir(final_directory)
            print('Made new folder called Youtube_Vids')        
        except FileExistsError as e:
            print('Youtube_Vids already exists')
            print('Adding to existing file')
        print(f'Final Directory of new Folder is: {final_directory}')
        
        audio_only = audioOnly()
        header()
        
        print('This may take a few minutes depending on the length and number of videos',flush=True)        
        for num,youtube_url in enumerate(url_list,1):
            try:
                video_id = get_video_id(youtube_url)
            except pytube.exceptions.RegexMatchError as e:
                print('\nCould not find youtube video matching that url',flush=True)
                p = inflect.engine()
                print(f'Check your {p.ordinal(num)} url',flush=True)
                continue
            
            API_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
            
            try_again = connect_open(API_url,audio_only,final_directory,youtube_url,num)
            
            #breakout of the loop if you get a error
            #pass into the next loop if no issues
            if try_again == 'y' :
                break
            elif try_again == 'n':
                break
            elif try_again == None:
                pass
        
        if try_again == None:
            p = inflect.engine()
            print('Download is complete for all',p.number_to_words(num),'videos',flush=True)
        elif try_again == 'y':
            looping = True
    
if __name__ == '__main__':
    main()