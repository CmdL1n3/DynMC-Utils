from helpers import *
import org.bukkit.potion.PotionEffect as PotionEffect
import org.bukkit.potion.PotionEffectType as PotionEffectType
import org.bukkit.event.player.PlayerJoinEvent as PlayerJoinEvent

jump_perm = "utils.jump"
speed_perm = "utils.speed"

#Jump boost
@hook.event("player.PlayerJoinEvent", "high")
def on_join(event):
    if event.getPlayer().hasPermission(jump_perm):
      player = event.getPlayer()		  
      player.addPotionEffect(PotionEffect(PotionEffectType.JUMP, 60000, 0))
	  
#Speed	  
@hook.event("player.PlayerJoinEvent", "high")
def on_join(event):
    if event.getPlayer().hasPermission(speed_perm):
      player = event.getPlayer()	  
      player.addPotionEffect(PotionEffect(PotionEffectType.SPEED, 60000, 0))