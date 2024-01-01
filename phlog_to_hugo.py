import sys
import re
from pathlib import Path

'''
Given an input and an output dir (by default, respectively, '.' and '/tmp'),
converts a list of plaintext files containing phlog posts into a list of 
hugo-compatible markdown files with the plaintext visualized as a code block.

Titles and dates are automatically extracted from the phlog filenames and
used to generate both .md filenames and their metadata.
'''

# quick and dirty way to get input and output dir
if len(sys.argv) > 1:
    path_in = Path(sys.argv[1])
else:
    path_in = Path('.')

if len(sys.argv) > 2:
    path_out = Path(sys.argv[2])
else:
    path_out = Path("/tmp")

# the format of my phlog filenames is as follows:
# YYYY-MM-DD - Post Title
r = re.compile("(^\d{4}-\d{2}-\d{2}) - (.*)$")

# loop over all valid files in input path
for fpath in path_in.iterdir():
    res = r.match(str(fpath))
    if res is not None:
        # looks like this is a valid filename for my phlog posts
        date, title = res.groups()

        # generate new filename
        new_fname = f"{date}-{re.sub('[^0-9a-zA-Z-]+', '', title.lower().replace(' ','-'))}.md"
        print(new_fname)

        # generate new content
        with fpath.open() as f:
            phlog_post = f.read()
        
        hugo_post = f'''
+++
title = "{title}"
date = {date}
+++

```
{phlog_post}
```
'''
        fpath_out = path_out / new_fname

        with fpath_out.open("wt") as f:
            f.write(hugo_post)
