class ContoCorrente():
    def __init__(self,nome,conto,importo):
        self.nome=nome
        self.conto=conto
        self.__saldo=importo
    def descrizione(self):
        print("Nome:\t"+self.nome)
        print("Conto:\t"+str(self.conto))
        print("Saldo:\t"+str(self.__saldo))
    def preleva(self,importo):
        self.__saldo-=importo
        if self.saldo<0:
            print('Attento '+self.nome+'! Hai saldo negativo')
    def deposita(self,importo):
        self.__saldo+=importo
    @property
    def saldo(self):
        return self.__saldo
    @saldo.setter
    def saldo(self,importo):
        self.preleva(self.__saldo)
        self.deposita(importo)


cc=ContoCorrente('Gianni',12345,-20)
print(cc.saldo)
cc.descrizione()
cc.saldo=200
cc.descrizione()