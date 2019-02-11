import random
import time
import curses
import sys
sys.__stdout__ = sys.stdout
stdscr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
iteration = 0
possGenes = ["H+","H-","E+","E-","F+","F-","NG","NG"]
listOfBeings = []
class Tamagotchi:
    def __init__(self, lifeExpectancy,genes,sex):
        self.dots={}
        self.iteration = iteration
        self.sex = sex 
        self.dead = False
        self.genes = genes
        self.lifeExpectancy = lifeExpectancy
        self.age = 0
        self.happiness = 100
        self.health = 100
        self.food = 100
        self.energy = 100
        self.clean = 100
        self.awake = True
        self.pregnant = False
        self.poop = 0
        self.meals = 0
        self.treats = 0
        ## Checks Genes
        for gene in self.genes:
            if gene == "H+":
                self.health += random.randint(1,15)
            elif gene == "H-":
                self.health -= random.randint(1,15)
            elif gene == "E+":
                self.energy += random.randint(1,15)
            elif gene == "E-":
                self.energy -= random.randint(1,15)
            elif gene == "F+":
                self.food += random.randint(1,15)
            elif gene == "F-":
                self.food -= random.randint(1,15)
            else:
                ##print(gene)
                pass
    def pregnantCheck(self):
        if self.sex == "F":
            if self.age > 25 and self.age < 45:
                if self.pregnant == False:
                    pregnantCheck = random.randint(1,8)
                    if pregnantCheck == 5:
                        self.pregnant = True
                        self.gestationPeriod = 10
                        self.maxGestation = self.gestationPeriod + (self.gestationPeriod / 10)
                        ##print("Being " + str(self.iteration) + " is pregnant\n")
        if self.pregnant:
            self.gestationPeriod -= 1
            chanceOfBirth = random.randint(1,self.maxGestation-self.gestationPeriod)
            if chanceOfBirth == 1:
                self.prengnat = False
                father = self.findMate()
                if father == False:
                    return 
                SomethingWrong = random.randint(1,self.health)
                if SomethingWrong == 1:
                    ## :(( rip baby
                    self.health -= 20
                    self.happiness -= 30
                    ##print("Being " + str(self.iteration) + " had problems at birth")
                else:
                    self.happiness += 20
                    newBeing(self,father)
            
    def findMate(self):
        listOfMales = []
        for being in listOfBeings:
            if being.sex == "M":
                listOfMales.append(being)
        if len(listOfMales) > 0:
            mate = random.choice(listOfMales)
        else:
            mate = False
        return mate
            
    def colourCheck(self):
        self.position=[[1,1],[1,4],
                       [2,1],[2,4],
                       [3,1],[3,4]]
        self.positionIteration = self.iteration
        while self.positionIteration > 16:
            for c in range(len(self.position)):
                self.position[c][0] += 4
            self.positionIteration -= 16
        for c in range(self.positionIteration):
            for x in range(len(self.position)):
                self.position[x][1] += 7
        if self.sex=="M":
            sexColour = 4
        else:
            sexColour = 5
        stdscr.addstr(self.position[0][0],self.position[0][1],str(self.sex),curses.color_pair(sexColour))
        stdscr.addstr(self.position[1][0],self.position[1][1],str(self.age),curses.color_pair(sexColour))
        for c in range(4):
            if "+" in self.genes[c]:
                stdscr.addstr(self.position[c+2][0],self.position[c+2][1],str(self.genes[c]),curses.color_pair(2))
            elif "-" in self.genes[c]:
                stdscr.addstr(self.position[c+2][0],self.position[c+2][1],str(self.genes[c]),curses.color_pair(1))
            else:
                stdscr.addstr(self.position[c+2][0],self.position[c+2][1],str(self.genes[c]),curses.color_pair(7))
        stdscr.refresh()
    def feedMeal(self):
        if self.food < 40:
            self.happiness -= random.randint(1,5)
            feedMeal = random.randint(1,5)
            if feedMeal == 3:
                if self.meals < 5:
                    self.food += random.randint(20,25)
                    self.happiness += random.randint(1,5)
    def cleanPoop(self):
        if self.poop > 1:
            self.poop = 0
            self.happiness += random.randint(1,5)
    def tick(self):
        if self.awake:
            poopDecider = random.randint(1,720) ## Minutes in 12 hours
            if poopDecider == 10:
                if self.poop < 4:
                    self.poop += 1
                    self.happiness -= random.randint(1,5)
                else:
                    self.happiness -= random.randint(1,20)
        self.food -= random.randint(1,3)
        if self.awake:
            self.pregnantCheck()
            self.food -= random.randint(1,5)
            self.clean -= random.randint(1,5)
            self.energy -= 1
            self.food -= random.randint(1,2)
            if self.energy < 10:
                self.awake = False
            self.cleanPoop()
            self.feedMeal()
            self.colourCheck()
        if self.awake == False:
            self.energy += 1
            if self.energy > 80:
                self.awake = True
        self.age += 1
        returnStr = self.checkForDying()
        self.pregnantCheck()
        return self.age
    def checkForDying(self):
        if self.age > self.lifeExpectancy:
            deathSavingThrow = random.randint(1,5)
            if deathSavingThrow > 4:
                self.dead = True
                self.reason =  "died of old age"
        elif self.happiness == 0:
            deathSavingThrow = random.randint(1,5)
            if deathSavingThrow > 4:
                self.dead = True
                self.reason = "died of low happiness"

        elif self.health < 40:
            deathSavingThrow = random.randint(1,5)
            if deathSavingThrow > 3:
                self.dead = True
                self.reason = "died of low health"
        if self.dead:
            listOfBeings.remove(self)
            stdscr.addstr(self.position[1][0],self.position[1][1],str("XX"),curses.color_pair(0))
            stdscr.refresh()
    def startTicking(self):
        while self.dead == False:
            age = self.tick()
            time.sleep(0.1)
            ##if self.dead:
               ## print("Being " + str(self.iteration) + " ("+self.sex +") "+ self.reason + " at the age of " + str(self.age)+"\n")
            
def initFirstTamagotchis(sex):
    global iteration
    newGenes = []
    for x in range(4):
        newGenes.append(random.choice(possGenes))
    iteration += 1
    listOfBeings.append(Tamagotchi(50,newGenes,sex))
def newBeing(father,mother):
    mutFlag = 1
    global iteration
    ##print(iteration)
    if iteration > 49:
        iteration = 1
    beingGenes =[]
    newGenes = father.genes + mother.genes
    while mutFlag == 1:
        mutChance = random.randint(1,4)
        if mutChance == 2:
            newGenes.append(random.choice(possGenes))
        else:
            mutFlag = 0
    for x in range(4):
        beingGenes.append(random.choice(newGenes))
    sex = random.choice(["M","F"])
    iteration += 1
    listOfBeings.append(Tamagotchi(50,beingGenes,sex))
    ##print("Being " + str(iteration) + " ("+sex +") "+ " is born")
    ##print("It has the genes " + "/ ".join(beingGenes)+"\n")
threadList = []
nameList = []
import threading
print("Your colony are dead")
print("Starting a new colony")
##time.sleep(3)
##print("///")
initFirstTamagotchis("M")
##print("Being 1 (M) is born")
##time.sleep(0.5)
initFirstTamagotchis("F")
##print("Being 2 (F) is born")
while True:
    for being in listOfBeings:
        if being.iteration in nameList:
            pass
        else:
            nameList.append(being.iteration)
            t = threading.Thread(target=being.startTicking)
            t.start()
            threadList.append(t)
            
            
