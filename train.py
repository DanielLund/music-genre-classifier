from preprocessing import analyse_playlist, PCA
from KNN_model import knn_func as knn

url_breaks = ""
url_house = ""

breaks = analyse_playlist(url_breaks)
house = analyse_playlist(url_house)

PCA_breaks = PCA("breaks.xlsx")
PCA_house = PCA("house.xlsx")


labelled_breaks = pd.read_excel("breaks.xlsx", index_col=0, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
labelled_house = pd.read_excel("house.xlsx", index_col=0, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
labelled_breaks["Class"] = 0
labelled_house["Class"] = 1

full_data = labelled_breaks.append(labelled_house[:24], ignore_cols=True)

full_data["Key"] = (full_data["Key"] / full_data["Key"].max())
full_data["Tempo"] = (full_data["Tempo"] / full_data["Tempo"].max())
full_data["Loudness"] = (full_data["Loudness"] / full_data["Loudness"].max())

full_data_random = full_data.sample(frac=1)

x_train = full_data_random[0:24]
y_train = x_train["Class"].values

x_train = x_train.drop("Class", axis=1)

knn(x_train, y_train)