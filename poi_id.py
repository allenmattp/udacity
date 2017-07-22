#!/usr/bin/python

import sys
import pickle
import matplotlib.pyplot as plt
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### The first feature must be "poi".

features_list = ['poi', 'bonus', 'total_stock_value', 'exercised_stock_options']

with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
    
### Task 2: Remove outliers
data_dict.pop('TOTAL', 0)
data_dict.pop('THE TRAVEL AGENCY IN THE PARK', 0)
data_dict.pop('LOCKHART EUGENE E', 0)

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
#for f in financial_features:
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
add_feature('bonus', 'total_payments', 'bonus_vs_totalcomp')
add_feature('salary', 'total_payments', 'salary_vs_totalcomp')
add_feature('salary', 'bonus', 'salary_vs_bonus')
add_feature('salary', 'total_stock_value', 'salary_vs_stock')
add_feature('salary', 'exercised_stock_options', 'salary_vs_ex_stock')
add_feature('exercised_stock_options', 'total_payments', 'ex_stock_vs_total_pay')
add_feature('exercised_stock_options', 'total_stock_value', 'ex_stock_vs_total_stock')
add_feature('from_this_person_to_poi', 'to_messages', 'pct_to_poi')

# from sklearn.preprocessing import MinMaxScaler
# scaler = MinMaxScaler()
# rescaled_feature = scaler.fit_transform(feature)


### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

def plot_feature(data):
    """ show a scatterplot with the
        first (x-axis) and second (y-axis)
        element of list (data)
    """
    for point in data:
        poi = point[0]
        feature = point[1]
        plt.scatter( poi, feature )
    plt.xlabel("POI?")
    plt.ylabel("Feature") 
    plt.show()

### Task 4: Try a varity of classifiers

from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.metrics import accuracy_score as acc
#clf = GaussianNB()
clf = tree.DecisionTreeClassifier(max_depth = 10, min_samples_leaf = 1, max_features='auto', min_samples_split = 2)

from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

clf = clf.fit(features_train, labels_train)
pred = clf.predict(features_test)

print "Accuracy Score: ", acc(pred, labels_test)

"""
from sklearn.model_selection import GridSearchCV

param_grid = [
        { 
   'max_features': ['auto', 'sqrt', 'log2', None],
    'max_depth': [1, 3, 10, 25, 50],
    'min_samples_split': [2, 5, 10, 25],
    'min_samples_leaf': [1, 5, 10],
    }]
cv_clf = GridSearchCV(estimator=clf, param_grid=param_grid, scoring='recall')
cv_clf.fit(features_train, labels_train)

print cv_clf.best_params_
"""   

"""
Evaluate feature_importances for decision tree
features_imp = clf.feature_importances_
location = 0
for f in features_imp:
    print features_list[location], f
    location += 1
"""

dump_classifier_and_data(clf, my_dataset, features_list)