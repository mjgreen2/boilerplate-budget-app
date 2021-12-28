#Solution to Budget App project
#Created in Visual Studio Code
#by Michael Green

'''Complete the `Category` class in `budget.py`. It should be able to instantiate objects based on 
different budget categories like *food*, *clothing*, and *entertainment*. When objects are created, 
they are passed in the name of the category. The class should have an instance variable called `ledger` 
that is a list.'''
class Category:
    def __init__(self, name) :
        self.name = name
        self.ledger = []
        self.total = 0.00
        self.printed_object = ""

        #used for 'create_spend_chart' fxn
        self.percentage = 0
        self.bar_graph = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",]

    """A `deposit` method that accepts an amount and description. If no description is given, 
    it should default to an empty string. The method should append an object to the ledger list 
    in the form of `{"amount": amount, "description": description}`."""
    def deposit(self, amount, description = ""):
        item = {"amount": amount, "description": description}
        (self.ledger).append(item)
        self.total += amount

    """A `withdraw` method that is similar to the `deposit` method, but the amount passed in should
 be stored in the ledger as a negative number. If there are not enough funds, nothing should be 
 added to the ledger. This method should return `True` if the withdrawal took place, and `False` otherwise."""
    def withdraw(self, amount, description = ""):
        item = {"amount": (amount * -1), "description": description}
        if (self.check_funds(amount) == True):
            (self.ledger).append(item)
            self.total -= amount
            return True
        else :
            return False

    """A `get_balance` method that returns the current balance of the budget category based on the deposits
 and withdrawals that have occurred."""
    def get_balance(self):
        return self.total

    """A `transfer` method that accepts an amount and another budget category as arguments. The method should
 add a withdrawal with the amount and the description "Transfer to [Destination Budget Category]". 
 The method should then add a deposit to the other budget category with the amount and the description 
 "Transfer from [Source Budget Category]". If there are not enough funds, nothing should be added to either 
 ledgers. This method should return `True` if the transfer took place, and `False` otherwise."""
    def transfer(self, amount, destination):
        if (self.check_funds(amount) == True):
            self.withdraw(amount, "Transfer to " + destination.name)
            destination.deposit(amount, "Transfer from " + self.name)
            return True
        else:
            return False

    """A `check_funds` method that accepts an amount as an argument. It returns `False` if the amount is greater 
than the balance of the budget category and returns `True` otherwise. This method should be used by both the 
`withdraw` method and `transfer` method."""
    def check_funds(self, amount):
        if (self.total >= amount):
            return True
        else:
            return False

    """When the budget object is printed it should display:
* A title line of 30 characters where the name of the category is centered in a line of `*` characters.
* A list of the items in the ledger. Each line should show the description and amount. 
* The first 23 characters of the description should be displayed, then the amount. 
* The amount should be right aligned, contain two decimal places, and display a maximum of 7 characters.
* A line displaying the category total."""
    def __str__(self):
        self.printed_object = f'{self.name:*^30}' + '\n'

        for ledgerCntr in range(len(self.ledger)):
            self.printed_object += self.ledger[ledgerCntr].get("description")[:23].ljust(23)
            self.printed_object += str("{:.2f}".format(self.ledger[ledgerCntr].get("amount"))).rjust(7)
            self.printed_object += '\n'
        self.printed_object += "Total: "
        self.printed_object += str(self.total)
        return self.printed_object

'''
Create a function (outside of the class) called `create_spend_chart` that takes a list of categories as 
an argument. It should return a string that is a bar chart.

The chart should show the percentage spent in each category passed in to the function. 
The percentage spent should be calculated only with withdrawals and not with deposits. 
Down the left side of the chart should be labels 0 - 100. The "bars" in the bar chart 
should be made out of the "o" character. The height of each bar should be rounded down to the nearest 10. 
The horizontal line below the bars should go two spaces past the final bar. 
Each category name should be written vertically below the bar. 
There should be a title at the top that says "Percentage spent by category"
'''
def create_spend_chart(categories):
    spend_total = 0
    withdraw_list = [0, 0, 0, 0]
    
    #Gather the withdrawals + total spend amount
    for catCntr in range(0, len(categories), 1):
        for ledgerCntr in range(0, len(categories[catCntr].ledger), 1):
            withdrawal = categories[catCntr].ledger[ledgerCntr].get("amount")
            if withdrawal < 0 :
                withdraw_list[catCntr] += abs(withdrawal)
                spend_total += abs(withdrawal)

    #Determine what percent of spend total is each category withdrawal
    for percentCntr in range(0, len(categories), 1):
        categories[percentCntr].percentage = int((withdraw_list[percentCntr]/spend_total) * 100)
        
    #Determine number of "bars" for each category graph
    for classCntr in range(0, len(categories), 1):
        graphCntr = 0
        yaxisCntr = 0
        while yaxisCntr <= categories[classCntr].percentage :
            categories[classCntr].bar_graph[graphCntr] = "o"
            graphCntr += 1
            yaxisCntr += 10

    #Construct y-axis and fill in bars
    y_header = ["  0|", " 10|", " 20|", " 30|", " 40|", " 50|", " 60|", " 70|", " 80|", " 90|", "100|"]
    spend_chart = "Percentage spent by category\n"
    for yheaderCntr in range(10, -1, -1):
        spend_chart += y_header[yheaderCntr] + ' '
        for xaxisCntr in range(0, len(categories), 1):
            spend_chart += categories[xaxisCntr].bar_graph[yheaderCntr] + '  '
        spend_chart += '\n'

    #Construct dashed line separating graph from x-axis labels
    dashed_line = "-"
    for dashCntr in range(0, len(categories), 1):
        dashed_line += "---"
    spend_chart += "    " + dashed_line + '\n'

    #Determine longest x-axis label
    max = 0
    for categoryCntr in range(0, len(categories), 1) :
        current = len(categories[categoryCntr].name)
        if current >= max :
            max = current

    #Construct x-axis labels. If loop exceeds category name, fill in with " "
    x_axis = ""
    for nameCntr in range(0, max, 1) :
        x_axis += "     " 
        for labelCntr in range(0, len(categories), 1):
            try:
                x_axis += categories[labelCntr].name[nameCntr] + "  "
            except:
                x_axis += " " + "  "
        #end with newline except for last line
        if nameCntr != (max - 1) :
            x_axis += '\n'
    spend_chart += x_axis
    return spend_chart