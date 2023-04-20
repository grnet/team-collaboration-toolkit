# Ασφαλές λογισμικό για συνεργασία

## Τι είναι αυτό το toolkit

Πολλές εταιρείες και οργανισμοί χρησιμοποιούν Google Drive ή άλλο
συναφές σύστημα για την αποθήκευση των αρχείων τους, Zoom ή συναφές για
βιντεοκλήσεις και τηλεσυσκέψεις, ενίοτε και Slack ή συναφές για
ανταλλαγή μηνυμάτων. Αν και βολικά στη χρήση, όλα αυτά τα συστήματα
έχουν το πρόβλημα ότι χρησιμοποιούν server και λογισμικό τρίτων
εταιρειών, με αποτέλεσμα να μην είναι γνωστό το κατά πόσον οι
επικοινωνίες και τα αρχεία διαρρέουν ή χρησιμοποιούνται με ανεπιθύμητο
τρόπο από αυτές τις τρίτες εταιρείες.

Για πολλούς χρήστες αυτό δεν είναι πρόβλημα, όμως μερικές εταιρείες και
οργανισμοί επιθυμούν ή επιβάλλεται να έχουν τον απόλυτο έλεγχο των
επικοινωνιών και των αρχείων τους. Αυτό εδώ το toolkit παρέχει
ολοκληρωμένη λύση, βασισμένη σε ελεύθερο λογισμικό, για τους
συγκεκριμένους οργανισμούς.

Ειδικότερα, για την αποθήκευση των αρχείων χρησιμοποιούμε το
[Nextcloud](https://nextcloud.com/), που επίσης διαθέτει ημερολόγιο και
άλλες εφαρμογές, καθώς και το
[CollaboraOffice](https://www.collaboraoffice.com/) για online
επεξεργασία αρχείων μέσα στο browser (όπως γίνεται με το Google Docs).
Για βιντεοκλήσεις και τηλεσυσκέψεις χρησιμοποιούμε το
[Jitsi](https://jitsi.org/). Τέλος, για ανταλλαγή μηνυμάτων (chat)
χρησιμοποιούμε [Matrix](https://matrix.org) και
[Element](https://element.io).

Αυτές δεν είναι οι μοναδικές λύσεις. Μερικοί οργανισμοί αντί για Jitsi
προτιμούν το [BigBlueButton](https://bigbluebutton.org), που είναι πιο
προσανατολισμένο σε παρουσιάσεις αλλά μπορεί μια χαρά να χρησιμοποιηθεί
και για τηλεσυσκέψεις. Επίσης, υπάρχει το [Nextcloud
Talk](https://nextcloud.com/talk/), που προσφέρει και
βιντεοκλήσεις/τηλεσυσκέψεις και chat, ενσωματώνεται πολύ ωραία στο
Nextcloud, και ενδέχεται σε πολλές περιπτώσεις να είναι καταλληλότερο
για οργανισμούς που ούτως ή άλλως χρησιμοποιούν (ή θα χρησιμοποιήσουν)
Nextcloud. Εντούτοις προς το παρόν εμείς δεν χρησιμοποιούμε (ακόμα)
αυτές τις λύσεις, οπότε στο toolkit έχουμε περιλάβει μόνο τα Nextcloud,
Jitsi και Matrix+Element.

## Απαιτήσεις

### Άνθρωποι

Καταρχήν χρειάζεται να υπάρχει ένας διαχειριστής συστημάτων ο οποίος θα
εγκαταστήσει τα συστήματα. Χρειάζεται γνώση σε ansible και docker. Ο
χρόνος που πρέπει να αφιερώσει για να έχει το πλήρες σύστημα έτοιμο
εκτιμάται σε μερικές μέρες (με την προϋπόθεση ότι υπάρχει γνώση σε
ansible και docker), χωρίς να περιλαμβάνεται το backup (επειδή ο κάθε
οργανισμός έχει διαφορετικές πρακτικές ως προς το backup, οι λύσεις που
παρέχονται εδώ δεν περιλαμβάνουν backup—περιλαμβάνονται όμως οδηγίες ως
προς το τι θα πρέπει να γίνει backup).

Χρειάζεται επίσης ένας άνθρωπος ο οποίος γνωρίζει ή θα μάθει τα
συστήματα απ' την πλευρά του χρήστη και θα προσφέρει εκπαίδευση και
υποστήριξη στους χρήστες.

### Υλικό

Χρειάζονται δύο (τουλάχιστον) server (καλό είναι το Nextcloud να
βρίσκεται σε διαφορετικό server απ' ό,τι τα Matrix/Element και Jitsi).
Γενικά για 50 χρήστες ένας server για το Nextcloud και ένας για τα
υπόλοιπα θα πρέπει να αρκεί. Περισσότερες πληροφορίες για τη
διαστασιολόγηση των server αναφέρονται παρακάτω.

Είναι προφανές ότι για να εξασφαλίζεται ο πλήρης έλεγχος των δεδομένων
οι server πρέπει να βρίσκονται σε χώρο της εταιρείας. Η εγκατάσταση σε
server φιλοξενούμενους από πάροχο μπορεί εντούτοις να δώσει μέρος των
πλεονεκτημάτων, όπως ανεξαρτησία (π.χ. δυνατότητα μετακόμισης σε άλλο
πάροχο) και εξασφάλιση του απορρήτου στην ανταλλαγή μηνυμάτων και στις
βιντεοκλήσεις, αφού τα Matrix και Jitsi υποστηρίζουν κρυπτογράφηση
end-to-end.

#### Nextcloud

Περίληψη: Για 50 χρήστες: 4 επεξεργαστές, 8 GB RAM, και χώρος στο δίσκο
όσο χρειάζονται οι χρήστες για τα αρχεία τους, συν 30 GB. Αυτά τα
ενδεικτικά νούμερα είναι με επιφύλαξη—διαβάστε αναλυτικά παρακάτω.

Στην ΕΔΥΤΕ όπου το Nextcloud χρησιμοποιείται επί του παρόντος από 50
χρήστες, το έχουμε εγκατεστημένο σε virtual servers που έχουν ιδιαίτερα
αργούς δίσκους, με αποτέλεσμα η ταχύτητα του δίσκου να είναι το
bottleneck. Για να αντιμετωπίσουμε αυτό το πρόβλημα, έχουμε βάλει τη
MySQL σε χωριστό virtual server, και αυτός ο χωριστός virtual server
έχει δύο διαφορετικούς δίσκους: έναν για τα redo logs κι έναν για τα
data files. Με αυτό τον τρόπο χρησιμοποιούμε τρεις δίσκους παράλληλα.
Όμως σε ένα server με σύγχρονους δίσκους (πολύ περισσότερο σε ένα server
με SSD), είναι απίθανο να χρειαστεί κάτι τέτοιο.

Ο server του Nextcloud που χρησιμοποιούμε έχει 16 CPU και 32 GB RAM, απ'
ό,τι βλέπουμε όμως τα CPU κάθονται, υπάρχουν 20 GB RAM ελεύθερα και 9 GB
που χρησιμοποιούνται για buffers+cache. Στο μηχάνημα με τη mysql είναι
δύσκολο να μιλήσουμε για RAM γιατί ούτως ή άλλως η mysql καταναλώνει όλη
τη διαθέσιμη, πάντως και πάλι τα 8 CPU κάθονται. Η εκτίμησή μας από αυτό
που βλέπουμε είναι ότι, αν είχαμε γρηγορότερο δίσκο, θα επαρκούσε ένας
server με τις προδιαγραφές που αναφέραμε στην περίληψη παραπάνω.

Όμως το πόσο ζορίζεται το μηχάνημα εξαρτάται και από το τι χρήση κάνουν
αυτοί οι 50 χρήστες, και σίγουρα κάθε οργανισμός είναι διαφορετικός.
Στην περίπτωσή μας, οι μισοί περίπου είναι developers/devops που
χρησιμοποιούν το Nextcloud ελάχιστα, αφού κατά κύριο λόγο δουλεύουν σε
editors και gitlab. Για το δικό σας οργανισμό δεν ξέρουμε, αλλά είναι
πιθανό ούτε εσείς να ξέρετε πριν εγκατασταθεί το σύστημα και το δείτε
στην πράξη.

Σε χώρο δίσκου, βλέπουμε ότι το εγκατεστημένο σύστημα και η MySQL με τα
δεδομένα της καταλαμβάνουν λίγο πάνω από 10 GB, αλλά η MySQL θα
διογκώνεται αργά καθώς περνά ο καιρός. Θεωρούμε λοιπόν ότι 30 GB που
προτείνουμε είναι περίπου το διπλάσιο απ' ό,τι χρειάζεται και θα
καταλήξει σε κατανάλωση χώρου περίπου 50%. Αυτό όμως το νούμερο δεν
περιλαμβάνει τα αρχεία των χρηστών.

#### Matrix/Element/Jitsi

Τα Matrix και Element έχουν μικρές απαιτήσεις. Γενικά 2 CPU, 2 GB RAM,
και 30 GB δίσκος πρέπει να αρκούν για τις περισσότερες χρήσεις.

Για το Jitsi οι απαιτήσεις εξαρτώνται από πολλούς παράγοντες: Πόσοι θα
είναι οι ταυτόχρονοι χρήστες και οι ταυτόχρονες τηλεσυσκέψεις, ποια θα
είναι η ποιότητα της εικόνας, και αν θα υπάρχει δυνατότητα εγγραφής των
τηλεσυσκέψεων, και πόσων τηλεσυσκέψεων ταυτόχρονα (το Jibri, δηλαδή το
component που πραγματοποιεί την εγγραφή, είναι ιδιαίτερα απαιτητικό).
Δεν υπάρχει λόγος να επαναλάβουμε εδώ τις [απαιτήσεις που
προδιαγράφονται στην τεκμηρίωση του
Jitsi](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-requirements/),
που είναι αναλυτικές.

Το component του Jitsi στο οποίο γίνονται οι τηλεσυσκέψεις λέγεται Jitsi
Video Bridge ή JVB. Μπορεί σε μία εγκατάσταση Jitsi να υπάρχουν πολλά
JVB, καθένα σε διαφορετικό server. Μία τηλεσύσκεψη γίνεται μόνο σε ένα
JVB, αλλά όταν γίνονται πολλές ταυτόχρονες συσκέψεις τότε γίνεται load
balancing στα υπάρχοντα JVB. Επομένως μπορεί να θέλετε να προβλέψετε
πολλά μηχανήματα με JVB ανάλογα με το τι περιμένετε. Το toolkit που
χρησιμοποιούμε έχει τον περιορισμό ότι το πρώτο JVB είναι στον ίδιο
server με τα Matrix και Element, όμως ο φόρτος που προκαλούν αυτά τα
δύο είναι αμελητέος σε σχέση με το Jitsi, επομένως αυτό δεν αναμένεται
να είναι πρόβλημα.

### Λειτουργικό σύστημα

Για το Nextcloud, επί του παρόντος υποστηρίζουμε μόνο Debian και Ubuntu.
Για τα Matrix, Element και Jitsi, οι απαιτήσεις σε λειτουργικό σύστημα
αναφέρονται στην αρχή της [τεκμηρίωσης του
toolkit](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/prerequisites.md).

## Περισσότερες πληροφορίες

### Nextcloud

Για την εγκατάσταση του Nextcloud έχουμε τους ρόλους Ansible
[nextcloud](https://gitlab.grnet.gr/digigov-oss/ansible/nextcloud),
[mysql](https://gitlab.grnet.gr/digigov-oss/ansible/mysql) και
[nextcloud-collabora](https://gitlab.grnet.gr/digigov-oss/ansible/nextcloud-collabora). 

Σ' αυτό εδώ το αποθετήριο υπάρχει παράδειγμα Ansible playbook που
χρησιμοποιεί αυτούς τους ρόλους και στήνει Nextcloud σε ένα server (μαζί
με mysql και collabora). Για να το δοκιμάσετε, η διαδικασία είναι η
εξής:

1. Αντιγράψτε το φάκελο `examples/nextcloud-deploy` κάπου αλλού και
   πηγαίνετε εκεί για να κάνετε αλλαγές.
2. Βρείτε όλες τις εμφανίσεις του `example.com` και τροποποιήστε τις
   κατάλληλα.
3. Εγκαταστήστε τα προαπαιτούμενα με `ansible-galaxy install -r
   requirements.yml`.
4. Τρέξτε το playbook με `ansible-playbook site.yml`.

Λεπτομέρειες για το τις διαθέσιμες παραμέτρους θα βρείτε στα README των
άνω ρόλων. Έχουμε κι ένα [FAQ](faq.md) με θέματα που μπορεί να
αντιμετωπίσετε κατά την εγκατάσταση.

### Matrix, Element, Jitsi

Το Matrix είναι ένα πρωτόκολλο (ή σύνολο πρωτοκόλλων), όπως είναι το
email. Ο Matrix Synapse είναι ένας matrix server, όπως ο Postfix είναι
ένας email server. Τέλος, το Element είναι ένας Matrix client, που είναι
μάλιστα web client. Στο παράδειγμα με το email, το αντίστοιχο είναι το
Roundcube.

Για την εγκατάσταση των Matrix (ειδικότερα του Matrix Synapse), Element
και Jitsi χρησιμοποιούμε το δημοφιλές
[matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy).
Η τεκμηρίωσή του είναι εκτενής και παραπέμπουμε σ' αυτό για περισσότερα.
Ειδικότερα, για το Jitsi, είναι χρήσιμη και η [περιγραφή της
αρχιτεκτονικής](https://gitlab.grnet.gr/digigov-oss/ansible/jitsi-meet#jitsi-architecture)
σε ένα Jitsi Ansible module που δημιουργήσαμε παλιότερα (του οποίου τη
χρήση δεν προτείνουμε γιατί είναι ασυντήρητο).

## Εκπαίδευση και υποστήριξη

### Nextcloud

Για τους ρόλους Ansible για Nextcloud και Collabora, υποστήριξη
προσφέρει η ΕΔΥΤΕ (και συγκεκριμένα ο δημιουργός των ρόλων, Αντώνης
Χριστοφίδης, achristofides@admin.grnet.gr).

Εκπαίδευση και υποστήριξη στους χρήστες σας θα πρέπει να προσφέρει ο
οργανισμός σας, δημιουργώντας μια ομάδα υποστήριξης. Η ΕΔΥΤΕ έχει
δημιουργήσει [εκπαιδευτικό
υλικό](https://howto.gov.gr/course/view.php?id=23) με μαθήματα σε
βίντεο. Έχει σχεδιαστεί με επίκεντρο το χρήστη, και περιέχει
παραδείγματα και σενάρια χρήσης της καθημερινής εργασίας. Το υλικό
ενημερώνεται συχνά με κάθε νέα λειτουργία και αλλαγή στα εργαλεία του
toolkit.

Η Nextcloud GmbH προσφέρει υποστήριξη δεύτερου επιπέδου. Η συνήθης ροή
είναι ότι οι χρήστες ζητούν υποστήριξη από την ομάδα υποστήριξης του
οργανισμού. Για θέματα που δεν μπορεί να αντιμετωπίσει η ομάδα
υποστήριξης ρωτάει τους διαχειριστές συστημάτων. Ακολούθως, αν
χρειάζεται, οι διαχειριστές ζητάνε βοήθεια από την υποστήριξη της
Nextcloud.  Το σχετικό προϊόν ονομάζεται [Nextcloud
Enterprise](https://nextcloud.com/enterprise/), πρακτικά όμως είναι
απλώς τεχνική υποστήριξη, αφού ο κώδικας του Nextcloud Enterprise είναι
ακριβώς ο ίδιος με του Nextcloud Community. 

Αν δεν αγοράσετε υποστήριξη από τη Nextcloud, τότε μένουν τα ανεπίσημα
κανάλια, όπως εμείς (η ΕΔΥΤΕ), με όση εμπειρία έχουμε από τη χρήση που
κάνουμε, και το [forum του Nextcloud
community](https://help.nextcloud.com/categories).

### Matrix/Element/Jitsi

Για το matrix-docker-ansible-deploy υπάρχει [υποστήριξη από την
κοινότητα](https://github.com/spantaleev/matrix-docker-ansible-deploy#support).
Όσες φορές χρειαστήκαμε κάτι μας έδωσαν την απάντηση στο σχετικό matrix
room.

Όπως και στο Nextcloud, υποστήριξη στους χρήστες σας θα πρέπει να
προσφέρει μια ομάδα υποστήριξης του οργανισμού. Το εκπαιδευτικό υλικό
που αναφέραμε για το Nextcloud παραπάνω καλύπτει και τα
Matrix/Element/Jitsi. Σύμφωνα με την εμπειρία μας, τα Matrix, Element
και Jitsi λειτουργούν πιο απρόσκοπτα και οι λειτουργίες τους είναι πιο
προφανείς στους χρήστες, με αποτέλεσμα οι ανάγκες υποστήριξης να είναι
μικρότερες σε σχέση με το Nextcloud, ενώ και η υποστήριξη δεύτερου
επιπέδου (πέραν της ανεπίσημης από την κοινότητα) είναι λιγότερο
αναγκαία σε σχέση με το Nextcloud.

## Γνωστά προβλήματα

### Nextcloud

* Σε «διαμοιρασμένα» ημερολόγια, [δεν ενημερώνει τους συμμετέχοντες σε
  events](https://github.com/nextcloud/server/issues/26668).
* Παρόλο που δεν τους ενημερώνει, [ισχυρίζεται ότι τους
  ενημέρωσε](https://github.com/nextcloud/calendar/issues/4983).

### Matrix/Element

* Ενοχλητικά [κόκκινα
  γράμματα](https://github.com/vector-im/element-meta/issues/744) στο
  Element.

### matrix-docker-ansible-deploy

* Λάθη στην [εγκατάσταση δεύτερου
  JVB](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/2513)
  (στο issue αναφέρονται και workarounds).
* Δεν υποστηρίζει (ακόμα) [εγγραφή
  τηλεσυσκέψεων](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/1473).

## Περισσότερες πληροφορίες

* [Εγκατάσταση Nextcloud για τις ανάγκες ενός
  οργανισμού](https://opensource.ellak.gr/2021/05/03/nextcloud-installation-for-the-needs-of-an-organization/)
  (άρθρο Χρήστου Καραμολέγκου από Μάιο 2021).

## Άδεια χρήσης για το παρόν

Αρμόδιος γι' αυτό το κείμενο είναι ο Αντώνης Χριστοφίδης,
achristofides@admin.grnet.gr.

© 2023 ΕΔΥΤΕ

Έχετε άδεια να αντιγράφετε, να διανέμετε και να τροποποιείτε το κείμενο
υπό τους όρους της άδειας χρήσης [CC BY-SA Greece
3.0](https://creativecommons.org/licenses/by-sa/3.0/gr/), και τα
παραδείγματα υπό τους όρους του [CC0
1.0](http://creativecommons.org/publicdomain/zero/1.0/).
