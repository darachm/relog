#!/usr/bin/python3

from pathlib import Path
import re

inbox_dir = Path("./inbox")

entries   = dict()
suppfiles = dict()

move_suppfile = re.compile("inbox/")

for each_file in inbox_dir.iterdir():
  basename = move_suppfile.sub("",str(each_file)) 
  if str(each_file).endswith(("png")):
    suppfiles[basename] = "files/"+basename
  else:
    entries[basename] = each_file.read_text()

tags = dict()

a_link = re.compile("!\[.*\]\((.+)\)")
for each_basename in entries.keys():
  links = a_link.search(entries[each_basename])
  for each_link in links.groups():
    if suppfiles[each_link]:
      entries[each_basename] = re.compile(each_link).sub(
        suppfiles[each_link]
        ,entries[each_basename] )
  Path("entries/"+each_basename).write_text(
    entries[each_basename] )
  these_tags_string = re.split("\n",entries[each_basename],1)[0]
  these_tags = re.split("\s+",these_tags_string)
  for each_tag in these_tags:
    if each_tag in tags:
      tags[each_tag].append(each_basename)
    else:
      tags[each_tag] = list()
      tags[each_tag].append(each_basename)

print(tags)

