from enum import Enum, auto

class DateGeneration(Enum):
    
    Backward = auto()      
    Forward = auto()       
    Zero = auto()          
    ThirdWednesday = auto()
    Twentieth = auto()     
    TwentiethIMM = auto()  
    OldCDS = auto()        
    CDS = auto()            
    CDS2015 = auto()        

    def __str__(self):
        return self.name