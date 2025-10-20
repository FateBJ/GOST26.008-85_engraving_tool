##VARIABLE SECTION##

mode=0 #mode. 0 - engraving, 1 - drawing
h=16 #font high in mm
origin=0 #position of the origin. 0 - bottom-center, 1 - bottom-left, 2 - bottom-right, 3 - center, 4 - center-left, 5 - center-right, 6 - upper-center, 7 - upper-left 8 - upper-right
talign=0 #type of aligning. 0 - center, 1 - left, 2 - right.
zdepth=-0.1 #z-depth. It uses negative numbers
shigh=1 #safe high Z mm
cspeed=100 #cutting/drawing moves speed
fspeed=3000 #free movement speed
spindel=25000 #spindel rotation speed RPM

##FETHING THE PARAMETERS##

def input_params():
    global mode
    global h
    global origin
    global talign
    global zdepth
    global shigh
    global cspeed
    global fspeed
    global spindel
    global text
    mode=int (input("Choose the mode.\n\n0-engraving\n1-drawing\n\n"))
    if mode!=1: mode=0
    h=float (input("Enter the high of the font.\n\n"))
    origin=int (input("Choose the anchor pont of the text box\n0 - bottom-center\n1 - bottom-left\n2 - bottom-right\n3 - center\n4 - middle-left\n5 - middle-right\n6 - upper-center\n7 - upper-left\n8 - upper-right\n"))
    talign=int (input("Aligning:\n0-center\n1-left\n2-right\n"))
    zdepth=float (input("Enter the z-depth\n-"))
    zdepth=0-zdepth
    shigh=float (input("Enter the safe high\n"))
    cspeed=int (input("Enter the speed of cutting/drawing\n"))
    fspeed=int (input("Enter the speed of free movements\n"))
    if mode==0: spindel=int (input("Enter the spindle rotation speed\n"))
    text=str (input("Enter the text\n"))

##ENSURING##

    print ("Mode: ")
    if mode==0: print("engraving\n")
    if mode==1: print("drawing\n")
    print("Text high: "+str(h)+"mm\n"+"Origin pont: ")
    if origin==0: print("bottom-center\n")
    if origin==1: print("bottom-left\n")
    if origin==2: print("bottom-right\n")
    if origin==3: print("center\n")
    if origin==4: print("middle-left\n")
    if origin==5: print("middle-right\n")
    if origin==6: print("upper-center\n")
    if origin==7: print("upper-left\n")
    if origin==8: print("upper-right\n")
    print("Text aligning: ")
    if talign==0: print("centered\n")
    if talign==1: print("to left\n")
    if talign==2: print("to right\n")
    print("Z-depth: "+str(zdepth)+"mm \nSafe high: "+str(shigh)+"mm \nCutting speed: "+str(cspeed)+"mm/min\nFree movement speed: "+str(fspeed)+"mm/min\n")
    if mode==0: print("Spindle speed: "+str(cspeed)+" RPM\n"+"Text: "+text+"\n")
    again=input("Is that correct? Y/N\n")
    if again=="Y" or again=="y": return ()
    else: input_params()
    return ()
input_params()

##VALIDATION##

#placeholder#

