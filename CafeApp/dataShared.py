class DataShared:
    cafe = []
    @classmethod
    def setCafeName(self, cafe):
        for i in cafe:
            self.cafe.append(i)
    @classmethod
    def getCafeName(self):
        return self.cafe
