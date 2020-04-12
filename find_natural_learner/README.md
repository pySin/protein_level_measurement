Find a natural learner

In the protein data (https://www.kaggle.com/ruslankl/mice-protein-expression) table we  have protein levels divided by class.
One of the classes is called 'stimulated to learn'. The average protein levels for the stimulated to learn mouse will be compared
with the average protein levels for every normal mouse. The mouse which has protein levels closest to the stimulated to learn
levels is our natural learner.


##Setup

* The file 'normal_genetic_learner.csv' is produced by the script 'normal_genetic_learner.py'.
* The file 'stimulated_protein_difference.csv'. This CSV file contains data about the average protein levels for stimulated to
learn mice and for individual normal mouse. The lower the difference between the two the closer that individual mouse is to the
stimulated mouse profile.
* This (natural_learner_results.csv) CSV file show the overall difference between the average protein levels for stimulated mouse and individual normal mice.
* The file 'natural_learner_winner.csv' shows the winner mouse closest to the average stimulated mouse protein levels profile.
