# Twitch-Marker-to-DaVinci
Workflow Integration for DaVinci Resolve to import Twitch VOD Markers from .csv files

![image](https://user-images.githubusercontent.com/106890554/188338246-94a0b830-fd6a-4280-8e80-e12af12a66d1.png)



## Installation:
* Place `Twitch CSV Importer.py` and the `img` folder into `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Workflow Integration Plugins` or where ever you have DaVinci installed.

* Open DaVinci Resolve and **create a new project** or **open an existing project**

* Make sure you have a **timeline created and opened**, and go to the **Edit** tab 

![image](https://user-images.githubusercontent.com/106890554/188337943-0b0bfd79-fe9c-41ed-8471-8c485222f229.png)

* At the top, go to **Workplace** -> **Workflow Integrations** -> **Twitch CSV Importer**

![image](https://user-images.githubusercontent.com/106890554/188338074-ad3a912c-16b8-4aae-adea-b0baab99d33b.png)

* The window should pop up and you'll be ready to go!
___
## How to use:
![image](https://user-images.githubusercontent.com/106890554/188339858-725dc65c-6c3e-4ddf-9ad5-3dea980fa907.png)

### 1. Import:
Click to open the file browser to select your CSV file. ***\*\*(WINDOW MAY APPEAR UNDER THE PROGRAM, MINIMIZE DAVINCI TO FIND)***
### 2. CSV Content Box:
When you import the CSV file, this box will show you the contents of the CSV file. You probably won't have to edit this ever, but it lets you peek at the markers to know what file you picked.
### 3. Start and End Time:
You can enable these if you downloaded only part of the VOD to edit, and enter the timecodes of the In and Out points of your clip so that the markers match. Otherwise, if you had, say, a clip of the original VOD that's only from minute 40 to 1h30m, and the original VOD was 2h long, the markers would be 40 minutes out of sync.
### 4. Marker Color
Here you can select the color of the markers you want to import and/or want to delete. *(More on deleting below)*
### 5. Add to Timeline/Track
This allows you to choose whether you want to import the markers on the timeline *(above the video/audio tracks)* or on the video track *(harder to see but can transfer over into the **Fusion** tab)* ***\*\*(Only applies to the selected track!)***
### 6. Delete markers
Pretty self-explanatory, the `All` button will delete all markers on the timeline **AND** track. The `By Color` button will delete all markers of the selected color above **(4)**
___
## How to get CSV data:
On Twitch, you can download a CSV file containing timestamps of popular clips and/or timestamps of markers placed by you. *(using /marker in the twitch chat)*
* First, go to `https://dashboard.twitch.tv/u/[YOUR CHANNEL NAME HERE]/content/video-producer`
* Then, pick a stream to pull data from and click the ***Highlight*** button to the right of it

![image](https://user-images.githubusercontent.com/106890554/188338527-6a821279-c11f-4e92-a855-121ac885d11a.png)

* You'll be taken to the highlighter page where you can see markers and popular clip times. To the bottom-right of the page, on the timeline there'll be 3 vertical dots. Click those to open a menu where you should see options to save CSV data.

![image](https://user-images.githubusercontent.com/106890554/188339400-37ceb364-bf2d-43b7-9b0c-376b23d05aa6.png)


![image](https://user-images.githubusercontent.com/106890554/188339385-ce6d0a82-5fd3-4d39-ab15-5d28ce5e7ca7.png)
