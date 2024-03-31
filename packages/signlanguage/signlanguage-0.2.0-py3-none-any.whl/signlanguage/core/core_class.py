from sklearn.cluster                                    import KMeans
from signlanguage.interfaces.interfaces_model           import IKmeans
import numpy                                            as np

RANGE_THRESHOLD_POOL = 0.01

## core dispertion - single core
class CorePool(IKmeans):
    def __init__(self, n_clusters=4, init='k-means++'):
        #core attr
        self.kmeans = KMeans(n_clusters=n_clusters, init='k-means++', n_init='auto')
        self.cluster_centers_ = None

    def fit(self, X):
        try:
            self.kmeans.fit(X)
            self.cluster_centers_ = self.kmeans.cluster_centers_
        except Exception as e:
            print("Error Ocurrido [Core - Kmeans model], Mensaje: {0}".format(str(e)))

    def predict(self, X):
        distances = self.kmeans.transform(X)
        closest_cluster_distance = np.min(distances, axis=1)
        if (closest_cluster_distance[0] <= RANGE_THRESHOLD_POOL):
            return 1
        return 0
    
    def predict_cluster(self, X):
        return self.kmeans.predict(X)
    
    def predict_min(self, X):
        cluster_asignado = self.kmeans.predict(X)
        distancia_al_centroide = np.linalg.norm(X - self.kmeans.cluster_centers_[cluster_asignado])
        if (distancia_al_centroide <= RANGE_THRESHOLD_POOL):
            return 1
        return 0
        
    async def predict_min_async(self, X):
        cluster_asignado = self.kmeans.predict(X)
        distancia_al_centroide = np.linalg.norm(X - self.kmeans.cluster_centers_[cluster_asignado])
        if (distancia_al_centroide <= RANGE_THRESHOLD_POOL):
            return 1
        return 0