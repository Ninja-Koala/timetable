#!/usr/bin/python3
import json, sys

input_file=""
output_file=""

column_width=240

weekday_y_pos=57

border_x=24
border_y=24

box_end_y=876

text_line_spacing=34

hor_line_pos=72

font_size=30

stroke_width=3.6

event_pos_start=97
event_pos_factor=0.66

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

svg_text="\t\t<text x=\"{0:.9g}\" y=\"{1:.9g}\">{2}</text>\n"

svg_box="M{0} {1} L{2} {1} L{2} {3} L{0} {3} Z"
svg_hor_line="M{0} {1} L{2} {1}"
svg_ver_line="\t\t\tM{0} {1} L{0} {2}\n"

ver_line_pos=border_x+column_width

svg_ver_lines=""
for i in range(len(timetable["week"])-1):
	svg_ver_lines+=svg_ver_line.format(ver_line_pos,border_y,box_end_y)
	ver_line_pos+=column_width

svg_box=svg_box.format(border_x,border_y,ver_line_pos,box_end_y)
svg_hor_line=svg_hor_line.format(border_x,hor_line_pos,ver_line_pos)

text_x_pos=border_x+column_width/2

full_text=""
for day in timetable["week"]:
	full_text+=svg_text.format(text_x_pos,weekday_y_pos,day["name"])
	for event in day["events"]:
		#TODO: better (configurable) time scaling
		ver_pos=event_pos_start+(int(event["time"]["hour"])*120+int(event["time"]["minute"])-960)*event_pos_factor
		full_text+=svg_text.format(text_x_pos,ver_pos+0*text_line_spacing,event["time"]["hour"] + ":" + event["time"]["minute"])
		full_text+=svg_text.format(text_x_pos,ver_pos+1*text_line_spacing,event["course"])
		full_text+=svg_text.format(text_x_pos,ver_pos+2*text_line_spacing,event["name"])
		if len(event["room"])>0:
			full_text+=svg_text.format(text_x_pos,ver_pos+3*text_line_spacing,event["room"])
	text_x_pos+=column_width


svg_path="""\"
			{0}
			{1}
{2}	        \"\
""".format(svg_box,svg_hor_line,svg_ver_lines)

template="""\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="{0}" height="{1}" version="1.1" xmlns="http://www.w3.org/2000/svg">
	<defs>
		<style type="text/css">
			@font-face {{
			font-family: Dosis;
			src: url('Dosis-VariableFont_wght.woff2');
		}}
		</style>
	</defs>
	<rect x="0" y="0" width="100%" height="100%" fill="white"/>
	<path d={2}
	style="fill:none;stroke:black;stroke-width:{3}"/>
	<g font-family=\"Dosis\" font-weight=\"600\"  fill=\"black\" style=\"font-size:{4}px\" text-anchor=\"middle\">
{5}	</g>
</svg>
""".format(ver_line_pos+border_x,box_end_y+border_y,svg_path,stroke_width,font_size,full_text)

try:
	svg_file=open(output_file,"w")
	svg_file.write(template)
except:
	print("Couldn't write file")
