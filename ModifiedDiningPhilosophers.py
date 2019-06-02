import random
import time
import threading

pfNum = 5
phi_nums = ('Philosopher 1','Philosopher 2','Philosopher 3','Philosopher 4', 'Philosopher 5')
Inventory = {
        'fork1': 0,
        'fork2': 0,
        'fork3': 0,
        'fork4': 0,
        'fork5': 0,
        'soup': 0,
        'bread': 0,
        'Philosopher 1': None,
        'Philosopher 2': None,
        'Philosopher 3': None,
        'Philosopher 4': None,
        'Philosopher 5': None,
    }

class Phi(threading.Thread):

    running = True

    def __init__(self, num, leftfork, rightfork, idn, bread, soup):               #initiate threads
        threading.Thread.__init__(self)
        self.num = num
        self.leftfork = leftfork
        self.rightfork = rightfork
        self.idn = idn
        self.bread = bread
        self.soup = soup
 
    def run(self):
        while(self.running):
            time.sleep(random.uniform(20,30))                  #time before hungry
            print ('%s is HUNGRY ' % self.num)
            self.dine()
 
    def dine(self):
        global Inventory
        fork1, fork2, bread, soup = self.leftfork, self.rightfork, self.bread, self.soup
        fork1num = self.idn % pfNum
        fork2num = (self.idn + 1) % pfNum
        if (fork1num == 0): fork1num = pfNum
        if (fork2num == 0): fork2num = pfNum    

        gotfork1 = False
        gotfork2 = False
        gotbread = False
        gotsoup = False

        acquisition = ['fork1', 'fork2', 'bread', 'soup']

        while self.running:

            random.shuffle(acquisition)
            print(str(self.num) + ' is getting items in this order ' + ', '.join(acquisition))
            
            for item in acquisition:

                if (item == 'fork1'): 
                    Inventory[self.num] = 'fork' + str(fork1num)
                if (item == 'fork2'):
                    Inventory[self.num] = 'fork' + str(fork2num)
                if (item == 'bread' or item == 'soup'):
                    Inventory[self.num] = item

                # time.sleep(2)
                # deadlock = DetectDeadlock(Inventory, self.idn + 1)
                # if (deadlock == True): return

                if (item == 'fork1'): 
                    gotfork1 = fork1.acquire(True)
                    print(str(self.num) + ' holds LEFT fork ' + str(fork1num))
                    Inventory['fork' + str(fork1num)] = self.idn + 1
                    Inventory[self.num] = None
                if (item == 'fork2'):
                    gotfork2 = fork2.acquire(True)
                    print(str(self.num) + ' holds RIGHT fork ' + str(fork2num))
                    Inventory['fork' + str(fork2num)] = self.idn + 1
                    Inventory[self.num] = None
                if (item == 'bread'):
                    gotbread = bread.acquire(True)
                    print(str(self.num) + ' gets BREAD ')
                    Inventory['bread'] = self.idn + 1
                    time.sleep(random.uniform(5,10))  
                    bread.release()
                    print(str(self.num) + ' releases plate of BREAD ')
                    Inventory['bread'] = 0
                    Inventory[self.num] = None
                if (item == 'soup'):
                    gotsoup = soup.acquire(True)
                    Inventory['soup'] = self.idn + 1

                    # THIS IS THE CODE THAT CAN CAUSE DEADLOCK 
                    if (random.randint(1,3)==1): # 1/5 probability that Philosopher will not release soup
                        print(str(self.num) + ' keeping the bowl of soup *******************') 
                        Inventory['soup'] = self.idn + 1
                        Inventory[self.num] = None
                    else:
                        print(str(self.num) + ' gets SOUP ')   
                        Inventory['soup'] = self.idn + 1 
                        time.sleep(random.uniform(5,10))  
                        soup.release()
                        print(str(self.num) + ' releases bowl of SOUP ')   
                        Inventory['soup'] = 0 
                        Inventory[self.num] = None

                #time.sleep(2)
                #deadlock = DetectDeadlock(Inventory, self.idn + 1)
                #if (deadlock == True): return

            #thread doesn't go past here unless acquired both forks and food!
       
            if (gotfork1 and gotfork2 and gotbread and gotsoup): break
       
        else:
            return

        self.dining()  
        fork1.release()
        Inventory['fork' + str(fork1num)] = 0
        fork2.release()     
        Inventory['fork' + str(fork2num)] = 0
        print ('%s released all forks, thinks Philosophy '% self.num)
                                               
    def dining(self):            
        print ('%s starts eating - feeds body, mind and spirit '% self.num)
        time.sleep(random.uniform(10,20))                       #time before finish eating, should less than time of thinking
        print ('%s FINISHES eating' % self.num)
            

 
def DiningPhilosophers():
    forks = [threading.Lock() for jj in range(pfNum)]
    bread = threading.Lock()
    soup = threading.Lock()
    phis= [Phi(phi_nums[ii], forks[ii%pfNum], forks[(ii+1)%pfNum], ii, bread, soup) for ii in range(pfNum)]   #choose fork next to them 

    Phi.running = True
    for num in phis: num.start()
    time.sleep(200)
    Phi.running = False
 
DiningPhilosophers()


#Reference:  https://github.com/KLdivergence/-dining-philosophers-problem