

'''
VERSION 1.5

Thanks for using Heroic Bash Launcher - A simple program that allows you to launch any of your Epic Store games from literally anywhere on Linux!

Do note that this project is open-source and is under the GPL-3.0 License. For more information, you can check out the LICENSE.md file.
Moreover, this software does not come without any warranty.

Hope you liked my little project! Have fun gaming!

-- By Redromnon
'''

import os, glob, json, time


#GETTING PATH OF PRESENT DIRECTORY
programfolderpath = os.getcwd()


#ASSIGNING PATH TO HEROIC GAMES CONFIG FILE
homeuser = os.path.expanduser("~")
path = homeuser + "/.config/heroic/GamesConfig"
os.chdir(path)
#print(os.getcwd())
print()


#GLOBAL VARIABLES
global heroic # Heroic's legendary launch

global legendaryinstalledpath # List of installed games
legendaryinstalledpath = homeuser + "/.config/legendary/installed.json"



#THE BODY PART
#####################################################################

#CREATING GAME LAUNCH (.sh) FILES
def launchfile(game):


  #Converting keys intro array to get game alias
  gamekeyarray = list(game.keys()) #Keys to array 
  gamename = gamekeyarray[0] #First index contains the game's name

  #################################

  #FINDING TITLE NAME OF THE GAME
  def findgamename(gamename): 

    #Convert the json file into a dictionary called installed
    with open(legendaryinstalledpath) as f:
      installed = json.load(f) 

    #Finding the game's title name
    realgamename = installed[gamename]["title"]
    #print(realgamename)

    return realgamename

  #################################

  realgamename = findgamename(gamename)

  print("\nPreparing " + realgamename + "....")


  #################################

  #CREATING THE LAUNCH FILE

  def gameFile(launchcommand, offline_launchcommand, cloudsync):
    
    #Creating the game file name
    gameFile = programfolderpath + "/GameFiles/" + gamename + ".sh"

    #Creating game file
    with open(gameFile, "w") as g:
        g.write('#!/bin/bash \n\n' + '#Game Name = ' + realgamename + '\n\n' + 'cd .. && ./setup.sh #Overrides launch parameters' + '\n\n' + cloudsync + '\n\n' + launchcommand + '|| (echo "NO INTERNET CONNECTION. Running game in offline mode..." && ' + offline_launchcommand + ')')

    #Making the file executable
    os.system("chmod u+x " + gameFile)


  ################################

  #CONFIGURING BOOLEAN PARAMETERS

  #audioFix
  if game[gamename]["audioFix"] == True:
    audioFix = "PULSE_LATENCY_MSEC=60 "
  else:
    audioFix = ""

  #print(audioFix)


  #enableEsync
  if game[gamename]["enableEsync"] == True:
    enableEsync = "WINEESYNC=1 "
  else:
    enableEsync = ""

  #print(enableEsync)


  #enableFsync
  if game[gamename]["enableFsync"] == True:
    enableFsync = "WINEFSYNC=1 "
  else:
    enableFsync = ""

  #print(enableFsync)


  #enableFSR
  if game[gamename]["enableFSR"] == True:
    enableFSR = "WINE_FULLSCREEN_FSR=1 "
  else:
    enableFSR = ""

  #print(enableFSR)


  #enableResizableBar
  if game[gamename]["enableResizableBar"] == True:
    enableResizableBar = "VKD3D_CONFIG=upload_hvv "
  else:
    enableResizableBar = ""

  #print(enableResizableBar)


  #nvidiaPrime
  if game[gamename]["nvidiaPrime"] == True:
    nvidiaPrime = "__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia "
  else:
    nvidiaPrime = ""

  #print(nvidiaPrime)


  #offlineMode
  if game[gamename]["offlineMode"] == True:
    offlineMode = "--offline "
  else:
    offlineMode = ""

  #offlineMode parameter when no internet connection
  force_offlineMode = "--offline "

  #print(offlineMode)


  #showFps
  if game[gamename]["showFps"] == True:
    showFps = "DXVK_HUD=fps "
  else:
    showFps = ""

  #print(showFps)


  #showMangohud
  if game[gamename]["showMangohud"] == True:
    showMangohud = "MANGOHUD=1 "
  else:
    showMangohud = ""

  #print(showMangohud)


  #useGameMode
  if game[gamename]["useGameMode"] == True:
    useGameMode = "/usr/bin/gamemoderun "
  else:
    useGameMode = ""

  #print(useGameMode)



  #CONFIGURING OTHER PARAMETERS

  #Check if parameters are present (launcherArgs, otherOptions, targetExe)
  def ifpresent(parameter):

    if parameter in game[gamename].keys():
      return True



  #maxSharpness
  if game[gamename]["enableFSR"] == True:
    maxSharpness = "WINE_FULLSCREEN_FSR_STRENGTH=" + str(game[gamename]["maxSharpness"]) + " "
  else:
     maxSharpness = ""

  #print(maxSharpness)


  #launcherArgs
  global launcherArgs #Declared this because of reference assignment error
  if ifpresent("launcherArgs") == True:

    if game[gamename]["launcherArgs"] == "":
      launcherArgs = ""
    else:
      launcherArgs = game[gamename]["launcherArgs"] + " "
  else:
    launcherArgs = ""

    #print(launcherArgs) 


  #otherOptions
  if ifpresent("otherOptions") == True:

    if game[gamename]["otherOptions"] == "":
      otherOptions = ""
    else:
      otherOptions = game[gamename]["otherOptions"] + " "
  else:
    otherOptions = ""

    #print(otherOptions)


  #targetExe
  if ifpresent("targetExe") == True:

    if game[gamename]["targetExe"] == "":
      targetExe = ""
    else:
      targetExe = "--override-exe " + game[gamename]["targetExe"] + " "
  else:
    targetExe = ""

    #print(targetExe)



  #winePrefix
  winePrefix = game[gamename]["winePrefix"]

  #print(winePrefix)


  #wineVersion (IMPACTS LAUNCH COMMAND)

  #bin 
  wineVersion_bin = game[gamename]["wineVersion"]["bin"]

  #print(wineVersion_bin)


  #name(IMPORTANT)

  launchcommand = " "
  launchgame = "launch " + gamename + " " 
  heroic = "/opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary "

  if "Proton" in game[gamename]["wineVersion"]["name"]:

    steamclientinstall = "STEAM_COMPAT_CLIENT_INSTALL_PATH=" + homeuser + "/.steam/steam "
    steamcompactdata = "STEAM_COMPAT_DATA_PATH='" + winePrefix + "' "
    bin = '--no wine --wrapper "' + wineVersion_bin + ' run" '

    launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + steamclientinstall + steamcompactdata + showMangohud + useGameMode + heroic + launchgame + targetExe + offlineMode + bin + launcherArgs
    offline_launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + steamclientinstall + steamcompactdata + showMangohud + useGameMode + heroic + launchgame + targetExe + force_offlineMode + bin + launcherArgs

  elif "Wine" in game[gamename]["wineVersion"]["name"]:

    bin = "--wine " + wineVersion_bin + " "
    wineprefix = "--wine-prefix '" + winePrefix + "' "

    launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + showMangohud + useGameMode + heroic + launchgame + targetExe + offlineMode + bin + wineprefix + launcherArgs
    offline_launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + showMangohud + useGameMode + heroic + launchgame + targetExe + force_offlineMode + bin + wineprefix + launcherArgs

  #savesPath (CloudSync)
  if ifpresent("savesPath") == True:

    if game[gamename]["savesPath"] == "":
      cloudsync = ""
    else:
      cloudsync = heroic + 'sync-saves --save-path "' + game[gamename]["savesPath"] + '" ' + gamename + ' -y '

  #print("CloudSync = " + cloudsync)


  #The entire launch command
  #print(launchcommand)

  #Now create the file
  gameFile(launchcommand,offline_launchcommand, cloudsync)
  print("Done!")



#####################################################################



#FINDING THE INSTALLED GAME FILES & GENERATING LAUNCH FILE PER GAME

print("Generating a list of installed games... ")


#Clean leftover files
print("\nCleaning left over game files if any...")
os.system("/opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary cleanup")



listofgames = glob.glob('./*.json') # List of all available .json game files

l = len(listofgames) # No. of games


#EXIT the program if no games are found
if l == 0:
  print("No games installed...\nCouldn't create game launch files.")
  exit()

i = 0

################################
#Convert the legendary installed.json file into a dictionary called installed
with open(legendaryinstalledpath) as f:
  installed = json.load(f)

#Converting "installed" keys into array to get game alias
installedkeyarray = list(installed.keys())

################################
#launchfile(list[7])

print("\n\nDone! Now creating launch files...\n")

#Loop for generating launch commands for each installed game 
while i != l:
	
  #Convert the json file into a dictionary called game
  with open(listofgames[i]) as f:
    game = json.load(f)

  checkList = list(game.keys()) # Keys into array contaning - Name of the game, version and explicit
  	
  #Check if game is installed
  if "version" in checkList:

    if checkList[0] in installedkeyarray:
    
      launchfile(game) # Call the main function
	
  i = i+1


#####################################


#END OF THE PROGRAM
print("\n...Process finished. Launch files stored in GameFiles folder.\n Have fun gaming!")
time.sleep(1.5)# wait for 1.5 seconds and then end
