"""Different modes of the bblame application"""
# Normal/standard view
MODE_NORMAL = 'normal'
# Visual select mode for selecting lines of the blame file
MODE_VISUAL = 'visual'
# Viewing a show not a blame
MODE_SHOW = 'show'
# Viewing a help message
MODE_HELP = 'help'

# Useful lists of modes
ALL_MODES = [MODE_NORMAL, MODE_VISUAL, MODE_SHOW, MODE_HELP]
ALL_MODES_BUT_HELP = [MODE_NORMAL, MODE_VISUAL, MODE_SHOW]
NORMAL_AND_VISUAL = [MODE_NORMAL, MODE_VISUAL]
