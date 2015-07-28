#pylint: disable = F0401
from helpers import *
from time import time as now
from time import sleep
from sys import exc_info
import thread
import org.bukkit.inventory.ItemStack as ItemStack
import org.bukkit.Bukkit as Bukkit
from basecommands import simplecommand



@hook.event("player.PlayerJoinEvent", "monitor")
def on_join(event):
    """
    Welcome new players
    """
    player = event.getPlayer()

    # send welcome broadcast
    if not player.hasPlayedBefore():
        broadcast("utils.greet_new", "\n&a&lPlease welcome &f" + player.getDisplayName() + " &a&lto DynaMC!\n")

        # clear out some eventual crap before
        msg(player, " \n \n \n \n \n \n \n \n \n \n \n \n ")
        msg(player, "  &4Welcome to the DynaMC Server!")
        msg(player, "  \n&6happy playing ;)")
        msg(player, " \n \n")

@simplecommand("sudo",
        usage        = "<player> [cmd..]",
        description  = "Makes <player> write [cmd..] in chat",
        amin         = 2,
        helpNoargs   = True)
def on_sudo_command(sender, command, label, args):
    target = args[0]
    cmd    =  " ".join(args[1:])
    msg(sender, "&2[SUDO] &rRunning '&e%s&r' as &3%s" % (cmd, target))
    is_cmd     = cmd[0] == "/"
    is_console = target.lower() in ["server", "console"]
    if is_console:
        server.dispatchCommand(server.getConsoleSender(), cmd[1:] if is_cmd else cmd)
        return None
    target_player = server.getPlayer(target)
    if target_player:
        target_player.chat(cmd)
        return None
    return "&cPlayer %s not found!" % target



@simplecommand("me", 
        usage        = "[message..]",
        description  = "Sends a message in third person",
        helpNoargs   = True)
def on_me_command(sender, command, label, args):
    text = colorify("&7- %s &7%s " % (sender.getDisplayName() if isinstance(sender, Player) else "&9CONSOLE", u"\u21E6"))
    broadcast("utils.me", text + " ".join(args), usecolor = sender.hasPermission("essentials.chat.color"))
    return None


@hook.command("echo")
def on_echo_command(sender, command, label, args):
    """
    /echo
    essentials echo sucks and prints mail alerts sometimes
    """
    msg(sender, " ".join(args).replace("\\n", "\n"))



def eval_thread(sender, code):
    """
    /pyeval
    run python ingame
    """
    try:
        result = eval(code)
        msg(sender, ">>> %s: %s" % (colorify("&3") + type(result).__name__, colorify("&a") + unicode(result) + "\n "), usecolor = False)
    except:
        e = exc_info()[1]
        try:
            eclass = e.__class__
        except AttributeError:
            eclass = type(e)
        msg(sender, ">>> %s: %s" % (eclass.__name__, e) + "\n ", False, "c")
    thread.exit()

@simplecommand("pyeval",
        usage       = "[code..]",
        description = "Runs python [code..] and returns the result",
        helpNoargs  = True)
def on_pyeval_command(sender, command, label, args):
    msg(sender, " ".join(args), False, "e")
    thread.start_new_thread(eval_thread, (sender, " ".join(args)))
    return None



@simplecommand("tempadd",
        usage       = "<user> <group> [duration]",
        description = "Temporarily adds <user> to <group> for \n[duration] minutes. Defaults to 1 week.",
        helpNoargs  = True,
        helpSubcmd  = True,
        amin        = 2,
        amax        = 3)
def tempadd_command(sender, command, label, args):
    if not sender.hasPermission("permissions.manage.membership." + args[1]):
        return "&cYou do not have permission to manage that group!"
    if len(args) == 3:
        if not args[2].isdigit():
            return "&cThats not a number!"
        duration = int(args[2]) * 60
    else:
        duration = 604800
    if duration <= 0:
        return "&cThats too short!"
    cmd = "pex user %s group add %s * %s" % (args[0], args[1], duration)
    runas(sender, cmd)

    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return "&aAdded to group for %dd%dh%dm" % (d, h, m)



@hook.command("modules")
def on_modules_command(sender, command, label, args):
    """
    /modules
    list all modules, unloaded modules in red
    """
    plugin_header(sender, "Modules")
    msg(sender, ", ".join([(("&a" if mod in shared["modules"] else "&c") + mod) for mod in shared["load_modules"]]))