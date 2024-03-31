from signlanguage.interfaces.interfaces_model   import Itrain
import signlanguage.core.core_class             as mk
import signlanguage.models.v2.handmodel_class    as hm
import pandas                      as pd
import numpy                       as np
import math

HANDMODEL_LENGHT= 51

## train model
class TrainModelPool(Itrain):

    def Train_models(self, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        try:

            if data is None:
                return None
            
            model_evaluation = []
            
            #model3
            data_model = [[] for _ in range(HANDMODEL_LENGHT)]

            for idx, val in enumerate(data):
                value_model = hm.HandModel().make_model(hand_Left=val['model_hand_Left'], hand_Right=val['model_hand_Right'], points_body=val['model_body'], face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation, hand_diff_relation=hand_diff_relation)
                
                for i, value in enumerate(value_model):
                    if len(value) > 0:
                        if len(data_model[i]) != len(value):
                            data_model[i] = [[] for _ in range(len(value))]
                        
                        for j, val_pos in enumerate(value):
                            data_model[i][j].extend([val_pos])
                            
            for i, dm in enumerate(data_model):
                if len(dm) > 0:
                    KmeansModel = []
                    for i, dm_pos in enumerate(dm):
                        if len(dm_pos) <= 0:
                            break
                        #configure values
                        data_index = np.array(dm_pos).T
                        df_real = pd.DataFrame(data_index).transpose()
                        n_clusters = min(len(dm), round((len(data)/3))) #determinar la cantidad de clusters
                        #Retrieve data
                        data_Train = np.array(df_real.values.tolist())
                        #init core pool
                        KmeanModel = mk.CorePool(n_clusters=n_clusters)
                        #train core pool
                        KmeanModel.fit(data_Train)
                        #add core pool, matrix values
                        KmeansModel.append(KmeanModel)
                    model_evaluation.append(KmeansModel)
                else:
                    model_evaluation.append([])
            
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
           
            for val in data:
                value_model = hm.HandModel().make_model_body(hand_Left=val['model_hand_Left'], hand_Right=val['model_hand_Right'], points_body=val['model_body'])
                for i, value in enumerate(value_model):
                    if len(value) > 0:
                        if not len(data_model[i]) == len(value):
                            data_model[i] = [[] for _ in range(len(value))]
                        for j, val_pos in enumerate(value):
                            data_model[i][j].extend([val_pos])

            for i, dm in enumerate(data_model):
                if len(dm) > 0:
                    KmeansModel = []
                    for i, dm_pos in enumerate(dm):
                        
                        if len(dm_pos) <= 0:
                            break
                        #configure values
                        data_index = np.array(dm_pos).T
                        df_real = pd.DataFrame(data_index).transpose()
                        n_clusters = min(len(dm), round((len(data)/3))) #determinar la cantidad de clusters
                        #Retrieve data
                        data_Train = np.array(df_real.values.tolist())
                        #init core pool
                        KmeanModel = mk.CorePool(n_clusters=n_clusters)
                        #train core pool
                        KmeanModel.fit(data_Train)
                        #add core pool, matrix values
                        KmeansModel.append(KmeanModel)
                    model_evaluation.append(KmeansModel)
                else:
                    model_evaluation.append([])

            return model_evaluation
        except Exception as e:
            print("Error Ocurrido [Train model Movement], Mensaje: {0}".format(str(e)))
            return None