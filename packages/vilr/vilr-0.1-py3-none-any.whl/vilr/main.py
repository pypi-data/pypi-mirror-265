def slr():
    x='''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)
from sklearn.metrics import mean_squared_error, r2_score

dataset = pd.read_csv('SAT to GPA.csv') 
dataset.head()


print("The shape of the Dataset")
print(dataset.shape)
print(" ")

print("The staistical Inference of the dataset")
print(dataset.describe())
print(" ")

print("Datatypes in the dataset")
print(dataset.info())
print(" ")

fig, ax = plt.subplots(2,1, figsize=(10,8))

sns.boxplot(ax= ax[0],x=dataset['SAT Score'])
sns.boxplot(ax=ax[1],x=dataset['GPA']) 
plt.show()


dups=dataset.duplicated()
print('number of duplicate rows = %d' % (dups.sum())) 
dataset.drop_duplicates(inplace=True) 

dataset.isnull().sum() 

X = dataset.iloc[:, :-1] 
y = dataset.iloc[:, -1] 


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0) 


print('X_train', X_train.shape)
print('X_test', X_test.shape)
print('train_labels', y_train.shape)
print('test_labels', y_test.shape)


from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)


print('slope:', regressor.coef_)
print("y-intercept: ", regressor.intercept_)

y_pred = regressor.predict(X_test) 


dataframe_training = pd.DataFrame()
dataframe_training['SAT Score'] = X_train['SAT Score']
dataframe_training['GPA'] = y_train 
ax = sns.regplot(x="SAT Score", y="GPA", data= dataframe_training)


dataframe_test = pd.DataFrame()
dataframe_test['SAT Score'] = X_test['SAT Score']
dataframe_test['GPA'] = y_test
ax = sns.regplot(x="SAT Score", y="GPA", data= dataframe_test)


print("Mean squared error: {}".format(mean_squared_error(y_test, y_pred)))
print("R square: {}".format(r2_score(y_test, y_pred)))

'''
    print(x)

def mlr():
    x='''import pandas as pd
data_set= pd.read_csv('Advertising.csv')

data_set.head()
x= data_set.iloc[:, :-1].values  
y= data_set.iloc[:, 3].values 

from sklearn.model_selection import train_test_split  
x_train, x_test, y_train, y_test= train_test_split(x, y, test_size= 0.3, random_state=0) 

from sklearn.linear_model import LinearRegression  
regressor= LinearRegression()  
regressor.fit(x_train, y_train) 

y_pred= regressor.predict(x_test) 

print('Train Score: ', regressor.score(x_train, y_train))  
print('Test Score: ', regressor.score(x_test, y_test))

print("Mean squared error: {}".format(mean_squared_error(y_test, y_pred))) # comparing y_pred with y_test
print("R square: {}".format(r2_score(y_test, y_pred)))

print('slope:', regressor.coef_)
print("y-intercept: ", regressor.intercept_)

'''
    print(x)

def pr():
    x='''data_set= pd.read_csv('Salary_Data.csv')
data_set.head()

X = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1] 

from sklearn.linear_model import LinearRegression
lin_reg = LinearRegression()
lin_reg.fit(X, y)

from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree = 4)
X_poly = poly_reg.fit_transform(X)
lin_reg_2 = LinearRegression()
lin_reg_2.fit(X_poly, y)

plt.scatter(X, y, color = 'red')
plt.plot(X, lin_reg.predict(X), color = 'blue')
plt.title('Linear Regression')
plt.xlabel('Experience')
plt.ylabel('Salary')
plt.show()

plt.scatter(X, y, color = 'red')
plt.plot(X, lin_reg_2.predict(poly_reg.fit_transform(X)), color = 'blue')
plt.title('Polynomial Regression')
plt.xlabel('Experience')
plt.ylabel('Salary')
plt.show()

print('slope:', lin_reg_2.coef_)
print("y-intercept: ", lin_reg_2.intercept_)

from sklearn.model_selection import train_test_split  
x_train, x_test, y_train, y_test= train_test_split(X, y, test_size= 0.2, random_state=0) 

lin_reg_2.fit(x_train, y_train) 
y_pred_poly= lin_reg_2.predict(x_test)

print("Mean squared error: {}".format(mean_squared_error(y_test, y_pred_poly)))
print("R square: {}".format(r2_score(y_test, y_pred_poly)))'''
    print(x)

def logr():
    x='''data_set= pd.read_csv('Iris.csv')
data_set.head(2)

X = data_set.iloc[:, :-1] 
y =data_set.iloc[:, -1] 

from sklearn import preprocessing
le=preprocessing.LabelEncoder()
le.fit(y)
label_Iris = le.transform(y)
label_Iris

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split  
x_train, x_test, y_train, y_test= train_test_split(X, y, test_size= 0.2, random_state=0) 
classifier = LogisticRegression(random_state = 0)
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)

from sklearn.metrics import accuracy_score
print ("Accuracy : ", accuracy_score(y_test, y_pred))
'''
    print(x)

def knn():
    x='''!pip install yellowbrick

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data = pd.read_csv('Heart_Disease_Prediction.csv')
data

from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()
data['Heart Disease'] = label_encoder.fit_transform(data['Heart Disease'])
data

features_cols = ['Age', 'Sex', 'Chest pain type', 'BP', 'Cholesterol', 'FBSover 120', 'EKG results',
'Max HR', 'Exercise angina', 'ST depression', 'Slope of ST','Number of vessels fluro','Thallium']
X = data.iloc[:, [0,12]].values
y = data.iloc[:, [13]].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25,random_state=0)

from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
import warnings
warnings.filterwarnings('ignore')
Scores = []
for i in range (2,11):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    score = knn.score(X_test,y_test)
    Scores.append(score)
print(knn.score(X_train,y_train))
print(Scores)

from sklearn.metrics import classification_report
print(classification_report(y_test,y_pred))

from yellowbrick.classifier import ClassificationReport
from yellowbrick.datasets import load_occupancy
classes = ["Heart disease _0","Heart disease _1"]
visualizer = ClassificationReport(knn, classes=classes, support=True)
visualizer.fit(X_train, y_train)
visualizer.score(X_test, y_test)
visualizer.show()

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm

'''
    print(x)

def dtr():
    x='''import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
data = pd.read_csv('Heart_Disease_Prediction.csv')
data

from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()
data['Heart Disease'] = label_encoder.fit_transform(data['Heart Disease'])
data

feature_cols = ['Age', 'Sex', 'Chest pain type', 'BP', 'Cholesterol', 'FBS over120', 'EKG results',
'Max HR', 'Exercise angina', 'ST depression', 'Slope of ST','Number of vessels fluro','Thallium']
X = data.iloc[:, [0,12]].values
y = data.iloc[:, [13]].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.25,random_state= 0)

from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)

from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier()
classifier = classifier.fit(X_train,y_train)

y_pred = classifier.predict(X_test)#Accuracy
from sklearn import metrics
print('Accuracy Score:', metrics.accuracy_score(y_test,y_pred))

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm

feature_cols = ['Cholesterol', 'BP']
from matplotlib.colors import ListedColormap
X_set, y_set = X_test, y_test
X1, X2 = np.meshgrid(np.arange(start = X_set[:,0].min()-1, stop= X_set[:,0].max()+1, step = 0.01),np.arange(start = X_set[:,1].min()-1, stop= X_set[:,1].max()+1, step = 0.01))
plt.contourf(X1,X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),alpha=0.75,cmap = ListedColormap(("red","green")))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i,j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set==j,0],X_set[y_set==j,1], c =ListedColormap(("red","green"))(i),label = j)
    plt.title("Decision Tree(Test set)")
    plt.xlabel("Age")
    plt.ylabel("Estimated Salary")
    plt.legend()
plt.show()

!pip install python-graphviz
!pip install pydotplus

from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO
from IPython.display import Image
import pydotplus
dot_data = StringIO()
export_graphviz(classifier, out_file=dot_data,
filled=True, rounded=True,
special_characters=True,feature_names =feature_cols,class_names=['Absence','Presence'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(graph.create_png())'''
    print(x)

def kmc():
    x='''import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans

X, y = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)
plt.scatter(X[:,0], X[:,1])

wcss = []
for i in range(1, 11): 
    kmeans = KMeans(i)
    kmeans.fit(X) 
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss) 
plt.title('Elbow Method') 
plt.xlabel('Number of clusters') 
plt.ylabel('WCSS') 
plt.show()

kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=300, n_init=10, random_state=0)
pred_y = kmeans.fit_predict(X)
plt.scatter(X[:,0], X[:,1]) 
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='red')
plt.show()

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans 
df=pd.read_csv('/dataset/dslab/Iris.csv')
X=df.iloc[:,[3,4]].values
wcss_list=[]
for i in range(1,11):
    kmeans=KMeans(n_clusters=i, init='k-means++',random_state=0) 
    kmeans.fit(X)
    wcss_list.append(kmeans.inertia_)
plt.plot(range(1,11),wcss_list) 
plt.title('The Elbow Method Graph') 
plt.xlabel('Number of Clusters(k)') 
plt.ylabel('wcss_list')
plt.show() 

kmeans=KMeans(n_clusters=2)
y_predict=kmeans.fit_predict(X)
#visualizing the clusters
plt.scatter(X[y_predict == 0, 0], X[y_predict == 0, 1], s = 100, c = 'blue', label = 'Cluster 1') 
plt.scatter(X[y_predict == 1, 0], X[y_predict == 1, 1], s = 100, c = 'green', label = 'Cluster 2') 

centers = kmeans.cluster_centers_
print('Cluster centroids:',centers)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 300, c = 'yellow', label = 'Centroid') 
plt.title('Clusters of customers')
plt.xlabel('Clusters')
plt.ylabel('Features')
plt.legend()
plt.show() 
centers = kmeans.cluster_centers_
print('Cluster centroids:',centers)
from sklearn.metrics import silhouette_score 
from sklearn.metrics import davies_bouldin_score
# Calculate Silhoutte Score
s_score = silhouetteb _score(X, kmeans.labels_, metric='euclidean')
# Calculate Davies-Bouldin Index
d_score = davies_bouldin_score(X, kmeans.labels_)
print('Silhouetter Score:',s_score) 
print('Davies-Bouldin Index:',d_score)'''
    print(x)

def rms():
    x='''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df_products = pd.read_csv("/dataset/dslab/shop.csv")
df_products

shop=df_products.iloc[:, 1:2]

shop['product']= shop['product'].str.strip()
shop

from sklearn.feature_extraction.text import TfidfVectorizer
tf = TfidfVectorizer()
tfidf_matrix = tf.fit_transform(shop['product'])
print(tfidf_matrix.shape)

from sklearn.metrics.pairwise import cosine_similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
print(cosine_sim.shape)

titles = shop['product']
indices = pd.Series(shop.index, index=shop['product'])

print(cosine_sim)

title=input("Enter the products related to recommend:")
num=int(input("Number of recommendations:"))

idx = indices[title]

sim_scores = list(enumerate(cosine_sim[idx]))
sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
sim_scores = sim_scores[1:num+1]
product_indices = [i[0] for i in sim_scores]
   
scores=[i[1] for i in sim_scores]

print("Recommending products similar to " + title + "...")   
print("-------")    
for rec in range(num): 
    print("Recommended: " + titles[product_indices[rec]] + " (score:" +      str(scores[rec]) + ")")

df_udemy = pd.read_csv("/dataset/dslab/udemy_courses.csv")
df_udemy

udemy=df_udemy.iloc[:, 1:2]

udemy['course_title']= udemy['course_title'].str.strip()
udemy

from sklearn.feature_extraction.text import TfidfVectorizer
tf = TfidfVectorizer()
tfidf_matrix = tf.fit_transform(udemy['course_title'])
print(tfidf_matrix.shape)

from sklearn.metrics.pairwise import cosine_similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
print(cosine_sim.shape)

titles = udemy['course_title']
indices = pd.Series(udemy.index, index=udemy['course_title'])

title=input("Enter the courses related to recommend:")
num=int(input("Number of recommendations:"))

idx = indices[title]

sim_scores = list(enumerate(cosine_sim[idx]))
sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
sim_scores = sim_scores[1:num+1]
udemy_indices = [i[0] for i in sim_scores]
   
scores=[i[1] for i in sim_scores]

print("Recommending courses similar to " + title + "...")   
print("-------")    
for rec in range(num): 
    print("Recommended: " + titles[udemy_indices[rec]] + " (score:" +      str(scores[rec]) + ")")'''
    print(x)
