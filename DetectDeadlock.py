import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='       (%(threadName)-9s) %(message)s',)

probe = None

def receiver(self, phid):
        with self:
                logging.debug(' waiting for probe to be available')
                self.wait()
                logging.debug(' got the probe: ' + ', '.join(str(x) for x in probe))

def sender(self, phid, msg):
        global probe

        with self:
                logging.debug(' creating probe to be sent')
                probe = msg
                logging.debug(' probe sent ')
                self.notifyAll()

def getreceiver(Inventory, need):
        if (need == None): 
                receiver = 0
        else:
                receiver = Inventory[need]
        return receiver

def DetectDeadlock(Inventory, philidn):
        condition = threading.Condition()

        philosopher = philidn
       
        initiatorid = philosopher  #initiator shouldn't change
        senderid = philosopher #at first, sender is the initiator
        log = []
        deadlock = False

        while True:
                need = Inventory['Philosopher ' + str(senderid)]
                log.append('Philosopher ' + str(senderid) + ' needs ' + str(need))
                receiverid = getreceiver(Inventory, need)
                log.append('Philosopher ' + str(receiverid) + ' holds ' + str(need))
                
                if (receiverid == 0 or need == None or senderid == receiverid):
                        deadlock = False
                        log.append('No deadlock')
                        break

                msg = [initiatorid, senderid, receiverid]
                sendername = 'Philosopher ' + str(senderid)
                receivername = 'Philosopher ' + str(receiverid)

                receiverthread = threading.Thread(name=receivername, target=receiver, args=(condition,receiverid,))
                senderthread = threading.Thread(name=sendername, target=sender, args=(condition,senderid,msg,))

                receiverthread.start()
                time.sleep(1)
                senderthread.start()
                time.sleep(1)

                senderid = receiverid
                if (senderid == initiatorid):
                        deadlock = True
                        log.append('DEADLOCK DETECTED!!')
                        break
        
        if (deadlock==True):
                print(Inventory)
                print(log)

        return deadlock
