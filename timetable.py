#!/usr/bin/python3
import json, sys

input_file=""
output_file=""

if len(sys.argv)<2:
	print("Usage: ./timetable.py input_json_file [output_svg_file]")
	exit(1)
else:
	if sys.argv[1].split(".")[1] != "json":
		print("Input must be in .json format!")
		exit(1)
	input_file=sys.argv[1]
	if len(sys.argv)==3:
		if sys.argv[2].split(".")[1] != "svg":
			print("Output must be in .svg format!")
			exit(1)
		output_file=sys.argv[2]
	else:
		output_file=sys.argv[1].split(".")[0]+".svg"
		
try:
	json_file=open(input_file,"r")
	file_content=json_file.read()
	timetable = json.loads(file_content)
except:
	print("Couldn't open file")
	exit(1)

column_width=150

svg_text="\t<text font-family=\"Monospace\" x=\"{0}\" y=\"{1}\" fill=\"black\" style=\"font-size:18px\" text-anchor=\"middle\">{2}</text>\n"

svg_box="M20 20 L{0} 20 L{0} 540 L20 540 Z"
svg_hor_line="M20 50 L{0} 50"
svg_ver_line="\t\t\tM{0} 20 L{0} 540\n"


svg_ver_lines=""
lines_pos=170
for i in range(len(timetable["week"])-1):
	svg_ver_lines+=svg_ver_line.format(lines_pos)
	lines_pos+=column_width

svg_box=svg_box.format(lines_pos)
svg_hor_line=svg_hor_line.format(lines_pos)

full_text=""
text_pos=100
for day in timetable["week"]:
	full_text+=svg_text.format(text_pos,40,day["name"])
	for event in day["events"]:
		ver_pos=70+(int(event["time"]["hour"])*60+int(event["time"]["minute"])-480)*0.75
		full_text+=svg_text.format(text_pos,ver_pos+00,event["time"]["hour"] + ":" + event["time"]["minute"])
		full_text+=svg_text.format(text_pos,ver_pos+20,event["course"])
		full_text+=svg_text.format(text_pos,ver_pos+40,event["name"])
		full_text+=svg_text.format(text_pos,ver_pos+60,"("+event["room"]+")")
	text_pos+=column_width


svg_path="""\"
			{0}
			{1}
{2}	        \"\
""".format(svg_box,svg_hor_line,svg_ver_lines)

template="""\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg height="560" width="{0}" version="1.1" xmlns="http://www.w3.org/2000/svg">
	<rect x="0" y="0" width="100%" height="100%" fill="white"/>
	<path d={1}
	style="fill:none;stroke:black;stroke-width:3" />
{2}</svg>
""".format(lines_pos+20,svg_path,full_text)

try:
	svg_file=open(output_file,"w")
	svg_file.write(template)
except:
	print("Couldn't write file")
