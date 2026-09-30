"""
Faisal Pranks - Prank email sender powered by Resend
Every message ends with a clear "prank by Faisal Pranks" note.
Secret code in the To field opens the hidden Main Control panel.
"""
import json
import threading
import datetime
from urllib import request as urlrequest, error as urlerror

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivy.metrics import dp

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SECRET_CODE = "fainet.org-1290"          # type this in "To" to open Main Control
RESEND_URL = "https://api.resend.com/emails"
STORE = JsonStore("faisal_pranks.json")

# The prank note that is ALWAYS added at the bottom (smallest font)
PRANK_NOTE = (
    '<p style="font-size:10px; color:#9ca3af; margin-top:24px;">'
    'This was a prank by Faisal Pranks 😄</p>'
)

BLUE = (0.11, 0.31, 0.85, 1)
DARK = (0.06, 0.09, 0.16, 1)
Window.clearcolor = (0.96, 0.97, 1, 1)


# ---------------------------------------------------------------------------
# Storage helpers
# ---------------------------------------------------------------------------
def get_setting(key, default=""):
    if STORE.exists("settings"):
        return STORE.get("settings").get(key, default)
    return default


def set_settings(api_key, from_email):
    STORE.put("settings", api_key=api_key, from_email=from_email)


def get_log():
    if STORE.exists("log"):
        return STORE.get("log").get("items", [])
    return []


def add_log(entry):
    items = get_log()
    items.insert(0, entry)          # newest first
    STORE.put("log", items=items[:200])


# ---------------------------------------------------------------------------
# Networking (runs in a background thread)
# ---------------------------------------------------------------------------
def resend_send(api_key, from_field, to, subject, html, reply_to=None, scheduled_at=None):
    payload = {
        "from": from_field,
        "to": [to],
        "subject": subject,
        "html": html,
    }
    if reply_to:
        payload["reply_to"] = reply_to
    if scheduled_at:
        payload["scheduled_at"] = scheduled_at

    data = json.dumps(payload).encode("utf-8")
    req = urlrequest.Request(RESEND_URL, data=data, method="POST")
    req.add_header("Authorization", "Bearer " + api_key)
    req.add_header("Content-Type", "application/json")
    try:
        with urlrequest.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return True, body
    except urlerror.HTTPError as e:
        try:
            return False, e.read().decode("utf-8")
        except Exception:
            return False, "HTTP error %s" % e.code
    except Exception as e:
        return False, str(e)


# ---------------------------------------------------------------------------
# KV layout
# ---------------------------------------------------------------------------
KV = r"""
#:import dp kivy.metrics.dp

<Field@TextInput>:
    size_hint_y: None
    height: dp(48)
    multiline: False
    padding: [dp(12), dp(12)]
    background_color: 1, 1, 1, 1
    foreground_color: 0.06, 0.09, 0.16, 1
    cursor_color: 0.11, 0.31, 0.85, 1
    font_size: dp(16)

<Btn@Button>:
    size_hint_y: None
    height: dp(50)
    background_normal: ""
    background_color: 0.11, 0.31, 0.85, 1
    color: 1, 1, 1, 1
    font_size: dp(17)
    bold: True

<Lbl@Label>:
    size_hint_y: None
    height: dp(24)
    color: 0.25, 0.3, 0.4, 1
    halign: "left"
    valign: "middle"
    font_size: dp(14)
    text_size: self.width, None

# ---------------- Compose screen ----------------
<ComposeScreen>:
    name: "compose"
    ScrollView:
        do_scroll_x: False
        BoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_height
            padding: dp(18)
            spacing: dp(10)

            BoxLayout:
                size_hint_y: None
                height: dp(90)
                Image:
                    source: "icon.png"
                    size_hint_x: None
                    width: dp(70)
                BoxLayout:
                    orientation: "vertical"
                    Label:
                        text: "Faisal Pranks"
                        color: 0.11, 0.31, 0.85, 1
                        font_size: dp(26)
                        bold: True
                        halign: "left"
                        text_size: self.width, None
                    Label:
                        text: "Send a prank email 😄"
                        color: 0.4, 0.45, 0.55, 1
                        font_size: dp(14)
                        halign: "left"
                        text_size: self.width, None

            Lbl:
                text: "Your Name  *required"
            Field:
                id: name
                hint_text: "e.g. Faisal"

            Lbl:
                text: "Your Gmail  (optional - for replies)"
            Field:
                id: gmail
                hint_text: "you@gmail.com"

            Lbl:
                text: "To  (recipient email)"
            Field:
                id: to
                hint_text: "friend@example.com"

            Lbl:
                text: "Subject  (optional)"
            Field:
                id: subject
                hint_text: "A little surprise..."

            Lbl:
                text: "Message"
            TextInput:
                id: body
                size_hint_y: None
                height: dp(140)
                multiline: True
                padding: [dp(12), dp(12)]
                hint_text: "Write your prank message here..."
                font_size: dp(16)

            BoxLayout:
                size_hint_y: None
                height: dp(48)
                spacing: dp(8)
                ToggleButton:
                    id: mode_now
                    text: "Send now"
                    group: "mode"
                    state: "down"
                    background_normal: ""
                    background_color: 0.11, 0.31, 0.85, 1
                    color: 1,1,1,1
                    bold: True
                ToggleButton:
                    id: mode_sched
                    text: "Schedule"
                    group: "mode"
                    background_normal: ""
                    background_color: 0.7, 0.75, 0.85, 1
                    color: 1,1,1,1
                    bold: True

            BoxLayout:
                id: time_row
                size_hint_y: None
                height: dp(48) if mode_sched.state == "down" else 0
                opacity: 1 if mode_sched.state == "down" else 0
                disabled: mode_sched.state != "down"
                spacing: dp(6)
                Field:
                    id: hh
                    hint_text: "HH"
                    text: "2"
                    input_filter: "int"
                Field:
                    id: mm
                    hint_text: "MM"
                    text: "30"
                    input_filter: "int"
                Spinner:
                    id: ampm
                    text: "PM"
                    values: ["AM", "PM"]
                    size_hint_y: None
                    height: dp(48)
                    background_normal: ""
                    background_color: 0.11, 0.31, 0.85, 1
                    color: 1,1,1,1

            Btn:
                text: "SEND PRANK"
                on_release: app.on_send()

            Label:
                id: status
                text: ""
                size_hint_y: None
                height: self.texture_size[1]
                color: 0.2, 0.5, 0.2, 1
                font_size: dp(14)
                halign: "center"
                text_size: self.width, None

            Label:
                text: "Every message ends with: This was a prank by Faisal Pranks"
                size_hint_y: None
                height: self.texture_size[1]
                color: 0.55, 0.6, 0.7, 1
                font_size: dp(12)
                halign: "center"
                text_size: self.width, None

# ---------------- Main Control screen ----------------
<ControlScreen>:
    name: "control"
    ScrollView:
        do_scroll_x: False
        BoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_height
            padding: dp(18)
            spacing: dp(10)

            Label:
                text: "Main Control"
                color: 0.11, 0.31, 0.85, 1
                font_size: dp(24)
                bold: True
                size_hint_y: None
                height: dp(40)
                halign: "left"
                text_size: self.width, None

            Lbl:
                text: "Resend API Key"
            Field:
                id: api_key
                hint_text: "re_xxxxxxxx"
                password: True

            Lbl:
                text: "From email  (your verified Resend sender)"
            Field:
                id: from_email
                hint_text: "prank@yourdomain.com"

            Btn:
                text: "SAVE SETTINGS"
                on_release: app.save_settings()

            Label:
                text: "Sent history"
                color: 0.11, 0.31, 0.85, 1
                font_size: dp(18)
                bold: True
                size_hint_y: None
                height: dp(34)
                halign: "left"
                text_size: self.width, None

            BoxLayout:
                id: history_box
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(6)

            Btn:
                text: "Clear history"
                background_color: 0.8, 0.3, 0.3, 1
                on_release: app.clear_history()

            Btn:
                text: "< Back"
                background_color: 0.4, 0.45, 0.55, 1
                on_release: app.go_compose()
"""


class ComposeScreen(Screen):
    pass


class ControlScreen(Screen):
    pass


class FaisalPranksApp(App):
    def build(self):
        self.title = "Faisal Pranks"
        Builder.load_string(KV)
        self.sm = ScreenManager()
        self.sm.add_widget(ComposeScreen())
        self.sm.add_widget(ControlScreen())
        return self.sm

    # ----- navigation -----
    def go_compose(self):
        self.sm.current = "compose"

    def open_control(self):
        c = self.sm.get_screen("control")
        c.ids.api_key.text = get_setting("api_key", "")
        c.ids.from_email.text = get_setting("from_email", "")
        self.refresh_history()
        self.sm.current = "control"

    # ----- settings -----
    def save_settings(self):
        c = self.sm.get_screen("control")
        set_settings(c.ids.api_key.text.strip(), c.ids.from_email.text.strip())
        self._toast(c, "Saved.")

    def clear_history(self):
        STORE.put("log", items=[])
        self.refresh_history()

    def refresh_history(self):
        from kivy.uix.label import Label
        c = self.sm.get_screen("control")
        box = c.ids.history_box
        box.clear_widgets()
        items = get_log()
        if not items:
            lbl = Label(text="No emails sent yet.", size_hint_y=None, height=dp(30),
                        color=(0.5, 0.55, 0.6, 1), halign="left")
            lbl.bind(width=lambda i, w: setattr(i, "text_size", (w, None)))
            box.add_widget(lbl)
            return
        for it in items:
            txt = "[%s] %s\nTo: %s  -  %s" % (
                it.get("status", "?"), it.get("subject", "(no subject)"),
                it.get("to", ""), it.get("time", ""))
            lbl = Label(text=txt, size_hint_y=None, markup=False,
                        color=(0.15, 0.2, 0.3, 1), halign="left", font_size=dp(13))
            lbl.bind(width=lambda i, w: setattr(i, "text_size", (w, None)))
            lbl.bind(texture_size=lambda i, ts: setattr(i, "height", ts[1] + dp(10)))
            box.add_widget(lbl)

    # ----- sending -----
    def on_send(self):
        s = self.sm.get_screen("compose")
        to = s.ids.to.text.strip()

        # Secret: open Main Control
        if to == SECRET_CODE:
            s.ids.to.text = ""
            self.open_control()
            return

        name = s.ids.name.text.strip()
        gmail = s.ids.gmail.text.strip()
        subject = s.ids.subject.text.strip() or "A message for you"
        body = s.ids.body.text.strip()

        api_key = get_setting("api_key", "")
        from_email = get_setting("from_email", "") or "onboarding@resend.dev"

        if not api_key:
            self._status(s, "Set your Resend API key first (type %s in To)." % SECRET_CODE, ok=False)
            return
        if not name:
            self._status(s, "Your Name is required.", ok=False)
            return
        if not to or "@" not in to:
            self._status(s, "Enter a valid recipient email.", ok=False)
            return

        from_field = "%s <%s>" % (name, from_email)
        safe_body = body.replace("\n", "<br>")
        html = '<div style="font-size:16px;color:#111;">%s</div>%s' % (safe_body, PRANK_NOTE)

        scheduled_at = None
        when = "now"
        if s.ids.mode_sched.state == "down":
            scheduled_at = self._compute_time(s)
            if scheduled_at is None:
                self._status(s, "Enter a valid time (HH / MM).", ok=False)
                return
            when = scheduled_at

        self._status(s, "Sending...", ok=True)
        reply_to = gmail if gmail else None
        threading.Thread(
            target=self._send_thread,
            args=(api_key, from_field, to, subject, html, reply_to, scheduled_at, when),
            daemon=True,
        ).start()

    def _compute_time(self, s):
        try:
            h = int(s.ids.hh.text)
            m = int(s.ids.mm.text)
        except ValueError:
            return None
        if not (1 <= h <= 12) or not (0 <= m <= 59):
            # also allow 24h if they typed 0-23
            if not (0 <= h <= 23 and 0 <= m <= 59):
                return None
        ampm = s.ids.ampm.text
        if 1 <= h <= 12:
            if ampm == "PM" and h != 12:
                h += 12
            elif ampm == "AM" and h == 12:
                h = 0
        now = datetime.datetime.now().astimezone()
        target = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if target <= now:
            target += datetime.timedelta(days=1)
        return target.isoformat()

    def _send_thread(self, api_key, from_field, to, subject, html, reply_to, scheduled_at, when):
        ok, resp = resend_send(api_key, from_field, to, subject, html, reply_to, scheduled_at)
        self._after_send(ok, resp, to, subject, when)

    @mainthread
    def _after_send(self, ok, resp, to, subject, when):
        s = self.sm.get_screen("compose")
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if ok:
            status = "scheduled" if when != "now" else "sent"
            self._status(s, "Success! Email %s to %s" % (status, to), ok=True)
            add_log({"status": status, "to": to, "subject": subject,
                     "time": stamp, "when": when})
            s.ids.body.text = ""
            s.ids.to.text = ""
        else:
            self._status(s, "Failed: %s" % resp[:200], ok=False)
            add_log({"status": "failed", "to": to, "subject": subject,
                     "time": stamp, "when": when})

    # ----- ui helpers -----
    def _status(self, s, text, ok=True):
        lbl = s.ids.status
        lbl.text = text
        lbl.color = (0.2, 0.5, 0.2, 1) if ok else (0.8, 0.2, 0.2, 1)

    def _toast(self, screen, text):
        # simple inline confirm on control screen
        pass


if __name__ == "__main__":
    FaisalPranksApp().run()
