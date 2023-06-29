from pytube import YouTube, exceptions
# I recommend installing pytube directly from github as it may throw some exceptions if installed through pip
# https://github.com/oncename/pytube/tree/master


def get_progressive_streams(video: YouTube):
    """
    Gets the progressive streams of a video and returns a list for each in a presentable format.
    The elements of the list are tuples with 2 elements: The first being the stream's itag and the second the stream description.
    Raises VideoUnavailable if the video url is not valid.
    """
    prog_streams = video.streams.filter(progressive='True')
    stream_list = []
    
    for stream in prog_streams:
        # The stream description
        stream_str = f"Type = '{stream.mime_type[6:]}' Resolution = {stream.resolution} FPS = {stream.fps}"
        stream_itag = stream.itag 
        stream_list.append((stream_itag, stream_str))
        
    return stream_list

# The two functions below are to improve readability
def convert_time(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes} m, {remaining_seconds} s"

def beautify_datetime(datetime_obj):
    formatted_datetime = datetime_obj.strftime("%B %d, %Y")
    return formatted_datetime

while True:
    print('Youtube Video Downloader')
    print('1. Videos\n2. Playlists (COMING SOON)\n3. Exit')
    
    try:
        ch = int(input('Enter your choice: '))
        
    except:
        print('Sorry, this is not a valid choice.\n')
        continue
    
    if ch == 1:
        
        while True:
            print('\nEnter the video URL:')
            url = input()
            
            try:
                video = YouTube(url)
                
            except:
                print('Sorry, this video could not be found. Please try again.\n')
                continue
            
            print('The video was found!')
            print(f'Title: {video.title}')
            print(f'By {video.author}')
            print(f'{video.views} views')
            print(convert_time(video.length))
            print(f'Published on {beautify_datetime(video.publish_date)}')
            
            # For now, I will implement only progressive streams. I may add DASH streams later.
            video_stream_desc = get_progressive_streams(video)
            
            print('\nChoose the stream that you wish to download.')
            num_streams = len(video_stream_desc)
            for i in range(num_streams):
                print(f'{i + 1}. {video_stream_desc[i]}')
            
            while True:
                
                try:
                    x = int(input('Enter your choice: '))
                    
                    if not (1 <= x <= num_streams):
                        print('This stream does not exist.\n')
                        continue
                    
                    break
                
                except:
                    print(f'Please enter a number between 1 and {num_streams}\n')

            stream_itag = video_stream_desc[x - 1][0]
            video.streams.get_by_itag(stream_itag).download()
            
            print('Successfully downloaded!\n')
            
            break
            
    else:
        break