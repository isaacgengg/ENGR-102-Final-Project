# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Ethan Choo c0808614@tamu.edu
#               Andrew Zheng boostme@tamu.edu
#               Isaac Geng isaacgeng@tamu.edu
#               Justein Hernadez jus.her457@tamu.edu
# Section:      564
# Assignment:   SELF DRIVING CAR PROJECT
# Date:         12 / 6 / 2022
#
#   1. Our first objective was to outline our project and plan out the
#      different types of functions/hierachy of the program
#   2. Our second objective was to program the GUI and debug it until it worked   
#   3. Next, we began parsing through the desired file to split it into
#      distances and directions 
#   4. Next objective, was to transform those distances and directions into the
#      turtle visualizer so that we could plot our directions
#   5. Lastly we debugged the program to clear up the edge cases, and ensure
#      that the program could execute smoothly and as intended
#

import PySimpleGUI as sg
import csv
import turtle
import numpy as np
import conversion

class directionFollower():   
    global info
    global distances
    global units 
    global words 
    global directions
    
    info = []
    distances = []
    units = []
    words = []
    directions = [] 
    turtle.Screen().bgcolor("green")
     
    def __init__(self):
        '''
        Description
        -----------
        Initializes variables (CONSTRUCTOR)

        Returns
        -------
        None.
        
        Written by : Justein Hernadez
        '''
        self.tr = turtle.Turtle()
        self.wn = turtle.Screen()
        self.wn.addshape('train.gif')
        self.tr.shape('train.gif')
        
    def resetVariables(self):
        '''
        Description
        -----------
        Resets all the lists for when rerunning each of the buttons

        Returns
        -------
        None.
        
        Written by : Justein Hernadez 
        '''
        info.clear()
        distances.clear()
        units.clear()
        words.clear()
        directions.clear()
    
    def turtlemove(self, feet, direction):
        '''
        Description
        -----------
        This function takes distance in feet and direction ranging from 0-6
        and moves the turtle accordingly. The turtle may left or right or
        turn towards a specific direction.
        Parameters
        ----------
        feet : FLOAT
        direction : INT 
        Returns
        -------
        None.
        
        Written by : Ethan Choo
        '''
        if direction == 1:
            self.tr.right(90)
        elif direction == 2:
            self.tr.left(90)
        elif direction == 3:
            self.tr.setheading(45)
        elif direction == 4:
            self.tr.setheading(135)
        elif direction == 5:
            self.tr.setheading(315)
        elif direction == 6:
            self.tr.setheading(225)
        feet /= 180
        self.tr.fd(feet)
    
    def cardrive(self):
        '''
        Description
        -----------
        This function reads the 'distance' list and the 'directions' list
        and passes these values onto the 'turtlemove' function. It accounts
        for the different ways in which information is ordered.
        Returns 
        -------
        None.
        
        Written by : Ethan Choo
        '''
        self.tr.clear()
        self.tr.home()
        print(f'{directionlist[0]}\n')  
        for command in range(len(distances)):
            try:
                print(directionlist[command+1],end="\n\n")
            except:
                print()
            if distances[command][1] != "min":
                if distances[command][1] == "mi":
                    self.turtlemove(conversion.convertmiles(float(distances[command][0])),int(directions[command]))
                else:
                    self.turtlemove(float(distances[command][0]),int(directions[command]))
            if len(distances[command]) == 4:
                if distances[command][3] == "mi)":
                    self.turtlemove(conversion.convertmiles(float(distances[command][2][1:])),int(directions[command]))
                else: 
                    self.turtlemove(float(distances[command][2][1:]),int(directions[command]))

    def gui(self):
        '''
        Description
        -----------
        Overall method to show to GUI display
        Returns
        -------
        None
        
        Written by : Andrew Zheng and Isaac Geng
        '''
        layout = [[sg.Text("What file do you want to run?", (30, 1))],
                  [sg.Button("STOP")],
                  [sg.Button("Easterwood2Coulter.txt")],
                  [sg.Button("Kyle2VetPk.txt")],
                  [sg.Button("Zach2StJo.txt")]]

        window = sg.Window("Map", layout)

        def file_reader(file_name):
            '''
            Description
            -----------
            
            Parameters
            ----------
            file_name : TYPE
                DESCRIPTION.

            Returns
            -------
            None.
            
            Written by : Andrew Zheng
            '''
            with open(file_name, 'r') as data_file:
                values = csv.reader(data_file, delimiter=' ')
                for value in values:
                    info.append(value)

                for i in range(len(info)):
                     if 0 < len(info[i]) <= 4 and (len(info[i][0]) < 4) and \
                            ('right' not in info[0]) and ('left' not in info[0]):
                        distances.append(info[i])

                global directions
                directions = infoToTurns(info)
        
        def getdirections(file_name):
            '''
            Description
            -----------
            Converts the file and returns a list of lines
            Parameters
            ----------
            file_name : STRING
            Returns
            -------
            lines : LIST
            
            Written by : Isaac Geng
            '''
            data_file = open(file_name,"r")
            lines = data_file.read().split("\n\n")
            return lines
        
        def infoToTurns(info):
            '''
            Description
            -----------
            Takes in a list and parses through converting directions into
            their key value pairs to encode turning instructions
            Parameters
            ----------
            info : LIST
            Returns
            -------
            directions : LIST
            
            Written by : Isaac Geng
            '''
            
            words = []
            directionDict = {'Continue': 0,
                              'Forward': 0,
                             'Follow': 0,
                             'Drive': 0,
                             'Take':0,
                             'right': 1,
                             'left': 2,
                             'northeast': 3,
                             'northwest':4,
                             'southeast':5,
                             'southwest':6
                             }
            i = 0
            if len(info[0]) > 4:
                words.append(info[0])
            for eachLine in info:
                if eachLine == []:
                    # words.append(inf)
                    words.append(info[i+1])
                i += 1
            i = 0
            for eachLine in words:
                for eachWord in eachLine:
                    if eachWord in directionDict:
                        directions.append(directionDict.get(eachWord))
                        break

                    if eachWord == 'Slight':
                        if eachLine[i + 1] == 'right':
                            directions.append(10)
                        elif eachLine[i + 1] == 'left':
                            directions.append(11)
            return directions
        
        selfState = True
        while selfState:
            event, values = window.read()
            global directionlist
            if event == "STOP" or event == sg.WIN_CLOSED:
                window.close()
                turtle.bye()
                selfState = False      
            elif event == "Easterwood2Coulter.txt":
                self.resetVariables()
                file_reader("Easterwood2Coulter.txt")
                directionlist = getdirections("Easterwood2Coulter.txt")
                self.tr.penup()
                self.tr.home()
                self.tr.pendown()
                self.cardrive()
                turtle.done()
            elif event == "Kyle2VetPk.txt":
                self.resetVariables()
                file_reader("Kyle2VetPk.txt")
                directionlist = getdirections("Kyle2VetPk.txt")
                self.tr.penup()
                self.tr.home()
                self.tr.pendown()
                self.cardrive()
                turtle.done()                           
            elif event == "Zach2StJo.txt":
                self.resetVariables()
                file_reader("Zach2StJo.txt")    
                directionlist = getdirections("Zach2StJo.txt")
                self.tr.penup()
                self.tr.home()
                self.tr.pendown()
                self.cardrive()
                turtle.done()

def main():
    '''
    Description
    -----------
    Main method to run the code 
    Returns
    -------
    None.

    Written by : Justein Hernadez
    '''
    test = directionFollower()
    test.gui()
    
main()


 
