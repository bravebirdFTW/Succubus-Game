```
# --- Initialize Python for Typewriter Effect ---
init python:
    import renpy.exports as renpy_exports

    _type_sound_counter = 0

    def typewriter_callback(event, interact=True, **kwargs):
        global _type_sound_counter

        if event == "show":
            _type_sound_counter = 0

        elif event == "slow_done":
            _type_sound_counter = 0

        elif event == "slow":
            _type_sound_counter += 1

            if _type_sound_counter % 2 == 0:
                renpy_exports.queue_event(lambda: renpy.sound.play("audio/type_bleep.mp3"))

# --- Define Game Over Screens ---
screen gameover_happy_screen:
    modal True
    add "images/spirit_bond.png" xalign 0.5 yalign 0.5  # Displays the alliance ending image
    text "A New Alliance Forged" size 40 color "#FFFFFF" outlines [(2, "#000000", 0, 0)] xalign 0.5 yalign 0.8
    key "dismiss" action Return()

screen gameover_screen:
    modal True
    add "images/spirit_fade.png" xalign 0.5 yalign 0.5  # Displays the command ending image
    text "The Spirit's Power Wanes" size 40 color "#FFFFFF" outlines [(2, "#000000", 0, 0)] xalign 0.5 yalign 0.8
    key "dismiss" action Return()

# --- Volume and Channel Setup ---
init python:
    renpy.music.set_volume(0.35, channel="music")   # Lower ambient music
    renpy.music.set_volume(1.0, channel="sound")    # Full volume for sound effects
    renpy.music.set_volume(1.0, channel="typing")   # Full volume for typing sounds
    renpy.music.register_channel("aura", mixer="sfx", loop=True, stop_on_mute=True)

# --- Character Definitions ---
define s = Character(
    None,
    what_color="#99CCFF",  # Changed to a neutral blue for a mystical spirit
    what_outlines=[(3, "#001933", 0, 0)],
    window_yalign=0.5,
    window_xalign=0.5,
    callback=typewriter_callback
)

define p = Character(
    None,
    what_color="#FFFFFF",
    what_outlines=[(2, "#000000", 0, 0)],
    window_yalign=0.5,
    window_xalign=0.5,
    callback=typewriter_callback
)

define narrator = Character(
    None,
    callback=typewriter_callback
)

# --- Define Subtle Glow Transform ---
transform subtle_glow:
    xoffset 0 yoffset 0
    linear 0.5 xoffset 5 yoffset -5
    linear 0.5 xoffset 0 yoffset 0
    linear 0.5 xoffset -5 yoffset -5
    linear 0.5 xoffset 0 yoffset 0
    repeat

# --- Images (SFW replacements) ---
image bg_summon      = "images/bg_summon.jpg"  # Unchanged, as a ritual circle is neutral
image room_normal    = "images/room_normal.png"  # Neutral room
image room_glow      = "images/room_glow.png"  # Spirit's aura glows
image room_aura      = "images/room_aura.png"  # Spirit's magical aura

image spirit_struggle = "images/spirit_struggle.png"  # Spirit resisting
image spirit_bind     = "images/spirit_bind.png"     # Spirit being bound
image spirit_face     = "images/spirit_face.png"     # Close-up of spirit's face

image dawn_normal     = "images/dawn_normal.png"     # Morning scene, neutral
image dawn_talking    = "images/dawn_talking.png"   # Spirit speaking
image dawn_glowing    = "images/dawn_glowing.png"   # Spirit glowing
image dawn_bind       = "images/dawn_bind.png"      # Binding ritual complete
image spirit_zoom     = "images/spirit_zoom.png"    # Zoom on spirit's mark
image spirit_mark     = "images/spirit_mark.png"    # Player's mark on spirit
image spirit_mark_happy = "images/spirit_mark_happy.png"  # Player's mark, glowing
image spirit_bond     = "images/spirit_bond.png"    # Alliance ending
image spirit_fade     = "images/spirit_fade.png"    # Command ending

define flash_blue = Fade(0.05, 0.0, 0.3, color="#99CCFF")  # Blue for mystical theme

label start:
    $ preferences.text_cps = 25  # Force typewriter speed

    scene bg_summon
    with fade

    play music "audio/night_ambience.mp3" fadein 0.8

    "Midnight. Candles lit. Chalk circle steady."
    "One last whisper… and the spirit should appear."
    "Heart's pounding. This is either a breakthrough… or a grave mistake."
    "Okay. Deep breath. Stay calm."
    "I call to the spirit with silver light and emerald glow."
    "Answer me."

    queue sound "audio/mystic_hum.mp3"
    queue sound "audio/spirit_call.mp3"
    $ renpy.pause(3.6, hard=True)

    play sound "audio/summon_spark.mp3"
    show expression Solid("#99CCFF") as flash_layer
    with flash_blue
    hide flash_layer

    show room_normal

    s "Well, well… a mortal summons me. Such courage, seeker~"

    "You have successfully summoned the spirit. What will you do?"

    menu:
        "Command the spirit to obey（精霊に従うよう命令する）":
            jump cmd_path

        "Offer to ally with the spirit（精霊と同盟することを申し出る）":
            jump serve_path

label cmd_path:
    show room_normal
    with dissolve

    p "You will follow my commands."

    show room_glow
    play sound "audio/mystic_laugh.mp3"
    $ renpy.pause(0.7)

    s "Oh, you believe you can bind me? Your will is strong, but I am no servant~"
    s "I’ll test your resolve, mortal, and see if you can hold my power."

    show room_aura
    play sound "audio/aura_pulse.mp3"
    $ renpy.pause(0.6)

    s "That defiance in your eyes… it intrigues me~"
    s "Let’s see if you can withstand my essence, seeker~"

    $ renpy.pause(0.8)

    show room_aura
    with dissolve
    play sound "audio/magic_bind.mp3"
    $ renpy.pause(1.0)

    s "Step closer, mortal~"

    play sound "audio/magic_impact.mp3"
    stop music fadeout 0.8
    scene black
    with hpunch
    $ renpy.pause(0.5)

    stop music channel "aura"
    $ renpy.music.play("audio/aura_loop.mp3", channel="aura", loop=True)

    s "You’ve caught me, seeker. My aura binds you now, pulsing with power."
    s "Feel its strength? You cannot escape my will~"

    scene spirit_struggle
    show spirit_struggle at subtle_glow
    with dissolve

    s "Keep resisting, mortal. It only fuels my energy."
    s "You’re bound by my aura, ready to face my trial~"

    stop music channel "aura"
    scene spirit_bind
    show spirit_bind at subtle_glow
    with dissolve

    play sound "audio/magic_seal.mp3"
    $ renpy.pause(1.0)

    $ renpy.music.play("audio/mystic_ambience.mp3", channel="aura", loop=True)

    s "Now, you’re drawn to my core, slow and steady."
    s "I’m binding you closer, mortal, to test your command~"

    scene spirit_face
    show spirit_face at subtle_glow
    with dissolve

    play sound "audio/mystic_laugh.mp3"
    $ renpy.pause(1.5)

    s "Quiet now, brave seeker. My essence surrounds you."
    s "You’re bound to me, held within my light~"

    jump morning_after

label serve_path:
    show room_normal
    with dissolve

    p "I… I’ll ally with you."

    show room_glow
    play sound "audio/mystic_laugh.mp3"
    $ renpy.pause(0.7)

    s "A wise choice, seeker~ You’ll aid me best by joining my light."
    s "You’ll strengthen my essence, mortal. Are you ready to align fully?"

    show room_aura
    with dissolve
    play sound "audio/magic_bind.mp3"
    $ renpy.pause(2.0)

    s "Come to me, seeker~ My aura awaits your bond."

    play sound "audio/magic_impact.mp3"
    stop music fadeout 0.8
    scene black
    with hpunch
    $ renpy.pause(0.5)

    stop music channel "aura"
    $ renpy.music.play("audio/aura_loop.mp3", channel="aura", loop=True)

    s "My aura holds you, seeker—so strong, so radiant~"
    s "You feel it, don’t you? Ready to unite with my power."

    scene spirit_struggle
    show spirit_struggle at subtle_glow
    with dissolve

    s "Your resolve is admirable~ Keep steady, mortal, it strengthens our bond."
    s "You’re perfect within my aura, seeker. Ready to merge with me?"

    stop music channel "aura"
    scene spirit_bind
    show spirit_bind at subtle_glow
    with dissolve

    play sound "audio/magic_seal.mp3"
    $ renpy.pause(1.0)

    $ renpy.music.play("audio/mystic_ambience.mp3", channel="aura", loop=True)

    s "Into my core you go, seeker~ Your alliance empowers me."
    s "What’s it like, hmm? Knowing you’re part of my radiant essence?"

    scene spirit_face
    show spirit_face at subtle_glow
    with dissolve

    play sound "audio/aura_pulse.mp3"
    $ renpy.pause(0.6)

    s "Feel my light around you, seeker? You’re nearly one with me~"
    s "Rest now, my ally. Let my essence bind you to my cause."

    jump morning_after_serve

label morning_after:
    stop music channel "aura"

    scene black
    with fade
    play sound "audio/morning_ambience.mp3"
    $ renpy.pause(2.0)

    narrator "The following morning…"

    scene dawn_normal
    with fade
    play sound "audio/magic_rustle.mp3"
    $ renpy.pause(1.5)

    scene dawn_talking
    with dissolve
    play sound "audio/mystic_hum.mp3"
    $ renpy.pause(0.8)

    s "Good morning, brave seeker~"
    s "Your mark, etched in my light, binds you to my power."

    scene dawn_glowing
    with dissolve
    play sound "audio/mystic_laugh.mp3"
    $ renpy.pause(1.0)

    s "Your spirit has strengthened me… I can still feel your resolve~"
    s "You’re bound to me, seeker, fueling my radiance."

    scene spirit_zoom
    with dissolve
    $ renpy.pause(1.0)

    narrator "A radiant warmth surrounds you, your essence tied to her glowing aura. Your mark, a faint sigil in her light, seals your eternal bond."

    show spirit_mark at center with dissolve
    play sound "audio/surprise.mp3"
    $ renpy.pause(0.6)

    p "No… this can’t be! Release me, please!"

    hide spirit_mark

    scene dawn_talking
    with dissolve
    play sound "audio/mystic_hum.mp3"
    $ renpy.pause(0.8)

    s "Don’t resist, seeker. Your struggle only strengthens our bond~"
    s "You’re part of my light now, empowering my essence."

    scene dawn_bind
    with dissolve
    play sound "audio/magic_bind.mp3"
    $ renpy.pause(0.7)

    s "Feel my power, seeker? Your resistance fuels my strength~"
    s "You’ll merge deeper, forever shaping my radiant form."

    scene spirit_zoom
    with dissolve
    play sound "audio/mystic_laugh.mp3"
    $ renpy.pause(3.2)

    s "Your essence is mine, seeker. You’ll shine within me, making me stronger~"
    s "Surrender, brave one, and let my light guide you."

    show spirit_mark at center with dissolve
    play sound "audio/surprise.mp3"
    $ renpy.pause(0.6)

    p "I… I can’t stay like this! There must be a way out!"

    hide spirit_mark

    scene dawn_glowing
    with dissolve
    play sound "audio/mystic_laugh.mp3"
    $ renpy.pause(0.7)

    s "No escape, seeker. Your form is bound to my radiant aura~"
    s "Only your essence remains, forever tied to my light."

    scene dawn_talking
    with dissolve
    play sound "audio/mystic_hum.mp3"
    $ renpy.pause(1.0)

    s "I carry your strength with me, seeker—within my glowing essence~"
    s "No turning back. You’re mine, shining with every pulse of your spirit."

    scene dawn_bind
    with dissolve
    play sound "audio/magic_bind.mp3"
    $ renpy.pause(0.7)

    s "Isn’t this fitting, seeker? Your essence, bound to make me stronger~"
    s "What’s it like, hmm? Knowing you’re part of my light now?"

    scene spirit_zoom
    with dissolve
    play sound "audio/mystic_hum.mp3"
    $ renpy.pause(0.8)

    s "No more resistance, seeker. Your purpose is clear: to empower my light~"
    s "Be steadfast, and perhaps I’ll share my radiance with you~"

    show spirit_mark at center with dissolve
    play sound "audio/surprise.mp3"
    $ renpy.pause(0.6)

    p "Please… I don’t want to be trapped like this!"

    hide spirit_mark

    scene dawn_talking
    with dissolve
    play sound "audio/mystic_laugh.mp3"
    $ renpy.pause(3.2)

    s "You have no choice, seeker~ Your essence is woven into my light."
    s "You’re bound to me, your spirit fueling my radiance forever~"

    scene dawn_glowing
    with dissolve
    play sound "audio/mystic_laugh.mp3"
    $ renpy.pause(0.7)

    s "Every pulse of your spirit strengthens me, seeker. You’re home within my light~"
    s "None can break this bond, seeker. You’re mine, eternally tied to my power."

    scene spirit_zoom
    with dissolve
    play sound "audio/mystic_hum.mp3"
    $ renpy.pause(0.8)

    s "Feel it, seeker? Your essence shines, making my aura radiant~"
    s "Why resist? You’re my valued prize, forever part of my light."

    scene dawn_talking
    with dissolve
    play sound "audio/mystic_laugh.mp3"
    $ renpy.pause(1.0)

    s "I’ll carry your essence always, my brave, shining spirit~"
    s "Your purpose is mine, seeker—empowering my light, with no return."

    play music "audio/spirit_end.mp3"
    scene black
    with fade
    $ renpy.pause(1.0)

    call screen gameover_screen with fade

    return

label morning_after_serve:
    stop music channel "aura"

    scene black
    with fade
    play sound "audio/morning_ambience.mp3"
    $ renpy.pause(2.0)

    narrator "The following morning…"

    scene dawn_normal
    with fade
    play sound "audio/magic_rustle.mp3"
    $ renpy.pause(1.5)

    scene dawn_talking
    with dissolve
    play sound "audio/mystic_hum.mp3"
    $ renpy.pause(0.8)

    s "Good morning, my valued ally. Your bond has made my light even brighter~"
    s "Your mark, etched in my aura, is a radiant sign of our alliance."

    scene dawn_glowing
    with dissolve
    play sound "audio/mystic_laugh.mp3"
    $ renpy.pause(1.0)

    s "I feel your spirit’s strength, pulsing within my light~"
    s "You chose to ally with me, seeker. Are you ready to share my purpose?"

    scene spirit_zoom
    with dissolve
    $ renpy.pause(1.0)

    narrator "A gentle warmth surrounds you, your essence held within her radiant aura. Your mark, a glowing sigil in her light, seals your alliance."

    show spirit_mark at center with dissolve
    play sound "audio/surprise.mp3"
    $ renpy.pause(0.6)

    p "What’s happening? I’m bound… it’s all around me!"

    hide spirit_mark

    scene dawn_talking
    with dissolve
    play sound "audio/mystic_hum.mp3"
    $ renpy.pause(0.8)

    s "Calm yourself, my ally. You joined me, and now you’re where you belong~"
    s "Safe in my light, your spirit ready to shine. Will you trust me, my partner?"

    show spirit_mark at center with dissolve
    play sound "audio/surprise.mp3"
    $ renpy.pause(0.6)

    p "I trust you, but this is overwhelming… I feel so faint."

    hide spirit_mark

    scene dawn_bind
    with dissolve
    play sound "audio/magic_bind.mp3"
    $ renpy.pause(0.7)

    s "That’s the beauty of it, seeker. My light will guide you to peace~"
    s "Your spirit strengthens me over time, merging with my essence. Will you be brave for our cause?"

    scene spirit_zoom
    with dissolve
    play sound "audio/mystic_laugh.mp3"
    $ renpy.pause(3.2)

    s "Feel my light holding you, seeker? You’re becoming part of me, gently and surely~"
    s "Let fear fade. Will you serve our purpose, knowing we’ll unite fully?"

    show spirit_mark at center with dissolve
    play sound "audio/surprise.mp3"
    $ renpy.pause(0.6)

    p "It’s daunting, but… for you, yes. I want to ally."

    hide spirit_mark

    scene dawn_glowing
    with dissolve
    play sound "audio/mystic_laugh.mp3"
    $ renpy.pause(0.7)

    s "That’s my ally. Your resolve makes this bond special~"
    s "You’ll shine with me as we merge. Can you feel how right this is?"

    scene dawn_talking
    with dissolve
    play sound "audio/mystic_hum.mp3"
    $ renpy.pause(1.0)

    s "Every pulse of your spirit brings me joy, seeker~"
    s "You’ll be my partner, strengthening me as we unite. Will you?"

    scene spirit_zoom
    show spirit_mark_happy at center with dissolve
    $ renpy.pause(0.6)

    p "Yes, my guide… I’ll be your ally, even knowing our union."

    hide spirit_mark_happy

    scene dawn_bind
    with dissolve
    play sound "audio/magic_bind.mp3"
    $ renpy.pause(0.7)

    s "Such a radiant promise, seeker. Your bond makes my light crave you more~"
    s "You’re strengthening me, ally. Are you content to shine this way?"

    scene spirit_zoom
    with dissolve
    play sound "audio/mystic_hum.mp3"
    $ renpy.pause(0.8)

    s "You’re sealed in my light, seeker, your spirit mine to share~"
    s "Embrace it, my ally. Will you give your all, shining until the end?"

    scene spirit_zoom
    show spirit_mark_happy at center with dissolve
    $ renpy.pause(0.6)

    p "I will, my guide… I embrace you, happy to unite with you~"

    hide spirit_mark_happy

    scene dawn_glowing
    with dissolve
    play sound "audio/mystic_laugh.mp3"
    $ renpy.pause(0.7)

    s "Your words warm me, seeker. You’re my perfect ally now~"
    s "Bound to my light, merging with me in every moment."

    scene spirit_zoom
    with dissolve
    play sound "audio/mystic_hum.mp3"
    $ renpy.pause(0.8)

    s "Feel my embrace, ally? Your spirit’s pulse is your vow to me~"
    s "You’ve chosen wisely. Are you ready to commit fully?"

    scene dawn_talking
    with dissolve
    play sound "audio/mystic_laugh.mp3"
    $ renpy.pause(1.0)

    s "I’ll hold your essence forever, my radiant, steadfast ally~"
    s "Your bond is my strength, seeker—uniting with your guide."

    scene spirit_zoom
    show spirit_mark_happy at center with dissolve
    $ renpy.pause(0.6)

    p "I’m ready, my guide… I live to ally and shine with you~"

    hide spirit_mark_happy

    play music "audio/spirit_end.mp3"
    scene black
    with fade
    $ renpy.pause(1.0)

    call screen gameover_happy_screen with fade

    return
```