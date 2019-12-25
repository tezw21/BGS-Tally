import Tkinter as tk
import myNotebook as nb
import sys
import ttk
from config import config
from theme import theme

this = sys.modules[__name__]	# For holding module globals
this.FactionName =""
this.MissionPoints =0
this.TradeProfit =0
this.BountiesCollected =0
this.CartDataSold=0


def plugin_prefs(parent, cmdr, is_beta):
   """
   Return a TK Frame for adding to the EDMC settings dialog.
   """
  
   frame = nb.Frame(parent)
   nb.Label(frame, text="Faction name to monitor").grid(column=0, sticky=tk.W)
   factionname = nb.Entry(frame, textvariable =this.FactionName ,width=40).grid(column=0, sticky=tk.W)
   
   return frame


def prefs_changed(cmdr, is_beta):
   """
   Save settings.
   """
   config.set('XFactionName', this.FactionName.get())	# Store new value in config
   this.factionlabel2["text"] = this.FactionName.get()
   this.MissionPoints =0
   this.TradeProfit =0
   this.BountiesCollected =0
   this.CartDataSold=0
   this.missioninf2["text"] = this.MissionPoints
   this.tradeprofit2["text"] = this.TradeProfit
   this.bountiescollected2["text"] = this.BountiesCollected
   this.cartdata2["text"] = this.CartDataSold
  
   
def plugin_start(plugin_dir):
   """
   Load this plugin into EDMC
   """
   this.FactionName = tk.StringVar(value =config.get("XFactionName")) #load faction name
   this.StationFaction = tk.StringVar(value =config.get("XStataionFaction")) #load faction name
      
   return "BGS Tally"


def plugin_stop():
    """
    EDMC is closing
    """
    print "Farewell cruel world!"

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
    missioninf = tk.Label(this.frame, text="Mission Points:")
    missioninf.grid(row=2, column=0, sticky=tk.W)
    this.missioninf2 = tk.Label(this.frame, text =this.MissionPoints)
    this.missioninf2.grid(row=2, column=1,sticky=tk.W)
    tradeprofit = tk.Label(this.frame, text="Trade Profit:")
    tradeprofit.grid(row=3, column=0, sticky=tk.W)
    this.tradeprofit2 = tk.Label(this.frame, text =this.TradeProfit)
    this.tradeprofit2.grid(row=3, column=1, sticky=tk.W)
    bountiescollected = tk.Label(this.frame, text="Bounties Collected:")
    bountiescollected.grid(row=4, column=0, sticky=tk.W)
    this.bountiescollected2 = tk.Label(this.frame, text =this.BountiesCollected)
    this.bountiescollected2.grid(row=4,column=1, sticky=tk.W)
    cartdata = tk.Label(this.frame, text="Cartographic Data:")
    cartdata.grid(row=5, column=0, sticky=tk.W)
    this.cartdata2 =tk.Label(this.frame, text =this.CartDataSold)
    this.cartdata2.grid(row=5, column=1, sticky=tk.W)
   
            
    return this.frame

def journal_entry(cmdr, is_beta, system, station, entry, state):
   if entry['event'] == 'Docked':   # set station name
      sf = entry['StationFaction']
      config.set('XStationFaction', sf)	# Store new value in config
      this.StationFaction = sf['Name']
         
   if entry['event'] =='MissionCompleted': # get mission influence value
      fe = entry['FactionEffects']
      for i in fe:
         fe3 = i['Faction']
         fe4 = i['Influence']
         for x in fe4:
            fe5 = x['Influence']
            inf = len(x['Influence'])
            if fe3.lower() == this.FactionName.get().lower():
               this.MissionPoints +=inf
               this.missioninf2["text"] = this.MissionPoints
               
   if entry['event'] =='SellExplorationData' or entry['event'] == "MultiSellExplorationData": # get carto data value
      print (entry)
      if this.StationFaction.lower() == this.FactionName.get().lower():
         this.CartDataSold += entry['TotalEarnings']
         this.cartdata2["text"] = format(this.CartDataSold ,',d')

   if entry['event'] =='RedeemVoucher' and entry['Type'] == 'bounty': # bounties collected
      for z in entry['Factions']:
         if z['Faction'].lower() == this.FactionName.get().lower():
            this.BountiesCollected += z['Amount']


      this.bountiescollected2['text'] = format(this.BountiesCollected ,',d')

      

   if entry['event'] == 'MarketSell': # Trade Profit
      if this.StationFaction.lower() == this.FactionName.get().lower():
         cost = entry['Count'] * entry['AvgPricePaid']
         profit = entry['TotalSale'] - cost
         this.TradeProfit += profit
         this.tradeprofit2['text'] = format(this.TradeProfit, ',d')
         
         
         

         
      
               
            
            
                   

