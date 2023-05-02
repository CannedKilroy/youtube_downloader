#built-in librarys
import json
import re
import urllib.request
import os,sys
import mimetypes
import tkinter
import time
from urllib.request import urlopen
from os import listdir
from os.path import isfile, join

#external modules
import inflect
import requests
from pytube import YouTube
import pytube
import hyperlink

#check python version is compatible
ver = sys.version
if int(ver[0]) != 3:
    raise Exception("Please update to python version 3")


### Custom Exceptions###
class ApiError(Exception):
    """ Custom Error"""
    def __init__(self, message=None):
        """
        :param message:
            (Optional) Message to raise when raised, default None
        :type message: str
        """
        super(ApiError, self).__init__(message)

class TitleExists(Exception):
    """Custom Error"""
    def __init__(self, message=None):
        """
        :param message:
            (Optional) Message to raise when raised, default None
        :type message: str
        """
        super(TitleExists, self).__init__(message)

### File Handling ###
def get_filename(ext='text'):
    """ Prompts for the file_name, validates it against given extension, and returns. 
    
    :param ext:
        (optional) Desired extension, default is text
    :type ext:
        str
    :returns:
        File Location, or raises Exception
    :rtype:
        str
    """
    while True:
        try:
            userInput = input('Please enter the name of the file holding the youtube url\'s, with extension: ')
            
            if mimetypes.guess_type(userInput)[0] == None:
                raise Exception('Error: Please add a extension\n')
            
            elif mimetypes.guess_type(userInput)[0][:4] != ext:
                raise Exception('Error: Invalid extension\n')                
            
            drive = os.path.splitdrive(os.path.abspath(__file__))[0]
            
            found,file_path = file_location(userInput, root = drive)
            
            if not found:
                raise Exception(f'Error: File does not exist in any subdirecties of {drive}\n')
            else:
                return file_path
        
        except Exception as e:
            print(e.args[0])

def file_location(file_name:str, root='C:\\Users\\'):
    """Checks if the file exists in subdirectory.
    
    :param file_name:
        Filename to be found.
    :type file_name: str
    :param root:
        Which directory to start the search from, defaults to Users
    :type root: str
    :returns:
        if file was found and file location
    :rtype: bool,str
    
    """
    print('Checking if file exists...', flush=True)
    
    found_file = False
    file_location = None
    
    for path, directories, files in os.walk(root, topdown=True):
        if file_name in files:
            file_location = os.path.join(path, file_name)
            print('File exists!')
            print(f'Path to file: {file_location}')
            found_file = True
            return found_file, file_location
    return found_file, file_location

def file_contents(file_name:str):   
    """ Reads, strips, and returns contents of given text file.
    
    :param file_name:
        File name to be read
    :type file_name: str
    :returns:
        Contents of file
    :rtype: list
    """
    with open(file_name,'r') as f:
        lines = f.readlines()
        newlines = [line.strip() for line in lines]
        contents = [line for line in newlines if line != '']
        return contents

###Handle Youtube#### 
def get_video_id(url:str):
    """Gets the video id
    :param url:
        Given youtube url
    : type url: str
    returns:
        video id of youtube video
    :rtype: str
    """
    return pytube.extract.video_id(url)

class YoutubeStats:
    """Container to hold the info from youtube url"""
    
    def __init__(self, apiUrl:str):
        """Constructs a :class: YoutubeStats.
        
        :param apiUrl:
            url of youtube video
        :type apiUrl: str
        """

        try:
            self.json_url = requests.get(apiUrl)
            print(self.json_url)
            
            if self.json_url.status_code != 200:
                raise ApiError
        except:
            raise ApiError('API key invalid or network error')
        
        self.data = json.loads(self.json_url.text)
    
    def get_video_title(self):
        """Gets the title of youtube video.
        
        :returns:
            Youtube video title
        :rtype: str
        """
        return self.data["items"][0]["snippet"]["title"]
    
    def download_highestQ_video(self, youtube_url:str, title:str, path:str):
        """Downloads the highest res video, audio and video, from given url.
        
        :param youtube_url:
            Url of youtube video to be downloaded
        :type youtube_url: str
        :param title:
            Title of downloaded file.
        :type title: str
        :param path:
            Proposed path to the download
        :type path: str
        """
        
        YouTube(youtube_url).streams.get_highest_resolution().download(filename=title,output_path=path)    
    
    def download_highestQ_audio(self, youtube_url:str, title:str, path:str):
        """ Downloads youtube video, audio only.
        
        :param youtube_url:
            URL of youtube video
        :type youtube_url: str
        :param title:
            Title of downloaded file.
        :type title: str
        :param path:
            Proposed path to the download
        :type path: str
        """
        YouTube(youtube_url).streams.get_audio_only().download(filename=title,output_path=path)
    
    def download_by_resolution(self, youtube_url:str, title:str, path:str, res:str):
        """ Downloads youtube video by resolution.
        
        :param youtube_url:
            URL of youtube video
        :type youtube_url: str
        :param title:
            Title of downloaded file.
        :type title: str
        :param path:
            Proposed path to the download
        :type path: str
        :param res:
            resolution of video
        :type res: str
        """        
        YouTube(youtube_url).streams.get_by_resolution(res).download(filename=title,output_path=path)
    
    def download_playlist(self, youtube_url:str, title:str, path:str):
        """ Downloads youtube playlist.
        
        :param youtube_url:
            URL of youtube video
        :type youtube_url: str
        :param title:
            Title of downloaded file.
        :type title: str
        :param path:
            Proposed path to the download
        :type path: str
        """        
        YouTube(youtube_url).streams.get_audio_only().download(filename=title,output_path=path)

class TxtForm:
    '''
    Simple wrapper for print and input statements
    '''
    def __init__(self,header:str):
        self.header=header
    
    def display(self, Dtype, clearScr=True, *dialogue):
        
        if clearScr == True:
            os.system('cls' if os.name=='nt' else 'clear')
            print(self.header)
        
        if Dtype == 'pr':
            print(*dialogue,flush=True)
        else:
            if len(dialogue)>1:
                txt = ' '.join(map(str,dialogue))
                return input(txt)
            else:
                return input(*dialogue)
            
    def new_header(self,header):
        self.header= header

def connect_open(API_url:str, audio_only:bool, final_directory:str, youtube_url:str, num:int, res:str):
    """
    Downloads each individual url
    
    :param API_url:
        URL to download video from
    :type API_url: str
    :param audio_only:
        if download audio only
    :type audio_only: str
    :param final_directory:
        directory for the yt vids
    :type final_directory: str
    :param youtube_url:
        url to the youtube video
    :type youtube_url: str
    :param num:
        number it is in the list
    :type num: str
    :param res:
        resolution
    :type res: str
    """
    yt_stats = YoutubeStats(API_url)
    title = yt_stats.get_video_title() 
    
    #truncate title if too long
    if len(title)>50:
        title = title[:50]
    
    #check if file already exists
    for file in os.listdir(final_directory):
        if file == title + '.mp4':
            print('File \''+file+'\' Exists',flush=True)
            return TitleExists('Title already exists in folder\n')
        
    
    print('Downloading...\n ',flush=True)
    
    if audio_only == True:
        yt_stats.download_highestQ_audio(youtube_url,title,final_directory) #downloads just audio
    else:
        if res != 'highest':
            yt_stats.download_by_resolution(youtube_url,title,final_directory,res)
        else:
            print('Got highest',flush=True)
            yt_stats.download_highestQ_video(youtube_url,title,final_directory) #downloads audio and video

def downloaderLoop(apiKey:str, audio_only:str, final_directory:str, urlList:list):
    """
    Loop through list of urls
    
    :param apiKey:
        Youtube api key
    :type apiKey: str
    :param audio_only:
        boolean if audio only
    :type audio_only: bool
    :param final_directory:
        final directory of yt vids
    :type path: str
    :param urlList:
        list of yt urls
    :type urlList: list
    """
    
    if not urlList:
        raise Exception('\nError. No videos found in playlist\n'
                        'Check url and playlist\n'
                        'Exiting...')
    
    resolution = input('Specified resolution or highest resolution? (144p,240p,360p,480p,720p,highest)')
    
    for num,yt_url in enumerate(urlList,1):
        try:
            video_id = get_video_id(yt_url)
            API_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={apiKey}"
            connect_open(API_url,
                         audio_only,
                         final_directory,
                         yt_url,
                         num,
                         resolution)
            
            print('Success!')
        
        except pytube.exceptions.RegexMatchError as e:
            print('\nCould not find youtube video matching that url',flush=True)
            p = inflect.engine()
            print(f'Check your {p.ordinal(num)} url',flush=True)
            print('Continuing...')
            continue  #to the next url
        
        except TitleExists as e:
            print(e.args[0])
            print('passing',flush=True)
            pass
        
        except ApiError:
            print('\nError occured connecting to Youtube API',flush=True)
            print('Check your API and internet connection',flush=True)
            try_again = input('Would you like to try again? (y/n): ')
            if try_again == 'y':
                pass
            else:
                raise ApiError
            
    return len(urlList) #number of videos downloaded 

def get_playlist():
    return pytube.Playlist(input('Input the url: '))

def main():
    """ Handles the main program flow."""
    
    looping = True
    while looping:
        looping = False
        api_key = input("Please enter your Youtube API key: ")
        
        header = (
            '--------------------------------------\n'
            '--------------------------------------\n'
            'For this project, you will need a youtube API key'
            '\nand a file holding your youtube url\'s'
            '\n visit: https://console.developers.google.com'
            '\n visit: https://www.youtube.com/watch?v=ZkYOvViSx3E&t=763s'
            '\nfor more info.\n'
            '--------------------------------------\n'
            '--------------------------------------\n')

        pg=TxtForm(header)
        dis = pg.display
        
        dis('in',True,True,'Press enter to Continue')
        
        if dis('in',False,'Audio only? (y/n)') == 'y':
            audio_only = True
        else:
            audio_only = False
        
        #get the final directory path
        final_directory = os.path.join(os.getcwd(),'YT_vids')
        
        #create directory
        try:
            os.mkdir(final_directory)
            dis('pr',True,'Made new folder called YT_vids')
        except FileExistsError as e:
            dis('pr',False,'YT_vids already exists')
            dis('pr',False,'Adding to existing file')
        
        dis('pr',False,f'Final Directory of new Folder is: {final_directory}')
        dis('in',False,'Press enter')        
        
        #check if downloading playlist or videos
        if dis('in',True,'Would you like to download a playlist or single video? (playlist/video)') == 'playlist':
            playlist = get_playlist()                              
            playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
            
            dis('pr',True,'This may take a few minutes depending on the length and number of videos')            
                        
            num = downloaderLoop(api_key, 
                                 audio_only, 
                                 final_directory, 
                                 playlist.video_urls)
        
        else:
            fileName = get_filename() #get name of the file holding the urls
            url_list = file_contents(fileName) #load urls into a list
            
            dis('pr',True,'This may take a few minutes depending on the length and number of videos')
            
            num = downloaderLoop(api_key,
                                 audio_only,
                                 final_directory,
                                 url_list)

        p = inflect.engine()
        print('Download is complete for all',p.number_to_words(num),'videos',flush=True)


if __name__ == '__main__':
    main()
    """ Creates youtube object, and tries to download video.
    :param API_url:
        Url for the api to connect to Youtube
    :type API_url: str
    :param audio_only:
        Whether user wants to download video only.
    :type audio_only: bool
    :param final_directory:
        Final directory of the downloaded video
    :type final_directory: str
    :param youtube_url:
        URL of video to be downloaded
    :type youtube_url: str
    returns:
        None if no error, otherwise user input if they would like to try again
    :rtype: None or str
    """