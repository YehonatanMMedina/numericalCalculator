import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
def clearMinuses(str): # a helper function that takes a function and returns it without erros like 4+-5 -> 4-5
    for i in range(len(str)-1):
        if(str[i]=='+'):
            if str[i+1]=='-':
                str = str[0:i] + '-' + str[i+2:len(str)]
        if(str[i]=='*'):
            if str[i+1]=='-':
                x = getIntFromThisIndex(str,i+2)
                if len(x) ==0:
                    str = str[0:i] + "*(-1)" + str[i + 2 + len(x):len(str)]
                else:
                    str = str[0:i] + "*(-" + str[i+2:i+2+len(x)]+")"+str[i+2+len(x):len(str)]
    return str
def isANumber(str):#checks if a given string is a number

    if len(str) == 0:
        return False

    for i in range(len(str)):
        if not (str[i].isnumeric() or str[i]=='.' or(str[i] =='-' and not str[i-1].isnumeric())):
            return False
    return True
def getStringStartingFromThisIndex(function, i): # given a function and an index - returns the string from this index forwards
    n=i
    while i < len(function) and function[i].isalpha():
        i=i+1
    return function[n:i]
def getIntFromThisIndex(function, i):  # given a function and an index - returns the int from this index forwards
    n=i
    while i < len(function) and function[i].isnumeric():
        i=i+1
    return function[n:i]
class Function:
    operation = ' ' # operation that we can split the function by
    placeOfOperation = -1 # the place of this operation

    def __init__(self, function):
        self.function= function
        self.func1=''
        self.func2=''
        self.newFunctionParser()

    def newFunctionParser(self): # this method splits the function into two functions
        counter = 0
        while self.canRemoveSograim():
            self.function = self.function[1:len(self.function)-1] # if the function is wrapet around two meaningless () then it removes them
        if len(self.function) != 0:#turns -5 to (-5)
            if self.function[0]=='-':
                self.function = "(" + self.function +")"

        for i in range(len(self.function)):
            if self.function[i] == "(":#checking if we are not inside a ()
                counter = counter + 1
            if self.function[i] == ")":
                counter = counter - 1
            if counter ==0:
                if self.function[i]=="+":#cosidering mathemtical order of operations finding the operation we can split the function by
                    self.operation ="+"
                    self.placeOfOperation=i
                elif self.function[i]=="-":
                    self.operation ="-"
                    self.placeOfOperation=i
                elif self.function[i] =="*" and not (self.operation == '+' or self.operation == '-'):
                    self.operation = "*"
                    self.placeOfOperation = i
                elif self.function[i] =="/" and not (self.operation == '+' or self.operation == '-'):
                    self.operation = "/"
                    self.placeOfOperation = i
                elif self.function[i]=="^"  and not (self.operation == '+' or self.operation == '-') and not (self.operation == '*' or self.operation == '/'):
                    self.operation ="^"
                    self.placeOfOperation = i
                elif self.function[i].isalpha() and self.function[i]!='x' and not (self.operation == '+' or self.operation == '-') and not (self.operation == '*' or self.operation == '/') and not (self.operation=='^'):
                    candidateOperation = getStringStartingFromThisIndex(self.function,i)
                    if candidateOperation == "sin" or candidateOperation == "cos" or candidateOperation== "tan" or candidateOperation == "exp"or candidateOperation == "ln":
                        self.operation = candidateOperation
                        self.placeOfOperation = i + len(self.operation) -1
        #defining the two child functions that construct the function
        self.func1 = self.function[0:self.placeOfOperation]
        self.func2 = self.function[self.placeOfOperation + 1:len(self.function)]

        # in case of a complex function we just have the second child wich is the contents of its - () - then the first child will be empty
        if self.operation == "sin" or self.operation == "cos" or self.operation == "tan" or self.operation == "exp" or self.operation == "ln":
            self.func1=""

    def calcvalue(self,x): # this method caclulates to value of a fuction at a given x value
        # base cases
        if self.function == "x":
            return x
        if self.function == "e":
            return math.e
        if self.function == "pi":
            return math.pi
        if isANumber(self.function) :
            return float(self.function)
        if self.function[0] == "(" and self.function[len(self.function)-1]==")" and isANumber(self.function[1:len(self.function)-2]): # if it is a number inside parentheses
            return float(self.function[1:len(self.function)-1])

        if len(self.func1)!=0: # a comple functin has no func1 then if the func1 ='' the function is comlex and we should not define it
            Func1 = Function(self.func1)
        Func2 = Function(self.func2)

        if self.operation == '+':# rec case: spliting the function based on its operation
            return float(Func1.calcvalue(x)) + float(Func2.calcvalue(x))
        elif self.operation == '-':
            return float(Func1.calcvalue(x)) - float(Func2.calcvalue(x))
        elif self.operation == '*':
            return float(Func1.calcvalue(x)) * float(Func2.calcvalue(x))
        elif self.operation == '/':
            return float(Func1.calcvalue(x)) / float(Func2.calcvalue(x))
        elif self.operation == '^':
            return math.pow(float(Func1.calcvalue(x)),float(Func2.calcvalue(x)))
        elif self.operation=='ln':
            return math.log((Func2.calcvalue(x)),math.e)
        elif self.operation=='sin':
            return math.sin(Func2.calcvalue(x))
        elif self.operation == 'cos':
            return math.cos(Func2.calcvalue(x))
        elif self.operation == 'tan':
            return math.tan(Func2.calcvalue(x))
        elif self.operation == 'sqrt':
            return math.sqrt(Func2.calcvalue(x))
        elif self.operation == 'exp':
            return math.exp(Func2.calcvalue(x))
    def canRemoveSograim(self): # checks if there are meaningless parentheses
        counter = 0
        if len(self.function)==0:
            return False

        if self.function[0] =="(" and self.function[len(self.function)-1]==")":
            for i in range(1,len(self.function)-2):
                if self.function[i] == "(":
                    counter = counter + 1
                if self.function[i] == ")":
                    counter = counter - 1
                if counter < 0:
                    return False
            return True
    def findDerivative(self): # finds the derivative a given function
        if self.function == "x": # integers and x base case
            return "1"
        if isANumber(self.function) or self.function == "pi" or self.function == "e":
            return "0"
        if isANumber(self.function[1:len(self.function)-2]) and self.function[0]=="(" and self.function[len(self.function)-1]==")":
            return "0"
        #polinomials base case
        if len(self.function)==5 and self.function[0].isnumeric() and self.function[1]=="*" and self.function[2]=="x" and self.function[3]=="^" and self.function[4].isnumeric():
                return "(" + self.function[0] + +"*"+ self.function[4] + ")*" + "x^"+ str(int(self.function[4])-1)
        if len(self.function)==3 and self.function[0]=="x" and self.function[1]=="^" and self.function[2].isnumeric():
                return "(" + self.function[2]+")*x^"+ str(int(self.function[2])-1)
        if self.operation== "+"or self.operation== "-" or self.operation== "*" or self.operation== "/":
            Func1= Function(self.func1)
        Func2 = Function(self.func2)

        if self.operation == "+": #rec case by the operation
            return Func1.findDerivative() + "+" + Func2.findDerivative()
        if self.operation == "-":
            return Func1.findDerivative() + "-" + Func2.findDerivative()
        if self.operation == "*":
            return "(" + Func1.findDerivative()+")*(" + Func2.function + ")+(" + Func2.findDerivative() + ")*(" +Func1.function +")"
        if self.operation == "/":
            return "(" + "(" + Func1.findDerivative()+")*(" + Func2.function + ")-(" + Func2.findDerivative() + ")*(" +Func1.function + "))" + "/" + "((" +Func2.function+")^2)"
        if self.operation == 'ln':
            return "(" +str(1) + "/" +"("+ Func2.function + ")" + ")*"+ "(" + Func2.findDerivative() + ")"
        if self.operation == "sin":
            return "cos(" + Func2.function + ")*("+ Func2.findDerivative()+")"
        if self.operation == "cos":
            return "-sin(" + Func2.function+ ")*" + "(" + Func2.findDerivative()+ ")"
        if self.operation == "tan":
            return "(" +str(1) + "/" + "(cos("+ Func2.function+"))^2" +")" + "*" + "("+ Func2.findDerivative() +")"
        if self.operation == "sqrt":
            return "(" + Func2.findDerivative() + ")/(2*sqrt("+Func2.function+"))"
        if self.operation == "exp":
            return "("+Func2.findDerivative() + ")/(2*sqrt(" + Func2.function + "))"

    def FRbinary_search(self, low=-10000000, high=10000000,epsilon=0.001 ,counter=0): # finding the root of a function using binary search

        # Check base case
        if high >= low:

            mid = (high + low) / 2

            # If value is exactly in the middle
            fmid=self.calcvalue(mid)
            if abs(fmid) <epsilon:
                return mid

            # If value is smaller than mid, then it can only
            # be present left in relation to the middle
            elif fmid > 0:
                print(counter)
                return self.FRbinary_search(low, mid,epsilon,counter+1)

            # If value is greater than mid, then it can only
            # be present right in relation to the middle
            else:
                print(counter)
                return self.FRbinary_search(mid, high,epsilon,counter+1)

        else:
            # x does not exist
            return -1

    def FRnewtonRaphson(self,x=2,epsilon=0.000000001): # finding the derivative of a function using newton raphson

        valueOfX = self.calcvalue(x) # f(x)
        if abs(valueOfX)<epsilon: # base case
            return x
        derivativeFunctionStr =clearMinuses(self.findDerivative())# find derivative
        derivativeFunction = Function(derivativeFunctionStr)#in order to calculate the derivatives value we define it as a function
        m= derivativeFunction.calcvalue(x)#derivative at x value
        nextx = x - valueOfX/m
        return self.FRnewtonRaphson(nextx,epsilon)

    def FRslope(self,lowx=-500,highx=705,epsilon=0.000000001,counter=0):#finds the root of a function using the slope technique

        lowy=self.calcvalue(lowx)
        highy=self.calcvalue(highx)
        #finding the slopes: m,b || y=mx+b
        m=(highy-lowy)/(highx-lowx)
        b= highy-m*highx
        x0 = (-b)/m # the intersection of the slope with the x-axis
        fx0 = self.calcvalue(x0)
        if(abs(fx0)<epsilon):#base case
            return x0
        if fx0 > 0:#rec case
            lowx=x0
        else:
            highx=x0
        return self.FRslope(lowx,highx,epsilon,counter+1)

    def definiteIntegralTRP(self,a,b,devideTo):# finding the definite integral using the trapezoid method
        step = (b-a)/devideTo# the interval
        p1 = a#defining the two points
        p2 = a+ step
        sum = 0
        for i in range(devideTo):
            fp2=self.calcvalue(p2)
            fp1= self.calcvalue(p1)
            space = (fp1+fp2)*0.5 * step # using the formula for a trapezoid space
            sum = sum +space
            p1 = p1+step
            p2= p2+step
        return sum
    def definiteIntegralREC(self,a,b,devideTo):# finding the definite integral using the rectangle method
        step = (b-a)/devideTo#the intervals
        p1 = a#the two edges of the interval
        p2 = a + step
        sum = 0
        for i in range(devideTo):
            mid = (p1+p2)/2
            fmid = self.calcvalue(mid)
            space = fmid * step#using the formula for rectangle space
            sum = sum +space
            p1 = p1+step
            p2= p2+step
        return sum

    def printGraph(self,start,finnish,points):#printing the graph
        y = np.zeros(points)# two arrays for x and y values
        x = np.linspace(start, finnish, points)
        for i in range(points):
            y[i] = self.calcvalue(x[i]) # calculating the y values

        plt.plot(x, y)
        plt.show()

print("Welcome to my numeric analasis project")
function = input("Enter A Function:")
f= Function(function)
isUsing = True
while isUsing:
    action = int(input("What do you want to find 1-value, 2-derivative, 3-Root, 4- definite integral, 5- graph:"))
    if action == 1:
        x = input("Enter x coordinate")
        print("The value of the function at x=" +str(x)+ " is:")
        print(f.calcvalue(x))
    if(action == 2):
        print("the derivative of the function is:")
        print(clearMinuses(f.findDerivative()))
    if action == 3:
        print("one root of the function is:")
        print(f.FRnewtonRaphson())
    if action == 4:
        start= int(input("enter the start of the integration area"))
        end= int(input("enter the end of the integration area"))
        print(f.definiteIntegralTRP(start,end,10000))
    if action == 5:
        start = int(input("enter the x value for the start of the graph"))
        end = int(input("enter the x value for the end of the graph"))
        f.printGraph(start,end,100*abs(start-end))
    userRespose = int(input("Would you like to try another operation on this function or enter a new one 1-another operation 2-leave:"))
    if userRespose==2:
        print("Thank you for trying my project!")
        isUsing = False
