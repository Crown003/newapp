from kivymd.uix.list import OneLineAvatarIconListItem
from kivy.properties import (
StringProperty,
)
class ListItemWithIcon(OneLineAvatarIconListItem):
    icon = StringProperty()
    main_color = StringProperty()