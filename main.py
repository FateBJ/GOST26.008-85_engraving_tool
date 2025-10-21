##VARIABLE SECTION##
output=str('') #Output file text
mode=0 #mode. 0 - engraving, 1 - drawing
h=16 #font high in mm
origin=0 #position of the origin. 0 - bottom-center, 1 - bottom-left, 2 - bottom-right, 3 - center, 4 - center-left, 5 - center-right, 6 - upper-center, 7 - upper-left 8 - upper-right
talign=0 #type of aligning. 0 - center, 1 - left, 2 - right.
zdepth=-0.1 #z-depth. It uses negative numbers
shigh=1 #safe high Z mm
cspeed=100 #cutting/drawing moves speed
fspeed=3000 #free movement speed
spindel=25000 #spindel rotation speed RPM
xpos=0
ypos=0
zpos=10
text=''
##FETHING THE PARAMETERS##

def input_params(mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text):

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
    if again=="Y" or again=="y": return (mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text)
    else: mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text=input_params(mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text)
    return (mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text)

#mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text=input_params(mode,h,origin,talign,zdepth,shigh,cspeed,fspeed,spindel,text)

##VALIDATION##

#placeholder#

#DEBUG
def cut(xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth): #Cutting stroke
    global output
    output += "G01 X"+str(xpos)+" Y"+str(ypos)+" Z" + str(zpos)+" F"+str(cspeed)+'\n'
    return(output)
def move(xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth): #Free movement stroke
    global output
    output += "G00 X" + str(xpos) + " Y" + str(ypos) + " Z" + str(zpos) + " F" + str(fspeed)+'\n'
    return(output)
########################################################################################################################
def latA(xpos,ypos,shigh,h,fspeed,cspeed,zdepth):
    global output
    K=h/16
    zpos=shigh
    startxpos=xpos
    startypos=ypos

    #1
    xpos+=(8*K)-(11.8*K)/2
    ypos+=10*K
    move(xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth)
    #2#
    zpos=zdepth
    cut(xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth)
    #3
    xpos+=(11.8*K)/2-(0.5*K)/2
    ypos+=13.9*K
    cut(xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth)
    #4
    xpos+=0.5*K
    cut(xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth)
    #5
    xpos += (11.8 * K) / 2 - (0.5 * K) / 2
    ypos -= 13.9 * K
    cut(xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth)
    #6
    zpos=shigh
    move(xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth)
    #7
    xpos-=11.8*K
    xpos+=(11.8*K-(2*3.7*K-11.8*K))/2
    ypos+=3.7*K
    move(xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth)
    #8
    zpos=zdepth
    cut(xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth)
    #9
    xpos+=2*3.7*K-11.8*K
    cut(xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth)
    #10
    zpos=shigh
    move(xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth)
    #11
    xpos=startxpos+16*K
    ypos=startypos
    move(xpos,ypos,zpos,shigh,h,fspeed,cspeed,zdepth)
    return (xpos,ypos)
########################################################################################################################

output+='G90 G94 G91.1 G40 G49 G17\nG21\nG28 G91 Z0.\nG90\nT3 M6\nS'
output+=str(spindel)
output+=' M3\nG17 G90 G94\nG54\n'

xpos,ypos=latA(xpos,ypos,shigh,h,fspeed,cspeed,zdepth)
print (output)
print(xpos,ypos,zpos)