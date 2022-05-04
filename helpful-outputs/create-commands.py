#!/usr/bin/env python

# This has to run as user omero-server.
# Assumes that omero-upload was installed on the server.
# git clone https://gitlab.com/idr/idr0082-pennycuick-lesions.git
# cd idr0082....
# cp attachments.txt /tmp
# cp upload_attachments.py /tmp
# chmod +x /tmp/upload_attachments.py
# sudo su omero-server
# cd /tmp
# . /opt/omero/server/venv3/bin/activate
# python upload_attachments.py

import csv
import collections

rows = []
plate_names = []
plate_name_ids = []
paths =[]
ids = []
match = 0
full_match = 0
match_count = 0
no_match_count = 0
ids_file = "./prod-130-C-ids"
attachment_map = "./screenC-attach-map.tsv"
duplicate_names = ['3DView.avi', '3DView.jpg']
prefix = "python /uod/idr/metadata/idr-utils/scripts/annotate/attach_file.py"

def process_line(line, count, match, rows):
    parts = line.split('	')
    path = parts[1]
    plate_name = parts[0]
    plate_names.append(plate_name)
    paths.append(path)
    return plate_names,paths

def write_tsv(rows):
    with open('./prod-130-C-commands.tsv', mode='w') as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter=" ")
        tsv_writer.writerows(rows)

with open(ids_file) as ip:
    line = ip.readline().strip()
    count2 = 0
    while line and len(line) > 0:
        bits = line.split(',')
        id = bits[0]
        print ("id")
        print(id)
        plate_name_id = bits[1]
        plate_name_ids.append(plate_name_id)
        ids.append(id)
        line = ip.readline().strip()

print(ids)
print(plate_name_ids)

with open(attachment_map) as fp:
    line = fp.readline().strip()
    count = 0
    while line and len(line) > 0:
        count += 1
        parts = line.split('	')
        path = parts[1]
        plate_name = parts[0]
        count += 1
        line = fp.readline().strip()
        for i in range (0, len(ids)):
            print (plate_name_ids[i])
            print (plate_name)
            if plate_name_ids[i] == plate_name:
                rows.append([prefix, path+" Plate:"+ids[i]])

            
print([item for item, count in collections.Counter(plate_names).items() if count > 1])
write_tsv(rows)

