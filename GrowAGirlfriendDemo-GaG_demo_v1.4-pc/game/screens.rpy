################################################################################
## Initialization
################################################################################

init offset = -1


################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say


init python:
    def reset_data():
        ## deletes all persistent data use with caution
        for attr in dir(persistent):
            if not callable(attr) and not attr.startswith("_"):
                setattr(persistent, attr, None)

        ## deletes all save games use with caution!
        for slot in renpy.list_saved_games(fast=True):
            renpy.unlink_save(slot)
        ## a Ren'Py relaunch is nessesary
        renpy.quit(relaunch=True)



screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)
    # background Frame(textualBox, 0, 0) 
# default theBox = "gui/textbox_trans.png"
# define textualBox = "[theBox]"

style namebox:
    
    #new
    xalign 0.5
    yalign 0.5
    xsize 317
    ysize 152
    xpos 590
    ypos 38
    background Image("gui/namebox.png")
    

    #old(safe to work):
    # xpos 470 #gui.name_xpos
    # xanchor 0.5
    # xsize 50# gui.namebox_width
    # ypos -160 #gui.name_ypos
    # ysize gui.namebox_height

    #background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    #padding gui.namebox_borders.padding


    

style say_dialogue:
    properties gui.text_properties("dialogue")
    color "#000000"
    yalign 0.2
    xalign 0.5
    ypos 100
    #ypos 50 #gui.dialogue_ypos
    #xpos 1000 #gui.dialogue_xpos
    xsize 900 #gui.dialogue_width
    ysize 225 #gui.dialogue_height
    
    #outlines [ (absolute(3), "#f6f0f0", absolute(0), absolute(0)) ]
    adjust_spacing False

## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"
    
    window:

        vbox:
            
            xanchor gui.dialogue_text_xalign
            xpos 700 #gui.dialogue_xpos
            xsize 1000 #gui.dialogue_width
            ypos 50 #gui.dialogue_ypos

            text prompt style "input_prompt" color "#000000"
            input id "input" color "#38425F" 

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):

    #Original code below --
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action
    #Original code above --


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing -50 #gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

default quick_menu = True

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:
        
        imagebutton:
            xalign 0.19 yalign 1.0 idle "gui/skip_symbol.png" hover_sound "audio/SFX/button_hover.wav" hover "gui/skip_symbol_hover.png" action Skip() alternate Skip(fast=True, confirm=True)
        hbox:
            style_prefix "quick"

            xalign 0.68
            yalign 1.0
            yoffset 5
            
            

            imagebutton:
                idle "gui/save_symbol.png" hover_sound "audio/SFX/button_hover.wav" hover "gui/save_symbol_hover.png" action ShowMenu('save')
            imagebutton:
                xpos 10 idle "gui/load_symbol.png" hover_sound "audio/SFX/button_hover.wav" hover "gui/load_symbol_hover.png" action ShowMenu('load')
            imagebutton:
                xpos 20 idle "gui/options_symbol.png" hover_sound "audio/SFX/button_hover.wav" hover "gui/options_symbol_hover.png" action ShowMenu('preferences')
            imagebutton:
                xpos 30 idle "gui/history_symbol.png" hover_sound "audio/SFX/button_hover.wav" hover "gui/history_symbol_hover.png" action ShowMenu('history')

            #textbutton _("Back") action Rollback()
            #textbutton _("History") action ShowMenu('history')
            #textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            #textbutton _("Auto") action Preference("auto-forward", "toggle")
            #textbutton _("Save") action ShowMenu('save')
            #textbutton _("Q.Save") action QuickSave()
            #textbutton _("Q.Load") action QuickLoad()
            #textbutton _("Load") action ShowMenu('load')
            #textbutton _("Prefs") action ShowMenu('preferences')


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")


style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.button_text_properties("quick_button")


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigation():

    vbox:
        style_prefix "navigation"
        if renpy.get_screen("main_menu"):
            
            xpos 0.104
            spacing 25
            yalign 0.681
        else:
            xpos 0.05
            yalign 0.5    

            spacing gui.navigation_spacing

        if main_menu:
            
            textbutton _("Start") hover_sound "audio/SFX/thud.wav" activate_sound "audio/SFX/website_click.wav" action Start():
                if renpy.get_screen("main_menu"):
                    at entertop

        else:

            textbutton _("History") hover_sound "audio/SFX/thud.wav" activate_sound "audio/SFX/website_click.wav" action ShowMenu("history")

            textbutton _("Save") hover_sound "audio/SFX/thud.wav" activate_sound "audio/SFX/website_click.wav" action ShowMenu("save")

        textbutton _("Load") hover_sound "audio/SFX/thud.wav" activate_sound "audio/SFX/website_click.wav" action ShowMenu("load"):
            if renpy.get_screen("main_menu"):
                at enter2ndtop

        textbutton _("Options") hover_sound "audio/SFX/thud.wav" activate_sound "audio/SFX/website_click.wav" action ShowMenu("preferences"):
            if renpy.get_screen("main_menu"):
                at entermiddle

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Main Menu") action MainMenu()

        #textbutton _("About") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## Help isn't necessary or relevant to mobile devices.
            textbutton _("Help") hover_sound "audio/SFX/thud.wav" activate_sound "audio/SFX/website_click.wav" action ShowMenu("help"):
                if renpy.get_screen("main_menu"):
                    at enter2ndbot

        if renpy.variant("pc"):

            ## The quit button is banned on iOS and unnecessary on Android and
            ## Web.
            textbutton _("Quit") hover_sound "audio/SFX/thud.wav" activate_sound "audio/SFX/website_click.wav" action Quit(confirm=not main_menu):
                if renpy.get_screen("main_menu"):
                    at enterbot


style navigation_button is gui_button
style navigation_button_text:
    xalign 0.5
    color "#ffffff"
    selected_color "#c86b85"
    hover_color "#FFFF00"

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")
    #font "fonts/Pompiere-Regular.ttf"
    font "fonts/Kingthings Clarity1.1.ttf"

## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

transform movemushrooms:

    ease 2 xoffset 460
    ease 2 xpos 300 ypos -300
    ease 0.3 alpha 0

transform scroll:
    xalign 0.0
    linear 10 xalign 1.0
    repeat
    
    # xalign 0.0
    # linear 10 xalign 1.0
    # repeat


transform hbounce:
    ease .05 xoffset 10
    ease .02 xoffset 0
    ease .03 xoffset -10
    ease .02 xoffset 0 

transform vbounce:
    ease 2 yoffset 20
    ease 2 yoffset -20
    repeat

transform folderappear:
    ypos 1.0
    ease 0.5 ypos 0.0

transform titleappear:
    ypos -0.5
    # pause 0.2
    ease 0.5 ypos 0.1
    ease 0.2 ypos -0.05
    ease 0.2 ypos 0.05
    ease 0.2 ypos -0.02
    ease 0.5 yoffset 20
    ease 1 yoffset -20
    ease 1.2 yoffset 20
    ease 1.5 yoffset -20
    vbounce
    
transform entergallery:
    # alpha 0.00
    # pause 0.5
    # easein 1 alpha 1
    on hover:
        linear 0.1 yoffset -5
    on idle:
        linear 0.1 yoffset 0



transform entermenu:
    xpos -0.5
    ease 1 xpos 0.0
    hbounce

transform entertop:
    xoffset -50 alpha 0
    # pause 0.7
    ease 0.3 xoffset 0 alpha 1
    on hover:
        linear 0.1 xoffset 5
    on idle:
        linear 0.1 xoffset 0

transform enter2ndtop:
    xoffset -50 alpha 0
    # pause 0.75
    ease 0.3 xoffset 0 alpha 1    
    on hover:
        linear 0.1 xoffset 5
    on idle:
        linear 0.1 xoffset 0

transform entermiddle:
    xoffset -50 alpha 0
    # pause 0.8
    ease 0.3 xoffset 0 alpha 1
    on hover:
        linear 0.1 xoffset 5
    on idle:
        linear 0.1 xoffset 0

transform enter2ndbot:
    xoffset -50 alpha 0
    # pause 0.85
    ease 0.3 xoffset 0 alpha 1
    on hover:
        linear 0.1 xoffset 5
    on idle:
        linear 0.1 xoffset 0

transform enterbot:
    xoffset -50 alpha 0
    # pause 0.9
    ease 0.3 xoffset 0 alpha 1
    on hover:
        linear 0.1 xoffset 5
    on idle:
        linear 0.1 xoffset 0     

transform enterending:
    xoffset -40
    yoffset 500
    ease 0.3 yoffset -20
    ease 0.2 yoffset 10
    ease 0.1 yoffset -7
    ease 0.1 yoffset 0           

transform enterending2:
    xoffset -10
    yoffset 500
    pause 0.1
    ease 0.3 yoffset -20
    ease 0.2 yoffset 10
    ease 0.1 yoffset -7
    ease 0.1 yoffset 0    

transform enterending3:
    xoffset -10
    yoffset 500
    pause 0.2
    ease 0.3 yoffset -20
    ease 0.2 yoffset 10
    ease 0.1 yoffset -7
    ease 0.1 yoffset 0

transform enterending4:
    xoffset -10
    yoffset 500
    pause 0.3
    ease 0.3 yoffset -20
    ease 0.2 yoffset 10
    ease 0.1 yoffset -7
    ease 0.1 yoffset 0 

transform enterending5:
    xoffset -10
    yoffset 500
    pause 0.4
    ease 0.3 yoffset -20
    ease 0.2 yoffset 10
    ease 0.1 yoffset -7
    ease 0.1 yoffset 0     

transform enterending6:
    xoffset -10
    yoffset 500
    pause 0.5
    ease 0.3 yoffset -20
    ease 0.2 yoffset 10
    ease 0.1 yoffset -7
    ease 0.1 yoffset 0 

transform enterending7:
    xoffset -10
    yoffset 500
    pause 0.6
    ease 0.3 yoffset -20
    ease 0.2 yoffset 10
    ease 0.1 yoffset -7
    ease 0.1 yoffset 0   

transform enterending8:
    xoffset -10
    yoffset 500
    pause 0.7
    ease 0.3 yoffset -20
    ease 0.2 yoffset 10
    ease 0.1 yoffset -7
    ease 0.1 yoffset 0   
transform enterending9:
    xoffset -10
    yoffset 500
    pause 0.8
    ease 0.3 yoffset -20
    ease 0.2 yoffset 10
    ease 0.1 yoffset -7
    ease 0.1 yoffset 0

transform enterjar:
    xoffset -10
    yoffset 500
    pause 3.4
    ease 0.3 yoffset -20
    ease 0.2 yoffset 10
    ease 0.1 yoffset -7
    ease 0.1 yoffset 0    

transform entersign:
    subpixel True
    alpha 0
    ease 0.3 alpha 1

transform enterendingtoggles:
    xoffset 30
    yoffset -150
    ease 0.5 yoffset 20




screen main_menu():

    
    
    if persistent.end1 and persistent.end2 and persistent.end3 and persistent.end4 and persistent.end5 and persistent.end6 and persistent.end7 and persistent.end8 and persistent.end9:
        $ persistent.got_all_button_endings = True
    else:
        $ persistent.got_all_button_endings = False
    if persistent.aend1 and persistent.aend2 and persistent.aend3 and persistent.aend4 and persistent.aend5:
        $ persistent.got_all_alice_endings = True
    else:
        $ persistent.got_all_alice_endings = False 
    if persistent.send1 and persistent.send2 and persistent.send3 and persistent.send4 and persistent.send5 and persistent.send6 and persistent.send7:
        $ persistent.got_all_sai_endings = True
    else:
        $ persistent.got_all_sai_endings = False

    if persistent.got_all_button_endings and persistent.got_all_alice_endings and persistent.got_all_sai_endings:
        $ persistent.got_all_endings = True
    else:
        $ persistent.got_all_endings = False

    ## This ensures that any other menu screen is replaced.
    tag menu

    if persistent.got_all_button_endings and config.steam_appid == 3807090:
        add "gui/main_menu_items/menu_bg_scroll_completed.png" at scroll
        python:
            achievement.grant("got_all_endings")
            achievement.sync()

    else:    
        add "gui/main_menu_items/menu_bg_scroll.png" at scroll
    add "gui/main_menu_items/menu_folder.png"
    if persistent.got_all_button_endings and config.steam_appid == 3807090:
        add "gui/main_menu_items/menu_title_completed.png" at titleappear
    else:    
        add "gui/main_menu_items/menu_title.png" at titleappear
    add "gui/main_menu_items/menu_menu.png"
    add "gui/main_menu_items/menu_top.png" at entertop
    add "gui/main_menu_items/menu_2ndtop.png" at enter2ndtop
    add "gui/main_menu_items/menu_middle.png" at entermiddle
    add "gui/main_menu_items/menu_2ndbottom.png" at enter2ndbot
    add "gui/main_menu_items/menu_bottom.png" at enterbot
    add "gui/main_menu_items/demo.png"


    # imagebutton at enterjar:
    #     xpos 1200 ypos 100
    #     idle "gui/main_menu_items/completed_jar_idle.png"
    #     hover "gui/main_menu_items/completed_jar_hover.png"
    #     action OpenURL("https://ko-fi.com/trubluis")
    #     focus_mask True



    imagebutton at entersign:
        idle "gui/main_menu_items/sign_idle.png"
        hover "gui/main_menu_items/sign_hover.png"
        hover_sound "audio/SFX/thud.wav"
        yoffset 600
        # action achievement.steam.activate_overlay_to_web_page(url)
        # action OpenURL("https://trubluis.itch.io/grow-a-girlfriend/devlog/666262/grow-a-girlfriend-is-expanding-patreon-launch")
        if achievement.steam is not None:
            action Function(achievement.steam.activate_overlay_to_store,3766830)
        else:
            action OpenURL("https://store.steampowered.com/app/3766830/Grow_a_Girlfriend/")
        focus_mask True     

    if persistent.got_all_button_endings and config.steam_appid == 3807090:
        imagebutton at entergallery:
            xpos 0 ypos 0
            idle "gui/main_menu_items/menu_star_idle.png"
            hover "gui/main_menu_items/menu_star_hover.png"
            hover_sound "audio/SFX/button_hover.wav"
            activate_sound "audio/SFX/plop.wav"
            action [Play("sound", "yay.wav"), ShowMenu("completed")]
            focus_mask True


    
    # testing toggling routes for dif mushrooms:

    # Button
    imagebutton at enterendingtoggles:
        yanchor 0 xanchor 0 xpos 1600 ypos -20
        idle "gui/main_menu_items/button_mini_shroom.png"
        hover "gui/main_menu_items/button_mini_shroom_hovered.png"
        
        # focus_mask True
        # if alice_endings_main_menu == True and sai_endings_main_menu == True:
        #     action [ToggleVariable("alice_endings_main_menu"), ToggleVariable("sai_endings_main_menu"), ToggleVariable("button_endings_main_menu")]
        # elif alice_endings_main_menu == True:
        #     action [ToggleVariable("alice_endings_main_menu"), ToggleVariable("button_endings_main_menu")]
        # elif sai_endings_main_menu == True:
        #     action [ToggleVariable("sai_endings_main_menu"), ToggleVariable("button_endings_main_menu")]
        # else:
        #     action ToggleVariable("button_endings_main_menu")
        
    
    # Alice
    imagebutton at enterendingtoggles:
        yanchor 0 xanchor 0 xpos 1700 ypos -20
        idle "gui/main_menu_items/alice_mini_shroom_locked.png"
    
    # Sai
    imagebutton at enterendingtoggles:
        yanchor 0 xanchor 0 xpos 1780 ypos -20
        idle "gui/main_menu_items/sai_mini_shroom_locked.png"


    # if persistent.button_endcounter >= 1:
    #     $ button_endings_main_menu = True

    
    
    # if button_endings_main_menu:
    if not persistent.end1:
        add "gui/main_menu_items/menu_end1_locked.png" at enterending
    else:
        imagebutton at enterending:
            xoffset 10
            
            idle "gui/main_menu_items/menu_end1_unlocked.png"
            hover "gui/main_menu_items/menu_end1_unlocked_hover.png"
            hover_sound "audio/SFX/button_hover1.wav"
            action Notify("End 1: So mushroom for improvement.")
            focus_mask True

    if not persistent.end2:
        add "gui/main_menu_items/menu_end1_locked.png" at enterending2 xoffset 100
    else:
        imagebutton at enterending2:
            xoffset 100
            idle "gui/main_menu_items/menu_end1_unlocked.png"
            hover "gui/main_menu_items/menu_end1_unlocked_hover.png"
            hover_sound "audio/SFX/button_hover2.wav"
            action Notify("End 2: Mush-room bound.")
            focus_mask True
        #add "gui/main_menu_items/menu_end1_unlocked.png" at enterending2 xoffset 100

    if not persistent.end3:
        add "gui/main_menu_items/menu_end1_locked.png" at enterending3 xoffset 220
    else:
        imagebutton at enterending3:
            xoffset 220
            idle "gui/main_menu_items/menu_end1_unlocked.png"
            hover "gui/main_menu_items/menu_end1_unlocked_hover.png"
            hover_sound "audio/SFX/button_hover3.wav"
            action Notify("End 3: Spore, unfortunate soul.")
            focus_mask True
        #add "gui/main_menu_items/menu_end1_unlocked.png" at enterending3 xoffset 220

    if not persistent.end4:
        add "gui/main_menu_items/menu_end1_locked.png" at enterending4 xoffset 340
    else:
        imagebutton at enterending4:
            xoffset 340
            idle "gui/main_menu_items/menu_end1_unlocked.png"
            hover "gui/main_menu_items/menu_end1_unlocked_hover.png"
            hover_sound "audio/SFX/button_hover4.wav"
            action Notify("End 4: Fast food.")
            focus_mask True
        #add "gui/main_menu_items/menu_end1_unlocked.png" at enterending4 xoffset 340

    if not persistent.end5:
        add "gui/main_menu_items/menu_end1_locked.png" at enterending5 xoffset 460
    else:
        imagebutton at enterending5:
            xoffset 460
            idle "gui/main_menu_items/menu_end1_unlocked.png"
            hover "gui/main_menu_items/menu_end1_unlocked_hover.png"
            hover_sound "audio/SFX/button_hover5.wav"
            action Notify("End 5: That's yummy! No cap.")
            focus_mask True
        #add "gui/main_menu_items/menu_end1_unlocked.png" at enterending5 xoffset 460

    if not persistent.end6:
        add "gui/main_menu_items/menu_end1_locked.png" at enterending6 xoffset 580
    else:
        imagebutton at enterending6:
            xoffset 580
            idle "gui/main_menu_items/menu_end1_unlocked.png"
            hover "gui/main_menu_items/menu_end1_unlocked_hover.png"
            hover_sound "audio/SFX/button_hover6.wav"
            action Notify("End 6:  Goodbye Button, my new friend.")
            focus_mask True
        #add "gui/main_menu_items/menu_end1_unlocked.png" at enterending6 xoffset 580

    if not persistent.end7:
        add "gui/main_menu_items/menu_end1_locked.png" at enterending7 xoffset 700
    else:
        imagebutton at enterending7:
            xoffset 700
            idle "gui/main_menu_items/menu_end1_unlocked.png"
            hover "gui/main_menu_items/menu_end1_unlocked_hover.png"
            hover_sound "audio/SFX/button_hover7.wav"
            action Notify("End 7: I'm sorry.")
            focus_mask True
        #add "gui/main_menu_items/menu_end1_unlocked.png" at enterending7 xoffset 700

    if not persistent.end8:
        add "gui/main_menu_items/menu_end1_locked.png" at enterending8 xoffset 820
    else:
        imagebutton at enterending8:
            xoffset 820
            idle "gui/main_menu_items/menu_end1_unlocked.png"
            hover "gui/main_menu_items/menu_end1_unlocked_hover.png"
            hover_sound "audio/SFX/button_hover8.wav"
            action Notify("End 8: Morel dilemma.")
            focus_mask True
        #add "gui/main_menu_items/menu_end1_unlocked.png" at enterending8 xoffset 820

    if not persistent.end9:
        add "gui/main_menu_items/menu_end1_locked.png" at enterending9 xoffset 940
    else:
        imagebutton at enterending9:
            xoffset 940
            idle "gui/main_menu_items/menu_end1_unlocked.png"
            hover "gui/main_menu_items/menu_end1_unlocked_hover.png"
            hover_sound "audio/SFX/button_hover9.wav"
            action Notify("End 9: Truffled mind.")
            focus_mask True
        #add "gui/main_menu_items/menu_end1_unlocked.png" at enterending9 xoffset 940
                                








    # end test
    
    if renpy.exists("translation_testing.rpy"):
        imagebutton at entergallery:
            xpos 0 ypos 0
            auto "gui/main_menu_items/language_%s.png"
            action ShowMenu("change_language")
            focus_mask True
            hover_sound "audio/SFX/button_hover.wav"
            activate_sound "audio/SFX/plop.wav"
    
    # Translations code end

    imagebutton at entergallery:
        xpos 0 ypos 0
        idle "gui/main_menu_items/menu_gallery_idle.png"
        hover "gui/main_menu_items/menu_gallery_hover.png"
        action ShowMenu("album")
        focus_mask True
        hover_sound "audio/SFX/button_hover.wav"
        activate_sound "audio/SFX/plop.wav"
    text _("{color=#000000}{font=NotoSans-Regular.ttf}{size=30}gallery"):
        xpos 0.465 ypos 0.73


    imagebutton at entergallery:
        xpos 0 ypos 0
        idle "gui/main_menu_items/menu_i_idle.png"
        hover "gui/main_menu_items/menu_i_hover.png"
        action ShowMenu("credits")
        focus_mask True
        hover_sound "audio/SFX/button_hover.wav"
        activate_sound "audio/SFX/plop.wav"
    text _("{color=#000000}{font=NotoSans-Regular.ttf}{size=30}credits"):
        xpos 0.58 ypos 0.73
    
    imagebutton at entergallery:
        focus_mask True
        xpos 0 ypos 0
        idle "gui/main_menu_items/menu_triggers_idle.png"
        hover "gui/main_menu_items/menu_triggers_hover.png"
        action ShowMenu("triggers")
        hover_sound "audio/SFX/button_hover.wav"
        activate_sound "audio/SFX/plop.wav"
    text _("{color=#000000}{font=NotoSans-Regular.ttf}{size=30}content\nwarning"):
        xpos 0.345 ypos 0.71
        

    
        
       
    
    
    


    ## This empty frame darkens the main menu.
    #frame:
    #    style "main_menu_frame"

    ## The use statement includes another screen inside this one. The actual
    ## contents of the main menu are in the navigation screen.
    use navigation

    if persistent.end6:
        if not persistent.displaystockmessageonce: # if false
            add "gui/main_menu_items/menu_bg_scroll.png"
            imagebutton at entergallery:
                idle "images/website/new_stock_message.png"
                hover "images/website/new_stock_message_hover.png"
                action ToggleVariable("persistent.displaystockmessageonce")   # make true so never shown again    

    # if gui.show_name:

    #     vbox:
    #         style "main_menu_vbox"

    #         text "[config.name!t]":
    #             style "main_menu_title"

    #         text "[config.version]":
    #             style "main_menu_version"


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 420
    yfill True

    #background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid".
## This screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0):

    style_prefix "game_menu"

    # if main_menu:
    #     add gui.main_menu_background
    # else:
    #     add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Return"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu
    add "gui/main_menu_items/menu_bg_scroll.png" at scroll
    add "gui/button/save_folder.png"
    use file_slots(_("Save"))


screen load():

    tag menu
    add "gui/main_menu_items/menu_bg_scroll.png" at scroll
    add "gui/button/load_folder.png"
    use file_slots(_("Load"))
        
screen file_slots(title):
    tag menu
    # imagebutton:
    #     idle "gui/main_menu_items/QL_idle.png"
    #     hover "gui/main_menu_items/QL_hover.png"
    #     action QuickLoad()
    #     focus_mask True
    imagebutton:
        idle "gui/main_menu_items/house_idle.png"
        hover "gui/main_menu_items/house_hover.png"
        action MainMenu()
        focus_mask True
    imagebutton:
        xpos -0.005 ypos -0.005
        idle "gui/main_menu_items/gallery_arrow_idle.png"
        hover "gui/main_menu_items/gallery_arrow_hover.png"
        action Return()
        focus_mask True
    imagebutton:
        idle "gui/button/load_idle.png"
        hover "gui/button/load_hover.png"
        activate_sound "audio/SFX/main_menu_SFX2.wav"
        action ShowMenu('load')
        focus_mask True
    
    imagebutton:
        idle "gui/button/help_idle.png"
        hover "gui/button/help_hover.png"
        activate_sound "audio/SFX/main_menu_SFX2.wav"
        action ShowMenu('help')
        focus_mask True        
    imagebutton:
        idle "gui/button/options_idle.png"
        hover "gui/button/options_hover.png"
        activate_sound "audio/SFX/main_menu_SFX2.wav"
        action ShowMenu('preferences')
        focus_mask True            
    
    imagebutton:
        idle "gui/button/save_idle.png"
        hover "gui/button/save_hover.png"
        activate_sound "audio/SFX/main_menu_SFX2.wav"
        action ShowMenu('save')
        focus_mask True        
    
    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    grid 3 2:
        style_prefix "slot"

        xalign 0.5
        yalign 0.75

        spacing 10

        for i in range(6):

            $ slot = i + 1

            button:
                action FileAction(slot)

                has vbox

                add FileScreenshot(slot) xalign 0.5

                text FileTime(slot, format=_("{#file_time}%B %d %Y, %H:%M")):
                    ypos 30
                    style "slot_time_text"

                text FileSaveName(slot):
                    style "slot_name_text"

                key "save_delete" action FileDelete(slot)

            
                imagebutton:
                    xpos 320 ypos -285
                    idle "gui/button/cross.png"
                    hover "gui/button/cross_hover.png"
                    action FileDelete(slot)
                    focus_mask True

    # Buttons to access other pages.
    vbox:
        style_prefix "page"

        xalign 0.5
        yalign 0.97

        hbox:
            xalign 0.5

            spacing gui.page_spacing

            

            ## range(1, 10) gives the numbers from 1 to 9.
            for page in range(1, 10):
                textbutton "[page]" action FilePage(page)

         

 
style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.button_text_properties("slot_button")


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():
    
    tag menu
    add "gui/main_menu_items/menu_bg_scroll.png" at scroll
    add "gui/button/options_folder.png"
    imagebutton:
        idle "gui/main_menu_items/house_idle.png"
        hover "gui/main_menu_items/house_hover.png"
        action MainMenu()
        focus_mask True
    imagebutton:
        xpos -0.005 ypos -0.005
        idle "gui/main_menu_items/gallery_arrow_idle.png"
        hover "gui/main_menu_items/gallery_arrow_hover.png"
        action Return()
        focus_mask True
    imagebutton:
        idle "gui/button/load_idle.png"
        hover "gui/button/load_hover.png"
        activate_sound "audio/SFX/main_menu_SFX2.wav"
        action ShowMenu('load')
        focus_mask True
    
    imagebutton:
        idle "gui/button/help_idle.png"
        hover "gui/button/help_hover.png"
        activate_sound "audio/SFX/main_menu_SFX2.wav"
        action ShowMenu('help')
        focus_mask True        
    imagebutton:
        idle "gui/button/options_idle.png"
        hover "gui/button/options_hover.png"
        activate_sound "audio/SFX/main_menu_SFX2.wav"
        action ShowMenu('preferences')
        focus_mask True            
    
    imagebutton:
        idle "gui/button/save_idle.png"
        hover "gui/button/save_hover.png"
        activate_sound "audio/SFX/main_menu_SFX2.wav"
        action ShowMenu('save')
        focus_mask True        



    #use game_menu(_("Options"), scroll="viewport"):



    hbox:
        pos (0.13, 0.28) anchor (0.0, 0.0)
        box_wrap True
        spacing 70
        
        if renpy.variant("pc") or renpy.variant("web"):
            
            vbox:
                spacing 30
                vbox:
                    style_prefix "radio"
                    label _("Display")
                    textbutton _("Window") action Preference("display", "window")
                    textbutton _("Fullscreen") action Preference("display", "fullscreen")
                
                # label _("Textbox")
                # textbutton _("Opaque") action ToggleVariable("theBox", "gui/textbox_opaq.png")
                # textbutton _("Transparent") action ToggleVariable("theBox", "gui/textbox_trans.png")

                vbox:
                    label _('Content Warnings')
                    
                    textbutton _('Alert on') action ToggleVariable("persistent.warning")
                vbox:
                    label _('Danger zone') 
                    textbutton _('Delete saves') action Confirm(_("Are you sure you want to delete all your save files and progress?\nThis action cannot be undone.\nNotice: The game will relaunch if you click \"Yes\"!"), Function(reset_data))
                

        vbox:
            style_prefix "check"
            label _("Skip")
            textbutton _("Unseen Text") action Preference("skip", "toggle")
            textbutton _("After Choices") action Preference("after choices", "toggle")
            textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

            label _('Cursor Style')
            textbutton _('System') action Preference('system cursor', 'enable')
            textbutton _('Custom') action Preference('system cursor', 'disable')

            

        ## Additional vboxes of type "radio_pref" or "check_pref" can be
        ## added here, to add additional creator-defined preferences.

    null height (4 * gui.pref_spacing)

    vbox:
        pos (0.6, 0.28) anchor (0.0, 0.0)
        style_prefix "slider"
        box_wrap True
          
        

        vbox:

            label _("Text Speed")

            bar value Preference("text speed")

            label _("Auto-Forward Time")

            bar value Preference("auto-forward time")

        vbox:

            
            label _("Music Volume")

            hbox:
                bar value Preference("music volume")

            if config.has_sound:

                label _("Sound Volume")

                hbox:
                    bar value Preference("sound volume")

                    if config.sample_sound:
                        textbutton _("Test") action Play("sound", config.sample_sound)


            if config.has_voice:
                label _("Voice Volume")

                hbox:
                    bar value Preference("voice volume")

                    if config.sample_voice:
                        textbutton _("Test") action Play("voice", config.sample_voice)
            if config.has_music or config.has_sound or config.has_voice:
                null height gui.pref_spacing

                textbutton _("Mute All"):
                    action Preference("all mute", "toggle")
                    style "mute_all_button"
    
    # vbox:
    #     style_prefix "radio"
    #     label _("Languages")

    #     textbutton _("English") action Language(None)

    #     for lang in get_available_translations():
    #         textbutton _(f"{lang.capitalize()}") action Language(lang)

    #     text "{size=-15}Place translations in directory game/tl"
        
            


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.button_text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.button_text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.button_text_properties("slider_button")

style slider_vbox:
    xsize 675


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    
    imagebutton:
        xpos -0.005 ypos -0.005
        idle "gui/main_menu_items/gallery_arrow_idle.png"
        hover "gui/main_menu_items/gallery_arrow_hover.png"
        action Return()
        focus_mask True

    ## Avoid predicting this screen, as it can be very large.
    predict False

    frame:
        style_prefix "history"
        background Frame("gui/history2.png")
        xmargin 200
        ymargin 50
        # xpadding 150
        top_padding 230
        bottom_padding 120
        vpgrid:
            yinitial 1.0
            cols 1
            draggable True
            mousewheel True
            scrollbars "vertical" 


            vbox:
                for h in _history_list:

                    window:

                        ## This lays things out properly if history_height is None.
                        has fixed:
                            yfit True

                        if h.who:

                            label h.who:
                                style "history_name"
                                substitute False

                                ## Take the color of the who text from the Character, if
                                ## set.
                                if "color" in h.who_args:
                                    text_color h.who_args["color"]

                        $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                        text what:
                            substitute False

                if not _history_list:
                    label _("The dialogue history is empty.")
        
# History screen backup
# screen history():

#     tag menu

#     add "gui/history.png"
    
#     imagebutton:
#         xpos -0.005 ypos -0.005
#         idle "gui/main_menu_items/gallery_arrow_idle.png"
#         hover "gui/main_menu_items/gallery_arrow_hover.png"
#         action Return()
#         focus_mask True

#     ## Avoid predicting this screen, as it can be very large.
#     predict False

#     use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0):

#         style_prefix "history"

#         for h in _history_list:

#             window:

#                 ## This lays things out properly if history_height is None.
#                 has fixed:
#                     yfit True

#                 if h.who:

#                     label h.who:
#                         style "history_name"
#                         substitute False

#                         ## Take the color of the who text from the Character, if
#                         ## set.
#                         if "color" in h.who_args:
#                             text_color h.who_args["color"]

#                 $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
#                 text what:
#                     substitute False

#         if not _history_list:
#             label _("The dialogue history is empty.")


## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen help():

    tag menu
    add "gui/main_menu_items/menu_bg_scroll.png" at scroll
    add "gui/button/help_folder.png"
    imagebutton:
        idle "gui/main_menu_items/house_idle.png"
        hover "gui/main_menu_items/house_hover.png"
        action MainMenu()
        focus_mask True
    imagebutton:
        xpos -0.005 ypos -0.005
        idle "gui/main_menu_items/gallery_arrow_idle.png"
        hover "gui/main_menu_items/gallery_arrow_hover.png"
        action Return()
        focus_mask True
    imagebutton:
        idle "gui/button/load_idle.png"
        hover "gui/button/load_hover.png"
        action ShowMenu('load')
        focus_mask True
    
    imagebutton:
        idle "gui/button/help_idle.png"
        hover "gui/button/help_hover.png"
        action ShowMenu('help')
        focus_mask True        
    imagebutton:
        idle "gui/button/options_idle.png"
        hover "gui/button/options_hover.png"
        action ShowMenu('preferences')
        focus_mask True            
    
    imagebutton:
        idle "gui/button/save_idle.png"
        hover "gui/button/save_hover.png"
        action ShowMenu('save')
        focus_mask True        
    
    use keyboard_help
    

    # default device = "keyboard"

    # use game_menu(_("Help"), scroll="viewport"):

    #     style_prefix "help"

    #     vbox:
    #         spacing 23

    #         hbox:

    #             textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
    #             textbutton _("Mouse") action SetScreenVariable("device", "mouse")

    #             if GamepadExists():
    #                 textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

    #         if device == "keyboard":
    #           use keyboard_help
            # elif device == "mouse":
            #     use mouse_help
            # elif device == "gamepad":
            #     use gamepad_help


screen keyboard_help():
    
    vbox:
        style_prefix "help"
        xalign 0.3 yalign 0.7
        hbox:
            label _("Enter/Space")
            text _("Advances text.")

        hbox:
            label _("Escape/Right click")
            text _("Accesses the game menu.")

        hbox:
            label _("Tab/Ctrl")
            text _("Skip.")

        hbox:
            label _("Scroll/Page Up")
            text _("Rolls back to earlier dialogue.")

        hbox:
            label "V"
            text _("Toggles assistive voicing.")

        hbox:
            label _("H/Middle click")
            text _("Hide user interface.")

        hbox:
            label "Shift+A"
            text _("Opens the accessibility menu.")




style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 20

style help_button_text:

    bottom_padding 20
    properties gui.button_text_properties("help_button")

style help_label:
    xsize 500
    bottom_padding 20
    right_padding 59

style help_label_text:
    size gui.text_size
    xalign 0
    textalign 1.0
    bottom_padding 20


################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.button_text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


# screen nvl(dialogue, items=None):

#     window:
#         style "nvl_window"

#         has vbox:
#             spacing gui.nvl_spacing

#         ## Displays dialogue in either a vpgrid or the vbox.
#         if gui.nvl_height:

#             vpgrid:
#                 cols 1
#                 yinitial 1.0

#                 use nvl_dialogue(dialogue)

#         else:

#             use nvl_dialogue(dialogue)

#         ## Displays the menu, if given. The menu may be displayed incorrectly if
#         ## config.narrator_menu is set to True.
#         for i in items:

#             textbutton i.caption:
#                 action i.action
#                 style "nvl_button"

#     add SideImage() xalign 0.0 yalign 1.0

# PHONE TEXT ----
screen nvl(dialogue, items=None):      #### ADD THIS TO MAKE THE PHONE WORK!! :) ###
    if nvl_mode == "phone":
        use PhoneDialogue(dialogue, items)
    else:
    ####
    ## Indent the rest of the screen
        window:
            style "nvl_window"
            # ...
# -----



screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")


## Bubble screen ###############################################################
##
## The bubble screen is used to display dialogue to the player when using speech
## bubbles. The bubble screen takes the same parameters as the say screen, must
## create a displayable with the id of "what", and can create displayables with
## the "namebox", "who", and "window" ids.
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Since a mouse may not be present, we replace the quick menu with a version
## that uses fewer and bigger buttons that are easier to touch.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            textbutton _("Back") action Rollback()
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menu") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign 0.5
    yalign 0.3
    size 60

# def updatefont():
#     if preferences.language is None:
#         style say_label:
#             properties gui.text_properties("name", accent=True)
#             xalign 0.5
#             yalign 0.3
#             size 60
            
#     else:
#         style say_label:
#             properties gui.text_properties("name", accent=True)
#             xalign 0.5
#             yalign 0.3
#             size 30