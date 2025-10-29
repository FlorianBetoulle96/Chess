# Chess Analyzer

Ce dépôt contient deux projets complémentaires d’analyse automatisée autour du moteur Stockfish et de données issues de parties d’échecs personnelles.
L’objectif global est de mesurer et comprendre les erreurs récurrentes dans les ouvertures, ainsi que d’évaluer les performances de Stockfish selon différents temps de calcul.
## 1. My_Opening_Mistakes

**Objectif :**
Identifier les positions d’ouverture où tu joues régulièrement un coup qui dégrade significativement la position, par rapport au meilleur coup suggéré par Stockfish.

**Fonctionnement :**

Le projet lit une liste de positions FEN (une par ligne) issues de tes parties.

Pour chaque position, Stockfish évalue la position actuelle et la meilleure continuation.

Les résultats sont nettoyés, agrégés et analysés via un script SQL.

**Configuration :**

Remplacer le fichier d’entrée (multiples_fens_stockfish.txt) par ta propre liste de FENs.

Ce fichier peut être exporté depuis chess.com
 ou tout autre site d’analyse PGN/FEN.

Le fichier doit contenir une FEN par ligne, sans guillemets.

**Exécution :**
Les fichiers Python sont à exécuter dans l’ordre numérique

**Résultats**
Un tableau avec comme colonnes : La position FEN, si vous êtes les blancs ou les noirs, votre move et son eval, le move de Stockfish et son eval, la différence d'évaluation, la récurrence de cette position
Avec ça vous pouvez copier-coller le FEN sur chess.com (ou autres) pour le visualiser et éventuellement l'analyser ou le sauvegarder.

## 2. Stockfish Performance Analysis

**Objectif :**
Comparer les performances de Stockfish (score d’évaluation et temps de calcul) selon différents temps d’exécution ou niveaux de profondeur.

**Fonctionnement :**

Plusieurs configurations de temps (ex. 0.1s, 0.5s, 1s, etc.) sont testées sur un même ensemble de positions.

Les résultats permettent d’identifier le meilleur compromis entre vitesse et précision d’évaluation.

**Exécution :**
Même principe : lancer les scripts Python dans l’ordre

**Résultats**
Un tableau avec une ligne par temps d'exécution et les colonnes : 
l'estimation d'elo, la moyenne de score en centipions, le pourcentage d'évaluations de Stockfish qui donne le même move, la différence moyenne d'évaluation, le plus grand écart d'évaluation
Ce qui est intéressant est de voir que la moyenne d'évaluation augmente avec l'elo -> **un gros élo est capable de plus facilement convertir son avantage**
Autres observations moins percutantes : 
- la différence moyenne d'évaluation s'améliore plus lentement que la différence maximale entre 2 évaluations
- le pourcentage de moves similaires s'améliore progressivement pour atteindre presque 100% à 2800+ elos

## Pré-requis

Bibliothèques Python :

pip install chess
pip install chess.engine
