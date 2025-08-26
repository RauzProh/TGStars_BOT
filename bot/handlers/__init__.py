from .user.commands import router as commands
from .chat.chat import router_chat
from .channel.channel import router_channel
from .admin.commands import router as admin_commands


routers = [
    commands,
    admin_commands,
    router_chat,
    router_channel
]
