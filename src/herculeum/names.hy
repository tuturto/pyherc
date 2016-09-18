;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2015 Tuukka Turto
;; 
;; Permission is hereby granted, free of charge, to any person obtaining a copy
;; of this software and associated documentation files (the "Software"), to deal
;; in the Software without restriction, including without limitation the rights
;; to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
;; copies of the Software, and to permit persons to whom the Software is
;; furnished to do so, subject to the following conditions:
;; 
;; The above copyright notice and this permission notice shall be included in
;; all copies or substantial portions of the Software.
;; 
;; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
;; IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
;; FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
;; AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
;; LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
;; OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
;; THE SOFTWARE.

(require hy.contrib.anaphoric)
(require pyherc.macros)

(import [random [Random]]
        [pyherc.utils [group]]
        [pyherc.markov [chain-factory]])

(setv male-names 
      ["acacius" "achaikos" "aeschylus" "aesop" "agapetos" "agapetus" "agapios"
                 "agathon" "akakios" "alcaeus" "alcibiades" "alexander" "alexandros" "alexios"
                 "alexis" "alexius" "alkaios" "alkibiades" "ambrosios" "ambrosius" "ampelios"
                 "ampelius" "amyntas" "anacletus" "anakletos" "anastasios" "anastasius"
                 "anatolios" "anatolius" "anaxagoras" "andreas" "androcles" "androkles"
                 "andronicus" "andronikos" "anicetus" "aniketos" "antigonos" "antigonus"
                 "antiochos" "antiochus" "antipater" "antipatros" "aphrodisios" "apollinaris"
                 "apollodoros" "apollonios" "arcadius" "archelaos" "archelaus" "archimedes"
                 "archippos" "argyros" "aristarchos" "aristarchus" "aristeides" "aristides"
                 "aristocles" "aristodemos" "aristokles" "ariston" "aristophanes" "aristoteles"
                 "aristotle" "arkadios" "arsenios" "arsenius" "artemidoros" "artemios"
                 "artemisios" "artemius" "artemon" "asklepiades" "athanas" "athanasios"
                 "athanasius" "auxentios" "auxentius" "basileios" "basilius" "bion" "callias"
                 "cassander" "chares" "chariton" "chrysanthos" "cleisthenes" "cleitus"
                 "cleon" "clitus" "cosmas" "cyrillus" "cyrus" "damianos" "damianus"
                 "dareios" "demetrios" "demetrius" "democritus" "demokritos" "demon"
                 "demosthenes" "diocles" "diodoros" "diodorus" "diodotos" "diodotus"
                 "diogenes" "diokles" "dion" "dionysios" "dionysius" "dionysodoros" "draco"
                 "drakon" "eirenaios" "epaphras" "epaphroditos" "epiktetos" "epiphanes"
                 "epiphanios" "epiphanius" "erasmos" "erastos" "euaristos" "euclid"
                 "eugenios" "eugenius" "eukleides" "euphemios" "euphranor" "euripides"
                 "eusebios" "eusebius" "eustachys" "eustathios" "eustathius" "eustorgios"
                 "eustorgius" "euthymios" "euthymius" "eutropios" "eutropius" "eutychios"
                 "eutychius" "eutychos" "evaristus" "gaios" "galenos" "gennadios"
                 "gennadius" "georgios" "georgius" "heliodoros" "heracleitus"
                 "heraclius" "herakleides" "herakleios" "herakleitos" "hermes" "hermogenes"
                 "hermokrates" "hermolaos" "hero" "herodes" "herodion" "herodotos"
                 "herodotus" "heron" "hesiod" "hesiodos" "hesperos" "hieronymos" "hieronymus"
                 "hilarion" "hippocrates" "hippokrates" "hippolytos" "homer" "homeros"
                 "hyacinthus" "hyakinthos" "hyginos" "hyginus" "hypatos" "iason" "irenaeus"
                 "ireneus" "isidoros" "isocrates" "isokrates" "kallias" "kallikrates"
                 "kallistos" "karpos" "kassandros" "kleisthenes" "kleitos" "kleon"
                 "kleopatros" "kosmas" "kyriakos" "kyrillos" "kyros" "leon" "leonidas"
                 "leontios" "leontius" "linos" "linus" "loukianos" "loukios" "lycurgus"
                 "lycus" "lykos" "lykourgos" "lysander" "lysandros" "lysimachos"
                 "lysimachus" "markos" "melanthios" "meliton" "methodios" "methodius"
                 "metrophanes" "miltiades" "mnason" "myron" "neophytos" "nereus" "nicanor"
                 "nicolaus" "nicomedes" "nicostratus" "nikandros" "nikanor" "nikephoros"
                 "niketas" "nikias" "nikodemos" "nikolaos" "nikomachos" "nikomedes"
                 "nikon" "nikostratos" "olympiodoros" "olympos" "onesimos" "onesiphoros"
                 "origenes" "pamphilos" "pancratius" "pankratios" "pantaleon" "panther"
                 "pantheras" "paramonos" "pelagios" "pelagius" "pericles" "perikles"
                 "phaedrus" "phaidros" "philandros" "philippos" "philo" "philokrates"
                 "philon" "philotheos" "phocas" "phoibos" "phokas" "photios" "plato"
                 "platon" "ploutarchos" "polycarp" "polykarpos" "porphyrios" "praxiteles"
                 "prochoros" "prokopios" "ptolemaios" "pyrrhos" "pyrrhus" "pythagoras"
                 "seleucus" "seleukos" "simonides" "socrates" "sokrates" "solon" "sophocles"
                 "sophokles" "sophos" "sophus" "sosigenes" "stephanos" "straton"
                 "telesphoros" "telesphorus" "thales" "themistocles" "themistokles"
                 "theocritus" "theodoros" "theodorus" "theodosios" "theodosius" "theodotos"
                 "theodotus" "theodoulos" "theodulus" "theokritos" "theophanes" "theophilos"
                 "theophilus" "theophylaktos" "theron" "thoukydides" "thucydides"
                 "timaeus" "timaios" "timon" "timoteus" "timotheos" "tryphon" "tycho"
                 "tychon" "xanthippos" "xenocrates" "xenokrates" "xenon" "xenophon" "zeno"
                 "zenobios" "zenon" "zephyros" "zopyros" "zosimos" "zosimus" "zoticus"
                 "zotikos"])

(setv female-names 
      ["agape" "agatha" "agathe" "agnes" "aikaterine" "alexandra" "alexis"
               "ambrosia" "anastasia" "anthousa" "aphrodisia" "apollonia" "aristomache"
               "artemisia" "aspasia" "athanasia" "athenais" "berenice" "berenike"
               "charis" "charmion" "chloe" "chrysanthe" "cleopatra" "corinna" "demetria"
               "demostrate" "doris" "eirene" "elpis" "euanthe" "eudocia" "eudokia"
               "eudoxia" "eugeneia" "eugenia" "eulalia" "eumelia" "eunike" "euphemia"
               "euphrasia" "eupraxia" "euthalia" "euthymia" "eutropia" "eutychia"
               "gaiana" "gaiane" "galene" "hagne" "helena" "helene" "hypatia" "irene"
               "isidora" "kallisto" "kallistrate" "kassandra" "kleopatra" "korinna"
               "ligeia" "lysandra" "lysistrata" "lysistrate" "melissa" "melitta"
               "menodora" "metrodora" "myrrine" "nike" "nikephoros" "nymphodora"
               "olympias" "pelagia" "pherenike" "phile" "phoibe" "photina" "photine"
               "ptolemais" "rhode" "roxana" "roxane" "sappho" "sophia" "sostrate"
               "syntyche" "thais" "theodora" "theodosia" "theokleia" "theophania"
               "theophila" "timo" "timothea" "tryphaina" "tryphosa" "xanthe" "xanthippe"
               "xenia" "xeno" "zenais" "zenobia" "zoe" "zosime"])

(defn split-into-parts [name length]
  "split name into parts of given length"
  (list (ap-map (.join "" it) (group name length))))

(defn add-to-links [links parts-list]
  "add list of chain parts into links, each with same frequency"
  (when parts-list
    (let [[first-item (first parts-list)]
          [second-item (ap-if (second parts-list)
                              #t (it 0 10)
                              #t (nil 0 10))]
          [tail (list (rest parts-list))]]
      (if (not (in first-item links))
        (assoc links first-item [second-item])
        (when (not (in second-item (get links first-item)))
          (.append (get links first-item) second-item)))
      (when tail (add-to-links links tail)))))

(defn add-starting-link [starting-links parts-list]
  "add starting link using standard frequency"
  (let [[first-item #t ((first parts-list) 0 10)]]
    (when (not (in first-item starting-links))
      (.append starting-links first-item))))

(defn add-names [links starting-links length names]
  "process a list of names and prepape configuration for markov chain factory"
  (ap-each names (do (add-starting-link starting-links (split-into-parts it length))
                     (add-to-links links (split-into-parts it length)))))

(defn create-name-generator [examples]
  "create and configure markov chain factory to create names based on examples"
  (let [[links {}]
        [starting-links []]]
    (add-names links starting-links 2 examples)
    (chain-factory starting-links links (fn [item] (not (is item nil))))))

(def greek-males (create-name-generator male-names))
(def greek-females (create-name-generator female-names))

(defn generate-name [factory &optional [seed nil]]
  "generate a name"
  (.capitalize (.join "" (list (factory)))))

(defn generate-random-name [&optional [seed nil]]
  "generate random name"
  (setv rng (if seed
              (Random seed)
              (Random)))
  (if (= 1 (.randint rng 1 2))
    (generate-male-name (.randint rng 0 9223372036854775807))
    (generate-female-name (.randint rng 0 9223372036854775807))))

(defn generate-male-name [&optional [seed nil]]
  "generate name for male"
  (generate-name greek-males seed))

(defn generate-female-name [&optional [seed nil]]
  "generate name for female"
  (generate-name greek-females seed))
