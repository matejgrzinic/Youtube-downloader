# Python script to download youtube videos or songs and cut them

**Flags:**
```
--url Url of video or song, this flag is REQUIRED
--format mp4|mp3 If you want a video or a song, mp4 is default
--output Output folder, Media is default
--filename Name of downloaded file, Video title is default

--start Start of video or song in seconds. Default is 0
--end End of video or song in seconds. Default is file length
```

**Examples:**
```
Downloads "Eminem - The Way I Am (Official Music Video)" video
python youtube.py --url https://www.youtube.com/watch?v=mQvteoFiMlg

Downloads "Eminem - The Way I Am (Official Music Video)" song
python youtube.py --url https://www.youtube.com/watch?v=mQvteoFiMlg --format mp3

Downloads "Eminem - The Way I Am (Official Music Video)" song, cuts it between 10 and 30 seconds
python youtube.py --url https://www.youtube.com/watch?v=mQvteoFiMlg --format mp3 --start 10 --end 30
```