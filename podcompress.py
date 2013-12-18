from urllib.request import urlopen
import feedparser
import os
import subprocess

rss_link = input("Enter link to rss feed: ")
podcast = feedparser.parse(rss_link)

title = podcast.feed.title
description = podcast.feed.description
latest_podcast = podcast.entries[0]

directory = "./" + title
if not os.path.exists(directory):
	os.makedirs(directory)

#print()
#print("Title: " + title)
#print("Description: " + description)

for entry in podcast.entries:
	print()
	print("\tPodcast: " + entry.title)
	print("\tDate: " + entry.published)
	print("\tLink: " + entry.enclosures[0].url)
	print()

	file_path = "./" + title + "/" + entry.title + ".mp3"
	compressed_file_path = "./" + title + "/" + entry.title + "_compressed.mp3"
	
	print("\t\tDownloading...")
	f = urlopen(entry.enclosures[0].url)
	data = f.read()
	with open("./" + title + "/" + entry.title + ".mp3", "wb") as code:
		code.write(data)
	
	print("\t\tCompressing...")
	subprocess.call(["lame","-S","--nohist","-b","32",file_path,compressed_file_path])
	
	subprocess.call(["rm",file_path])
	print("\t\tDone!")
