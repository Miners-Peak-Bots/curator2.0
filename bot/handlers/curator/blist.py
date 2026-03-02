"""
$blist / $blist20 - View blacklisted words/phrases
Only works in DM (private chat) for security
"""
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ParseMode
from django.conf import settings
from django.core.cache import cache
from blacklist.models import Blacklist

CMD_PREFIX = settings.BOT_COMMAND_PREFIX


def blist(client, msg):
    """List all permanent blacklisted words (DM only)"""
    if msg.from_user.id not in settings.BOT_MASTER:
        return False
    
    blacklist = cache.get('blacklist', [])
    
    if not blacklist:
        # Try loading from DB if cache is empty
        blacklist = list(Blacklist.objects.filter(is_temp=False))
    
    if not blacklist:
        msg.reply_text("Blacklist is empty.", parse_mode=ParseMode.HTML)
        return True
    
    # Format the list
    lines = [f"<b>Blacklist ({len(blacklist)} entries):</b>\n"]
    
    for i, item in enumerate(blacklist, 1):
        # Clean up the regex pattern for display
        pattern = str(item.regex.pattern)
        # Remove the \s+ wrappers for readability
        display = pattern.replace(r'\s+', '').replace('\\', '')
        lines.append(f"{i}. <code>{display}</code>")
        
        # Send in chunks to avoid message too long
        if i % 50 == 0:
            msg.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)
            lines = []
    
    if lines:
        msg.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)
    
    return True


def blist20(client, msg):
    """List all temp blacklisted words (first 20 msgs) - DM only"""
    if msg.from_user.id not in settings.BOT_MASTER:
        return False
    
    blacklist = cache.get('blacklist20', [])
    
    if not blacklist:
        # Try loading from DB if cache is empty
        blacklist = list(Blacklist.objects.filter(is_temp=True))
    
    if not blacklist:
        msg.reply_text("Temp blacklist (20-msg) is empty.", parse_mode=ParseMode.HTML)
        return True
    
    # Format the list
    lines = [f"<b>Temp Blacklist - 20 msg ({len(blacklist)} entries):</b>\n"]
    
    for i, item in enumerate(blacklist, 1):
        pattern = str(item.regex.pattern)
        display = pattern.replace(r'\s+', '').replace('\\', '')
        lines.append(f"{i}. <code>{display}</code>")
        
        if i % 50 == 0:
            msg.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)
            lines = []
    
    if lines:
        msg.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)
    
    return True


def reloadcache(client, msg):
    """Force reload blacklist from DB into cache"""
    if msg.from_user.id not in settings.BOT_MASTER:
        return False
    
    # Reload permanent blacklist
    blacklist = list(Blacklist.objects.filter(is_temp=False))
    cache.set('blacklist', blacklist)
    
    # Reload temp blacklist
    blacklist20 = list(Blacklist.objects.filter(is_temp=True))
    cache.set('blacklist20', blacklist20)
    
    msg.reply_text(
        f"✅ Cache reloaded:\n"
        f"• Permanent blacklist: {len(blacklist)} entries\n"
        f"• Temp blacklist (20-msg): {len(blacklist20)} entries",
        parse_mode=ParseMode.HTML
    )
    return True


__HANDLERS__ = [
    # Only in private/DM - not groups
    MessageHandler(blist, filters.command('blist', prefixes=CMD_PREFIX) & filters.private),
    MessageHandler(blist20, filters.command('blist20', prefixes=CMD_PREFIX) & filters.private),
    MessageHandler(reloadcache, filters.command(['reloadcache', 'reloadbl'], prefixes=CMD_PREFIX) & filters.private),
]


__HELP__ADMIN__ = (
    '$blist: View all blacklisted words/phrases (DM only)\n'
    '$blist20: View temp blacklist for new users (DM only)\n'
    '$reloadcache: Force reload blacklist from database\n'
)
