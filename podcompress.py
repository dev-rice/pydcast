from urllib.request import urlopen
import feedparser
import os
import subprocess
import sys

BITRATE = str(16)

podcast_dir = "/home/chris/Podcasts/"

names = []
links = []

#read from the podcast file set up by the user
podcast_file = open("podcast_list.txt")

for line in podcast_file:
	names.append(line.split(",")[0])
	links.append(line.split(",")[1].replace(" ", ""))

#print out a numbered list for the user to choose from
x = 0
for name in names:
	x = x + 1
	print(str(x) + ". " + name)

#let the user select the podcast, make sure they enter a valid index	
podcast_number = 0
while podcast_number < 1 or podcast_number > len(links):
	podcast_number = int(input("Which podcast? (1 - " + str(len(links)) + ") "))

#get the current podcast name and link to rss feed
name = names[podcast_number-1]
link = links[podcast_number-1]
	
#parse the rss feed
podcast = feedparser.parse(link)

#if the podcast directory doesn't exit, create it
directory = podcast_dir + name
if not os.path.exists(directory):
	os.makedirs(directory)

titles = []
download_links = []
y = 0

#read through the <entry> tags from the rss feed and
#print out a numbered list for the user to choose from
for entry in podcast.entries:
	y = y + 1
	title = entry.title
	print("\t" + str(y) + ". ",end="") 
	#This is not the code you are looking for. Look away!
	#Need some way to fix this
	print(str(title.encode('ascii', 'ignore')).replace("b'","").replace("b","").replace("'",""))
	
	titles.append(entry.title)
	download_links.append(entry.enclosures[0].url)

#let the user select the episode number and make sure its a valid index
episode_number = 0
while episode_number < 1 or episode_number > len(titles):
	episode_number = int(input("Which episode? (1 - " + str(len(titles)) + ") "))

#once it is selected, find the corresponding title and download link
episode_title = titles[episode_number - 1]
episode_link = download_links[episode_number - 1]

#set up paths for downloaded and compressed files
file_path = podcast_dir + name + "/" + episode_title + "temp.mp3"
compressed_file_path = podcast_dir + name + "/" + episode_title + ".mp3"

#download the file	
print("\tDownloading...")
f = urlopen(episode_link)
data = f.read()
with open(file_path, "wb") as code:
	code.write(data)

print("\tCompressing...")
#send lame output to the abyss!
null = open("/dev/null","wb")
#compress the file with lame
subprocess.call(["lame","-S","--nohist","-b",BITRATE,file_path,compressed_file_path], stdout = null, stderr = subprocess.STDOUT)

#remove the original file, leaving only the compressed one
subprocess.call(["rm",file_path])
print("\tDone!")
