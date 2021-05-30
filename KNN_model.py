from sklearn.neighbours import KNeighborsClassifier
from sklearn.model_selection import cross_val_score

def knn_func(x_train, y_train):
    knn = KNeighborsClassifier(n_neighbors=10)
    cv_scores = cross_val_score(knn, x_train, y_train, cv=10)
   
    return knn.fit(x_train, y_train)