class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class Check_Id:
    def __init__ (self):
        self.id = 0
        self.data = ""

    def set_device_id(self, device):
        self.id = int (device[0])

    def get_device_id(self):
        return self.id

    def set_device_data(self, device):
        self.data = device[1]

    def get_device_data(self):
        return self.data

    def send_data(self):
        if self.id == 1: # compass - degree/bearing
            return int(data)
        elif self.id == 2: # accelerometer - xyz
            return data
        elif self.id == 3: # sensor L
            return data 
        elif self.id == 4: # sensor R
            return data
        elif self.id == 5: # sensor F
            return data 
        elif self.id == 6: # sensor B
            return data
        elif self.id == 7: # gyroscope - rate xyz
            return data
        elif self.id == 8: # keypad
            return data




            