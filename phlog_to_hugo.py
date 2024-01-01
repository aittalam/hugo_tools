import sys
import re
import datetime
from pathlib import Path
from dateutil.relativedelta import relativedelta

'''
Given an input and an output dir (by default, respectively, '.' and '/tmp'),
converts a list of plaintext files containing phlog posts into a list of 
hugo-compatible markdown files with the plaintext visualized as a code block.

Titles and dates are automatically extracted from the phlog filenames and
used to generate both .md filenames and their metadata.

The variable relativedelta_months allows to skew posts date by a given amount
of months (I use this to publish my phlog posts on hugo one year later).
'''

relativedelta_months = 12

# quick and dirty way to get input and output dir
if len(sys.argv) > 1:
    path_in = Path(sys.argv[1])
else:
    path_in = Path('.')

if len(sys.argv) > 2:
    path_out = Path(sys.argv[2])
else:
    path_out = Path("/tmp")

print(f"[i] Input dir: {str(path_in)}")
print(f"[i] Output dir: {str(path_out)}")

# the format of my phlog filenames is as follows:
# YYYY-MM-DD - Post Title
r = re.compile("^(\d{4}-\d{2}-\d{2}) - (.*)$")

# loop over all valid files in input path
for fpath in path_in.iterdir():
    fname = fpath.parts[-1]
    res = r.match(str(fname))
    if res is not None:
        # looks like this is a valid filename for my phlog posts
        date, title = res.groups()

        # posts are nt 
        orig_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        repost_date = orig_date + relativedelta(months=relativedelta_months)
        
        # generate new filename
        new_fname = f"{repost_date}-{re.sub('[^0-9a-zA-Z-]+', '', title.lower().replace(' ','-'))}.md"

        # generate new content
        with fpath.open() as f:
            phlog_post = f.read()
        
        hugo_post = f'''+++
title = "+mala's gopherhole: {orig_date} - {title}"
date = {repost_date}
+++

```
{phlog_post}
```
'''
        fpath_out = path_out / new_fname

        print(f"{fpath} -> {fpath_out}")
        with fpath_out.open("wt") as f:
            f.write(hugo_post)
