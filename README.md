# SignSense
!(assets/logo.png)
Progetto d'esame di [Pietro Coloretti](https://github.com/ogrish15) e [Iacopo Sbalchiero](https://github.com/IacopoSb) per il corso Sistemi Digitali M presso il corso di Ingegneria Informatica M @ Unibo A.A. 2023-2024.


## L'idea
Il progetto si concentra sulla creazione di un sistema basato su computer vision e intelligenza artificiale per la traduzione del linguaggio dei segni in testo. Utilizzando una webcam USB e un Raspberry Pi, il sistema offre un'interfaccia portatile e autonoma senza la necessità di un monitor esterno o una connessione a Internet.
Il cuore del sistema è una rete neurale implementata con Yolo (basato su PyTorch), TensorFlow e OpenCV, progettata per riconoscere e interpretare i segni delle mani nel linguaggio dei segni. La webcam cattura i gesti delle mani e trasmette le immagini ad un Raspberry Pi, dove la rete neurale elabora i dati in tempo reale.
Il risultato della traduzione viene visualizzato su un display LCD 16x2, rendendo l'output immediatamente accessibile all'utente. Questa soluzione compatta e portatile è ideale per situazioni in cui uno schermo esterno non è pratico, come in ambienti pubblici o in luoghi con restrizioni di spazio.
La traduzione eseguita è di tipo "letterale": questa si basa sull'alfabeto LIS italiano e permette di assemblare parole e frasi (sono supportate le lettere dell'alfabeto latino di base (alfabeto italiano esteso a 26 lettere) e dei simboli aggiuntivi per 'spazio', 'elimina ultimo carattere' e 'reset'.
Infine, è stato eseguito un porting su piattaforma Android ottenendo una applicazione con il medesimo scopo di traduzione sfruttando l'hardware del dispositivo per la cattura di immagini e la loro elaborazione attraverso la CNN. 
## La raccolta dei campioni
Per il processo di acquisizione delle immagini, abbiamo adottato un approccio manuale che ha comportato la cattura di circa trenta campioni per ciascun simbolo. Durante questa fase, abbiamo prestato particolare attenzione alla variazione dell'angolazione e della profondità, al fine di ottenere una gamma completa di rappresentazioni per i segni. 
!(assets/img1.jpg) !(assets/img2.jpg)
Dopo aver completato la fase di acquisizione, ci siamo dedicati all'etichettatura mediante l'utilizzo del programma Python LableImg.  Questo strumento ci ha consentito di associare a ciascuna immagine un'etichetta XML contenente le coordinate delle bounding box, fornendo così la base per la successiva fase di analisi ed elaborazione. Successivamente, abbiamo trasferito l'intero set di dati su Roboflow, una piattaforma che ci ha permesso di organizzare e standardizzare la dimensione dei campioni. Questo è stato particolarmente cruciale poiché le immagini provenivano da dispositivi diversi e presentavano originariamente risoluzioni eterogenee. Mediante l'utilizzo di Roboflow, siamo riusciti a garantire una coerenza nell'elaborazione dei dati, facilitando ulteriormente le fasi successive del nostro progetto.
## La realizzazione della rete neurale
Il primo passo cruciale nella creazione della rete neurale è stato quello di ottenere un modello addestrato utilizzando i campioni precedentemente raccolti. Questo processo di addestramento è stato eseguito mediante l'implementazione della libreria YOLOv5. Tuttavia, è importante notare che l'output di questo processo non era immediatamente utilizzabile per le nostre esigenze specifiche. Ciò è dovuto al fatto che, se l'applicazione Android richiedeva un modello nel formato TFLite con quantizzazione intera, il Raspberry Pi, pur non necessitando di tale restrizione, ha una limitata capacità computazionale. Pertanto, abbiamo deciso di utilizzare lo stesso modello su entrambe le piattaforme, anche se ciò comportava una perdita di precisione. Questa scelta è stata motivata dalla necessità di garantire una maggiore velocità di elaborazione sul Raspberry Pi, anche a discapito della precisione complessiva del modello.
!(assets/img3.jpg)
## Deployment su Raspberry Pi
Il sistema operativo installato sul Raspberry Pi è basato su un'immagine precompilata di Raspbian basato su Debian 11 che include una serie di framework già configurati per l'utilizzo delle reti neurali. Questa immagine, disponibile all'indirizzo GitHub [https://github.com/Qengineering/RPi-Bullseye-DNN-image](https://github.com/Qengineering/RPi-Bullseye-DNN-image), semplifica notevolmente il processo di avvio e configurazione per l'uso delle reti neurali sul dispositivo.
Lo script utilizzato per eseguire il riconoscimento delle lettere si basa sull'utilizzo del modello tflite precedentemente generato. Il codice originale è stato modificato in modo che ad ogni iterazione, se la lettera con il più alto grado di riconoscimento supera una soglia del 50%, venga attivata una funzione appartenente a una libreria creata per il controllo del display. Questa funzione, a sua volta, si occupa di manifestare la lettera riconosciuta sul monitor esterno.
!(assets/img4.jpg)
Per comunicare con il display LCD, è stata sviluppata una libreria personalizzata utilizzante due buffer: uno temporaneo per le lettere in arrivo e uno per il salvataggio delle lettere considerate valide. Cuore della libreria è la funzione charRaised a cui viene passata in ingresso la lettera riconosciuta in modo tale che possa essere salvata nel buffer temporaneo. Successivamente, se la stessa lettera viene riconosciuta per un numero di iterazioni consecutive (nel nostro caso abbiamo scelto 4), la lettera viene considerata valida e memorizzata nel buffer per essere visualizzata sul display. Se invece il valore non viene validato, allora esso viene considerato come un'identificazione spuria e viene quindi scartato senza essere memorizzato nel buffer. 
Al momento dell'avvio del Raspberry Pi, viene eseguito uno script che permette l'inizializzazione del display LCD e avvia il codice per il riconoscimento dei segni. In questo modo il dispositivo si avvia automaticamente appena alimentato e non è necessario eseguire azioni sul sistema operativo.
!(assets/img5.png)
Lo schema di cablaggio descritto indica i pin GPIO utilizzati per collegare il display LCD al Raspberry Pi. Ogni pin GPIO è associato a una funzione specifica del display, come la trasmissione dei dati, il controllo dell'attivazione e la selezione della modalità di invio dei dati. Questo schema garantisce una corretta comunicazione e funzionamento del display LCD con il Raspberry Pi.
| GPIO Raspberry Pi | Tipo PIN | Collegamento |
| ---------------- | -------- | ------------ |
| GPIO17           | Output   | 1602, pin D5 |
| GPIO18           | Output   | 1602, pin D6 |
| GPIO22           | Output   | 1602, pin D7 |
| GPIO23           | Output   | 1602, pin D4 |
| GPIO24           | Output   | 1602, pin EN |
| GPIO25           | Output   | 1602, pin RS |


## Deployment su Android
Per quanto riguarda l'applicazione Android, siamo partiti da uno scheletro base già costruito, presente nel [repository ufficiale del progetto Tensorflow](https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection) applicandogli il modello esportato nel formato TFLite.
L'applicazione è stata quindi modificata aggiungendo al feed video che compare nella schermata principale alcuni elementi utili per il debugging e in generale per verificare l'andamento e la performance del riconoscimento, come gli FPS e l'inference time. 
Le modifiche più rilevanti eseguite sull'applicazione riguardano la gestione delle dipendenze Gradle e delle versioni di Java. Si è infatti dimostrato necessario effettuare un downgrade dalle versioni più recenti di Gradle (specificamente dalla versione 8.4 alla 7.2) e di Java (dalla versione 17 alla versione 11) e questo è stato fatto principalmente a causa della mancanza di compatibilità con alcune delle dipendenze utilizzate nel progetto, che hanno portato ad errori di compilazione e conflitti tra le diverse librerie utilizzate. Dell'applicazione è quindi stato eseguito il deployment su dispositivi fisici in modo da testarne il funzionamento. 
!(assets/img6.jpg)
## Problematiche riscontrate
Durante l'intero svolgimento del progetto, si sono incontrate numerose problematiche. Inizialmente, si prevedeva lo sviluppo del modello utilizzando la libreria TensorFlow, fornita da Google. Tuttavia, l'utilizzo di questa libreria ha portato alla creazione di alcuni modelli TFLite che, al momento del loro impiego per il riconoscimento dei segni, risultavano corrotti e privi di metadati. Inoltre, si era pianificato di eseguire l'allenamento tramite la macchina virtuale Colab, sempre fornita da Google, al fine di garantire un processo di training più rapido e affidabile. Nonostante ciò, le restrizioni imposte dal piano base di Colab e la mancanza di risorse gratuite hanno reso necessaria una modifica dei piani operativi, portando infine all'allenamento in locale. Si era inoltre ipotizzato di effettuare l'allenamento utilizzando la libreria tflite-model-maker; tuttavia, anche questa ha presentato problemi durante l'installazione sia su Colab sia su macchine Windows e Linux.
Il primo tentativo su un ambiente di sviluppo basato su Raspberry Pi prevedeva l'utilizzo dell'ultima versione del sistema operativo Raspbian (basata su Debian 12), ma questa si è rivelata incompatibile con numerose librerie, inclusi TensorFlow e TensorFlow Lite. Di conseguenza, si è reso necessario eseguire un downgrade alla penultima versione di Raspbian, basata su Debian 11 a 64 bit e contenente Python 3.9.2. Infine, come già citato, si è optato per l'uso di una versione di Raspbian già dotata degli strumenti necessari per la computer vision, inclusi le librerie essenziali per il riconoscimento attraverso i modelli creati.
Anche lo sviluppo dell'applicazione Android ha riscontrato delle difficoltà, specialmente riguardo all'utilizzo del modello ottenuto. Inizialmente, infatti, il modello necessario per l'esecuzione dell'applicazione richiedeva metadati che non venivano importati correttamente all'interno del modello esportato. Di conseguenza, è stata utilizzata una versione modificata del modello che, oltre ad includere il modello stesso, richiedeva anche l'inserimento di un file contenente le label associate.
Successivamente, per superare questa problematica, si è tentato di integrare manualmente i metadati mancanti nel modello esportato, ma questo approccio si è rivelato inefficace poiché ha comportato una perdita di coerenza nel modello stesso. Si è anche provato a utilizzare diverse versioni di TensorFlow e TensorFlow Lite. Questi tentativi non solo non hanno risolto il problema, ma hanno anche comportato un ulteriore rallentamento nello sviluppo dell'applicazione Android e nel conseguimento degli obiettivi prefissati.
## Obiettivi futuri
L'idea del progetto potrebbe essere ampliata aggiungendo un secondo modello dedicato al riconoscimento non più dell'alfabeto, ma delle singole parole, al fine di ottenere traduzioni più rapide e precise. Questa nuova implementazione sarebbe stata proposta come un'alternativa di traduzione nel contesto del progetto. Tuttavia, a causa delle difficoltà incontrate durante l'allenamento del primo modello e del conseguente spreco di tempo, questa idea non è stata realizzata.
Per implementare questa funzionalità, si potrebbe introdurre la possibilità di cambiare tra le due modalità di riconoscimento attraverso un pulsante dedicato all'interno del dispositivo Raspberry Pi. Tale pulsante interromperebbe il processo di riconoscimento con il modello selezionato e lo riavvierebbe con il nuovo modello per il riconoscimento delle parole e viceversa. Per l'applicazione Android, invece, si potrebbe implementare uno scambio tra le modalità attraverso un menu a tendina, consentendo agli utenti di selezionare la modalità desiderata in modo rapido e intuitivo.
Un'altra possibile estensione potrebbe essere apportata all'interno dell'applicazione Android. Attualmente, quest'ultima riconosce esclusivamente i segni visualizzati in tempo reale senza mantenerli in memoria per formare frasi complete. A differenza del progetto realizzato su Raspberry Pi, che consente la visualizzazione e la memorizzazione di intere parole e frasi impartite al dispositivo, l'applicazione Android si limita al riconoscimento immediato della lettera indicata, senza mantenere alcun tipo di storico in memoria. Questo rende difficile la lettura e l'interpretazione del testo impartito.
