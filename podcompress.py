from urllib.request import urlopen
import feedparser
import os
import subprocess

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

directory = "./" + name
if not os.path.exists(directory):
	os.makedirs(directory)

for entry in podcast.entries:
	print()
	print("\tPodcast: " + entry.title)
	print("\tDate: " + entry.published)
	print("\tLink: " + entry.enclosures[0].url)
	print()

	file_path = "./" + name + "/" + entry.title + ".mp3"
	compressed_file_path = "./" + name + "/" + entry.title + "_compressed.mp3"
	
	print("\t\tDownloading...")
	f = urlopen(entry.enclosures[0].url)
	data = f.read()
	with open(file_path, "wb") as code:
		code.write(data)
	
	print("\t\tCompressing...")
	subprocess.call(["lame","-S","--nohist","-b","32",file_path,compressed_file_path])
	
	subprocess.call(["rm",file_path])
	print("\t\tDone!")
