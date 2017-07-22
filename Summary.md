# 1. Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?

Enron was an enormous company and the majority of its employees were neither
aware nor involved in fraudulent activity. Similarly, our dataset is huge and
most of the individuals included within were uninvolved in the fraud and 
consequently of little interest to our investigation. 

The dataset contains 146 records. From these, three were removed as outliers: 
'TOTAL' was removed as it contained the aggregate of all values, 
'THE TRAVEL AGENCY IN THE PARK' was removed as it's not a person, and 
'LOCKHART EUGENE E' was removed as he had no values associated with any of 
his features. There are certainly other outliers found within the dataset 
(e.g. Kenneth Lay with $80,000,000 in loan advances compared $2,000,000 for 
the next greatest amount, or David Haug with millions in stock but no salary) 
but these are untouched as they are meaningful information.

Of the 143 individuals, 18 are identified as POI based on outside criteria 
(indictments, settlements or immunity deals). Included for each data point are 
21 features. However, many features are missing data points:

| feature | missing values |
| ------- | --------------:|
| salary | 49 |
| deferral_payments | 105 |
| total_payments | 20 |
| loan_advances | 140 |
| bonus | 62 |
| restricted_stock_deferred | 126 |
| deferred_income | 95 |
| total_stock_value | 18 |
| expenses | 49 |
| exercised_stock_options | 42 |
| other | 52 |
| long_term_incentive | 78 |
| restricted_stock | 34 |
| director_fees | 127 |
| to_messages | 57 |
| from_poi_to_this_person | 57 |
| from_messages | 57 |
| from_this_person_to_poi | 57 |
| shared_receipt_with_poi | 57 |

This project seeks to sift through the enormous amount of data contained 
within our set and identify the persons of interest (POI). Machine Learning is 
useful in accomplishing this as, if we assume the POI possess specific 
features that distinguish them from the rest of the population, we can tune 
and train our algorithm to identify them. 

# 2. What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it. (You do not necessarily have to use it in the final analysis, only engineer and test it.) In your feature selection step, if you used an algorithm like a decision tree, please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, please report the feature scores and reasons for your choice of parameter values.

To select features I deployed a decision tree with default parameters, using 
most features (all but loan_advances, director_fees, restricted_stock_deferred 
due to their small size, and email_address due to type). With all these features, 
the decision tree scored:

| Algorithm | Accuracy | Precision | Recall |
| --------- | -------- | --------- | ------ |
| Decision Tree | .80 | .23 | .22 |

I then ran feature_importances_ attribute ten times, making note of features 
that scored at least .2:

| Feature | Frequency |
| ------- | --------- |
| total_payments | XXXXXXXXXX | 
| bonus | XXXXX | 
| exercised_stock_options | XXXXX | 
| total_stock_value | XX | 

Removing all but these features, the decision tree scored:

| Algorithm | Accuracy | Precision | Recall |
| --------- | -------- | --------- | ------ |
| Decision Tree | .82 | .33 | .33 |

We're already within specifications! Let's try these features with the Naive 
Bayes (the SVC was unable to return sufficient true positive predictions):

| Algorithm | Accuracy | Precision | Recall |
| --------- | -------- | --------- | ------ |
| GaussianNB | .86 | .46 | .26 |

No feature scaling was performed for multiple reasons: There was a wide range 
of values in both the financial and email feature. Many features contained 
some sort of outlier and most were missing a substantial number of values. 
Additionally, because the financial features are all measured in US Dollars, 
and (with the exception of the emails provided as text) the email features are 
measured in quantity of emails, each type of feature already resides in a 
consistent scale.

In order to uncover further insights, I created a function to compare existing 
features to each other. None of the email features made it through the 
feature_importances_ test, so I first wanted to see if I could create new 
email feature that proved useful:

I compared the number of emails the individual wrote to POI versus their total 
outgoing messages and named the new feature 'pct_to_poi'.

| Algorithm | Accuracy | Precision | Recall |
| --------- | -------- | --------- | ------ |
| GaussianNB | .86 | .46 | .26 |
| Decision Tree | .82 | .33 | .33 |

No improvement. Next, because I felt exercised stock options and total stock 
value described similar things, I sought to combine them into a single feature. 
I created 'ex_stock_vs_total_stock', which divided an individual's exercised 
stock options by their total stock value. Adding it to the feature list did little:

| Algorithm | Accuracy | Precision | Recall |
| --------- | -------- | --------- | ------ |
| GaussianNB | .86 | .46 | .26 |
| Decision Tree | .82 | .33 | .33 |

Replacing total stock value and exercised stock options with the single feature 
was counterproductive:

| Algorithm | Accuracy | Precision | Recall |
| --------- | -------- | --------- | ------ |
| GaussianNB | .84| .36| .14|
| Decision Tree | .78| .27| .29|

Changing tack, I decided to test my algorithms by removing some of the remaining
 4 features:

| Algorithm | sans total_payments | sans bonus | sans total_stock_value | sans exercised_stock_options |
| --------- | -------- | --------- | ------ | ------- |
| GaussianNB | .84/.49/.35 | .85/.39/.23 | .85/.45/.24 | .85/.39/.23 |
| Decision Tree | .80/.36/.39 | .83/.35/.36 | .79/.30/.34 | .81/.30/.29 |

Surprising to me was how much removing total_payments improved each algorithm. 
Removing bonus was also interesting, although removing both at the same time
did not help:

| Algorithm | Accuracy | Precision | Recall |
| --------- | -------- | --------- | ------ |
| GaussianNB | .84| .47 | .27 |
| Decision Tree | .77| .22| .20 |

Trying to replace both with a new feature, Bonus / Total Payments, 
was better but still not good:

| Algorithm | Accuracy | Precision | Recall |
| --------- | -------- | --------- | ------ |
| GaussianNB | .84| .47 | .29 |
| Decision Tree | .77| .27| .29 |

I moved forward using:

| Feature | Importance |
| ------- | ----- |
| poi | 0.254017926911 |
| bonus | 0.37436442603 |
| total_stock_value | 0.281266968326 |
| exercised_stock_options | 0.090350678733 |

Note: Dropping exercised_stock_options and using just bonus/total_stock_value 
doesn't change the Decision Trees performance much, but damaages recall for 
the Naive Bayes.

# 3. What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?
and
# 4. What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?  How did you tune the parameters of your particular algorithm? What parameters did you tune? (Some algorithms do not have parameters that you need to tune -- if this is the case for the one you picked, identify and briefly explain how you would have done it for the model that was not your final choice or a different model that does utilize parameter tuning, e.g. a decision tree classifier).

I was able to quickly discard SVM for this task as it was not able to predict 
any true positives out of the box. I began using a Naive Bayes classifier 
because it is easy to implement and I did not think it would be prone to 
breaking with this dataset. It provided a useful starting point to become 
more comfortable with the dataset and begin to gain an understanding of 
how the features behaved. However, in order to more systematically approach 
feature selection, I implemented a decision tree so that I could utilize its 
features_importances_ attribute. The Naive Bayes was generally more precise, 
while the decision tree had better recall. 

Every dataset is different, and so by necessity the optimal classifier will 
have its parameters tuned so that it can complete the specific learning tesk 
in the best way possible. While many algorithims work pretty well using their 
default parameters, in order to produce "better" (the definition of better will 
change depending on the task) results tuning the model is necessary. In order 
to find the "best" set of parameters, one might manually experiment with 
different parameter settings, or they might utilize a built-in method such as 
GridSearchCV to exhuastively search over specified parameters. Failure to 
tune parameters may result in a classifier that is unable to make useful 
predictions or just works sub-optimally. 

The GaussianNB() does not have parameters to tune and was meeting 
specifications with my selected features.

In order to improve the Decision Tree, I utilized the GridSearchCV method to 
suggest values for the max_depth, min_samples_leaf, max_features and 
min_samples_split parameters. Making these changes improved my classifier:

| Algorithm | Accuracy | Precision | Recall |
| --------- | -------- | --------- | ------ |
| Default | .80| .36 | .39 |
| Optimized | .82| .41| .42 |


```
tree.DecisionTreeClassifier(max_depth = 10, min_samples_leaf = 1, 
							max_features='auto', min_samples_split = 2)

```

While not as precise as the Naive Bayes, the tuned Decision Tree exceeds .40
in both precision and necall.

# 5. What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis?

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

# 6. Give at least 2 evaluation metrics and your average performance for each of them.  Explain an interpretation of your metrics that says something human-understandable about your algorithm’s performance. 

The metrics I used to evaluate my classifier were accuracy, precision and 
recall. Accuracy is the most straightforward of the three; it simply tells us 
what percentage of the total sample size did we predict correctly. This 
usually provides a good indication of how well we're doing, but is 
unsatisfcatory for the current task. Because the dataset largely consists of 
individuals who are not POI, we could create a relatively accurate algorithm 
that simply identifies everyone as a non-POI. For a better idea of how our 
classifier performs, we'll also use Precision and Recall.

Precision is an indicator of how confident we can be that a person labeled POI 
actually is POI. If our goal was to only label indvidials as POI if we were 
nearly certain that they actually were POI (ie we want to avoid false 
accusations), we would endeavor to construct a classifier with a very high 
precision.

Recall measures how well we avoid missing POIs. If our investigation simply 
wanted to identify persons who we might want to question (not necessarily 
charge), casting a wider net and seeking out a higher Recall would be 
important.

# References

This project was completed using the sklearn documentation and the Udacity
course videos.
