# ------------------------ Global Variables
varInputXpos = 270;
unitsXpos = 370;
wrapLength = 250;
btnFramePadX = 470;
btnFramePadY = 10;

# Read default var
numOfVar = 12; defaultVar = []; defaultVarIndex = 0
f = open("./Setup.txt", "r");
for i in range(numOfVar):
    var = f.readline().split()
    defaultVar.append(var[0])
f.close()

# ------------------------ Frame, Varialbes ------------------------
## varialbes 
pos_y = 10
hlt = 1
hlbgNormal = "black" # Background -> normal state, not clicked
hlCAllowed = "green" 
hlCNotAllowed = "red" 

## Functions
def updateYposAndIndex(degree=30):
    global pos_y;
    global defaultVarIndex
    pos_y += degree; 
    defaultVarIndex +=1;
    return pos_y, defaultVarIndex
    
