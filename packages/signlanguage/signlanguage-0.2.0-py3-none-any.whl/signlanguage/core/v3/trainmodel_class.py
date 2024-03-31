from signlanguage.interfaces.interfaces_model   import Itrain
import signlanguage.core.v3.core_class             as mk
import signlanguage.models.v3.handmodel_class      as hm
import numpy                       as np

HANDMODEL_LENGHT= 30

## train model
class TrainModelPool(Itrain):

    def Train_models(self, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        try:

            if data is None:
                return None
            
            model_evaluation = [None for _ in range(HANDMODEL_LENGHT)]
            
            #model3
            data_model = [[] for _ in range(HANDMODEL_LENGHT)]

            for idx, val in enumerate(data):
                value_model = hm.HandModel().make_model(hand_Left=val['model_hand_Left'], hand_Right=val['model_hand_Right'], points_body=val['model_body'], face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation, hand_diff_relation=hand_diff_relation)
                
                for i in range(len(value_model)):
                    data_model[i].extend(value_model[i])
                            
            for i, dm in enumerate(data_model):
                if len(dm) > 0:
                    #manage data
                    data_eval = np.array(dm)
                    #get cluster size - handmodel eval destination
                    n_clusters = hm.HandModel().cluster_sizes(i)
                    #init core pool
                    KmeanModel = mk.CorePool(n_clusters=n_clusters)
                    #train core pool
                    KmeanModel.fit(X=data_eval)
                    #assign model evaluation
                    model_evaluation[i] = KmeanModel # type: ignore
            
            return model_evaluation
        except Exception as e:
            print("Error Ocurrido [Train model], Mensaje: {0}".format(str(e)))
            return None

## train model
class TrainModelMovement(Itrain):
    def Train_models(self, data=None):
        try:

            if data is None:
                return None
            
            
            model_evaluation = []
            data_model = [[] for _ in range(6)]
           
            return model_evaluation
        except Exception as e:
            print("Error Ocurrido [Train model Movement], Mensaje: {0}".format(str(e)))
            return None