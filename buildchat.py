#pylint: disable = F0401
from helpers import *
from basecommands import simplecommand

bc_permission  = "dynmc.bc"

bc_defaultkey  = ";"
bc_keys        = open_json_file("buildchat_keys", {})

bc_toggle_list = []
bc_prefix      = "&8[&bBC&8]"

def buildchat(sender, msg):
    name = "&7{unknown}"
    try:
        name = sender.getDisplayName()
    except AttributeError:
        name = sender.getName()
    broadcast(bc_permission, "%s &9%s&8: &a%s" % (bc_prefix, name, msg))
    # Needs something here like fine(message) to show up in the logs when you use ackey, but fine doesnt work for some reason. It did on the server with /pyeval (not show up on console, but show up in logs nevertheless)


# ac toggle
@hook.command("bct")
def on_bct_command(sender, args):
    if sender.hasPermission(bc_permission):
        p = sender.getName()
        if p in bc_toggle_list:
            bc_toggle_list.remove(p)
            msg(sender, "%s &aBC toggle: off" % bc_prefix)
        else:
            bc_toggle_list.append(p)
            msg(sender, "%s &aBC toggle: on" % bc_prefix)
    else:
        noperm(sender)
    return True


@hook.command("bc")
def on_bc_command(sender, args):
    if sender.hasPermission(bc_permission):
        if not checkargs(sender, args, 1, -1):
            return True
        buildchat(sender, " ".join(args))
    else:
        noperm(sender)
    return True

def get_key(uuid):
    key = bc_keys.get(uuid)
    return key if key != None else bc_defaultkey

@hook.command("bckey")
def bckey_command(sender, command, label, args):
    key = " ".join(args)
    uuid = uid(sender)
    if key.lower() == "default" or key == bc_defaultkey:
        del bc_keys[uuid]
        save_keys()
        return "&aYour buildchat key was set to the default character: '&c%s&a'" % bc_defaultkey
    bc_keys[uid(sender)] = key
    save_keys()
    return "&aYour buildchat key was set to: '&c%s&a'" % key

def save_keys():
    save_json_file("buildchat_keys", bc_keys)


@hook.event("player.AsyncPlayerChatEvent", "low")
def on_chat(event):
    sender = event.getPlayer()
    msg = event.getMessage()
    if sender.hasPermission(bc_permission) and not event.isCancelled():
        key = get_key(uid(sender))
        if sender.getName() in bc_toggle_list:
            buildchat(sender, msg)
            event.setCancelled(True)
        if msg[:len(key)] == key:
            buildchat(sender, msg[len(key):])
            event.setCancelled(True)
