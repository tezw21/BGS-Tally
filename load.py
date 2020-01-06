import Tkinter as tk
import myNotebook as nb
import sys
import ttk
import json
import requests
from config import config
from theme import theme

this = sys.modules[__name__]	# For holding module globals

this.MissionPoints =0
this.TradeProfit =0
this.BountiesCollected =0
this.CartDataSold=0


def plugin_prefs(parent, cmdr, is_beta):
   """
   Return a TK Frame for adding to the EDMC settings dialog.
   """
   
   frame = nb.Frame(parent)
   nb.Label(frame, text="Faction to monitor").grid(column=0, sticky=tk.W)
   factionname = nb.Entry(frame, textvariable = this.FactionName ,width=40).grid(column=0, sticky=tk.W)
   systemlabel = nb.Label(frame, text="System to monitor").grid(column=0, sticky=tk.W)
   systemname = nb.Entry(frame, textvariable =this.SystemName, width=40).grid(column=0, sticky=tk.W)
   Reset = nb.Button(frame, text="Reset Counter").place(x=0 , y=290)
   return frame


def prefs_changed(cmdr, is_beta):
   """
   Save settings.
   """
   this.factionlabel2["text"] = this.FactionName.get()
   this.systemlabel2["text"] = this.SystemName.get()
   this.MissionPoints.set(0)
   this.TradeProfit.set(0)
   this.BountiesCollected.set(0)
   this.CartDataSold.set(0)
   this.missioninf2["text"] = this.MissionPoints.get()
   this.tradeprofit2["text"] = this.TradeProfit.get()
   this.bountiescollected2["text"] = this.BountiesCollected.get()
   this.cartdata2["text"] = this.CartDataSold.get()
   
     
   
def plugin_start(plugin_dir):
   """
   Load this plugin into EDMC
   """
   this.FactionName = tk.StringVar(value =config.get("XFactionName")) #load monitored faction name
   this.StationFaction = tk.StringVar(value =config.get("XStataionFaction")) #load station controlling faction name
   this.SystemName = tk.StringVar(value =config.get("XSystemName")) # load monitored system name
   this.SystemAddress = tk.StringVar(value =config.get("XSystemAddress")) # load system address
   this.MissionPoints = tk.IntVar(value=config.getint("XMissionPoints"))
   this.TradeProfit = tk.IntVar(value=config.getint("XTradeProfit"))
   this.BountiesCollected = tk.IntVar(value = config.getint("XBountiesCollected"))
   this.CartDataSold = tk.IntVar(value = config.getint("XCartDataSold"))
   

   return "BGS Tally"


def plugin_stop():
    """
    EDMC is closing
    """
    
    config.set('XFactionName', this.FactionName.get())
    config.set('XStataionFaction', this.StationFaction.get())
    config.set('XSystemName', this.SystemName.get())
    config.set('XSystemAddress', this.SystemAddress.get())
    config.set('XMissionPoints', this.MissionPoints.get())
    config.set('XTradeProfit', this.TradeProfit.get())
    config.set('XBountiesCollected', this.BountiesCollected.get())
    config.set('XCartDataSold', this.CartDataSold.get())
    print ("Farewell cruel world!")

def plugin_app(parent):
    """
    Create a frame for the EDMC main window
    """
    this.frame = tk.Frame(parent)
    
    Title = tk.Label(this.frame, text="BGS Tally")
    Title.grid(row=0, column=0, sticky=tk.W)
    factionlabel = tk.Label(this.frame, text="Faction:")
    factionlabel.grid(row=1, column=0, sticky=tk.W)
    this.factionlabel2 = tk.Label(this.frame, text = this.FactionName.get())
    this.factionlabel2.grid(row=1, column=1, sticky=tk.W)
    systemlabel = tk.Label(this.frame, text="System:")
    systemlabel.grid(row=2, column=0, sticky=tk.W)
    this.systemlabel2 = tk.Label(this.frame, text = this.SystemName.get())
    this.systemlabel2.grid(row=2, column=1, sticky=tk.W)
    missioninf = tk.Label(this.frame, text="Mission Points:")
    missioninf.grid(row=3, column=0, sticky=tk.W)
    this.missioninf2 = tk.Label(this.frame, text =this.MissionPoints.get())
    this.missioninf2.grid(row=3, column=1,sticky=tk.W)
    tradeprofit = tk.Label(this.frame, text="Trade Profit:")
    tradeprofit.grid(row=4, column=0, sticky=tk.W)
    this.tradeprofit2 = tk.Label(this.frame, text =format(this.TradeProfit.get(), ',d'))
    this.tradeprofit2.grid(row=4, column=1, sticky=tk.W)
    bountiescollected = tk.Label(this.frame, text="Bounties Collected:")
    bountiescollected.grid(row=5, column=0, sticky=tk.W)
    this.bountiescollected2 = tk.Label(this.frame, text =format(this.BountiesCollected.get(), ',d'))
    this.bountiescollected2.grid(row=5,column=1, sticky=tk.W)
    cartdata = tk.Label(this.frame, text="Cartographic Data:")
    cartdata.grid(row=6, column=0, sticky=tk.W)
    this.cartdata2 =tk.Label(this.frame, text =format(this.CartDataSold.get(), ',d'))
    this.cartdata2.grid(row=6, column=1, sticky=tk.W)
   
            
    return this.frame

def journal_entry(cmdr, is_beta, system, station, entry, state):
  
   if entry['event'] == 'Docked':   # set controlling faction name
      sf = entry['StationFaction']
      sa = entry['SystemAddress']
      if system.lower() == this.SystemName.get().lower(): #set system address if system monitored
         this.SystemAddress.set(sa)
         
      this.StationFaction.set(sf['Name']) #set controlling faction name
      
      
   if entry['event'] =='MissionCompleted': # get mission influence value
      fe = entry['FactionEffects']
      
      for i in fe:
         fe3 = i['Faction']
         fe4 = i['Influence']
         print (fe3)
         for x in fe4:
            fe5 = x['Influence']
            fe6 = str(x['SystemAddress'])

            inf = len(x['Influence'])
            if fe3.lower() == this.FactionName.get().lower()and fe6 == this.SystemAddress.get():
               this.MissionPoints.set(this.MissionPoints.get() + inf)
               this.missioninf2["text"] = this.MissionPoints.get()
               
   if entry['event'] =='SellExplorationData' or entry['event'] == "MultiSellExplorationData": # get carto data value
      if this.StationFaction.get().lower() == this.FactionName.get().lower() and this.SystemName.get().lower() == system.lower():
         this.CartDataSold.set(this.CartDataSold.get() + entry['TotalEarnings'])
         this.cartdata2["text"] = format(this.CartDataSold.get() ,',d')

   if entry['event'] =='RedeemVoucher' and entry['Type'] == 'bounty': # bounties collected
      for z in entry['Factions']:
         if z['Faction'].lower() == this.FactionName.get().lower() and this.SystemName.get().lower() == system.lower():
            this.BountiesCollected.set(this.BountiesCollected.get + z['Amount'])
            this.bountiescollected2['text'] = format(this.BountiesCollected.get() ,',d')

      

   if entry['event'] == 'MarketSell': # Trade Profit
      if this.StationFaction.get().lower() == this.FactionName.get().lower() and this.SystemName.get().lower() == system.lower():
         cost = entry['Count'] * entry['AvgPricePaid']
         profit = entry['TotalSale'] - cost
         this.TradeProfit.set(this.TradeProfit.get() + profit)
         this.tradeprofit2['text'] = format(this.TradeProfit.get(), ',d')
         
         
         

         
      
               
            
            
                   

