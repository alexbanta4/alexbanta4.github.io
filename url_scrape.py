import re
import requests
import bs4
import os, shutil
from pytube import YouTube

# This script serves the purpose of converting the Million Song Dataset to a collection of MP3s
# It first organizes the MSD text file into a list of SecondHandSong IDs,and then extracts the youtube links from those pages
# It ends by converting the youtube links to MP3 files and storing them in folders, by song

shs_file = open("shs_dataset_train.txt","r",encoding="utf-8")
shs_dict = {}
curr_entry = ''
for line in shs_file: # Create a dictionary entry for each row, and add the track IDs
    if line[0:1] == '#':
        continue
    elif line[0:1] == '%':
        line_parts = [component.strip('%').strip('\n').strip() for component in line.split(',')]
        curr_entry = line_parts[-1]
        shs_dict[curr_entry] = line_parts[0:-1] # Add originals to dict
        shs_dict[curr_entry].append('|') # separate originals from covers
    else:
        split = line.split('<SEP>')
        id = split[2].strip('\n')
        if id in shs_dict[curr_entry]:
            continue
        shs_dict[curr_entry].append(id)
performance_template = 'https://secondhandsongs.com/performance/'
work_template = 'https://secondhandsongs.com/work/'

# This is the result of this entire analysis: It stores, for each row, the original with all covers.
fullDataset = []

# This is the number of songs which will be analyzed; useful for getting truncated datasets.
# The full dataset is 4084 song titles and has ~12000 songs; this takes many hours just to get through SHS.
# You will probably want to truncate it unless you have lots of time or a supercomputer.
limit = 300;

for rowTitle in shs_dict.keys():
    ind = list(shs_dict).index(rowTitle)+1
    if ind > limit:
        print("----------------------LIMIT REACHED-----------------------------")
        break
    print("----------------------------------------------------{} of {}".format(ind,len(shs_dict.keys())))
    cover = False
    possibleOriginals = []
    rowDataEntry = []
    for val in shs_dict[rowTitle]:
        if val == '|': # Find the true original song and begin to fill the row entry
            cover = True
            if len(possibleOriginals) == 0:
                # We may not have been able to find any originals. If so, just break.
                break
            elif len(possibleOriginals)==1:
                # If there's one original, use it and move on
                original = possibleOriginals[0]
            else:
                # If we're here, figure out which original is the true original
                original = min(possibleOriginals,key = lambda it: it[1])
                if original[2] == 'None': # If original doesn't have an mp3, it's unusable and we can use the other original.
                    possibleOriginals.remove(original)
                    if possibleOriginals[0][2] == 'None': # None of the originals have mp3s, and we can't really do anything with this dataset
                        break
                    else:
                        original = possibleOriginals[0]
            rowDataEntry.append(["Original",original[0],original[2]])
            print("Separator: There are {} possibles, and the original is {}".format(len(possibleOriginals),original[0]))
            for o in possibleOriginals:
                if o == original:
                    continue
                else:
                    rowDataEntry.append(["Cover",original[2]])
            continue

        # Otherwise, do the actual web scraping
        work_url = work_template+val+"/versions"
        performance_url = performance_template+val+"/versions"
        working_page = ''
        for url in [work_url,performance_url]:
            page = requests.get(url)
            content = bs4.BeautifulSoup(page.text, "html.parser")
            find_song = content.findAll(text=re.compile(re.escape(rowTitle),re.IGNORECASE), limit=1)
            youtube_url = 'None'
            if len(find_song) > 0:

                if cover:
                    working_page = page.url
                    youtube_element = content.findAll("a", {"class": "youtube-video-play"})
                    try:
                        youtube_url = "http://youtube.com/watch?v={}".format(youtube_element[0]['data-video-id'])
                    except: # No youtube video. Sad!
                        print("No youtube video found for {}.".format(val))
                        break
                    print("New cover: {}, page {} at {}".format(val,working_page,youtube_url))
                    rowDataEntry.append(["Cover",youtube_url])

                else: # It's an original! Switch to the original page.
                    # These are more complicated because they sometimes come in pairs.
                    # In these cases, the older original is the 'original' and the newer is treated as a cover.
                    working_page = page.url.replace("/versions","/originals")
                    original_page = requests.get(working_page)
                    content = bs4.BeautifulSoup(original_page.text, "html.parser")
                    original_versions = content.findAll("article", {"itemprop": "recordingOf"})
                    for o in original_versions:
                        title = o.find("h2").find("span",{"itemprop":"name"}).text.strip()
                        try:
                            info = o.find("div",{"class":"media-body"}).find("p")
                        except:
                            print("No youtube video found for {}.".format(val))
                            break
                        for child in info.children:
                            if type(child) == bs4.NavigableString:
                                date = re.search("(\d\d\d\d)\)",child)
                                if date is not None:
                                    date = date.group(1)
                                    break
                        try:
                            date = int(date)
                        except:
                            print("No date found for {}; original song cannot be determined.".format(val))
                            break
                        youtube_element = o.findAll("a", {"class": "youtube-video-play"})
                        try:
                            youtube_url = "http://youtube.com/watch?v={}".format(youtube_element[0]['data-video-id'])
                        except:
                            print("No youtube video found for {}.".format(val))
                            break
                        songInfo = [title,date,youtube_url]
                        if songInfo not in possibleOriginals:
                            possibleOriginals.append([title,date,youtube_url])
                            print("New original: {}, release on {}, at {}".format(title,str(date),youtube_url))
                            # Don't add it to the dataset yet; we do that at the separator
                break
    if len(rowDataEntry) > 1:
        fullDataset.append(rowDataEntry)

shs = "D:\\Dropbox\\Documents\\Northwestern Year 4\\Quarter 1\\EECS 396 - Pardo Deep Learning\\Project\\SHS_Dataset"
target = "test"
path = os.path.join(shs,target)
if not os.path.isdir(path):
    os.mkdir(path)
for songs in fullDataset:
    title = songs[0][1]
    song_dir = os.path.join(path,title)
    if not os.path.isdir(song_dir):
        os.mkdir(song_dir)
    has_covers = False
    for i in range(0,len(songs)):
        song = songs[i]
        is_orig = (song[0] == "Original")
        if is_orig:
            filename = title + " Original"
        else:
            filename = title + " Cover {}".format(i)

        try:
            if not os.path.isfile(os.path.join(song_dir,filename)):
                yt_obj = YouTube(song[-1])
                yt_streams = yt_obj.streams.filter(only_audio=True)
                yt_streams[0].download(song_dir,filename)
                has_covers = True
        except:
            print("\tCouldn't download {} to {}".format(song[-1], filename))
            if is_orig:
                break
    if not has_covers:
        print("\t{} is missing an original or covers; deleting...".format(title))
        shutil.rmtree(song_dir)
    print("Done with {}, {} out of {}".format(title,fullDataset.index(songs),len(fullDataset)))
