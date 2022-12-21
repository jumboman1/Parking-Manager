# PARKING MANAGEMENT
class parkingfarecalc:
    def __init__(self, s=0, t=0, vno='', vname='', oname='', Date='',intime=''):
        print("\n")
        print("\t* * * * * * * * * * * * * * * * * * * * *")
        print("\t*\t\t\t\t\t\t\t\t\t\t*")
        print("\t*\t\tWELCOME TO PARKING MANAGER\t\t*")
        print("\t*\t\t\t\t\t\t\t\t\t\t*")
        print("\t* * * * * * * * * * * * * * * * * * * * *")
        self.s = s;
        self.vno = vno;
        self.vname = vname;
        self.oname = oname;
        self.Date = Date;
        self.intime = intime;
        
    # INPUT DATA MODULE
    def inputdata(self):
        self.vno = int(input("\n\tEnter vehicle number:"))
        self.vname = input("\n\tEnter vehicle name:")
        self.oname = input("\n\tEnter Owner name:")
        self.Date = input("\n\tEnter your check in date (YYYY/MM/DD):")
        self.intime = input("\n\tEnter check-in time(HH:MM:SS):\n")
            
        # MYSQL INTEGRATION
        
        import mysql.connector as mycon  
        con1=mycon.connect(host='localhost',user='root',passwd='root')
        cur=con1.cursor()
        sql1='create database if not exists parkingdb'
        cur.execute(sql1)
        con1.commit()

        con1=mycon.connect(host='localhost',user='root',passwd='root',database='parkingdb')
        cur=con1.cursor()
        sql2='create table if not exists vehicleinfo (vno int primary key, vname varchar(30), oname varchar(30), Date date, intime time)'
        cur.execute(sql2)
        con1.commit()
        
        cur=con1.cursor()      
        sql3="insert into vehicleinfo values ({}, '{}', '{}','{}','{}')".format(self.vno, self.vname, self.oname, self.Date, self.intime)
        cur.execute(sql3)
        con1.commit()

        cur=con1.cursor()
        sql4='create table if not exists parkbill (vno int primary key, oname varchar(30), Date date, Totalcost int, foreign key(vno) references vehicleinfo(vno))'
        cur.execute(sql4)
        con1.commit()

        cur=con1.cursor()
        sql15="insert into parkbill values ({},'{}','{}',{})".format(self.vno, self.oname, self.Date, self.s)
        cur.execute(sql15)
        con1.commit()

    # PARKING FEE MODULE
    def parkfee(self):
        v=int(input("\tEnter vehicle number:"))
        print("\n\tWe have the following vehicles for you:-")
        print("\n\t1.  Bicycle ==> Rs 20 PH\-")
        print("\t2.  Bike ==> Rs 40 PH\-")
        print("\t3.  Car ==> Rs 60 PH\-")
        print("\t4.  Truck ==> Rs 70 PH\-")
        x = int(input("\n\tEnter Your Choice:"))
        n = int(input("\tEnter number of hours parked:"))
        if x == 1:
            print("\n\tYou have selected Bicycle\n")
            self.s = 20 * n
        elif x == 2:
            print("\n\tYou have selected Bike\n")
            self.s = 40 * n
        elif x == 3:
            print("\n\tYou have selected Car\n")
            self.s = 60 * n
        elif x == 4:
            print("\n\tYou have selected Truck\n")
            self.s = 70 * n
        else:
            print("\tPlease select a vehicle")
        print("\tYour parking fee is =", self.s, "\n\n")
                 
        import mysql.connector as mycon
        con2=mycon.connect(host='localhost',user='root',passwd='root',database='parkingdb')
        cur=con2.cursor()
        sql5="update parkbill set Totalcost={} where vno={}".format(self.s,v)
        cur.execute(sql5)
        con2.commit()

    # DELETE ENTRY MODULE
    def delete(self):
        v=int(input("\tEnter vehicle number:"))
        import mysql.connector as mycon
        con3=mycon.connect(host='localhost',user='root',passwd='root',database='parkingdb')
        '''
        cur=con3.cursor()
        sql9="set foreign_key_checks=0 delete from parkbill where vno={} set foreign_key_checks=1".format(v)
        cur.execute(sql9)
        '''
        cur=con3.cursor()
        sql6="delete from parkbill where vno={}".format(v)
        cur.execute(sql6)
        
        cur=con3.cursor()
        sql7="delete from vehicleinfo where vno={}".format(v)
        cur.execute(sql7)
        con3.commit()
        

    # VIEW PARKED VEHICLES
    def view(self):    
        from tabulate import tabulate
        import mysql.connector as mycon
        con4=mycon.connect(host='localhost',user='root',passwd='root',database='parkingdb')
        cur=con4.cursor()
                
        sql8="select vno, vname, oname, intime, Totalcost from parkbill natural join vehicleinfo"
        cur.execute(sql8)
        v=cur.fetchall()
        print(tabulate(v, headers=["Vehicle Number","Vehicle Name","Owner Name","Check-in time","Total Cost"],numalign="center", tablefmt="fancy_grid"),"\n")

    def amount(self):
        print("\t* * * * * * * * * * * * * * * * * * * * *")
        print("\t*\t\t\t\t\t\t\t\t\t\t*")
        print("\t*\t\t\tAmount Details\t\t\t\t*")
        print("\t*\t\t\tBicycle ==> Rs.20\t\t\t*")
        print("\t*\t\t\tBike ==> Rs.40\t\t\t\t*")
        print("\t*\t\t\tCar ==> Rs.60\t\t\t\t*")
        print("\t*\t\t\tTruck ==> Rs.70\t\t\t\t*")
        print("\t*\t\t\t\t\t\t\t\t\t\t*")
        print("\t* * * * * * * * * * * * * * * * * * * * *\n\n")

def main():
    a = parkingfarecalc()
    while 1:
        print("\t* * * * * * * * * * * * * * * * * * * * *")
        print("\t*\t\t\t\t\t\t\t\t\t\t*")
        print("\t*\t\t1.Enter Vehicle Data\t\t\t*")
        print("\t*\t\t2.Calculate Parking Fee\t\t\t*")
        print("\t*\t\t3.Delete Entry\t\t\t\t\t*")
        print("\t*\t\t4.Show All Vehicles\t\t\t\t*")
        print("\t*\t\t5.View Amount Details\t\t\t*")
        print("\t*\t\t6.Exit\t\t\t\t\t\t\t*")
        print("\t*\t\t\t\t\t\t\t\t\t\t*")
        print("\t* * * * * * * * * * * * * * * * * * * * *")
        b = int(input("\n\tEnter your choice:"))
        if b == 1:
            a.inputdata()
        if b == 2:
            a.parkfee()
        if b == 3:
            a.delete()
        if b == 4:
            a.view()
        if b == 5:
            a.amount()
        if b == 6:
            break

v=vno=0
main()