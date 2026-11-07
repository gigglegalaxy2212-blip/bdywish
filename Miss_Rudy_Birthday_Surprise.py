import os
import random
import tkinter as tk
from tkinter import messagebox

import pygame

# ============================================================
# A SPECIAL BIRTHDAY SURPRISE FOR MISS RUDY
# Keep this Python file and the song in the SAME folder.
# Song filename must be: kabhi kabhi_rudy_song.mp3.mpeg
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SONG_FILE = os.path.join(BASE_DIR, "kabhi kabhi_rudy_song.mp3.mpeg")

# -------------------- WINDOW & COLOURS -----------------------

root = tk.Tk()
root.title("A Special Birthday Surprise for Miss Rudy 💗")
root.geometry("850x720")
root.minsize(650, 560)
root.configure(bg="#67afd8")

BG = "#024d70"
PANEL = "#0B2A30"
PINK = "#ff79aa"
LIGHT_PINK = "#ffd1e1"
GOLD = "#ffd477"
WHITE = "#fff7fb"
PURPLE = "#9c83ff"
POEM_BG = "#182c35"
POEM_CARD = "#203b43"
GREEN = "#bce6c9"

# -------------------- MUSIC SETUP ----------------------------

try:
    pygame.mixer.init()
    MUSIC_READY = True
except pygame.error as error:
    MUSIC_READY = False
    print("Audio could not be initialized:", error)

song_started = False
song_finished = False
next_slide_shown = False

# -------------------- SCROLLABLE WINDOW ----------------------

outer = tk.Frame(root, bg=BG)
outer.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(outer, orient="vertical")
scrollbar.pack(side="right", fill="y")

canvas = tk.Canvas(
    outer,
    bg=BG,
    highlightthickness=0,
    yscrollcommand=scrollbar.set
)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.config(command=canvas.yview)

content = tk.Frame(canvas, bg=BG)
content_window = canvas.create_window((0, 0), window=content, anchor="nw")

def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfigure(content_window, width=canvas.winfo_width())

content.bind("<Configure>", update_scroll_region)
canvas.bind("<Configure>", update_scroll_region)

def on_mousewheel(event):
    canvas.yview_scroll(int(-event.delta / 120), "units")

def bind_mousewheel(widget):
    widget.bind("<MouseWheel>", on_mousewheel)
    for child in widget.winfo_children():
        bind_mousewheel(child)

# -------------------- SMALL HELPERS --------------------------

def make_label(parent, text, size=14, color=WHITE, bg=None,
               bold=False, italic=False, wrap=700, pady=7):
    if bg is None:
        bg = parent.cget("bg")
    style = "bold" if bold else ("italic" if italic else "normal")
    label = tk.Label(
        parent,
        text=text,
        font=("Georgia", size, style),
        fg=color,
        bg=bg,
        justify="center",
        wraplength=wrap
    )
    label.pack(pady=pady)
    return label

def make_button(parent, text, command, color=PINK, width=None):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 13, "bold"),
        bg=color,
        fg="#29172b",
        activebackground=GOLD,
        activeforeground="#29172b",
        relief="flat",
        cursor="hand2",
        padx=24,
        pady=12,
        width=width
    )
    button.pack(pady=12)
    return button

def scroll_to(widget, offset=20):
    root.update_idletasks()
    y = widget.winfo_rooty() - content.winfo_rooty() - offset
    total = max(1, content.winfo_height())
    canvas.yview_moveto(max(0, min(1, y / total)))

# -------------------- WELCOME SCREEN -------------------------

welcome = tk.Frame(content, bg=BG)
welcome.pack(fill="x", pady=(35, 15))

make_label(welcome, "✨  A LITTLE SURPRISE FOR YOU  ✨",
           15, GOLD, bold=True, pady=12)
make_label(welcome, "Hey, Birthday Girl! 💗",
           31, LIGHT_PINK, bold=True, pady=12)
make_label(welcome, "A tiny birthday world made just for you...",
           16, WHITE, italic=True, pady=8)

cake_frame = tk.Frame(content, bg=BG)
cake_frame.pack(pady=8)
make_label(cake_frame, "🕯️  🕯️  🕯️", 25, GOLD, pady=2)
make_label(cake_frame, "🎂", 55, LIGHT_PINK, pady=2)
make_label(cake_frame, "HAPPY BIRTHDAY, MISS RUDY!", 17, GOLD, bold=True)

name_frame = tk.Frame(content, bg=BG)
name_frame.pack(fill="x", pady=20)
make_label(name_frame, "First, one tiny question… 😉", 16, WHITE)
make_label(name_frame, "What is the birthday girl's name?", 14, LIGHT_PINK)

name_entry = tk.Entry(
    name_frame,
    font=("Arial", 17),
    justify="center",
    bg="#fff0f5",
    fg="#35152a",
    relief="flat",
    width=22
)
name_entry.pack(ipady=9, pady=8)

error_label = make_label(name_frame, "", 12, PINK, italic=True, pady=3)

# -------------------- BIRTHDAY REVEAL ------------------------

reveal_frame = tk.Frame(content, bg="#2b1b3b")

make_label(reveal_frame, "🎉  ✨  🌻  ✨  🎉",
           30, GOLD, bg="#2b1b3b", pady=22)
make_label(reveal_frame, "YOU GOT IT RIGHT!",
           24, GOLD, bg="#2b1b3b", bold=True)
make_label(reveal_frame, "💗  MISS RUDY  💗",
           30, LIGHT_PINK, bg="#2b1b3b", bold=True, pady=12)
make_label(reveal_frame, "Today, the whole little universe is cheering for YOU.",
           15, WHITE, bg="#2b1b3b", italic=True)

birthday_text = (
    "Heyyy, Miss Rudy! ❤️\n\n"
    "Happiest Birthday to youuu! 🎂\n\n"
    "I hope this new year of your life brings you peaceful days, "
    "unexpected happiness, exciting adventures and a thousand reasons to smile.\n\n"
    "Stay exactly as wonderfully you as you are — cute, funny, a little "
    "rude sometimes (yes, I said it 😂), and very special to me.\n\n"
    "I’m really glad our paths crossed. Here’s to more silly talks, "
    "random laughs and memories we’ll keep collecting. 🌻"
)
make_label(reveal_frame, birthday_text, 15, WHITE,
           bg="#2b1b3b", wrap=690, pady=22)
make_label(reveal_frame, "🌻  sending you one sunflower and a giant hug  🌻",
           16, GOLD, bg="#2b1b3b", pady=15)

# -------------------- SLIDE 2: MOOD MOMENT -------------------

slide2 = tk.Frame(content, bg="#171326")

make_label(slide2, " •  THE MOOD CHECK 💞",
           15, GOLD, bg="#171326", bold=True, pady=24)
make_label(slide2, "How is my favourite human feeling today?",
           21, LIGHT_PINK, bg="#171326", bold=True, wrap=700)
make_label(slide2, "Pick the mood that matches you best. No wrong answers!",
           13, WHITE, bg="#171326", italic=True)

mood_result = make_label(slide2, "", 15, GOLD, bg="#171326", pady=12)
mood_buttons_frame = tk.Frame(slide2, bg="#171326")
mood_buttons_frame.pack(pady=8)

mood_messages = {
    "😊 Happy": "THAT'S THE ENERGY! Keep that smile; it looks good on you. 🌻",
    "😢 Sad": "Sending you a soft virtual hug. You don't have to be cheerful every second. 💗",
    "😡 Angry": "Birthday rule: take a breath, drink some water, and let the world wait a minute. 😌",
    "😭 Crying": "A tiny reminder: you are loved, even on the teary days. Here's a sunflower. 🌻",
    "😴 Sleepy": "Official birthday permission to rest like a sleepy anime cat. 🐱",
    "🤗 Excited": "Then let's make today feel like the best episode of your season! 🎉",
    "😶 Confused": "Plot twist: you don't need to figure everything out today. Just enjoy your cake. 🍰",
    "🥺 Missing someone": "Sending a little hug across the miles. Distance can't cancel care. 💌"
}

mood_response = make_label(slide2, "", 14, LIGHT_PINK,
                           bg="#171326", italic=True, wrap=700, pady=12)

def select_mood(mood):
    mood_result.config(text=f"Today's mood: {mood} 💗")
    mood_response.config(text=mood_messages[mood])
    for button in mood_buttons_frame.winfo_children():
        button.config(state="disabled")
    # A little playful birthday response before revealing the song and poem.
    root.after(1600, reveal_music_and_poem)

def reveal_music_and_poem():
    music_poem_area.pack(fill="x", padx=15, pady=25)
    root.update_idletasks()
    scroll_to(music_poem_area)

for mood in mood_messages:
    mood_button = tk.Button(
        mood_buttons_frame,
        text=mood,
        command=lambda choice=mood: select_mood(choice),
        font=("Arial", 12, "bold"),
        bg="#302443",
        fg=LIGHT_PINK,
        activebackground=PINK,
        activeforeground="#24112f",
        relief="flat",
        cursor="hand2",
        width=22,
        pady=9
    )
    mood_button.pack(pady=5)

# -------------------- MUSIC + POEM AREA ----------------------

music_poem_area = tk.Frame(content, bg=POEM_BG)

make_label(music_poem_area, "  •  A SONG, THEN A LETTER 🎧",
           15, GOLD, bg=POEM_BG, bold=True, pady=24)
make_label(music_poem_area, "A SONG FOR YOU",
           27, LIGHT_PINK, bg=POEM_BG, bold=True, pady=10)
make_label(music_poem_area,
           "Press play, relax, and scroll down whenever you feel like reading.",
           14, WHITE, bg=POEM_BG, italic=True, wrap=700)

song_status = make_label(
    music_poem_area,
    "Your song is waiting for you… 🎵",
    13, LIGHT_PINK, bg=POEM_BG, italic=True, pady=8
)

def play_song():
    global song_started

    if song_started:
        return

    if not MUSIC_READY:
        song_status.config(text="Audio setup failed. Please check that pygame is installed.")
        return

    if not os.path.isfile(SONG_FILE):
        song_status.config(
            text="Song not found. Keep the MP3 in the same folder as this Python file."
        )
        messagebox.showwarning(
            "Song file not found",
            "Put 'kabhi kabhi_rudy_song.mp3.mpeg' beside this Python file, then run it again."
        )
        return

    try:
        pygame.mixer.music.load(SONG_FILE)
        pygame.mixer.music.play()
        song_started = True
        play_button.config(text="🎵  MUSIC IS PLAYING", state="disabled")
        song_status.config(
            text="Enjoy the music. The poem is just below — scroll down when you're ready. 💗"
        )
        # The next-slide button appears after 60 seconds.
        root.after(60_000, reveal_next_slide_button)
        root.after(500, monitor_song)
    except pygame.error as error:
        song_status.config(text=f"Couldn't play the song: {error}")

play_button = make_button(music_poem_area, "▶  Play Your Song", play_song)
make_label(music_poem_area, "✦  ✦  ✦  ✦  ✦", 15, PINK, bg=POEM_BG, pady=8)

# Poem card is intentionally AFTER the music player.
poem_card = tk.Frame(music_poem_area, bg=POEM_CARD,
                     highlightthickness=1, highlightbackground="#55727a")
poem_card.pack(fill="x", padx=28, pady=22)

make_label(poem_card, "🌻  A FRIENDSHIP BEYOND DISTANCE  🌻",
           19, GOLD, bg=POEM_CARD, bold=True, wrap=700, pady=24)

poem_text = (
    "We've never needed the same sky,\n"
    "or the same place to share a smile.\n\n"
    "Miles may keep our worlds apart,\n"
    "but distance cannot measure a heart.\n\n"
    "Through little chats and silly talks,\n"
    "through random laughs and endless thoughts,\n"
    "a beautiful friendship found its way,\n"
    "and made ordinary moments special every day.\n\n"
    "It’s been almost a year of this friendship,\n"
    "with little pauses, comebacks and stories in between.\n"
    "Sometimes you disappear, then pop back into my world,\n"
    "and somehow there's always another conversation waiting.\n\n"
    "Maybe we haven't met just yet,\n"
    "but you're someone I won't forget.\n"
    "And even when life takes us different ways,\n"
    "I'll be cheering for you through all your days.\n\n"
    "I’m going to miss you, Rudy — more than these lines can say.\n"
    "So here's a wish across the miles:\n"
    "may life always give you reasons to smile.\n\n"
    "Happy Birthday, Miss Rudy! 💗"
)
poem_label = make_label(
    poem_card, poem_text, 15, WHITE, bg=POEM_CARD, wrap=690, pady=22
)

make_label(poem_card, "🌻  ✨  🌻  ✨  🌻",
           23, GOLD, bg=POEM_CARD, pady=15)
make_label(poem_card,
           "Take your time. The song will keep playing while you read.",
           12, LIGHT_PINK, bg=POEM_CARD, italic=True, pady=12)

# Gentle moving decorations in the poem section.
decor_canvas = tk.Canvas(
    poem_card, height=46, bg=POEM_CARD, highlightthickness=0
)
decor_canvas.pack(fill="x", padx=15, pady=(0, 10))

decorations = []
for i, symbol in enumerate(["✦", "🌻", "♡", "✧", "🌻", "♡", "✦"]):
    x = 35 + i * 105
    item = decor_canvas.create_text(
        x, random.randint(12, 34),
        text=symbol,
        fill=random.choice([PINK, GOLD, LIGHT_PINK, PURPLE]),
        font=("Segoe UI Emoji", random.randint(12, 19))
    )
    decorations.append(item)

def animate_poem_decor():
    for item in decorations:
        x, y = decor_canvas.coords(item)
        decor_canvas.move(item, 0, -1 if int(y) % 2 else 1)
        if y < 8:
            decor_canvas.coords(item, x, 38)
        elif y > 39:
            decor_canvas.coords(item, x, 9)
    root.after(350, animate_poem_decor)

# -------------------- ONE-MINUTE CONTINUE BUTTON -------------

continue_button = make_button(
    music_poem_area,
    "Continue to the next surprise  ➜",
    lambda: go_to_slide3(),
    color=GOLD
)
continue_button.pack_forget()

def reveal_next_slide_button():
    global next_slide_shown
    if next_slide_shown:
        return
    next_slide_shown = True
    song_status.config(
        text="Your next birthday thing is ready. the song will keep playing while you read. 💗"
    )
    continue_button.pack(pady=25)

def monitor_song():
    global song_finished
    if not song_started or song_finished:
        return
    try:
        if pygame.mixer.music.get_busy():
            root.after(700, monitor_song)
        else:
            song_finished = True
            song_status.config(
                text="The song has finished, but you can keep reading at your own pace. 💗"
            )
    except pygame.error:
        pass

# -------------------- SLIDE 3: NEXT CHAPTER ------------------

slide3 = tk.Frame(content, bg="#241b35")

make_label(slide3, "• THE NEXT THING  💌",
           15, GOLD, bg="#061527", bold=True, pady=28)
make_label(slide3, "Our friendship is still being written…",
           24, LIGHT_PINK, bg="#241b35", bold=True, wrap=700, pady=12)

next_page_text = (
    "If our friendship were a book, I think it would be one of those "
    "stories with funny chapters, unexpected plot twists, long gaps, "
    "and a favourite character who returns like nothing happened. 😂\n\n"
    "And if it were an anime, you'd definitely be the cute-but-slightly "
    "rude character with the best expressions and a surprisingly soft heart. 🌻\n\n"
    "I hope this year brings you beautiful chapters, kind people, "
    "new places, books you can't put down, and anime stories that make "
    "you laugh, cry and stay up way too late.\n\n"
    "Thank you for being my friend. Even across the distance, "
    "you matter to me. I'll miss you, and I'll always wish good things for you.\n\n"
    "No matter how many pages turn, I hope life keeps a little space "
    "for our random talks and silly jokes. 💗"
)
make_label(slide3, next_page_text, 15, WHITE,
           bg="#241b35", wrap=700, pady=25)
make_label(slide3, "🌻  YOU DESERVE A WHOLE FIELD OF SUNFLOWERS  🌻",
           16, GOLD, bg="#463522", bold=True, pady=18)
make_label(slide3, "Happy Birthday once again, Rudy! 🎂",
           21, LIGHT_PINK, bg="#352c1b", bold=True, pady=18)

# -------------------- NAVIGATION -----------------------------

def go_to_slide2():
    slide2.pack(fill="x", padx=15, pady=25)
    root.update_idletasks()
    scroll_to(slide2)

def go_to_slide3():
    if not slide3.winfo_manager():
        slide3.pack(fill="x", padx=15, pady=25)
    root.update_idletasks()
    scroll_to(slide3)
    # Do not stop or restart pygame music here. It continues in the background.

def reveal_name():
    entered = name_entry.get().strip().casefold()
    if entered != "rudy":
        error_label.config(text="Hmm… try the birthday girl's name again 😉")
        name_entry.delete(0, tk.END)
        return

    error_label.config(text="")
    name_entry.config(state="disabled")
    unlock_button.config(state="disabled", text="Surprise unlocked! 🎉")

    reveal_frame.pack(fill="x", padx=15, pady=25)
    go_to_slide2()
    launch_confetti()

def launch_confetti():
    confetti = tk.Toplevel(root)
    confetti.overrideredirect(True)
    confetti.attributes("-topmost", True)
    confetti.geometry("850x260+100+100")
    confetti.configure(bg=BG)
    try:
        confetti.attributes("-alpha", 0.92)
    except tk.TclError:
        pass

    confetti_canvas = tk.Canvas(confetti, bg=BG, highlightthickness=0)
    confetti_canvas.pack(fill="both", expand=True)
    pieces = []
    colours = [PINK, GOLD, PURPLE, LIGHT_PINK, GREEN, WHITE]

    for _ in range(75):
        x = random.randint(0, 850)
        y = random.randint(-260, 0)
        symbol = random.choice(["✦", "♥", "✿", "🎉"])
        item = confetti_canvas.create_text(
            x, y, text=symbol,
            fill=random.choice(colours),
            font=("Segoe UI Emoji", random.randint(10, 19))
        )
        pieces.append(item)

    def fall(step=0):
        if step > 45 or not confetti.winfo_exists():
            confetti.destroy()
            return
        for item in pieces:
            confetti_canvas.move(item, random.choice([-2, -1, 0, 1, 2]),
                                 random.randint(3, 8))
        confetti.after(45, lambda: fall(step + 1))

    fall()

unlock_button = make_button(
    name_frame, "Unlock My Surprise 💝", reveal_name, color=PINK
)
name_entry.bind("<Return>", lambda event: reveal_name())

# -------------------- FOOTER & START -------------------------

make_label(content, "Made with friendship, a little mischief, and lots of love. 💗",
           11, LIGHT_PINK, bg=BG, italic=True, pady=28)

animate_poem_decor()
bind_mousewheel(content)
root.mainloop()

# Keep the mixer clean when the app is closed.
try:
    pygame.mixer.music.stop()
    pygame.mixer.quit()
except pygame.error:
    pass
