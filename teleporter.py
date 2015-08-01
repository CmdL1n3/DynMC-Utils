from helpers import *
from basecommands import simplecommand


prefix = "&a-=[&cteleporter&a]=-&e"


"""   Command handling:    """

#set teleporter locations
def set_pos(self, sender, type):
	if args[1] == "pos":
	  loc = sender.getLocation()
	  if args[2] in ["co1"]:
			self.pos1 = Coords(loc)
			msg(sender, "%s position 2 set!" % prefix)
	  elif args[2] in ["co2"]:
			self.pos2 = Coords(loc)
			msg(sender, "%s position 2 set!" % prefix)
		
@hook.event("player.PlayerMoveEvent", "high")
def onMove(event):
	if player.getLocation() == self.pos1:
		player.teleport(self.pos2)
		
		
		
		
		
		
		
"""  Command setup   """

@simplecommand("teleporter",
        aliases = ["tpr"], 
        usage = "pos <co1|co2>", 
        description = "Creates teleporters",
        senderLimit = 0,
        helpNoargs = True,
        helpSubcmd = True,
        amax = 2)
def on_teleporter_command(sender, command, label, args):
	if args < 1:
		msg(sender, "%s Info:" % prefix)
		msg(sender, "&e /teleporter pos <co1|co2>")
		msg(sender, "&e Sets the positions for a teleporter")
		msg(sender, "&e")
		msg(sender, "&e more to come")
	
	return set_pos(self, sender, type)