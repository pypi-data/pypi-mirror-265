# dsame3
Python EAS SAME Alert Message Decoder

**dsame3** is a program to decode [EAS](http://en.wikipedia.org/wiki/Emergency_Alert_System)/[SAME](http://en.wikipedia.org/wiki/Specific_Area_Message_Encoding) (Emergency Alert System/Specific Area Message Encoding) alert messages. These messages are primarily used by the National Weather Service for weather-related warnings. **dsame** will decode a demodulated message, filter by SAME ([US](http://www.nws.noaa.gov/nwr/coverage/county_coverage.html)/[CA](http://www.ec.gc.ca/meteo-weather/default.asp?lang=En&n=E5A4F19C-1)) and/or event code, provide readable text, or run an external program.

**DO NOT RELY ON THIS PROGRAM WHEN LOSS, DAMAGE, INJURY OR DEATH MAY OCCUR!**

###NOTICE

This program was originally written by [cuppa_joe](https://github.com/cuppa-joe/dsame), and was rewritten to include new updates and upgrade compatibility so others can modify the code without the headache of trying to work with Python 2.7. THIS IS NOT MY ORIGINAL CODE! I have modified it, and I will be updating it as necessary, since updates seem to have stopped on the original repository. 

###Requirements

* [Python](https://www.python.org/) 3.8+

###Installation

`pipx install dsame3_simple`

Check [here](https://github.com/jamieden/dsame3/releases/latest) to download the latest release.

###Command Line Options

```
usage: dsame3_simple [-h] [--msg MSG] [--same [SAME [SAME ...]]]
                     [--event [EVENT [EVENT ...]]] [--lang LANG]
                     [--loglevel {10,20,30,40,50}] [--version]
                     [--call CALL] [--command COMMAND]
```
####Options

Option            | Description                                                           | Example
:-----------------|:----------------------------------------------------------------------|:----------------------
`msg`             | Message to decode. Omit to read from standard input                   | `--msg "ZCZC-WXR-RWT-020103-020209-020091-020121-029047-029165-029095-029037+0030-1051700-KEAX/NWS"`
`same`            | List of SAME codes to monitor                                         | `--same 029165 029095`
`event`           | List of event codes to monitor                                        | `--event RWT TOR SVR`
`loglevel`        | Set log level                                                         | `--loglevel 10`
`call`            | Call an external program                                              | `--call alert.sh`
`lang`            | Selects the language for the program**                                | `--lang EN`
`command`         | External command line. Omit --call to send to standard output         | `--command "Event Code: {EEE}"`
`wrap`            | Line length to wrap message (0 for no wrap)                           | `--wrap 80`

** The only available language options so far are English (EN) and Spanish (SP). The program defaults to English. 

###Usage

**dsame3** can decode EAS messages from the command line, directly from the output of an external command, or by capturing the ouput of a shell script/batch file or external program. Use `msg` for single command line decoding. Without this option, standard input is used. Press `CTRL-C` to exit the program.

###Filtering Alerts

There are two comands used to filter alerts. None, one or both can be specified. The `same` command is a list of SAME area codes ([United States](http://www.nws.noaa.gov/nwr/coverage/county_coverage.html)/[Canada](http://www.ec.gc.ca/meteo-weather/default.asp?lang=En&n=E5A4F19C-1)), and the `event` command is a list of event codes to monitor.

####Event Codes

*This list includes current and proposed event codes.*

Code| Description                  |Code| Description
:--:|:-----------------------------|:--:|:-----------------------------
ADR | Administrative Message       |AVA | Avalanche Watch
AVW | Avalanche Warning            |BHW | Biological Hazard Warning
BWW | Boil Water Warning           |BZW | Blizzard Warning
CAE | Child Abduction Emergency    |CDW | Civil Danger Warning
CEM | Civil Emergency Message      |CFA | Coastal Flood Watch
CFW | Coastal Flood Warning        |CHW | Chemical Hazard Warning
CWW | Contaminated Water Warning   |DBA | Dam Watch
DBW | Dam Break Warning            |DEW | Contagious Disease Warning
DMO | Demo Warning                 |DSW | Dust Storm Warning
EAN | Emergency Action Notification|EAT | Emergengy Action Termination
EQW | Earthquake Warning           |EVA | Evacuation Watch
EVI | Evacuation Immediate         |EWW | Extreme Wind Warning
FCW | Food Contamination Warning   |FFA | Flash Flood Watch
FFS | Flash Flood Statement        |FFW | Flash Flood Warning
FLA | Flood Watch                  |FLS | Flood Statement
FLW | Flood Warning                |FRW | Fire Warning
FSW | Flash Freeze Warning         |FZW | Freeze Warning
HLS | Hurricane Local Statement    |HMW | Hazardous Materials Warning
HUA | Hurricane Watch              |HUW | Hurricane Warning
HWA | High Wind Watch              |HWW | High Wind Warning
IBW | Iceberg Warning              |IFW | Industrial Fire Warning
LAE | Local Area Emergency         |LEW | Law Enforcement Warning
LSW | Land Slide Warning           |NAT | National Audible Test
NIC | National Information Center  |NMN | Network Message Notification
NPT | National Periodic Test       |NST | National Silent Test
NUW | Nuclear Plant Warning        |POS | Power Outage Statement
RHW | Radiological Hazard Warning  |RMT | Required Monthly Test
RWT | Required Weekly Test         |SMW | Special Marine Warning
SPS | Special Weather Statement    |SPW | Shelter in Place Warning
SSA | Storm Surge Watch            |SSW | Storm Surge Warning
SVA | Severe Thunderstorm Watch    |SVR | Severe Thunderstorm Warning
SVS | Severe Weather Statement     |TOA | Tornado Watch
TOE | 911 Outage Emergency         |TOR | Tornado Warning
TRA | Tropical Storm Watch         |TRW | Tropical Storm Warning
TSA | Tsunami Watch                |TSW | Tsunami Warning
VOW | Volcano Warning              |WFA | Wild Fire Watch
WFW | Wild Fire Warning            |WSA | Winter Storm Watch
WSW | Winter Storm Warning         |SQW | Snow Squall Warning*

* Snow Squall Warnings are not conveyed to the EAS, however, it was added just in case/for futureproofing.

An alert must match one of each specified alert type in order to be processed. If an alert type is omitted, any alert will match that type. In most cases, using only SAME codes to filter alerts will be the best option.

###External Commands

The `call` option runs an external program, script/batch file for each alert.  The `command` option defines the command string sent to that program, script or batch file, or to standard output if the `call` option is omitted. The following variables can be used in command strings.

####Command Variables

Variable        | Description                       | Example
:---------------|:----------------------------------|:------------------
 {ORG}          | Organization code                 | WXR
 {EEE}          | Event code                        | RWT
 {PSSCCC}       | Geographical area (SAME) codes    | 020103-020209-020091-020121-029047-029165-029095-029037
 {TTTT}         | Purge time code                   | 0030
 {JJJHHMM}      | Date code                         | 1051700
 {LLLLLLLL}     | Originator code                   | KEAX/NWS
 {COUNTRY}      | Country code                      | US
 {organization} | Organization name                 | National Weather Service
 {location}     | Originator location               | Pleasant Hill, Missouri
 {event}        | Event type                        | Required Weekly Test
 {type}         | Event type indicator              | T
 {start}        | Start time                        | 12:00 PM
 {end}          | End time                          | 12:30 PM
 {length}       | Length of event                   | 30 minutes
 {seconds}      | Event length in seconds           | 1800 
 {date}         | Local date                        | 04/15/15 12:00:38
 {MESSAGE}      | Readable message                  | *(See sample text output below)*


###Sample Commands

Decoding from a text file using standard input:

`cat zczc.txt | dsame3_simple --same 029165`

Call an external script with the event type and length:

`dsame3_simple --same 029165 --call alert.sh --command "{length}" "{event}"`

Decoding a message from the command line:

`dsame3_simple --msg "ZCZC-WXR-RWT-020103-020209-020091-020121-029047-029165-029095-029037+0030-1051700-KEAX/NWS" --text`

Send an alert to a [Pushbullet](https://www.pushbullet.com) channel:

`dsame3_simple --call pushbullet-channel.sh --command "{event}" "{MESSAGE}"`

###Sample Text Output

>The National Weather Service in Pleasant Hill, Missouri has issued a Required Weekly Test valid until 12:30 PM for the following counties in Kansas: Leavenworth, Wyandotte, Johnson, Miami, and for the following counties in Missouri: Clay, Platte, Jackson, Cass. (KEAX/NWS)


###Known Issues

* ~~SASMEX/SARMEX, a Mexican system for seismic alerts, is not implemented due to lack of documentation.~~ This issue has *HOPEFULLY* been resolved
* ~~A correct and complete list of ICAO location codes used by the National Weather Service messages is not available.~~ This issue has *HOPEFULLY* been resolved
* ~~Country detection may not be reliable for some locations with duplicate SAME codes.~~ This issue has *HOPEFULLY* been resolved
* Date and time information may not be accurate when decoding old messages or messages from another time zone.
* Multimon-ng will not decode the same alert in succession. This should only be an issue during testing and can be avoided by alternating test alerts.

---
