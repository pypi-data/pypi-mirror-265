from amethyst.amethyst import BaseWidget, Client, Plugin, WidgetPlugin
from amethyst.widget.command import CommandWidget, command
from amethyst.widget.event import Event, EventWidget, event
from amethyst.widget.event.library import *  # noqa: F403
from amethyst.widget.menu import ContextMenuWidget, context_menu
from amethyst.widget.schedule import ScheduleWidget, schedule

__version__ = "2.0.0"
__author__ = "NimajnebEC <nimajnebec@users.noreply.github.com>"

__all__ = (
    "CommandWidget",
    "EventWidget",
    "ContextMenuWidget",
    "ScheduleWidget",
    "WidgetPlugin",
    "BaseWidget",
    "command",
    "Client",
    "Plugin",
    "Event",
    "event",
    "schedule",
    "context_menu",
)
