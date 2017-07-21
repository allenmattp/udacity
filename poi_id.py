#!/usr/bin/python

import sys
import pickle
import matplotlib.pyplot as plt
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

financial_features =  ['salary', 'deferral_payments', 'total_payments', 
'loan_advances', 'bonus', 'restricted_stock_deferred', 'deferred_income', 
'total_stock_value', 'expenses', 'exercised_stock_options', 
'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

# text feature 'email_address' removed
email_features = ['to_messages', 'from_poi_to_this_person', 
'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']

my_feature_list = ['salary_vs_totalcomp', 'salary_vs_bonus', 
'pct_to_poi', 'ex_stock_vs_total', 'salary_vs_def_pay', 'salary_vs_def_inc',
'def_inc_vs_total', 'def_pay_vs_stock']

features_list = ['poi', 'exercised_stock_options', 'total_payments', 'pct_to_poi' ]

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
    
### Task 2: Remove outliers
data_dict.pop('TOTAL', 0) # Remove the 'Total' entry for dataset

def count_NaN(feature):
    """ given a feature,
        return the number of entries
        with a value of 'NaN'
    """
    nan_count = 0
    for key in data_dict:
        if data_dict[key][feature] == 'NaN':
            nan_count += 1
    print feature, nan_count

### Count the number of 'NaN' values in a feature or list of features
# for f in financial_features:
#    count_NaN(f)

#for f in email_features:
#    count_NaN(f)


### Task 3: Create new feature(s)

def compute_ratio(num, den):
    """ given a numerical feature (num)erator
        that is a subset of another numerical feature (den)ominator,
        return the ratio of those two features
        if either feature missing, return 0
    """
    ratio = 0.
    if num == 'NaN' or den == 'NaN':
        pass
    else:
        ratio = float(num) / float(den)
    return ratio

def add_feature(num_feat, den_feat, new_feat):
    """ given a numerical (num)erator (feat)ure
        that is a subset of another numerical (den)ominator (feat)ure,
        add their ratio (via compute_ratio) 
        as a (new feat)ure to data_dict
    """
    for name in data_dict:
    
        data_point = data_dict[name]
        num = data_point[num_feat]
        den = data_point[den_feat]
        ratio = compute_ratio(num, den)
        data_point[new_feat] = ratio

### Add features to dataset 
add_feature('salary', 'total_payments', 'salary_vs_totalcomp')
add_feature('salary', 'bonus', 'salary_vs_bonus')
add_feature('from_this_person_to_poi', 'to_messages', 'pct_to_poi')
add_feature('exercised_stock_options', 'total_payments', 'ex_stock_vs_total')
add_feature('salary', 'deferral_payments', 'salary_vs_def_pay')
add_feature('salary', 'deferred_income', 'salary_vs_def_inc')
add_feature('deferred_income', 'total_payments', 'def_inc_vs_total')
add_feature('deferral_payments', 'total_stock_value', 'def_pay_vs_stock')

# from sklearn.preprocessing import MinMaxScaler
# scaler = MinMaxScaler()
# rescaled_feature = scaler.fit_transform(feature)


### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Uncomment to plot first feature against POI
# for point in data:
#     poi = point[0]
#     feature = point[1]
#     plt.scatter( poi, feature )
# plt.xlabel("POI?")
# plt.ylabel("Feature")
# plt.show()

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn import svm
from sklearn.ensemble import GradientBoostingClassifier, ExtraTreesClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score as acc
#clf = GaussianNB()
#clf = svm.SVC(kernel='rbf')
#clf = tree.DecisionTreeClassifier()
#clf = RandomForestClassifier(n_estimators = 500, max_features = None, max_depth = 3, min_samples_leaf = 1)
clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, 
                                 max_depth=1, min_samples_split=10)
#clf = ExtraTreesClassifier(n_estimators = 10, max_features = 'auto', max_depth = 50, min_samples_leaf = 1)



### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

clf = clf.fit(features_train, labels_train)
pred = clf.predict(features_test)

print "Accuracy Score: ", acc(pred, labels_test)

from sklearn.model_selection import GridSearchCV

param_grid = [
        { 
    'n_estimators': [10, 50, 100, 500, 1000,],
    'max_depth': [1, 3, 10, 25, 50],
    'min_samples_leaf': [1, 5, 10],
    'max_features': ['auto', 'sqrt', 'log2', None]
    }]
#cv_clf = GridSearchCV(estimator=clf, param_grid=param_grid, scoring='recall')
#cv_clf.fit(features_train, labels_train)

#print cv_clf.best_params_
    

### Evaluate feature_importances for decision tree
#features_imp = clf.feature_importances_
#location = 0
#for f in features_imp:
#    if f > 0.2:
#        print f, location
#    location += 1

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)