# Sample Workflow Integration script

import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from types import NoneType

# element IDs
winID = "com.blackmagicdesign.resolve.TwitchCSVImport"	# should be unique for single instancing
importID = "Import"
filepathID = "URL"
fileContentID = "TextEdit"
startToggleID = "StartToggle"
startTimeID = "StartTime"
endToggleID = "EndToggle"
endTimeID = "EndTime"
colorID = "ColorBox"
timelineID = "Timeline"
trackID = "Track"
deleteID = "Delete"
deleteColorID = "DeleteByColor"

#Globals
ui = fusion.UIManager
dispatcher = bmd.UIDispatcher(ui)
timeline = project.GetCurrentTimeline()

# check for existing instance
win = ui.FindWindow(winID)
if win:
	win.Show()
	win.Raise()
	exit()
	
# otherwise, we set up a new window, with HTML header
logoPath = fusion.MapPath(r"C:/ProgramData/Blackmagic Design/DaVinci Resolve/Support/Workflow Integration Plugins/img/twitch_icon_small.png")
header = '<html><body><h2 style="vertical-align:middle;">'
header = header + '<img src="' + logoPath + '"/>&nbsp;&nbsp;'
header = header + '<b>Twitch Marker CSV Importer</b>'
header = header + '</h2></body></html>'

# define the window UI layout
win = dispatcher.AddWindow({
	'ID': winID,
	'Geometry': [ 100,100,655,500 ],
	'WindowTitle': "Twitch Marker CSV Importer",
	},
	ui.VGroup([
		ui.Label({ 'Text': header, 'Weight': 0.1, 'Font': ui.Font({ 'Family': "DDG_ProximaNova" }) }),

		ui.HGroup({ 'Weight': 0 }, [
			ui.Button({ 'ID': importID, 'Weight': 0, 'Text': "Import", "ToolTip": "Select file for import" }),
			ui.Label({ 
				'ID': filepathID,
				'Text': "No file selected",
				'WordWrap': False,
				'Font': ui.Font({ 'Family': "DDG_ProximaNova", 'PixelSize': 12 }) 
				}),
			]),

		ui.TextEdit({
			'ID': fileContentID,
			'TabStopWidth': 28,
			'Font': ui.Font({ 'Family': "Sans Mono", 'PixelSize': 12, 'MonoSpaced': True, 'StyleStrategy': { 'ForceIntegerMetrics': True } }),
			'LineWrapMode': "NoWrap",
			'AcceptRichText': False
			}),

		ui.HGroup({ 'Weight': 0, }, [
			ui.CheckBox({ 'Weight': 0, 'ID': startToggleID, 'Text': "Start Time:", 'MaxLength': 2 }),
			ui.LineEdit({ 'Weight': 1, 'ID': startTimeID, 'PlaceholderText': "hh:mm:ss", 'Enabled': False, 'MaxLength': 8 }),
			ui.HGap(1),
			ui.CheckBox({ 'Weight': 0, 'ID': endToggleID, 'Text': "End Time:", 'MaxLength': 2 }),
			ui.LineEdit({ 'Weight': 1, 'ID': endTimeID, 'PlaceholderText': "hh:mm:ss", 'Enabled': False, 'MaxLength': 8 }),
			ui.HGap(1),
			ui.Label({ 
				'Weight': 0,
				'Text': "Marker Color:",
				'Font': ui.Font({ 'Family': "DDG_ProximaNova", 'PixelSize': 12 }) 
				}),
			ui.ComboBox({ "ID": colorID, "ItemText": "test", "Editable": False }),
			ui.HGap(0, 2),
			]),

		ui.HGroup({ 'Weight': 0, }, [
			ui.Button({ 'ID': timelineID,  'Text': "Add to Timeline" }),
			ui.Button({ 'ID': trackID,  'Text': "Add to Track" }),
			ui.HGap(2),
			ui.Label({ 
				'Weight': 0,
				'Text': "Delete markers:",
				'Font': ui.Font({ 'Family': "DDG_ProximaNova", 'PixelSize': 12 }) 
				}),
			ui.Button({ 'ID': deleteID, 'Weight': 0, 'Text': "All" }),
			ui.Button({ 'ID': deleteColorID, 'Weight': 0, 'Text': "By Color" }),
			ui.HGap(0, 2),
			])
		])
	)

win.Find(colorID).AddItems([
	"Blue","Cyan","Green","Yellow","Red","Pink",
	"Purple","Fuchsia","Rose","Lavender","Sky",
	"Mint","Lemon","Sand","Cocoa","Cream"
])

# Event handlers
def OnClose(ev):
	dispatcher.ExitLoop()

def OnImport(ev):
	FileReady()

def OnStartToggle(ev):
	win.Find(startTimeID).Enabled = not win.Find(startTimeID).Enabled

def OnEndToggle(ev):
	win.Find(endTimeID).Enabled = not win.Find(endTimeID).Enabled

def OnTimeline(ev):
	url = win.Find(filepathID).Text
	CSVImport(url, "timeline")

def OnTrack(ev):
	path = win.Find(filepathID).Text
	CSVImport(path, "track")

def OnDeleteAll(ev):
	track = timeline.GetCurrentVideoItem()

	timeline.DeleteMarkersByColor("All")
	track.DeleteMarkersByColor("All")

def OnDeleteColor(ev):
	track = timeline.GetCurrentVideoItem()
	color = win.Find(colorID).CurrentText
	timeline.DeleteMarkersByColor(color)
	track.DeleteMarkersByColor(color)

# assign event handlers
win.On[winID].Close      		= OnClose
win.On[importID].Clicked 		= OnImport
win.On[startToggleID].Clicked	= OnStartToggle
win.On[endToggleID].Clicked		= OnEndToggle
win.On[timelineID].Clicked  	= OnTimeline
win.On[trackID].Clicked  		= OnTrack
win.On[deleteID].Clicked  		= OnDeleteAll
win.On[deleteColorID].Clicked  	= OnDeleteColor

# Functions
def FileReady():
	root = tk.Tk()

	root.withdraw()
	root.geometry('0x0+0+0')
	root.attributes('-alpha', 0)
	root.deiconify()
	root.lift()
	root.focus_force()

	path = filedialog.askopenfilename(title="Select Twitch CSV data file", filetypes=[('CSV File', '*.csv')])
	root.destroy()

	if path != "":
		win.Find(filepathID).Text = path
		file = open(path, "r")
		win.Find(fileContentID).Text = file.read()
		return path
	else:
		win.Find(filepathID).Text = "No file selected"
		win.Find(fileContentID).Text = ""
		return

def CSVImport(path, mode: str):
	if path != "No file selected":
		track = timeline.GetCurrentVideoItem()
		color = win.Find(colorID).CurrentText
		if type(timeline) != NoneType:
			with open(path, newline='') as csvfile:
				spamreader = csv.reader(csvfile, quotechar='|')
				for row in spamreader:
					time = parseToFrames(row[0])
					author = row[2]
					title = row[3]
					if len(row[3]) <= 0:
						title = "Twitch Marker"
					clip = time
					start = int(timeline.GetStartFrame())
					end = int(timeline.GetEndFrame())

					if win.Find(startTimeID).Enabled == True:
						userStart = int(parseToFrames(win.Find(startTimeID).Text))
						clip = time - userStart
						start = userStart
					if win.Find(endTimeID).Enabled == True:
						userEnd = int(parseToFrames(win.Find(endTimeID).Text))
						end = userEnd
					frames = end - start
					
					if clip > 0 and clip < frames:
						if mode == "timeline":
							timeline.AddMarker(time, color, title, author, 1, "imported")
						elif mode == "track":
							track.AddMarker(time, color, title, author, 1, "imported")
					else:
						print("Marker \"" + title + "\" is not within specified time range.")
		else:
			alert("No timeline selected!", "Must have timeline currently selected.")
	else:
		alert("No file selected!", "Must select CSV file for import.")

def parseToFrames(timestamp: str):
	time_delim = timestamp.split(":")
	hour   = int(time_delim[0])
	minute = int(time_delim[1])
	second = int(time_delim[2])
	
	frame = ((((hour*60)*60)*60) + ((minute*60)*60) + (second*60))
	return frame

def alert(title: str, message: str, kind='info', hidemain=True):
    if kind not in ('error', 'warning', 'info'):
        raise ValueError('Unsupported alert kind.')

    show_method = getattr(messagebox, 'show{}'.format(kind))
    show_method(title, message)

# Main dispatcher loop
win.Show()
dispatcher.RunLoop()