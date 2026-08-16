import os
import json
import threading
import urllib.parse
import urllib.request
import yt_dlp

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.slider import Slider
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

PLAYLIST_FILE = "playlist.json"

def load_playlist():
    if os.path.exists(PLAYLIST_FILE):
        try:
            with open(PLAYLIST_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_playlist(playlist):
    with open(PLAYLIST_FILE, "w") as f:
        json.dump(playlist, f)

class YodhasMusicApp(App):
    def build(self):
        self.playlist = load_playlist()
        self.current_index = 0
        self.current_sound = None
        self.is_looping = False
        self.current_song = None

        os.makedirs("downloads", exist_ok=True)

        # Root Layout
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # App Title
        root.add_widget(Label(text="YODHAS Music Player", font_size='22sp', bold=True, size_hint_y=None, height=40))

        # Input Area
        input_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=5)
        self.query_input = TextInput(hint_text="Enter Song Name or YouTube Link", multiline=False)
        add_btn = Button(text="Add", size_hint_x=0.25, background_color=(0.11, 0.72, 0.33, 1))
        add_btn.bind(on_release=self.add_song)
        input_box.add_widget(self.query_input)
        input_box.add_widget(add_btn)
        root.add_widget(input_box)

        # Playlist Header & Clear Button
        pl_header = BoxLayout(size_hint_y=None, height=40)
        pl_header.add_widget(Label(text="Playlist", font_size='18sp', bold=True))
        clear_btn = Button(text="Clear", size_hint_x=0.3)
        clear_btn.bind(on_release=self.clear_playlist)
        pl_header.add_widget(clear_btn)
        root.add_widget(pl_header)

        # Playlist Scroll View
        scroll = ScrollView()
        self.playlist_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.playlist_layout.bind(minimum_height=self.playlist_layout.setter('height'))
        scroll.add_widget(self.playlist_layout)
        root.add_widget(scroll)

        # Player Controls Section
        player_box = BoxLayout(orientation='vertical', size_hint_y=None, height=280, spacing=5)

        self.cover_art = AsyncImage(source='', size_hint_y=None, height=100)
        self.now_playing = Label(text="Select a song to play", font_size='16sp', bold=True, size_hint_y=None, height=30)
        player_box.add_widget(self.cover_art)
        player_box.add_widget(self.now_playing)

        # Transport Buttons
        controls = BoxLayout(size_hint_y=None, height=40, spacing=5)
        btn_prev = Button(text="Prev")
        btn_prev.bind(on_release=self.prev_song)
        self.btn_loop = Button(text="Loop: OFF")
        self.btn_loop.bind(on_release=self.toggle_loop)
        btn_next = Button(text="Next")
        btn_next.bind(on_release=self.next_song)
        btn_dl = Button(text="Download")
        btn_dl.bind(on_release=self.download_song)
        btn_lyrics = Button(text="Lyrics")
        btn_lyrics.bind(on_release=self.fetch_lyrics)

        controls.add_widget(btn_prev)
        controls.add_widget(self.btn_loop)
        controls.add_widget(btn_next)
        controls.add_widget(btn_dl)
        controls.add_widget(btn_lyrics)
        player_box.add_widget(controls)

        # Volume Control
        vol_box = BoxLayout(size_hint_y=None, height=30, spacing=5)
        vol_box.add_widget(Label(text="Volume", size_hint_x=0.2))
        vol_slider = Slider(min=0, max=1, value=1)
        vol_slider.bind(value=self.set_volume)
        vol_box.add_widget(vol_slider)
        player_box.add_widget(vol_box)

        # Lyrics Display Box
        self.lyrics_label = Label(text="Lyrics will appear here", font_size='12sp', size_hint_y=None, height=60)
        player_box.add_widget(self.lyrics_label)

        root.add_widget(player_box)

        self.update_playlist_ui()
        return root

    def update_playlist_ui(self):
        self.playlist_layout.clear_widgets()
        for idx, song in enumerate(self.playlist):
            btn = Button(text=f"{idx+1}. {song['title']}", size_hint_y=None, height=40, halign='left')
            btn.bind(on_release=lambda instance, i=idx: self.play_song_index(i))
            self.playlist_layout.add_widget(btn)

    def add_song(self, instance):
        query = self.query_input.text.strip()
        if not query:
            return
        self.now_playing.text = "Fetching song info..."
        self.query_input.text = ""
        threading.Thread(target=self._add_song_worker, args=(query,)).start()

    def _add_song_worker(self, query):
        if not query.startswith("http"):
            query = f"ytsearch1:{query}"
        ydl_opts = {'quiet': True, 'extract_flat': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                if 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            v_url = f"https://youtube.com/watch?v={entry['id']}"
                            self._extract_details(v_url)
                else:
                    self._extract_details(query)
            save_playlist(self.playlist)
            Clock.schedule_once(lambda dt: self.update_playlist_ui())
            Clock.schedule_once(lambda dt: setattr(self.now_playing, 'text', 'Added to playlist!'))
        except Exception as e:
            Clock.schedule_once(lambda dt: setattr(self.now_playing, 'text', f'Error loading song: {str(e)[:50]}'))

    def _extract_details(self, url):
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            song = {"url": url, "title": info.get('title', 'Unknown'), "thumbnail": info.get('thumbnail', '')}
            if not any(s['url'] == url for s in self.playlist):
                self.playlist.append(song)

    def play_song_index(self, index):
        if index < 0 or index >= len(self.playlist):
            return
        self.current_index = index
        self.current_song = self.playlist[index]
        self.now_playing.text = f"Loading: {self.current_song['title']}"
        self.cover_art.source = self.current_song.get('thumbnail', '')
        threading.Thread(target=self._stream_and_play, args=(self.current_song['url'],)).start()

    def _stream_and_play(self, url):
        ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                stream_url = info['url']
                
                def start_audio(dt):
                    if self.current_sound:
                        self.current_sound.stop()
                    self.current_sound = SoundLoader.load(stream_url)
                    if self.current_sound:
                        self.current_sound.play()
                        self.now_playing.text = f"Playing: {self.current_song['title']}"
                    else:
                        self.now_playing.text = "Playback Error"

                Clock.schedule_once(start_audio)
        except Exception as e:
            Clock.schedule_once(lambda dt: setattr(self.now_playing, 'text', f'Stream Error: {str(e)[:50]}'))

    def next_song(self, instance=None):
        if self.current_index < len(self.playlist) - 1:
            self.play_song_index(self.current_index + 1)

    def prev_song(self, instance=None):
        if self.current_index > 0:
            self.play_song_index(self.current_index - 1)

    def toggle_loop(self, instance):
        self.is_looping = not self.is_looping
        self.btn_loop.text = f"Loop: {'ON' if self.is_looping else 'OFF'}"
        if self.current_sound:
            self.current_sound.loop = self.is_looping

    def set_volume(self, instance, value):
        if self.current_sound:
            self.current_sound.volume = value

    def fetch_lyrics(self, instance):
        if not self.current_song:
            return
        self.lyrics_label.text = "Loading lyrics..."
        threading.Thread(target=self._lyrics_worker, args=(self.current_song['title'],)).start()

    def _lyrics_worker(self, title):
        try:
            url = f"https://lrclib.net/api/search?track_name={urllib.parse.quote(title)}"
            req = urllib.request.urlopen(url)
            data = json.loads(req.read().decode())
            lyrics_text = data[0]['plainLyrics'] if data and len(data) > 0 else "Lyrics not found"
        except Exception:
            lyrics_text = "Lyrics not found"

        Clock.schedule_once(lambda dt: setattr(self.lyrics_label, 'text', lyrics_text[:200] + "..."))

    def download_song(self, instance):
        if not self.current_song:
            return
        self.now_playing.text = "Downloading audio..."
        threading.Thread(target=self._download_worker, args=(self.current_song['url'],)).start()

    def _download_worker(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            Clock.schedule_once(lambda dt: setattr(self.now_playing, 'text', 'Download Complete!'))
        except Exception as e:
            Clock.schedule_once(lambda dt: setattr(self.now_playing, 'text', f'Download Failed: {str(e)[:50]}'))

    def clear_playlist(self, instance):
        self.playlist = []
        save_playlist(self.playlist)
        self.update_playlist_ui()
        if self.current_sound:
            self.current_sound.stop()
        self.now_playing.text = "Playlist cleared"

if __name__ == "__main__":
    YodhasMusicApp().run()
