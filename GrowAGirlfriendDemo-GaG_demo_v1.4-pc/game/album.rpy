transform gallery_thumbnail_hover:
    matrixcolor TintMatrix("#cf84bb")
    on hover:
        linear 0.2 matrixcolor TintMatrix("#ffffff")
    on idle:
        linear 0.2 matrixcolor TintMatrix("#cf84bb")

transform halfzoom:
    subpixel True
    truecenter zoom 0.5

transform halfzoom:
    subpixel True
    truecenter zoom 0.5


transform halfthere:
    alpha 0.8

init python:
    

    gallery=Gallery()
    
    gallery.button("drawing")
    gallery.image("images/instructions/button_drawing.png")
    gallery.condition("persistent.end6")

    gallery.button("depression")
    gallery.image("images/bg/depression/depression_manicalsmile.png", "images/bg/depression/fog_base.png")
    gallery.condition("persistent.buttondepression1")
    gallery.image("images/bg/depression/depression_annoyed.png", "images/bg/depression/fog_base.png", "images/bg/depression/fog_1.png")
    gallery.condition("persistent.buttondepression2")
    gallery.image("images/bg/depression/depression_annoyed2.png","images/bg/depression/fog_base.png", "images/bg/depression/fog_1.png")
    gallery.condition("persistent.buttondepression3")
    gallery.image("images/bg/depression/depression_sad.png", "images/bg/depression/fog_base.png", "images/bg/depression/fog_1.png")
    gallery.condition("persistent.buttondepression4")
    gallery.image("images/bg/depression/depression_vsad.png", "images/bg/depression/fog_base.png", "images/bg/depression/fog_1.png","images/bg/depression/fog_2.png")
    gallery.condition("persistent.buttondepression5")
    gallery.image("images/bg/depression/depression_vvsad.png", "images/bg/depression/fog_base.png", "images/bg/depression/fog_1.png","images/bg/depression/fog_2.png")
    gallery.condition("persistent.buttondepression6")
    gallery.image("images/bg/depression/depression_vvsad_red.png",  "images/bg/depression/fog_base.png", "images/bg/depression/fog_1.png","images/bg/depression/fog_2.png", "images/bg/depression/fog_3.png")
    gallery.condition("persistent.buttondepression7")
    gallery.image("images/bg/depression/depression_gratefulsmile.png","images/bg/depression/glow.png")
    gallery.condition("persistent.buttondepression8")

    gallery.button("beach")
    gallery.image("images/bg/beach_sunset.png","images/bg/beachkiss 1.png")
    gallery.transform(halfzoom, halfzoom)
    gallery.condition("persistent.buttonbeach1")
    gallery.image("images/bg/beach_sunset.png","images/bg/beachkiss 2.png")
    gallery.transform(halfzoom, halfzoom)
    gallery.condition("persistent.buttonbeach2")

    gallery.button("button_beheading")
    gallery.image("images/bg/Eat Button/button_eat still.png")
    gallery.condition("persistent.dismmember_1")
    gallery.image("images/bg/Eat Button/button_eat together.png")
    gallery.condition("persistent.dismmember_2")
    gallery.image("images/bg/Eat Button/body_dismembered.png","images/bg/Eat Button/head_float.png")
    gallery.condition("persistent.dismmember_3")

    
screen album:

    tag menu
    add "gui/main_menu_items/menu_bg_scroll.png" at scroll
    add "gui/main_menu_items/gallery_folder.png"
    imagebutton:
        xpos 0 ypos 0
        idle "gui/main_menu_items/gallery_arrow_idle.png"
        hover "gui/main_menu_items/gallery_arrow_hover.png"
        action ShowMenu("main_menu")
        focus_mask True

    hbox at entergallery:
       
        xalign 0.5
        ypos 0.37
        spacing 30
        grid 2 2:
            add gallery.make_button(name="drawing", unlocked = "images/instructions/small_drawing.png", locked = "gui/button/locked.png") at gallery_thumbnail_hover
            add gallery.make_button(name="depression", unlocked = "images/instructions/small_depression.png", locked = "gui/button/locked.png") at gallery_thumbnail_hover
            add gallery.make_button(name="beach", unlocked = "images/instructions/small_beach.png", locked = "gui/button/locked.png") at gallery_thumbnail_hover
            add gallery.make_button(name="button_beheading", unlocked = "images/instructions/small_behead.png", locked = "gui/button/locked.png") at gallery_thumbnail_hover

    
   
screen credits:
    tag menu
    add "gui/main_menu_items/menu_bg_scroll.png" at scroll
    add "gui/main_menu_items/credits_folder.png" at folderappear

    imagebutton:
        xpos 0 ypos 0
        idle "gui/main_menu_items/gallery_arrow_idle.png"
        hover "gui/main_menu_items/gallery_arrow_hover.png"
        action ShowMenu("main_menu")
        focus_mask True
    imagebutton:
        xpos 0 ypos 0
        idle "gui/main_menu_items/credits/onurubu_idle.png" at folderappear

        hover "gui/main_menu_items/credits/onurubu_hover.png"
        action OpenURL("https://twitter.com/onurubu")
        focus_mask True   
    imagebutton:
        xpos 0 ypos 0
        idle "gui/main_menu_items/credits/yaeba_idle.png" at folderappear

        hover "gui/main_menu_items/credits/yaeba_hover.png"
        action OpenURL("https://twitter.com/YaebaFang")
        focus_mask True        
    imagebutton:
        xpos 0 ypos 0
        idle "gui/main_menu_items/credits/trubluIs_idle.png" at folderappear

        hover "gui/main_menu_items/credits/trubluIs_hover.png"
        action OpenURL("https://twitter.com/trubluIs")
        focus_mask True

   

screen triggers:
    tag menu
    add "gui/main_menu_items/menu_bg_scroll.png" at scroll
    add "gui/main_menu_items/triggers_folder.png"
    add "gui/frame.png":
        subpixel True
        zoom 0.75
        pos (0.5, 0.5) anchor (0.0, 0.0)
    text _("You can enable alerts with descriptive warnings in the options menu!"):
        pos (0.53, 0.52) anchor (0.0, 0.0)
        xmaximum 600
        style_prefix "help"
        color "#6B1963"
    imagebutton:
        xpos 0 ypos 0
        idle "gui/main_menu_items/gallery_arrow_idle.png"
        hover "gui/main_menu_items/gallery_arrow_hover.png"
        action ShowMenu("main_menu")
        focus_mask True

    vbox:
        spacing 25
        style_prefix "help"
        pos (0.12, 0.35) anchor (0.0, 0.0)
        
        hbox:
            text _("This game contains discussions and depictions of topics which some may find unsettling:") xmaximum 1400 
            

        vbox:
            spacing 25
            text _("Anxiety")
            text _("Depression")
            text _("Self-harm/Suicide")

screen completed:
    tag menu
    add "gui/main_menu_items/menu_bg_scroll_completed.png" at scroll
    add "gui/main_menu_items/completed_message.png" at folderappear

    imagebutton:
        xpos 0 ypos 0
        idle "gui/main_menu_items/gallery_arrow_idle.png"
        hover "gui/main_menu_items/gallery_arrow_hover.png"
        action ShowMenu("main_menu")
        focus_mask True
    imagebutton at entergallery:
        xpos 1000 ypos -500
        idle "gui/main_menu_items/completed_jar_idle.png"
        hover "gui/main_menu_items/completed_jar_hover.png"
        action OpenURL("https://ko-fi.com/trubluis")
        focus_mask True    
    imagebutton at entergallery:
        ypos 0
        idle "gui/main_menu_items/itchio_idle.png"
        hover "gui/main_menu_items/itchio_hover.png"
        action OpenURL("https://www.patreon.com/c/trubluIs")
        focus_mask True        
    imagebutton at entergallery:
        xpos 230 ypos -10
        idle "gui/main_menu_items/x_idle.png"
        hover "gui/main_menu_items/x_hover.png"
        action OpenURL("https://twitter.com/trubluIs")
        focus_mask True   
    
