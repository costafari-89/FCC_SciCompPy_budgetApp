import math

class Category:
    
    def __init__(self, cat_name):
        self.cat_name = cat_name
        self.ledger = []
        self.balance = 0
                

    def __str__(self): 
        budget_str = ''
        total_stars = 30 - len(self.cat_name)
        star_left = total_stars // 2
        title_str = "{:*^30}\n".format(self.cat_name)
        budget_str += title_str
        for ele in self.ledger:
            
            desc_str = ele["description"][:23]
            amount_str = "{:.2f}".format(ele["amount"])
            desc_len = len(desc_str)
            
            rjust_amt = 30 - desc_len
            
            new_string = desc_str + amount_str.rjust(rjust_amt) + "\n"
            budget_str += new_string

        budget_str += "Total: " + str(self.balance)

        return budget_str

    def get_balance(self):
        return self.balance
    
    def check_funds(self, withdrawal):
        if self.balance - withdrawal < 0:
            return False
        else:
            return True
    
    def deposit(self, amount, desc = ''):
        self.ledger.append({"amount": amount, "description": desc})
        self.balance += amount
        return True
        #pass

    def withdraw(self, amount, desc = ''):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": desc})
            self.balance -= amount
            return True
        else:
            return False
            
    def transfer(self, amount, cat_object):
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + cat_object.cat_name)
            cat_object.deposit(amount, "Transfer from " + self.cat_name)
            return True
        else:
            return False
        

food = Category("food")
food.deposit(900, "deposit")
food.withdraw(105.55)
entertainment = Category("entertainment")
entertainment.deposit(900, 'deposit')
entertainment.withdraw(33.40)
entertainment.withdraw(33.40)
entertainment.withdraw(33.40)
entertainment.withdraw(33.40)
entertainment.withdraw(33.40)
business = Category('business')
business.deposit(900,'deposit')
business.withdraw(10.99)
print(entertainment.ledger)

def create_spend_chart(categories):
    #First line in bar graph string
    return_str = "Percentage spent by category\n"

    with_totals = []
    ele_with = 0

    for i in range(len(categories)):
        for ele in categories[i].ledger:
            if ele["amount"] < 0:
                ele_with += ele["amount"]
            
        with_totals.append(ele_with)
        ele_with = 0
    
    
    perc_total = [math.floor(100 * x//sum(with_totals)/10)*10 for x in with_totals]
    print(perc_total)

    L = len(categories)

    #Creating percentage values for height of graph
    for perc_val in range(100,-1,-10):
        if perc_val > max(perc_total):
            return_str += f"{perc_val}|".rjust(4) + (L*3 + 1)*' ' + '\n'
        else:
            return_str += f"{perc_val}|".rjust(4)

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

            # if perc_total[0] >= perc_val:
            #     return_str += '-o'
            # else:
            #     return_str += '--'
            # if perc_total[1] >= perc_val:
            #     return_str += '--o'
            # else:
            #     return_str += '---'
            # if perc_total[2] >= perc_val:
            #     return_str += '--o--'
            # else:
            #     return_str += '-----'
            

            # for i, perc_cat in enumerate(perc_total):
            #     if perc_cat >= perc_val and i == 0:
            #         return_str += ' o'
            #     elif perc_cat >= perc_val:
            #         return_str += '  o'
                #elif i == (L-1):
                    #print(len(return_str))
                    #return_str += ((L*3 + 1) - len(return_str)) * '-'
            return_str += '\n'


    #Creating divider between values and categories
    return_str += (" "*4) + ((L*3)*"-") + "-\n"

    #Returning names of provided categories to create vertical strings
    cat_names = []
    for cat in categories:
        cat_names.append(cat.cat_name)
    
    #Adding additional spaces to smaller strings so they all have the same length
    max_len = len(max(cat_names, key = len))

    print(cat_names)

    for i in range(len(cat_names)):
        if len(cat_names[i]) < max_len:
            cat_names[i] = cat_names[i] + ' '*(max_len - len(cat_names[i]))
    
    print(cat_names)

    #joining the lists horizontally with appropriate spacing
    #first letter of each cat_name joined "t  t  t"
    joined_list = list(map('  '.join, zip(*cat_names)))

    #For each joined list element adding 5 spaces at front and new line character at end
    for i in range(len(joined_list)):
        if i == len(joined_list) - 1:
            new_string =  (' '*5) + joined_list[i] + '  '
        else:
            new_string = (' '*5) + joined_list[i] + "  \n"
        return_str += new_string
    return return_str

categories = [food, entertainment, business]
print(create_spend_chart(categories))
