from absl import app, flags, logging
from absl.flags import FLAGS
import code as yt
import os
import sys
import time
from subprocess import Popen

flags.DEFINE_string('url', '', 'video url')
flags.DEFINE_string('format', 'mp4', '(mp3, mp4)')
flags.DEFINE_string('output', 'Media', 'Folder to save into')
flags.DEFINE_string('filename', None, 'Output filename')
flags.DEFINE_string('quality', 'best', 'Output quality')

flags.DEFINE_integer('start', -1, 'start of file in seconds')
flags.DEFINE_integer('end', -1, 'end of file in seconds')
    
def main(_argv):               
    # FLAGS.url = "https://www.youtube.com/watch?v=JByDbPn6A1o"
    path, file_length = yt.download(FLAGS.url, FLAGS.format, FLAGS.quality, FLAGS.output, FLAGS.filename)
    
    if FLAGS.format == "mp3":
        new_file_name = f"{path[:-3]}{FLAGS.format}"
        ffmpeg_process = Popen(["ffmpeg", "-i", path, new_file_name])
        ffmpeg_process.wait()
        os.remove(path)
        path = new_file_name
    
    if FLAGS.start != -1 or FLAGS.end != -1:
        if FLAGS.start == -1:
            FLAGS.start = 0
        if FLAGS.end == -1:
            FLAGS.end = file_length
        
        # ffmpeg_process = Popen(["ffmpeg", "-i", "Media/Eminem - Space Bound (Official Video).mp4", "-ss", FLAGS.start, "-to", FLAGS.end, "-c", "copy", "poop.mp4"])
        
        ffmpeg_process = Popen(["ffmpeg", "-i", path, "-ss", str(FLAGS.start), "-to", str(FLAGS.end), "-c", "copy", f"tmp.{FLAGS.format}"])
        ffmpeg_process.wait()
        os.replace(f"tmp.{FLAGS.format}", path)
        
        

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass


