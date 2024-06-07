import math

class Category:
    
    #Create instance variables 
    def __init__(self, cat_name):
        self.cat_name = cat_name
        self.ledger = []
        self.balance = 0
                

    def __str__(self): 
        budget_str = ''
        #Creating title string with cat_name centered by *, ******food******
        title_str = "{:*^30}\n".format(self.cat_name)
        budget_str += title_str

        #Pulling description and value from each dictionary element of ledger list
        for ele in self.ledger:
            
            #Truncating description string to first 23 characters
            desc_str = ele["description"][:23]

            #Formating amount to two decimal places
            amount_str = "{:.2f}".format(ele["amount"])
            desc_len = len(desc_str)
            
            #determing the amount of spaces to add after description to align all amounts to right edge
            rjust_amt = 30 - desc_len
            
            #Concatenating description string with amount string
            new_string = desc_str + amount_str.rjust(rjust_amt) + "\n"
            budget_str += new_string

        #Applying final line to string of total balance
        budget_str += "Total: " + "{:.2f}".format(self.balance)

        return budget_str

    def get_balance(self):
        return self.balance
    
    def check_funds(self, withdrawal):
        #Checking that a withdrawal of money does not cause overdraft
        if self.balance - withdrawal < 0:
            return False
        else:
            return True
    
    def deposit(self, amount, desc = ''):
        #Append dictionary to ledger with description and amount
        self.ledger.append({"amount": amount, "description": desc})
        #modifying balance by deposit amount
        self.balance += amount
        return True

    def withdraw(self, amount, desc = ''):
        #Check that withdrawl for given amount does not overdraft
        if self.check_funds(amount):
            #If it does not overdraft, append description and amount and modify balance
            self.ledger.append({"amount": -amount, "description": desc})
            self.balance -= amount
            return True
        else:
            return False
            
    def transfer(self, amount, cat_object):
        #Check that transfer does not cause overdraft
        if self.check_funds(amount):
            #Use withdraw method to append amount and description to self ledger
            self.withdraw(amount, "Transfer to " + cat_object.cat_name)
            #User Deposit method to append amount and description to given class object ledger
            cat_object.deposit(amount, "Transfer from " + self.cat_name)
            return True
        else:
            return False
        

#For testing purposes this creates a set of transactions for ledgers and balances used
#In future use cases
food = Category("food")
food.deposit(900, "deposit")
food.withdraw(105.55)
entertainment = Category("entertainment")
entertainment.deposit(900, 'deposit')
entertainment.withdraw(33.40, 'candy')
entertainment.withdraw(33.40, 'candy')
entertainment.withdraw(33.40, 'candy')
entertainment.withdraw(33.40, 'candy')
entertainment.withdraw(33.40, 'candy')
business = Category('business')
business.deposit(900,'deposit')
business.withdraw(10.99)
print(entertainment)

def create_spend_chart(categories):
    #First line in bar graph string
    return_str = "Percentage spent by category\n"

    #Initialize with_totals list to hold total withdrawls for each class object given
    with_totals = []
    ele_with = 0

    #iterate through each category and then each item in ledger for given category
    for i in range(len(categories)):
        for ele in categories[i].ledger:
            #If the amount is negative it is a withdrawal add it to the running sum ele_with
            if ele["amount"] < 0:
                ele_with += ele["amount"]
        #Append running sum ele_with to with_totals    
        with_totals.append(ele_with)
        #reset running sum for next category
        ele_with = 0
    
    #List comprehension of with_totals to recalculate with_totals as percentage of total withdrawals
    #Rounded down to the near 10th percentage ie 20% 10% 0% etc
    perc_total = [math.floor(100 * x//sum(with_totals)/10)*10 for x in with_totals]

    #print(perc_total)

    #Determine many categories are given to function
    L = len(categories)

    #Creating percentage values for height of graph, intital for loop 100 -> 0 by 10s
    for perc_val in range(100,-1,-10):
        #If current percentage value (perc_val) is greater than the max percentage of withdrawals by category
        #Add string of percentage ie "100|    " and spaces to appropriate width
        if perc_val > max(perc_total):
            return_str += f"{perc_val}|".rjust(4) + (L*3 + 1)*' ' + '\n'
        
        #Once operating in percentages that need to be marked with o character evaluate
        else:
            #Append start of newline string ie " 70|"
            return_str += f"{perc_val}|".rjust(4)
            
            #Iterate through each total percentage and its position either first postion [0] middle [>0] [<maxi] last [maxi]
            for i, perc_cat in enumerate(perc_total):
                if i == 0 and perc_cat >= perc_val:
                    return_str += ' o'
                elif i == 0 and perc_cat <= perc_val:
                    return_str += '  '
                elif i < L-1 and i > 0 and perc_cat >= perc_val:
                    return_str += '  o'
                elif i < L-1 and i > 0 and perc_cat <= perc_val:
                    return_str += '   '
                elif i == L-1 and perc_cat >= perc_val:
                    return_str += '  o  '
                elif i == L-1 and perc_cat <= perc_val:
                    return_str += '     '

            #Since new line is complete add new line character to end
            return_str += '\n'


    #Creating divider between values and categories, ie "--------"
    return_str += (" "*4) + ((L*3)*"-") + "-\n"

    #Creating list of names of provided categories to create vertical strings
    cat_names = []
    for cat in categories:
        cat_names.append(cat.cat_name)
    
    #What is the longest length of the names given
    max_len = len(max(cat_names, key = len))

    #print(cat_names)

    #Making all names the same length as longest name by appending spaces to end of string
    for i in range(len(cat_names)):
        if len(cat_names[i]) < max_len:
            cat_names[i] = cat_names[i] + ' '*(max_len - len(cat_names[i]))
    
    #print(cat_names)

    #joining the lists vertically with appropriate spacing
    #first letter of each cat_name joined with two spaces in betwenn ie "t  t  t" for names test, test, test
    joined_list = list(map('  '.join, zip(*cat_names)))

    #For each joined list element adding 5 spaces at front and 2 spaces and new line character at end ie "     t  t  t  \n"
    for i in range(len(joined_list)):
        #if last element do not add \n to end of string, rejected by unittest for having ending \n
        if i == len(joined_list) - 1:
            new_string =  (' '*5) + joined_list[i] + '  '
        else:
            new_string = (' '*5) + joined_list[i] + "  \n"
        return_str += new_string
    return return_str

categories = [food, entertainment, business]
print(create_spend_chart(categories))
