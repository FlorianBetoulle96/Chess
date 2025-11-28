♟️ Chess Analyzer

Ce dépôt contient deux projets complémentaires d’analyse automatisée autour du moteur Stockfish et de données issues de parties d’échecs personnelles.
L’objectif global est de mesurer et comprendre les erreurs récurrentes dans les ouvertures, ainsi que d’évaluer les performances de Stockfish selon différents temps de calcul.

🧠 1. My Opening Mistakes

Objectif :
Identifier les positions d’ouverture où tu joues régulièrement un coup qui dégrade significativement la position, par rapport au meilleur coup suggéré par Stockfish.

Fonctionnement :

Le projet lit une liste de positions FEN (une par ligne) issues de tes parties.

Pour chaque position, Stockfish évalue la position actuelle et la meilleure continuation.

Les résultats sont nettoyés, agrégés et analysés via un script SQL.

Configuration :

Remplacer le fichier d’entrée (multiples_fens_stockfish.txt) par ta propre liste de FENs.

Ce fichier peut être exporté depuis chess.com
 ou tout autre site d’analyse PGN/FEN.

Le fichier doit contenir une FEN par ligne, sans guillemets.

Exécution :
Les fichiers Python sont à exécuter dans l’ordre numérique


⚙️ 2. Stockfish Performance Analysis

Objectif :
Comparer les performances de Stockfish (score d’évaluation et temps de calcul) selon différents temps d’exécution ou niveaux de profondeur.

Fonctionnement :

Plusieurs configurations de temps (ex. 0.1s, 0.5s, 1s, etc.) sont testées sur un même ensemble de positions.

Les résultats permettent d’identifier le meilleur compromis entre vitesse et précision d’évaluation.

Exécution :
Même principe : lancer les scripts Python dans l’ordre


🧩 Pré-requis

Bibliothèques Python :

pip install chess
pip install chess.engine
