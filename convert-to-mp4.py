#!/usr/bin/env python

import os
import subprocess
import re
import sys

MATCH = re.compile(r'.+\.(avi|mkv)$', re.IGNORECASE)

start_path = sys.argv[1]

for (path, dirs, files) in os.walk(start_path):
    for movie_name in [f for f in files if MATCH.match(f)]:
        in_path = os.path.join(path, movie_name)
        out_path = os.path.join(path, os.path.splitext(movie_name)[0] + ".mp4")
        if os.path.exists(out_path):
            print "Skipping " + in_path + " (" + out_path + " exists)"
            continue
        print "Processing " + in_path
        result = subprocess.call(["/usr/local/bin/ffmpeg",
                                  "-loglevel", "error",
                                  "-i", in_path,
                                  "-acodec", "copy",
                                  "-vcodec", "copy",
                                  out_path])
        if result == 0:
            print "Success. Removing " + in_path
            os.remove(in_path)
        else:
            print "Failed: " + str(result)
            if os.path.exists(out_path):
                os.remove(out_path)
