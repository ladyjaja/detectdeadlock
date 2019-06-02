from DetectDeadlock import DetectDeadlock 


if __name__ == '__main__':
    print('Detecting Deadlock...')

    #Deadlock Detected...
    Inventory = {'fork1': 2, 'fork2': 2, 'fork3': 4, 'fork4': 4, 'fork5': 5, 'soup': 1, 'bread': 0, 
        'Philosopher 1': 'fork5', 'Philosopher 2': 'soup', 'Philosopher 3': 'soup', 'Philosopher 4': None, 
        'Philosopher 5': 'fork1'}
    deadlock = DetectDeadlock(Inventory, 1)

    #No Deadlock....
    # Inventory = {'fork1': 2, 'fork2': 2, 'fork3': 4, 'fork4': 4, 'fork5': 5, 'soup': 1, 'bread': 0, 
    #     'Philosopher 1': 'fork5', 'Philosopher 2': 'bread', 'Philosopher 3': 'soup', 'Philosopher 4': None, 
    #     'Philosopher 5': 'fork1'}

    # deadlock = DetectDeadlock(Inventory, 2)

    print(deadlock)