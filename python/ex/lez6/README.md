determinare due indici chiamati i specifico e i descrittivo sul'insieme dei 4p (4 polimini quadrati) in modo che sia possibile
determinare:
1- Un modo per costruire una partizione tra tutti che li distingua attraverso una caratteristica da voi determinata (classe)
2- Un modo per distinguerli singolarmente (id, rotazione ignorata ha stesso id)
3- Generalizzare i specifico e i descrittivo ad un insieme NP qualsiasi

1- Considerando il polimino come un insieme di più elementi, possiamo dire che è composto da elementi singoli ma anche composti
    per esempio se prendiamo il polimino: [][] consideriamo ogni spigolo di ogni elemento (senza contare i duplicati) e partendo
    da in alto a sinistra contiamo        [][]
    quanti elementi condividono quello spigolo. Sommiamo le righe pari e sottraiamo el righe dispari. In questo caso il polimino
    sarà di classe 1+2+1-(2+4+2)+1+2+1=0
    mentre nel caso del polimino   [][] la sua classe diventa 1+2+1-(3+3+1)+1+2+1=1
                                 [][]
2- Consideriamo per ogni elemento del polimino i suoi lati liberi adiacenti. Possiamo stabilire una regola di costruzione univoca
    molto simile a un puzzle. Ogni lato libero ha un valore (0:su, 1:destra,2:sotto, 3:sinistra). riprendiamo il polimino: [][]
    partendo da in alto a sinistra il [] ha posizioni libere 0 e 3. In conclusione il polimino avrà come identificativo    [][]
    "03,01,12,23". Se mescoliamo i valori otteniamo un altro nome ma il polimino risultante sarà lo stesso
    mentre il polimino   [][] lo possiamo chiamare "03,012,12,230" o anche "012,230,03,12"
                       [][]
3- Le regole precedenti sono applicabili per qualsiasi insieme di polimini, esempio veloce:
    [][][][][] ha classe 0 e id "02,02,02,012,023"

    [][][]     ha classe 1 e id "02,01,23,012,023"
        [][]