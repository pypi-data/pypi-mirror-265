from sklearn.cluster                                    import KMeans
from signlanguage.interfaces.interfaces_model           import IKmeans
import numpy                                            as np
import matplotlib.pyplot as plt
from functools import reduce

RANGE_THRESHOLD_POOL = 0.1
RANGE_THRESHOLD_RESL = 0.95

## core dispertion - single core
class CorePool(IKmeans):
    def __init__(self, n_clusters=5):
        #core attr
        self.kmeans = KMeans(n_clusters=n_clusters, init='k-means++', n_init=1)
        self.cluster_centers_ = []

    def fit(self, X):
        try:
            self.kmeans.fit(X)
            self.cluster_centers_ = self.kmeans.cluster_centers_
            etiquetas = self.kmeans.labels_
        except Exception as e:
            print("Error Ocurrido [Core - Kmeans model], Mensaje: {0}".format(str(e)))

    def predict(self, X):
        cluster_asignado = self.kmeans.predict(X)
        distancia_al_centroide = np.linalg.norm(X - self.cluster_centers_[cluster_asignado], axis=1)
        resultado = [1 if distancia <= RANGE_THRESHOLD_POOL else 0 for distancia in distancia_al_centroide]
        return np.mean(resultado)#1 if np.mean(resultado) >= RANGE_THRESHOLD_RESL else 0
    
    def predict_cluster(self, X):
        return self.kmeans.predict(X)
    
    def predict_min(self, X):
        cluster_asignado = self.kmeans.predict(X)
        distancia_al_centroide = np.linalg.norm(X - self.cluster_centers_[cluster_asignado], axis=1)
        resultado = [1 if distancia <= RANGE_THRESHOLD_POOL else 0 for distancia in distancia_al_centroide]
        return np.mean(resultado)#1 if np.mean(resultado) >= RANGE_THRESHOLD_RESL else 00
        
    async def predict_async(self, X):
        cluster_asignado = self.kmeans.predict(X)
        distancia_al_centroide = np.linalg.norm(X - self.cluster_centers_[cluster_asignado], axis=1)
        resultado = [1 if distancia <= RANGE_THRESHOLD_POOL else 0 for distancia in distancia_al_centroide]
        return np.mean(resultado)#1 if np.mean(resultado) >= RANGE_THRESHOLD_RESL else 0