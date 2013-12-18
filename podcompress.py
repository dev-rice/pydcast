from urllib.request import urlopen
import feedparser
import os
import subprocess

podcast_dir = "/home/chris/Podcasts/"

names = []
links = []

podcast_file = open("podcast_list.txt")

for line in podcast_file:
	names.append(line.split(",")[0])
	links.append(line.split(",")[1].replace(" ", ""))

x = 0
for name in names:
	x = x + 1
	print(str(x) + ". " + name)
	
podcast_number = 0
while podcast_number < 1 or podcast_number > len(links):
	podcast_number = int(input("Which podcast? (1 - " + str(len(links)) + ") "))

name = names[podcast_number-1]
link = links[podcast_number-1]
	
print("Reading from: " + link)
podcast = feedparser.parse(link)

directory = podcast_dir + name
if not os.path.exists(directory):
	print("Making directory: " + directory)
	os.makedirs(directory)

titles = []
download_links = []
y = 0
for entry in podcast.entries:
	y = y + 1
	print("\t" + str(y) + ". " + entry.title)
	#print("\tDate: " + entry.published)
	#print("\tLink: " + entry.enclosures[0].url)
	#print()
	
	titles.append(entry.title)
	download_links.append(entry.enclosures[0].url)

episode_number = 0
while episode_number < 1 or episode_number > len(titles):
	episode_number = int(input("Which episode? (1 - " + str(len(titles)) + ") "))

episode_title = titles[episode_number - 1]
episode_link = download_links[episode_number - 1]

file_path = podcast_dir + name + "/" + episode_title + ".mp3"
compressed_file_path = podcast_dir + name + "/" + episode_title + "_compressed.mp3"
	
print("\t\tDownloading to " + file_path + " ...")
f = urlopen(episode_link)
data = f.read()
with open(file_path, "wb") as code:
	code.write(data)

print("\t\tCompressing to " + compressed_file_path + " ...")
subprocess.call(["lame","-S","--nohist","-b","32",file_path,compressed_file_path])
	
subprocess.call(["rm",file_path])
print("\t\tDone!")
