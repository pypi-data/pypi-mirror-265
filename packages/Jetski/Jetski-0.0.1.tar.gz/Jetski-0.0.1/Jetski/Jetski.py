import datetime
import json
# import prettytable 

class JetskiRental:
    def __init__(self,stock=0):
        self.stock = stock

    def displaystock(self):
        print(f"We have currently {self.stock} jetskis available to rent.")
        return self.stock

    def rentJetskiOnHourlyBasis(self, n):
        if n <= 0:
            print("Number of jetskis should be positive!")
            return None
        elif n > self.stock:
            print(f"Sorry! We have currently {self.stock} jetskis available to rent.")
            return None
        else:
            now = datetime.datetime.now()
            print(f"You have rented a {n} jetski(s) on hourly basis today at {now.hour} hours.")
            print("You will be charged $55 for each hour per jetski.")
            print("We hope that you enjoy our service.")
            self.stock -= n
            return now

    def rentJetskiOnHalfDailyBasis(self, n):
        if n <= 0:
            print("Number of jetskis should be positive!")
            return None
        elif n > self.stock:
            print(f"Sorry! We have currently {self.stock} jetskis available to rent.")
            return None
        else:
            now = datetime.datetime.now()
            print(f"You have rented {n} jetski(s) on half daily basis today at {now.hour} hours.")
            print("You will be charged $110 for each 4 hours per jetski.")
            print("We hope that you enjoy our service.")
            self.stock -= n
            return now

    def rentJetskiOnDailyBasis(self, n):
        if n <= 0:
            print("Number of jetskis should be positive!")
            return None
        elif n > self.stock:
            print(f"Sorry! We have currently {self.stock} jetskis available to rent.")
            return None
        else:
            now = datetime.datetime.now()            
            print(f"You have rented {n} jetski(s) on daily basis today at {now.hour} hours.")
            print("You will be charged $165 for each 8 hrs per jetski.")
            print("We hope that you enjoy our service.")
            self.stock -= n
            return now


    def returnJetski(self, request):
        """
        1. Accept a rented jetski from a customer
        2. Replensihes the inventory (เติมของ)
        3. Return a bill
        """
        rentalTime, rentalBasis, numOfJetskis = request
        bill = 0

        if rentalTime and rentalBasis and numOfJetskis:
            self.stock += numOfJetskis
            now = datetime.datetime.now()
            rentalPeriod = now - rentalTime

            if rentalBasis == 1:
                bill = round(rentalPeriod.seconds / 3600) * 55 * numOfJetskis

            elif rentalBasis == 2:
                bill = round(rentalPeriod.seconds / (3600*4)) * 110 * numOfJetskis

            elif rentalBasis == 3:
                bill = round(rentalPeriod.seconds / (3600*8)) * 165 * numOfJetskis

            # family discount calculation
            if (3 <= numOfJetskis <= 5):
                print("You are eligible for Family rental promotion of 20% discount")
                bill = bill * 0.8
            print("Thanks for returning your jetski. Hope you enjoyed our service!")
            print(f"That would be ${bill}")
            return bill
        else:
            print("Are you sure you rented a jetski with us?")
            return None
    
    # Save
    def save_file(self, data=[], filename="JetskiInformation.json"):
        with open(filename, "w") as file:
            json.dump(data, file)
            
    # Load
    def load_file(self, filename="JetskiInformation.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print("We don't have that file...")


class Customer:
    def __init__(self):
        self.jetskis = 0
        self.rentalBasis = 0                # Note: rentalBasis 1(1 hr), 2(4 hrs), 3(8 hrs) 
        self.rentalTime = 0
        self.bill = 0

    def requestJetski(self):
        jetskis = input("How many jetskis would you like to rent?")

        try:
            jetskis = int(jetskis)
        except ValueError:
            print("That's not a positive integer!")
            return -1

        if jetskis < 1:
            print("Invalid input. Number of jetskis should be greater than zero!")
            return -1
        else:
            self.jetskis = jetskis
        return self.jetskis

    def returnJetski(self):
        if self.rentalBasis and self.rentalTime and self.jetskis:
            return self.rentalTime, self.rentalBasis, self.jetskis
        else:
            return 0,0,0
        
def main():
    shop = JetskiRental()
    mydata = shop.load_file()
    
    while True:
        print("Menu:")
        print("1: Display informations")
        print("2: To rent jetskis")
        print("3: To return jetskis")
        print("4: Exit and Save")
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            print("--------------")
            print(f"Stocks:{mydata['Stock']}")
            for key,value in mydata['Customers'].items():
                print(f"{key}: {value}")
            print("--------------")
            
        elif choice == '2':
            customer = Customer()
            name = input("Enter your name: ")
            print("--------------")
            jetskis = customer.requestJetski()
            if mydata["Stock"]>=jetskis and jetskis>=1:
                mydata["Stock"] -= jetskis
                rentalBasis = int(input("Choose the rentalBasis: 1(1 hr), 2(4 hrs), 3(8 hrs): "))
                rentalTime = datetime.datetime.now()
                date_list = list(rentalTime.timetuple())
                del date_list[5:]
                date_list[3] -= 2
                mydata['Customers'][name] = [jetskis, rentalBasis, date_list]
                shop.save_file(mydata)
            print("--------------")
            
        elif choice == '3':
            customer = Customer()
            name = input("Enter your name: ")
            print("--------------")
            customer.jetskis = mydata["Customers"][name][0]
            customer.rentalBasis = mydata["Customers"][name][1]
            list_time  = mydata["Customers"][name][2]
            customer.rentalTime = datetime.datetime(*list_time)
            request = customer.returnJetski()
            shop.returnJetski(request)
            
            '''
            if 3<=mydata["Customers"][name][0]<=5: discount = bill
                       
            myTable = prettytable.PrettyTable(["Customer", "Type", "Amount", "Start", "End", "Period", "Discount", "Price"]) 
            myTable.add_row([name, 
                             mydata["Customers"][name][1], 
                             mydata["Customers"][name][0],
                             customer.rentalTime,
                             datetime.datetime.now(),
                             datetime.datetime.now()-customer.rentalTime,
                             discount,
                             bill
                             ])
            print(myTable)
            '''
            mydata["Stock"] += mydata["Customers"][name][0]
            del mydata["Customers"][name]
            shop.save_file(mydata)
            print("--------------")
        else:
            break          
    
#Test   
if __name__ == '__main__':
    main()