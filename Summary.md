# 1. Summarize for us the goal of this project and how machine learning is 
useful in trying to accomplish it. As part of your answer, give some 
background on the dataset and how it can be used to answer the project 
question. Were there any outliers in the data when you got it, and how did you
 handle those?

Enron was an enormous company and the majority of its employees were neither
aware nor involved in fraudulent activity. Similarly, our dataset is huge and
most of the individuals included within were uninvolved in the fraud and 
consequently of little interest to our investigation. 

The dataset contains 146 records: 145 unique individuals and one 'TOTAL' entry 
that is removed for the purpose of this task. There are certainly other 
outliers found within the dataset (e.g. Kenneth Lay with $80,000,000 in loan 
advances compared $2,000,000 for the next greatest amount, or David Haug with 
millions in stock but no salary) but these are untouched as they are 
meaningful information.

Of the 145 individuals, 18 are identified as POI based on outside criteria 
(indictments, settlements or immunity deals). Included for each data point are 
21 features. However, many features are missing data points:

* feature | missing values
* salary | 51
* deferral_payments | 107
* total_payments | 21
* loan_advances | 142
* bonus | 64
* restricted_stock_deferred | 128
* deferred_income | 97
* total_stock_value | 20
* expenses | 51
* exercised_stock_options | 44
* other | 53
* long_term_incentive | 80
* restricted_stock | 36
* director_fees | 129
* to_messages | 59
* from_poi_to_this_person | 59
* from_messages | 59
* from_this_person_to_poi | 59
* shared_receipt_with_poi | 59

This project seeks to sift through the enormous amount of data contained 
within our set and identify the persons of interest (POI). Machine Learning is 
useful in accomplishing this as, if we assume the POI possess specific 
features that distinguish them from the rest of the population, we can tune 
and train our algorithm to identify them. 

# 2. What features did you end up using in your POI identifier, and what 
selection process did you use to pick them? Did you have to do any scaling? 
Why or why not? As part of the assignment, you should attempt to engineer your 
own feature that does not come ready-made in the dataset -- explain what 
feature you tried to make, and the rationale behind it. (You do not 
necessarily have to use it in the final analysis, only engineer and test it.) 
In your feature selection step, if you used an algorithm like a decision tree, 
please also give the feature importances of the features that you use, and if 
you used an automated feature selection function like SelectKBest, please 
report the feature scores and reasons for your choice of parameter values.

My POI identifier utilizes the features 'exercised_stock_options', 
'total_payments' and the ratio of 'from_this_person_to_poi' and 'to_messages' 
('pct_to_poi'). To select these features, I used a decision tree algorithm 
with all available finance features. Using the features_importances_ attribute 
of decision trees I identified features with values greater than .2 and 
systematically removed these:

All financial features: 'loan_advances', .2204 and 'total_stock_value', .2385

next: 'total_payments', .2941; 'restricted_stock_deferred', .2120; 
'exercised_stock_options', .2387

next: 'deferral_payments', .2381; 'bonus', .2598; 'deferred_income', .2828

next: 'salary', .4902

next: 'other', .2368

I repeated this process for the email features:

All email features: 'to_messages', .2372; 'from_poi_to_this_person', .2451; 
'from_messages', .2417; 'from_this_person_to_poi', .2587

I then used my decision tree classifier with each of these features 
individually, plotting them to perform an eye test and taking note of their 
accuracy score. Some features were dismissed outright due to low sample size 
(eg loan_advances, which only contained information on 3 individuals), others 
because they would cause overfitting (eg restricted_stock_deferred, which 
contained values for 17 non-POI but no POI).

No feature scaling was performed for multiple reasons: There was a wide range 
of values in both the financial and email feature. Many features contained 
some sort of outlier and most were missing a substantial number of values. 
Additionally, because the financial features are all measured in US Dollars, 
and (with the exception of the emails provided as text) the email features are 
measured in quantity of emails, each type of feature already resides in a 
consistent scale.

In order to uncover further insights, I created a function to compare existing 
features to each other. Examples included:

salary / total_payments in order to get a sense of how much of an individual's 
total compensation was made up by their base salary.

salary / bonus to get a sense of how their base salary compared to the size of 
their bonus.

from_this_person_to_poi / to_messages to measure what percentage of outgoing 
messages were sent to POIs.

Through experimentation, most of these new features did not perform any better 
than existing features. The effort was not wasted however, as the new feature 
'pct_to_poi' is used in my classifier.

# 3. What algorithm did you end up using? What other one(s) did you try? How 
did model performance differ between algorithms?
and
# 4. What does it mean to tune the parameters of an algorithm, and what can 
happen if you don’t do this well?  How did you tune the parameters of your 
particular algorithm? What parameters did you tune? (Some algorithms do not 
have parameters that you need to tune -- if this is the case for the one you 
picked, identify and briefly explain how you would have done it for the model 
that was not your final choice or a different model that does utilize 
parameter tuning, e.g. a decision tree classifier).

I was able to quickly discard SVM for this task as it was not able to predict 
any true positives out of the box. I began using a Naive Bayes classifier 
because it is easy to implement and I did not think it would be prone to 
breaking with this dataset. While its accuracy was usually near .80 for 
accuracy with precision and recall scores under .3, it provided a useful 
starting point to become more comfortable with the dataset and begin to gain 
an understanding of how the features behaved. However, in order to more 
systematically approach feature selection, I implemented a decision tree so 
that I could utilize its features_importances_ attribute. While both 
algorithms performed similarly for Accuracy and Precision, the Decision Tree 
outperformed the Naive Bayes in terms of Recall.

Committed to the decision tree, I utilized ensemble algorithms in order to 
boost the performance of my algorithm. Using their default parameters, 
ExtraTrees and Random Forest each increased Precision by over 10 points but 
lost more than that in Recall performance. Due to its robusiness to outliers, 
I also implemented a Gradient Tree Boosting classifier which improved 
Precision without sacrificing Recall. 

Every dataset will be different, and so by necessity the optimal classifier 
needs to be calibrated. Failure to do so can produce a classifier that is 
either unable to usefully make predictions or to properly generalize. In order 
to optimize my algorithms, I employed the GridSearchCV method and was able to 
produce the following scores for each:

Algorithm | Default(Accuracy, Precision, Recall) | Optimized(Accuracy, 
Precision, Recall)
RandomForest: (.87, .55, .23) | (.87, .58, .23)
ExtraTrees: (.87, .55, .28) | (.87, .53, .28)
GradientBoosting: (.85, .45, .35) | (.87, .61, .18)

While some categories improved, overall performance did not. I then realized 
that the GridSearch was optimizing for the default metric, which is not 
optimal for our task at hand. Because Recall has been the biggest challenge, I 
set GridSearch's parameter accordingly and retuned GradientBoosting:

(.86, .46, .31)

Still not ideal. After manually tuning the parameters, my classifier usually 
returned .87, .50, .37 ... take that, GridSearchCV.

It was challenging to do, as I found that nearly every improvement in recall 
was at the expense of precision. However, this is an intuitive trade-off!

# 5. What is validation, and what’s a classic mistake you can make if you do 
it wrong? How did you validate your analysis?

Validation is important as it gives us an estimate of how our classifier will 
perform on an independent dataset, and it helps to prevent us from overfitting 
our algorithm to the data we have. If an algorithm is overfit, it will appear 
to make very accurate predictions. However, once applied to foreign data, its 
accuracy will plummet.

This exercise uses sklearn's train_test_split method from cross_validation. 
This splits the data into two sets: one for training the algorithm and a 
smaller section for testing. Although this reduces the size of an already 
small dataset, one can use a stratified shuffle split cross validation. This 
randomly performs the cross validation multiple times and returns its average 
in order to realize its benefits while still utilizing all of the data.

# 6. Give at least 2 evaluation metrics and your average performance for each 
of them.  Explain an interpretation of your metrics that says something 
human-understandable about your algorithm’s performance. 

The metrics I used to evaluate my classifier were accuracy, precision and 
recall. Accuracy is the most straightforward of the three; it simply tells us 
what percentage of the total sample size did we predict correctly. This 
usually provides a good indication of how well we're doing, but is 
unsatisfcatory for the current task. Because the dataset largely consists of 
individuals who are not POI, we could create a relatively accurate algorithm 
that simply identifies everyone as a non-POI. For a better idea of how our 
classifier performs, we'll also use Precision and Recall.

Precision, where all three of the ensemble decision trees fared well, is an 
indicator of how confident we can be that a person labeled POI actually is 
POI. If our goal was to only label indvidials as POI if we were nearly certain 
that they actually were POI (ie we want to avoid false accusations), we would 
endeavor to construct a classifier with a very high precision.

Recall was a challenge for most of the decision trees. Recall measures how 
well we avoid missing POIs. If our investigation simply wanted to identify 
persons who we might want to question (not necessarily charge), casting a 
wider net and seeking out a higher Recall would be important.

# References

This project was completed using the sklearn documentation and the Udacity 
course videos.