def cut(): #Cutting stroke
    global xpos
    global ypos
    global zpos
    global shigh
    global h
    global cspeed
    global fspeed
    global zdepth
    global output
    output += "G01 X"+str(xpos)+" Y"+str(ypos)+" Z" + str(zpos)+" F"+str(cspeed)
    return()
def move(): #Free movement stroke
    global xpos
    global ypos
    global zpos
    global shigh
    global h
    global cspeed
    global fspeed
    global zdepth
    global output
    output += "G00 X" + str(xpos) + " Y" + str(ypos) + " Z" + str(zpos) + " F" + str(fspeed)
    return()
def main():
    ##VAR SECTION##
    global xpos
    global ypos
    global zpos
    global shigh
    global h
    global cspeed
    global fspeed
    global zdepth
    global output
    K=h/16
    zpos=shigh
    startxpos=xpos
    startypos=ypos

    #1
    xpos+=(8*K)-(11.8*K)/2
    ypos+=10*K
    move()
    #2#
    zpos=zdepth
    cut()
    #3
    xpos+=(11.8*K)/2-(0.5*K)/2
    ypos+=13.9*K
    cut()
    #4
    xpos+=0.5*K
    cut()
    #5
    xpos += (11.8 * K) / 2 - (0.5 * K) / 2
    ypos -= 13.9 * K
    cut()
    #6
    zpos=shigh
    move()
    #7
    xpos-=11.8*K
    xpos+=(11.8*K-(2*3.7*K-11.8*K))/2
    ypos+=3.7*K
    move()
    #8
    zpos=zdepth
    cut()
    #9
    xpos+=2*3.7*K-11.8*K
    cut()
    #10
    zpos=shigh
    move()
    #11
    xpos=startxpos+16*K
    ypos=startypos
    move()
    return (16*K)
