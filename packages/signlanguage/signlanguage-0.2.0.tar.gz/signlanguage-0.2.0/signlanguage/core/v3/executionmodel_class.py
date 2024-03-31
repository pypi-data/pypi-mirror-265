from signlanguage.interfaces.interfaces_model    import Imodel
import signlanguage.models.v3.handmodel_class       as hm
import numpy                        as np
import asyncio

HANDMODEL_LENGHT= 30

#HANDS---------------------------------------------------------
HAND_EVALUATION_VALUES = {0, 1, 2, 3, 4, 5}
HAND_RELATION_EVALUATION_VALUES = {6, 7, 8}

#FACE---------------------------------------------------------
FACE_EVALUATION_VALUES = {24, 25, 26, 27, 28, 29}

#BODY------------------------------------------------------------
BODY_EVALUATION_VALUES = {9, 10, 11, 12, 13, 14}
BODY_RELATION_EVALUATION_VALUES = {15, 16, 17}

#BODY_FACE------------------------------------------------------
BODY_FACE_EVALUATION_VALUES = {18, 19, 20, 21, 22, 23}

class ExecutionModelPool(Imodel):
    def transform_dataEvaluation(self, data_model=None):
        if data_model is None:
            return None
        
        data_evaluation = [[] for _ in range(HANDMODEL_LENGHT)]

        for i in range(len(data_model)):
            data_evaluation[i].extend(data_model[i])
        
        return data_evaluation

    #model3
    async def evaluation_async(self, model_evaluation=None, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        try:
            if model_evaluation is None or data is None:
                return None
            
            results = None
            ##evaluation_model
            #construct model data evaluation -- transform data evaluation
            data_model = hm.HandModel().make_model(
                hand_Left=data['model_hand_Left'],
                hand_Right=data['model_hand_Right'],
                points_body=data['model_body'],
                face_relation=face_relation,
                body_relation=body_relation,
                hand_relation=hand_relation,
                hand_diff_relation=hand_diff_relation
            )

            if not (face_relation or body_relation):
                results = await self.hand_evaluation_async(data_model=data_model, model_evaluation=model_evaluation, data=data, face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation, hand_diff_relation=hand_diff_relation)      

            elif face_relation and not body_relation:
                results = await self.face_evaluation_async(data_model=data_model, model_evaluation=model_evaluation, data=data, face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation, hand_diff_relation=hand_diff_relation)         
            
            elif body_relation:
                results = await self.body_evaluation_async(data_model=data_model, model_evaluation=model_evaluation, data=data, face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation, hand_diff_relation=hand_diff_relation)
            ##results_recog
            return results
            
        except Exception as e:
            print("Error Ocurrido [Model Exec], Mensaje: {0}".format(str(e)))
            return None
        
    ## Evalua los puntos de interseccion de las manos especificas, para reconocer unicamente movimiento de mano
    async def hand_evaluation_async(self, data_model: hm.HandModel, model_evaluation=None, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):

        if model_evaluation is None or data is None or data_model is None:
            return None
        
        defined_index = {i for i, model in enumerate(model_evaluation) if model is not None}
        defined_intersection = list(defined_index.intersection(HAND_EVALUATION_VALUES))
        
        if len(defined_intersection) not in(3, 6):
            return None

        matrix_evaluation = [None for _ in range(HANDMODEL_LENGHT)]
        
        if hand_relation:
            if len(data['model_hand_Left'])==0 or len(data['model_hand_Right'])==0:
                return None
            
        if not hand_relation:
            if len(data['model_hand_Left'])>0 and len(data['model_hand_Right'])>0:
                return None 
            
        data_evaluation = self.transform_dataEvaluation(data_model=data_model)
        if data_evaluation is None: return None

        tasks = []

        for idx in defined_intersection:
            evaluation_data  = data_evaluation[idx]
            evaluation_model = model_evaluation[idx]
            
            if evaluation_model is None or len(evaluation_data) ==0:
                return None
            
            data = np.array(evaluation_data)
            tasks.append(evaluation_model.predict_async(data))

        results = await asyncio.gather(*tasks)
        for i in range(len(results)):
            index_intersection = defined_intersection[i]
            matrix_evaluation[index_intersection] = results[i]

        if hand_relation:

            defined_intersection = list(defined_index.intersection(HAND_RELATION_EVALUATION_VALUES))

            if len(defined_intersection) != 3:
                return None
            
            tasks = []

            for idx in defined_intersection:
                evaluation_data  = data_evaluation[idx]
                evaluation_model = model_evaluation[idx]
                
                if evaluation_model is None or len(evaluation_data) ==0:
                    return None
                
                data = np.array(evaluation_data)
                tasks.append(evaluation_model.predict_async(data))

            results = await asyncio.gather(*tasks)
            for i in range(len(results)):
                index_intersection = defined_intersection[i]
                matrix_evaluation[index_intersection] = results[i]

        return matrix_evaluation
    
    ## Evalua los puntos de interseccion de la cara-mano especificos, para reconocer relaciones definidas
    async def face_evaluation_async(self, data_model: hm.HandModel, model_evaluation=None, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        
        if model_evaluation is None or data is None or data_model is None or not face_relation:
            return None
        
        # evaluate hand vals
        matrix_evaluation = await self.hand_evaluation_async(data_model=data_model, model_evaluation=model_evaluation, data=data, face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation)

        if matrix_evaluation is None or len(matrix_evaluation) != HANDMODEL_LENGHT:
            return None

        #pre evaluation model, defined
        defined_index = {i for i, model in enumerate(model_evaluation) if model is not None}
        defined_intersection = list(defined_index.intersection(FACE_EVALUATION_VALUES))

        if len(defined_intersection) not in(3, 6):
            return None
        
        data_evaluation = self.transform_dataEvaluation(data_model=data_model)
        if data_evaluation is None: return None
        
        tasks = []

        for idx in defined_intersection:
            evaluation_data  = data_evaluation[idx]
            evaluation_model = model_evaluation[idx]
            
            if evaluation_model is None or len(evaluation_data) ==0:
                return None
            
            data = np.array(evaluation_data)
            tasks.append(evaluation_model.predict_async(data))

        results = await asyncio.gather(*tasks)
        for i in range(len(results)):
            index_intersection = defined_intersection[i]
            matrix_evaluation[index_intersection] = results[i]
        
        return matrix_evaluation
      
    ## Evalua los puntos de interseccion del cuerpo en general
    async def body_evaluation_async(self, data_model: hm.HandModel, model_evaluation=None, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        if model_evaluation is None or data is None or data_model is None or not body_relation:
            return None
        
        matrix_evaluation = await self.hand_evaluation_async(data_model=data_model, model_evaluation=model_evaluation, data=data, face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation)

        if matrix_evaluation is None or len(matrix_evaluation) != HANDMODEL_LENGHT:
            return None

        #pre evaluation model, defined
        defined_index = {i for i, model in enumerate(model_evaluation) if model is not None}
        defined_intersection = list(defined_index.intersection(BODY_EVALUATION_VALUES))

        if len(defined_intersection) not in(3, 6):
            return None

        if hand_relation:
            if len(data['model_hand_Left'])==0 or len(data['model_hand_Right'])==0:
                return None
            
        data_evaluation = self.transform_dataEvaluation(data_model=data_model)
        if data_evaluation is None: return None
        
        tasks = []

        for idx in defined_intersection:
            evaluation_data  = data_evaluation[idx]
            evaluation_model = model_evaluation[idx]
            
            if evaluation_model is None or len(evaluation_data) ==0:
                return None
            
            data = np.array(evaluation_data)
            tasks.append(evaluation_model.predict_async(data))

        results = await asyncio.gather(*tasks)
        for i in range(len(results)):
            index_intersection = defined_intersection[i]
            matrix_evaluation[index_intersection] = results[i]
    
        if hand_relation:

            defined_intersection = list(defined_index.intersection(BODY_RELATION_EVALUATION_VALUES))

            if len(defined_intersection) != 3:
                return None
            
            tasks = []

            for idx in defined_intersection:
                evaluation_data  = data_evaluation[idx]
                evaluation_model = model_evaluation[idx]
                
                if evaluation_model is None or len(evaluation_data) ==0:
                    return None
                
                data = np.array(evaluation_data)
                tasks.append(evaluation_model.predict_async(data))

            results = await asyncio.gather(*tasks)
            for i in range(len(results)):
                index_intersection = defined_intersection[i]
                matrix_evaluation[index_intersection] = results[i]
            
        if face_relation:
            
            defined_intersection = list(defined_index.intersection(BODY_FACE_EVALUATION_VALUES))

            if len(defined_intersection) not in(3, 6):
                return None
            
            tasks = []

            for idx in defined_intersection:
                evaluation_data  = data_evaluation[idx]
                evaluation_model = model_evaluation[idx]
                
                if evaluation_model is None or len(evaluation_data) ==0:
                    return None
                
                data = np.array(evaluation_data)
                tasks.append(evaluation_model.predict_async(data))

            results = await asyncio.gather(*tasks)
            for i in range(len(results)):
                index_intersection = defined_intersection[i]
                matrix_evaluation[index_intersection] = results[i]

        return matrix_evaluation
    

class ExecutionModelMovement(Imodel):
    def transform_dataEvaluation(self, data_model=None):
        if data_model is None:
            return None
        
        data_evaluation = [[] for _ in range(6)]
        
        for i in range(len(data_model)):
            value = data_model[i]
            if value:
                if len(data_evaluation[i]) != len(value):
                    data_evaluation[i] = value[:]
                else:
                    data_evaluation[i] = value[:]
        
        """
        for i, value in enumerate(data_model):
            if len(value) > 0:
                if not len(data_evaluation[i]) == len(value):
                    data_evaluation[i] = [[] for _ in range(len(value))]
                
                for j, val_pos in enumerate(value):
                    data_evaluation[i][j].extend([val_pos])
        """
        
        return data_evaluation
        
    async def evaluation_async(self, model_evaluation=None, data=None):
        try:
            if None in (model_evaluation, data):
                    return None
            
            matrix_evaluation = [[] for _ in range(6)]            
                
            return matrix_evaluation
        except Exception as e:
            print("Error Ocurrido [Model Exec Movement], Mensaje: {0}".format(str(e)))
            return None
