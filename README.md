# BGS-Tally
A simple plugin for EDMC to count BGS work

# Installation
Download the [latest release](https://github.com/tezw21/BGS-Tally/releases/tag/V1.1) of BGS Tally
 - In EDMC, on the Plugins settings tab press the “Open” button. This reveals the plugins folder where this app looks for plugins.
 - Open the .zip archive that you downloaded and move the folder contained inside into the plugins folder.

You will need to re-start EDMC for it to notice the new plugin.

# Usage
Enter the Faction and system name that you want to monitor in the *BGS Tally* tab in *Settings*. The names are not case sensitive. Once set the Faction and System is persistent until changed by the user. It is up to the user to ensure that the Faction is present in the selected System and spelling is correct. Ctrl-v can be used to paste a name cut from 3rd party tools. 
Once the Faction and System has been set the user needs to dock or launch and redock in the System to initalise the mission counter system. This only needs to be done once after they have been changed

Only four positive actions are counted at the moment. Mission inf + , Total trade profit sold to Faction controlled station, Cartographic data sold to Faction controlled station, Bounties issued by named Faction. These total during the session and reset on restart of EDMC

The data is now saved locally. The counters can be reset by using the Counter Reset button. This could be used at each tick.
