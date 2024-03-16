# SignSense

Progetto d'esame di [Pietro Coloretti](https://github.com/ogrish15) e [Iacopo Sbalchiero](https://github.com/IacopoSb) per il corso Sistemi Digitali M presso il corso di Ingegneria Informatica M @ Unibo.

## Il progetto

Il progetto si concentra sulla creazione di un sistema basato su computer vision e intelligenza artificiale per la traduzione del linguaggio dei segni in testo. Utilizzando una webcam USB e un Raspberry Pi, il sistema offre un'interfaccia portatile e autonoma senza la necessità di uno schermo esterno o una connessione a Internet.

Il cuore del sistema è una rete neurale implementata con TensorFlow e OpenCV, progettata per riconoscere e interpretare i segni delle mani nel linguaggio dei segni. La webcam cattura i gesti delle mani e trasmette le immagini ad un Raspberry Pi, dove la rete neurale elabora i dati in tempo reale.

Il risultato della traduzione viene visualizzato su un display LCD 16x2, rendendo l'output immediatamente accessibile all'utente. Questa soluzione compatta e portatile è ideale per situazioni in cui uno schermo esterno non è pratico, come in ambienti pubblici o in luoghi con restrizioni di spazio.

La traduzione avviene "letteralmente": utilizzando l'alfabeto LIS italiano permette di assemblare parole e frasi (sono supportate le lettere dell'alfabeto latino di base (alfabeto italiano esteso a 26 lettere) e dei simboli aggiuntivi per 'spazio', 'elimina ultimo carattere' e 'reset'.

## Descrizione delle cartelle

| Cartella                     | Descrizione                                                          |
| ---------------------------- | -------------------------------------------------------------------- |
| lcdDriver                    | Contiene script per il funzionamento del display 1602 su RaspberryPi |
| RealTimeObjectDetection-main | Contiene i programmi per la cattura di immagini e il suo allenamento |

## Materiale e schema di assemblaggio

- Raspberry Pi 4
- HD44780 1602 Modulo LCD
- Resistenza 2Kohm
- Webcam USB

### Diagramma dei PIN di collegamento al Raspberry Pi

| PIN Raspberry Pi | Tipo PIN | Collegamento |
| ---------------- | -------- | ------------ |
| GPIO17           | Output   | 1602, pin D5 |
| GPIO18           | Output   | 1602, pin D6 |
| GPIO22           | Output   | 1602, pin D7 |
| GPIO23           | Output   | 1602, pin D4 |
| GPIO24           | Output   | 1602, pin EN |
| GPIO25           | Output   | 1602, pin RS |

## Estensione ad applicazione Android

