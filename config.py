from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from check_internet_widget import check_connectivity

mod = "mod4"
terminal = guess_terminal()

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show run"), desc="rofi"),
    # language
    Key([mod], "F1", lazy.spawn("setxkbmap us"), desc="Change to US layout"),
    Key([mod], "F2", lazy.spawn("setxkbmap ro std"), desc="Change to RO-STD layout"),
]

groups = [
    Group("1", label="1dev", spawn=["code"]),
    Group("2", label="2edit", spawn=["alacritty"]),
    Group("3", label="3www", spawn=["firefox"]),
    Group("4", label="4sys", spawn=["alacritty", "-e", "ranger"]),
    Group("5", label="5docs", ),
    Group("6", label="6media", spawn=["chromium youtube.com"] ),
    Group("7", label="7misc", ),
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

layouts = [
    layout.Columns(
        border_focus="#ADD8E6",
        border_normal="#1e1e2e",
        border_width=2,
        margin = 4,
        name="",
    ),
]

widget_defaults = dict(
    font="NotoNerdFont Bold", 
    fontsize=14,
    padding=2,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(fmt="Running: {}"),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    nae_transform=lambda name: name.upper(),
                ),
                widget.Systray(),
                widget.Clipboard(fmt="Clipped {} "),
                widget.GenPollText(fmt="📡 status: {} ", func=check_connectivity, update_interval=10),
                widget.OpenWeather(location='Bucharest', format='{main_temp} °{units_temperature} ~ {main_feels_like}°{units_temperature}, {weather_details}, {pressure}hPa, {wind_speed}km/h, {humidity}%H, {sunrise}|{sunset}', fmt='🏙️ {}'),
                widget.DF(
                    visible_on_warn=False,
                    fmt="💾 {} ",
                    format="{uf}{m}|{r:.1f}{m}|{r:.0f}%",
                    partition="/",
                ),
                widget.Memory(fmt = '🐏 {}', measure_mem='G', format='{MemUsed:.0f}{mm}|{MemTotal:.0f}{mm}'),
                widget.CPU(fmt = '🧠 {}', format = '{freq_current}GHz|{load_percent}%', width = 120),
                # widget.ThermalSensor(fmt="🔥 {}", tag_sensor="Package id 0"),
                widget.Volume(fmt="📢 {}"),
                widget.Clock(format="%Y.%m.%d %a %I:%M", fmt="⏳️ {} "),
                widget.KeyboardLayout(fmt="👅 {} ", configured_keyboards=["us", "ro"]),
            ],
            24,
            background='#1e1e2e'
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
        border_focus="#ADD8E6",
        border_normal="#1e1e2e",
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

wmname = "LG3D"
