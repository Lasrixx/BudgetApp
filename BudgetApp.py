class Category:
    def __init__(self,name):
        #initalise variables for the class
        self.name=name
        self.ledger = list()
        self.spent=0
        self.percentageSpent = 0
        self.bar = ""
    def deposit(self,amount, description=""):
        #accept +sums of money and add to ledger
        self.ledger.append({"amount":amount, "description":description})
    def withdraw(self,amount,description=""):
        #accept -sums of money and add to ledger
        if self.check_funds(amount) == True:
            self.ledger.append({"amount":-amount, "description":description}) 
            #This line will save time in the create bar chart function
            self.spent+=amount   
            return True
        return False    
    def get_balance(self):
        #Return the net money spent and recieved so far
        balance=0
        for i in range(0,len(self.ledger)):
            balance+=self.ledger[i].get("amount")
        return balance
    def transfer(self,amount,target):
        #Take funds from one category and put them in another
        if self.check_funds(amount)==True:
            self.withdraw(amount,"Transfer to "+target.name)        
            target.deposit(amount,"Transfer from "+self.name)
            return True
        return False
    def check_funds(self,amount):
        #Check that a category has a + amount of money overall
        balance = self.get_balance()
        if amount > balance:
            return False
        return True
    def __str__(self):
        #Used to print out the object's ledger in a specific form (like a receipt)
        total = 0
        output = "*"*int(((30-len(self.name))/2))+self.name+"*"*int(((30-len(self.name))/2)) + "\n"
        for i in range(0,len(self.ledger)):
            shortDescription = self.ledger[i].get("description")[:23]
            output += "%-23s%7.2f"%(shortDescription, self.ledger[i].get("amount")) + "\n"
            total+=self.ledger[i].get("amount")
        output+="%s%.2f"%("Total: ",total)
        return output

def create_spend_chart(categories):
    #Calculate the percentage spent in each category out of the total amount spent
    barChart=""
    totalSpent = 0
    for category in categories:
        totalSpent+=category.spent
    for category in categories:
        category.percentageSpent = category.spent/totalSpent * 100
    #Build the bar chart
    #Title
    barChart="Percentage spent by category\n"
    #Vertical axis - here I can also add the 'bars' row by row
    #Bars can be made by making a string for each category that is made of ' ' and 'o'
    #Built in the same way as the bar labels below
    for category in categories:
        percentInBar = int(category.percentageSpent/10)+1
        category.bar = " "*(11-percentInBar)+"o"*(percentInBar)
    for i in range(100,-1,-10):
        barChart+="%3d| %s  %s  %s\n"%(i,categories[0].bar[int(10-(i/10))],categories[1].bar[int(10-(i/10))],categories[2].bar[int(10-(i/10))])
    #Horizontal axis
    barChart+="    "+"-"*(3*len(categories)+1)+"\n"
    #For the column titles, I need to figure out which category has the longest name
    #Then I can make all other categories just as long so formatting is simple
    longestName = ""
    for category in categories:
        if len(category.name) > len(longestName):
            longestName = category.name
    for category in categories:
        category.name+=" "*(len(longestName)-len(category.name))
    for i in range(len(longestName)):
        barChart+="   %3s%3s%3s\n"%(categories[0].name[i],categories[1].name[i],categories[2].name[i])
    barChart=barChart[:len(barChart)-1]

    return barChart

food=Category("Food")
entertainment = Category("Entertainment")
business=Category("Business")
food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)
print(business)
print(create_spend_chart([business, food, entertainment]))

