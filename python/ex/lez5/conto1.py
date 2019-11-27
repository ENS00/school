class ContoCorrente():
    def __init__(self,nome,conto,importo):
        self.nome=nome
        self.conto=conto
        self.saldo=importo
    def preleva(self,importo):
        self.saldo-=importo
        if self.saldo<0:
            print('Attento '+self.nome+'! Hai saldo negativo')
    def deposita(self,importo):
        self.saldo+=importo
    def descrizione(self):
        print("Nome:\t"+self.nome)
        print("Conto:\t"+str(self.conto))
        print("Saldo:\t"+str(self.saldo))

cc=ContoCorrente('Gianni',12345,0)
cc.deposita(200)
cc.preleva(120.5)
cc.descrizione()
cc.preleva(130)