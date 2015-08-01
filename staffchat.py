#pylint: disable = F0401
from helpers import *
from basecommands import simplecommand

sc_permission  = "dynmc.sc"

sc_defaultkey  = "<"
sc_keys        = open_json_file("staffchat_keys", {})

sc_toggle_list = []
sc_prefix      = "&8[&5SC&8]"

def staffchat(sender, msg):
    name = "&7{unknown}"
    try:
        name = sender.getDisplayName()
    except AttributeError:
        name = sender.getName()
    broadcast(sc_permission, "%s &9%s&8: &3%s" % (sc_prefix, name, msg))
    # Needs something here like fine(message) to show up in the logs when you use ackey, but fine doesnt work for some reason. It did on the server with /pyeval (not show up on console, but show up in logs nevertheless)


# ac toggle
@hook.command("sct")
def on_sct_command(sender, args):
    if sender.hasPermission(sc_permission):
        p = sender.getName()
        if p in sc_toggle_list:
            sc_toggle_list.remove(p)
            msg(sender, "%s &asC toggle: off" % sc_prefix)
        else:
            sc_toggle_list.append(p)
            msg(sender, "%s &asC toggle: on" % sc_prefix)
    else:
        noperm(sender)
    return True


@hook.command("sc")
def on_sc_command(sender, args):
    if sender.hasPermission(sc_permission):
        if not checkargs(sender, args, 1, -1):
            return True
        staffchat(sender, " ".join(args))
    else:
        noperm(sender)
    return True

def get_key(uuid):
    key = sc_keys.get(uuid)
    return key if key != None else sc_defaultkey

@simplecommand("staffchatkey", 
        aliases = ["sckey"], 
        senderLimit = 0, 
        helpNoargs = True, 
        helpSubcmd = True, 
        description = "Sets a key character for staffchat", 
        usage = "<key>")
def staffchatkey_command(sender, command, label, args):
    key = " ".join(args)
    uuid = uid(sender)
    if key.lower() == "default" or key == sc_defaultkey:
        del sc_keys[uuid]
        save_keys()
        return "&aYour staffchat key was set to the default character: '&c%s&a'" % sc_defaultkey
    sc_keys[uid(sender)] = key
    save_keys()
    return "&aYour staffchat key was set to: '&c%s&a'" % key

def save_keys():
    save_json_file("staffchat_keys", sc_keys)


@hook.event("player.AsyncPlayerChatEvent", "low")
def on_chat(event):
    sender = event.getPlayer()
    msg = event.getMessage()
    if sender.hasPermission(sc_permission) and not event.isCancelled():
        key = get_key(uid(sender))
        if sender.getName() in sc_toggle_list:
            staffchat(sender, msg)
            event.setCancelled(True)
        if msg[:len(key)] == key:
            staffchat(sender, msg[len(key):])
            event.setCancelled(True)
