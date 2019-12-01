class GestoreContiCorrente():
    @staticmethod
    def bonifico(sorgente,destinatario,importo):
        sorgente.preleva(importo)
        destinatario.deposita(importo)
class Conto():
    def __init__(self,nome,conto):
        self.nome=nome
        self.conto=conto
class ContoCorrente(Conto):
    def __init__(self,nome,conto,importo):
        super().__init__(nome,conto)
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


cc1=ContoCorrente('Gianni',12345,-20)
cc2=ContoCorrente('Giovanna',15326,220)
print(cc1.saldo)
cc1.descrizione()
cc1.saldo=200
cc1.descrizione()
print('-----')
cc2.descrizione()
GestoreContiCorrente.bonifico(cc1,cc2,65.25)
cc1.descrizione()
cc2.descrizione()