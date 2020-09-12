class Note:
    def __init__(self, id, time, text):
        self.id = id
        self.time = time
        self.text = text

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        if time is not None:
            self.__time = time

    @property
    def notebook(self):
        return self.__notebook

    @notebook.setter
    def notebook(self, n):
        self.__notebook = n

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, t):
        self.__text = t
