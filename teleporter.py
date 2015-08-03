from helpers import *

pos1 = None
pos2 = None

def help(sender):
	msg(sender," \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n")
	msg(sender,"&a \n \n \n \n-=[&6Teleporter&a]=- \n \n \n \n \n")
	msg(sender,"&6/teleporter pos <pos1|pos2>")
	msg(sender,"&6Sets points for a teleporter.")
	
	
def noArgs(sender):
	msg(sender," \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n")
	msg(sender,"&cLooks like you supplied no args!")
	msg(sender,"&cIf you need help, use /teleporter help!")
	msg(sender," \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n")	

@simplecommand("teleporter",
	usage       = "<pos> <pos1|pos2>",
	description = "creates teleporters",
	senderLimit = 0,
	helpNoargs  = False)
def onTeleporterCommand(sender, command):
	if args[0] == "pos":
		if args[1] == "pos1":
			pos1 = sender.getLocation()
			msg(sender,"&6Position 1 saved!")		
		elif args[1] == "pos2":
			pos2 = sender.getLocation()
			msg(sender,"&6Position 2 saved!")
		else:
			noArgs()
	elif args[0] == "help":
		help()	
	else:
		noArgs()
		
		
@hook.command("tpr")
def onTeleporterCommand(sender, command):
	return onTeleporterCommand(sender, command)
	
@hook.event("player.PlayerMoveEvent", "high")
def onMove(event):
	loc1 = player.getLocation()
	if not int(pos1.x) == int(loc1x) and int(pos1.y) == int(loc1.y) and int(pos1.z) == int(loc1.z) and pos1.world.getName() == loc1.world.getName():
		return
	else:	
		safetp(sender, pos2.getWorld(), pos2.x, pos2.y, pos2.z)