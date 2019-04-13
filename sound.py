from pygame import mixer


sounds_root = "assets/sounds/"


def load_sound(name):
    if not mixer.get_init():
        # mixer.pre_init(44100, 16, 2, 4096)
        mixer.init(44100)
    return mixer.Sound(sounds_root + name + ".ogg")


sounds = {
    "ding": load_sound("ding"),
    "flip1": load_sound("flip1"),
    "flip2": load_sound("flip2"),
    "roll": load_sound("roll"),
    "win": load_sound("win")
}


def sound(name):
    sounds[name].play()
