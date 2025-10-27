'''
essentially we used boosting and bagging
- list out the actos of each row
- keep the actors with the highest occurences
- take the top 100 actors
- use multi hot encoding to represent the presence of each actor in the movie
- target encoding for the rest of the actors what is it ?


tmom hanks1: 40
tom hanks2: 35
tom hanks3: 30

then multihot encoding

a1 a2 a3 other_column
1 1 0 0 0
0 0 0 0 1

those 100 columsn are a seperate dataframe and then you concatinate it to the original dataframe,
this allows to know for each movie which, if any, one of the top 100 actors are in the movie

target encoding:
I accessed all rows where the column for which the tomhanks actor is 1, and calculated the average of the rating for those rows, this essentially gives me the average rating for movies with tom hanks in them ( its as if it's a rating for the actor itself )

we access movie 1,
we saw the actors of the movie,
we compared the averages of the actors for a given movie,

max_rating, min_rating, average_rating

max_rating is the one for the most succeffull actor
min_rating is the ...
average is the avergage of those

after this process, for each row, the model will now for a given max_rating, min_rating and average_rating

hadi, [hadi1, hadi2, hadi3], 50, 20, 35
hadi, [hadi1, hadi2, hadi3], 50, 20, 35
hadi, [hadi1, hadi2, hadi3], 50, 20, 35
hadi, [hadi1, hadi2, hadi3], 50, 20, 35

what is cross validation?
Cross-validation is a statistical method used to estimate the skill of machine learning models. It is primarily used in scenarios where the goal is to assess how the results of a predictive model will generalize to an independent dataset. The most common form of cross-validation is k-fold cross-validation, where the dataset is divided into 'k' subsets (or folds). The model is trained on 'k-1' folds and tested on the remaining fold. This process is repeated 'k' times, with each fold being used as the test set once. The results from each iteration are then averaged to produce a single performance metric. This technique helps in mitigating overfitting and provides a more reliable estimate of model performance compared to a single train-test split.
'''
