import Undecided
import Counselor
import uuid
class Chat:
    def __init__(self, subject:str, intensity:int):
        self.__id = uuid.uuid1().int
        self.__subject = subject
        self.__intensity = intensity
        self.__undecided = None
        self.__counselor = None
        

    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def undecided(self) -> Undecided:
        return self.__undecided
    
    @undecided.setter
    def undecided (self, undecided:Undecided):
        self.__undecided = undecided

    @property
    def counselor(self) -> Counselor:
        return self.__counselor

    @counselor.setter
    def counselor(self, counselor:Counselor):
        self.__counselor = counselor

    @property
    def subject(self) -> str:
        return self.__subject

    @subject.setter
    def subject(self, subject:str):
        self.__subject = subject
    
    @property
    def intensity(self) -> int:
        return self.__intensity

    @intensity.setter
    def intensity(self, intensity:int):
        self.__intensity = intensity
        
    @staticmethod
    def validateIntensity( intensity:str) -> bool:
        if intensity not in ["1","2","3"]:
            return False
        return True 
    
    @staticmethod
    def validateSubject(subject:str) -> bool:
        if len(subject) < 2 or len(subject) >= 50:
            return False
        return True
    
    def __str__(self) -> str:
        return f"""[{self.__subject} , {self.__intensity}, {self.__undecided.username}, {self.__id}]"""
