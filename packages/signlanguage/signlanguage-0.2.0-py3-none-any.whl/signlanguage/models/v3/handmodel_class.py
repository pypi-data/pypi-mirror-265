## hand modeltransform_zbody
class HandModel:

    def elements_evaluation(self, hand_Left=None, hand_Right=None, points_body=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        if hand_Left is None or hand_Right is None or points_body is None:
                return None

        #HANDS----------------------------------------------------
        ## hands difference --> when: hand_relation
        points_hand_diffX = False
        points_hand_diffY = False
        points_hand_diffZ = False
        ## hands relation  --> indepent of hand_relation, same hands
        points_hand_Right_diffX = False
        points_hand_Right_diffY = False
        points_hand_Right_diffZ = False
        points_hand_Left_diffX = False
        points_hand_Left_diffY = False
        points_hand_Left_diffZ  = False
        #BODY----------------------------------------------------
        ## body difference --> when: hand_relation
        points_body_diffX = False
        points_body_diffY = False
        points_body_diffZ = False
        ## hands_body relation --> indepent of hand_relation, same hands
        points_body_XRight = False
        points_body_YRight = False
        points_body_ZRight = False
        points_body_XLeft = False
        points_body_YLeft = False
        points_body_ZLeft = False
        #BODY_FACE----------------------------------------------------#hand_relation does not exists
        ## body_face relation --> indepent of hand_relation, same hand
        points_body_face_XRight = False
        points_body_face_YRight = False
        points_body_face_ZRight = False
        points_body_face_XLeft = False
        points_body_face_YLeft = False
        points_body_face_ZLeft = False
        #FACE----------------------------------------------------#hand_relation does not exists
        ## face relation  --> indepent of hand_relation, sane hand
        points_face_XRight = False
        points_face_YRight = False
        points_face_ZRight = False
        points_face_XLeft = False
        points_face_YLeft = False
        points_face_ZLeft = False
        
        #HANDS----------------------------------------------------
        if len(hand_Right) > 0:
            points_hand_Right_diffX = True
            points_hand_Right_diffY = True
            points_hand_Right_diffZ = True
        
        if len(hand_Left) > 0:
            points_hand_Left_diffX = True
            points_hand_Left_diffY = True
            points_hand_Left_diffZ = True

        if len(hand_Right) > 0 and len(hand_Left) > 0 and hand_relation:
            points_hand_diffX =True
            points_hand_diffY = True
            points_hand_diffZ = True

        #BODY----------------------------------------------------
        if body_relation and len(points_body)>0:
            ## relation into same hands
            if len(hand_Right) > 0:
                points_body_XRight = True
                points_body_YRight = True
                points_body_ZRight = True

            if len(hand_Left) > 0:
                points_body_XLeft = True
                points_body_YLeft = True
                points_body_ZLeft =True

            ## hand_relation
            if len(hand_Left) > 0 and len(hand_Right) > 0 and hand_relation:
                points_body_diffX = True
                points_body_diffY = True
                points_body_diffZ = True
        
        #BODY_FACE----------------------------------------------------
        if (body_relation and face_relation) and len(points_body)>0:
            ## relation into same hands
            if len(hand_Left) > 0:
                points_body_face_XLeft = True
                points_body_face_YLeft = True
                points_body_face_ZLeft = True

            if len(hand_Right) > 0:

                points_body_face_XRight = True
                points_body_face_YRight = True
                points_body_face_ZRight = True

        #FACE----------------------------------------------------
        if (face_relation) and not body_relation and len(points_body)>0:
            ## relation into same hands
            if len(hand_Left)>0:
                points_face_XLeft = True
                points_face_YLeft = True
                points_face_ZLeft = True

            if len(hand_Right)>0:
                points_face_XRight = True
                points_face_YRight = True
                points_face_ZRight = True

        return [
            #HANDS---------------------------------------------------------
            ## hands relation  --> indepent of hand_relation, same hands
            points_hand_Right_diffX,#0
            points_hand_Right_diffY,#1
            points_hand_Right_diffZ,#2
            points_hand_Left_diffX,#3
            points_hand_Left_diffY,#4
            points_hand_Left_diffZ,#5
            ## hands difference --> when: hand_relation
            points_hand_diffX,#6
            points_hand_diffY,#7
            points_hand_diffZ,#8
            #BODY------------------------------------------------------------
            ## hands_body relation --> indepent of hand_relation, same hands
            points_body_XRight,#9
            points_body_YRight,#10
            points_body_ZRight,#11
            points_body_XLeft,#12
            points_body_YLeft,#13
            points_body_ZLeft,#14
                ## body difference --> when: hand_relation
            points_body_diffX,#15
            points_body_diffY,#16
            points_body_diffZ,#17
            #BODY_FACE------------------------------------------------------
            ## body_face relation --> indepent of hand_relation, same hand
            points_body_face_XRight,#18
            points_body_face_YRight,#19
            points_body_face_ZRight,#20
            points_body_face_XLeft,#21
            points_body_face_YLeft,#22
            points_body_face_ZLeft,#23
            #FACE---------------------------------------------------------
            ## face relation  --> indepent of hand_relation, sane hand
            points_face_XRight,#24
            points_face_YRight,#25
            points_face_ZRight,#26
            points_face_XLeft,#27
            points_face_YLeft,#28
            points_face_ZLeft #29
        ]

    ## return array_cluster_sizes
    def cluster_sizes(self, pos=-1):
        #return values
        sizes = [
                #HANDS---------------------------------------------------------
                ## hands relation  --> indepent of hand_relation, same hands
                27,#0
                27,#1
                27,#2
                6,#3
                6,#4
                6,#5
                ## hands difference --> when: hand_relation
                5,#6
                5,#7
                5,#8
                #BODY------------------------------------------------------------
                ## hands_body relation --> indepent of hand_relation, same hands
                5,#9
                5,#10
                5,#11
                5,#12
                5,#13
                5,#14
                ## body difference --> when: hand_relation
                14,#15
                14,#16
                14,#17
                #BODY_FACE------------------------------------------------------
                ## body_face relation --> indepent of hand_relation, same hand
                11,#18
                11,#19
                11,#20
                11,#21
                11,#22
                11,#23
                #FACE---------------------------------------------------------
                ## face relation  --> indepent of hand_relation, sane hand
                20,#24
                20,#25
                20,#26
                20,#27
                20,#29
                20#29    
            ]
            
        if pos == -1: return 5
        return sizes[pos]
    
    ## calculate indertemidiate pairs points - handpoints diff  
    def make_model(self, hand_Left=None, hand_Right=None, points_body=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        try:
            if hand_Left is None or hand_Right is None or points_body is None:
                return None

            #HANDS----------------------------------------------------
            ## hands difference --> when: hand_relation
            points_hand_diffX = []
            points_hand_diffY = []
            points_hand_diffZ = []
            ## hands relation  --> indepent of hand_relation, same hands
            points_hand_Right_diffX = []
            points_hand_Right_diffY = []
            points_hand_Right_diffZ = []
            points_hand_Left_diffX = []
            points_hand_Left_diffY = []
            points_hand_Left_diffZ  = []
            #BODY----------------------------------------------------
            ## body difference --> when: hand_relation
            points_body_diffX = []
            points_body_diffY = []
            points_body_diffZ = []
            ## hands_body relation --> indepent of hand_relation, same hands
            points_body_XRight = []
            points_body_YRight = []
            points_body_ZRight = []
            points_body_XLeft = []
            points_body_YLeft = []
            points_body_ZLeft = []
            #BODY_FACE----------------------------------------------------#hand_relation does not exists
            ## body_face relation --> indepent of hand_relation, same hand
            points_body_face_XRight = []
            points_body_face_YRight = []
            points_body_face_ZRight = []
            points_body_face_XLeft = []
            points_body_face_YLeft = []
            points_body_face_ZLeft = []
            #FACE----------------------------------------------------#hand_relation does not exists
            ## face relation  --> indepent of hand_relation, sane hand
            points_face_XRight = []
            points_face_YRight = []
            points_face_ZRight = []
            points_face_XLeft = []
            points_face_YLeft = []
            points_face_ZLeft = []
           
            #HANDS----------------------------------------------------
            if len(hand_Right) > 0:
                hands_x = list(map(lambda a: (a['x']), hand_Right))
                hands_y = list(map(lambda a: (a['y']), hand_Right))
                hands_z = list(map(lambda a: (a['z']), hand_Right))

                points_hand_Right_diffX =[
                    #thumb
                    [hands_x[4], (hands_x[4]-hands_x[3])],    [hands_x[3], (hands_x[3]-hands_x[2])],    [hands_x[2], (hands_x[2]-hands_x[1])],    [hands_x[1], (hands_x[1]-hands_x[0])],
                    #index
                    [hands_x[8], (hands_x[8]-hands_x[7])],    [hands_x[7], (hands_x[7]-hands_x[6])],    [hands_x[6], (hands_x[6]-hands_x[5])],    [hands_x[5], (hands_x[5]-hands_x[0])],
                    #middle
                    [hands_x[12], (hands_x[12]-hands_x[11])], [hands_x[11], (hands_x[11]-hands_x[10])], [hands_x[10], (hands_x[10]-hands_x[9])],  [hands_x[9], (hands_x[9]-hands_x[0])],
                    #ring
                    [hands_x[16], (hands_x[16]-hands_x[15])], [hands_x[15], (hands_x[15]-hands_x[14])], [hands_x[14], (hands_x[14]-hands_x[13])], [hands_x[13], (hands_x[13]-hands_x[0])],
                    #pinky
                    [hands_x[20], (hands_x[20]-hands_x[19])], [hands_x[19], (hands_x[19]-hands_x[18])], [hands_x[18], (hands_x[18]-hands_x[17])], [hands_x[17], (hands_x[17]-hands_x[0])],
                    #WIRST
                    [hands_x[0], (hands_x[4]-hands_x[0])], [hands_x[0], (hands_x[8]-hands_x[0])], [hands_x[0], (hands_x[12]-hands_x[0])], [hands_x[0], (hands_x[16]-hands_x[0])], [hands_x[0], (hands_x[20]-hands_x[0])],
                    #diff-between TIP
                    [(hands_x[4]-hands_x[8]),    4], [(hands_x[8]-hands_x[12]),   8], [(hands_x[12]-hands_x[16]), 12],  [(hands_x[16]-hands_x[20]), 16],  [(hands_x[16]-hands_x[4]), 16],
                    #diff-between IP
                    [(hands_x[3]-hands_x[7]),    3], [(hands_x[7]-hands_x[11]),   7], [(hands_x[11]-hands_x[15]), 11],  [(hands_x[15]-hands_x[19]), 15],  [(hands_x[19]-hands_x[3]), 19],
                    #diff-between MCP
                    [(hands_x[2]-hands_x[6]),    2], [(hands_x[6]-hands_x[10]),   6], [(hands_x[10]-hands_x[14]), 10],  [(hands_x[14]-hands_x[18]), 14],  [(hands_x[18]-hands_x[2]), 18],
                    #diff-between 
                    [(hands_x[4]-hands_x[6]),    4], [(hands_x[4]-hands_x[10]),   4], [(hands_x[4]-hands_x[14]),   4],  [(hands_x[4]-hands_x[18]),   4],
                    [(hands_x[8]-hands_x[2]),    8], [(hands_x[8]-hands_x[10]),   8], [(hands_x[8]-hands_x[14]),   8],  [(hands_x[8]-hands_x[18]),   8],
                    [(hands_x[12]-hands_x[2]),  12], [(hands_x[12]-hands_x[6]),  12], [(hands_x[12]-hands_x[14]), 12],  [(hands_x[12]-hands_x[18]), 12],
                    [(hands_x[16]-hands_x[2]),  16], [(hands_x[16]-hands_x[6]),  16], [(hands_x[16]-hands_x[10]), 16],  [(hands_x[16]-hands_x[18]), 16],
                    [(hands_x[20]-hands_x[2]),  20], [(hands_x[20]-hands_x[6]),  20], [(hands_x[20]-hands_x[10]), 20],  [(hands_x[20]-hands_x[14]), 20],
                    #diff-between 
                    [(hands_x[4]-hands_x[7]),    4], [(hands_x[4]-hands_x[11]),   4], [(hands_x[4]-hands_x[15]),   4],  [(hands_x[4]-hands_x[19]),   4],
                    [(hands_x[8]-hands_x[3]),    8], [(hands_x[8]-hands_x[11]),   8], [(hands_x[8]-hands_x[15]),   8],  [(hands_x[8]-hands_x[19]),   8],
                    [(hands_x[12]-hands_x[3]),  12], [(hands_x[12]-hands_x[7]),  12], [(hands_x[12]-hands_x[15]), 12],  [(hands_x[12]-hands_x[19]), 12],
                    [(hands_x[16]-hands_x[3]),  16], [(hands_x[16]-hands_x[7]),  16], [(hands_x[16]-hands_x[11]), 16],  [(hands_x[16]-hands_x[19]), 16],
                    [(hands_x[20]-hands_x[3]),  20], [(hands_x[20]-hands_x[7]),  20], [(hands_x[20]-hands_x[11]), 20],  [(hands_x[20]-hands_x[15]), 20],
                    #diff-between 
                    [(hands_x[4]-hands_x[8]),    4], [(hands_x[4]-hands_x[12]),   4], [(hands_x[4]-hands_x[16]),   4],  [(hands_x[4]-hands_x[20]),   4],
                    [(hands_x[8]-hands_x[4]),    8], [(hands_x[8]-hands_x[12]),   8], [(hands_x[8]-hands_x[16]),   8],  [(hands_x[8]-hands_x[20]),   8],
                    [(hands_x[12]-hands_x[4]),  12], [(hands_x[12]-hands_x[8]),  12], [(hands_x[12]-hands_x[16]), 12],  [(hands_x[12]-hands_x[20]), 12],
                    [(hands_x[16]-hands_x[4]),  16], [(hands_x[16]-hands_x[8]),  16], [(hands_x[16]-hands_x[12]), 16],  [(hands_x[16]-hands_x[20]), 16],
                    [(hands_x[20]-hands_x[4]),  20], [(hands_x[20]-hands_x[8]),  20], [(hands_x[20]-hands_x[12]), 20],  [(hands_x[20]-hands_x[16]), 20]
                ]

                points_hand_Right_diffY = [
                    #thumb
                    [hands_y[4], (hands_y[4]-hands_y[3])],    [hands_y[3], (hands_y[3]-hands_y[2])],    [hands_y[2], (hands_y[2]-hands_y[1])],    [hands_y[1], (hands_y[1]-hands_y[0])],
                    #index
                    [hands_y[8], (hands_y[8]-hands_y[7])],    [hands_y[7], (hands_y[7]-hands_y[6])],    [hands_y[6], (hands_y[6]-hands_y[5])],    [hands_y[5], (hands_y[5]-hands_y[0])],
                    #middle
                    [hands_y[12], (hands_y[12]-hands_y[11])], [hands_y[11], (hands_y[11]-hands_y[10])], [hands_y[10], (hands_y[10]-hands_y[9])],  [hands_y[9], (hands_y[9]-hands_y[0])],
                    #ring
                    [hands_y[16], (hands_y[16]-hands_y[15])], [hands_y[15], (hands_y[15]-hands_y[14])], [hands_y[14], (hands_y[14]-hands_y[13])], [hands_y[13], (hands_y[13]-hands_y[0])],
                    #pinky
                    [hands_y[20], (hands_y[20]-hands_y[19])], [hands_y[19], (hands_y[19]-hands_y[18])], [hands_y[18], (hands_y[18]-hands_y[17])], [hands_y[17], (hands_y[17]-hands_y[0])],
                    #TIP
                    [hands_y[0], (hands_y[4]-hands_y[0])], [hands_y[0], (hands_y[8]-hands_y[0])], [hands_y[0], (hands_y[12]-hands_y[0])], [hands_y[0], (hands_y[16]-hands_y[0])], [hands_y[0], (hands_y[20]-hands_y[0])],
                    #diff-between TIP
                    [(hands_y[4]-hands_y[8]),    4], [(hands_y[8]-hands_y[12]),   8], [(hands_y[12]-hands_y[16]), 12],  [(hands_y[16]-hands_y[20]), 16],  [(hands_y[16]-hands_y[4]), 20],
                    #diff-between IP
                    [(hands_y[3]-hands_y[7]),    3], [(hands_y[7]-hands_y[11]),   7], [(hands_y[11]-hands_y[15]), 11],  [(hands_y[15]-hands_y[19]), 15],  [(hands_y[19]-hands_y[3]), 19],
                    #diff-between MCP
                    [(hands_y[2]-hands_y[6]),    2], [(hands_y[6]-hands_y[10]),   6], [(hands_y[10]-hands_y[14]), 10],  [(hands_y[14]-hands_y[18]), 14],  [(hands_y[18]-hands_y[2]), 18],
                    #diff-between 
                    [(hands_y[4]-hands_y[6]),    4], [(hands_y[4]-hands_y[10]),   4], [(hands_y[4]-hands_y[14]),   4],  [(hands_y[4]-hands_y[18]),   4],
                    [(hands_y[8]-hands_y[3]),    8], [(hands_y[8]-hands_y[10]),   8], [(hands_y[8]-hands_y[14]),   8],  [(hands_y[8]-hands_y[18]),   8],
                    [(hands_y[12]-hands_y[2]),  12], [(hands_y[12]-hands_y[6]),  12], [(hands_y[12]-hands_y[14]), 12],  [(hands_y[12]-hands_y[18]), 12],
                    [(hands_y[16]-hands_y[2]),  16], [(hands_y[16]-hands_y[6]),  16], [(hands_y[16]-hands_y[10]), 16],  [(hands_y[16]-hands_y[18]), 16],
                    [(hands_y[20]-hands_y[2]),  20], [(hands_y[20]-hands_y[6]),  20], [(hands_y[20]-hands_y[10]), 20],  [(hands_y[20]-hands_y[14]), 20],
                    #diff-between 
                    [(hands_y[4]-hands_y[7]),    4], [(hands_y[4]-hands_y[11]),   4], [(hands_y[4]-hands_y[15]),   4],  [(hands_y[4]-hands_y[19]),   4],
                    [(hands_y[8]-hands_y[3]),    8], [(hands_y[8]-hands_y[11]),   8], [(hands_y[8]-hands_y[15]),   8],  [(hands_y[8]-hands_y[19]),   8],
                    [(hands_y[12]-hands_y[3]),  12], [(hands_y[12]-hands_y[7]),  12], [(hands_y[12]-hands_y[15]), 12],  [(hands_y[12]-hands_y[19]), 12],
                    [(hands_y[16]-hands_y[3]),  16], [(hands_y[16]-hands_y[7]),  16], [(hands_y[16]-hands_y[11]), 16],  [(hands_y[16]-hands_y[19]), 16],
                    [(hands_y[20]-hands_y[3]),  20], [(hands_y[20]-hands_y[7]),  20], [(hands_y[20]-hands_y[11]), 20],  [(hands_y[20]-hands_y[15]), 20],
                    #diff-between 
                    [(hands_y[4]-hands_y[8]),    4], [(hands_y[4]-hands_y[12]),   4], [(hands_y[4]-hands_y[16]),   4],  [(hands_y[4]-hands_y[20]),   4],
                    [(hands_y[8]-hands_y[4]),    8], [(hands_y[8]-hands_y[12]),   8], [(hands_y[8]-hands_y[16]),   8],  [(hands_y[8]-hands_y[20]),   8],
                    [(hands_y[12]-hands_y[4]),  12], [(hands_y[12]-hands_y[8]),  12], [(hands_y[12]-hands_y[16]), 12],  [(hands_y[12]-hands_y[20]), 12],
                    [(hands_y[16]-hands_y[4]),  16], [(hands_y[16]-hands_y[8]),  16], [(hands_y[16]-hands_y[12]), 16],  [(hands_y[16]-hands_y[20]), 16],
                    [(hands_y[20]-hands_y[4]),  20], [(hands_y[20]-hands_y[8]),  20], [(hands_y[20]-hands_y[12]), 20],  [(hands_y[20]-hands_y[16]), 20]
                ]

                points_hand_Right_diffZ = [
                    #thumb
                    [hands_z[4], (hands_z[4]-hands_z[3])],    [hands_z[3], (hands_z[3]-hands_z[2])],    [hands_z[2], (hands_z[2]-hands_z[1])],    [hands_z[1], (hands_z[1]-hands_z[0])],
                    #index
                    [hands_z[8], (hands_z[8]-hands_z[7])],    [hands_z[7], (hands_z[7]-hands_z[6])],    [hands_z[6], (hands_z[6]-hands_z[5])],    [hands_z[5], (hands_z[5]-hands_z[0])],
                    #middle
                    [hands_z[12], (hands_z[12]-hands_z[11])], [hands_z[11], (hands_z[11]-hands_z[10])], [hands_z[10], (hands_z[10]-hands_z[9])],  [hands_z[9], (hands_z[9]-hands_z[0])],
                    #ring
                    [hands_z[16], (hands_z[16]-hands_z[15])], [hands_z[15], (hands_z[15]-hands_z[14])], [hands_z[14], (hands_z[14]-hands_z[13])], [hands_z[13], (hands_z[13]-hands_z[0])],
                    #pinky
                    [hands_z[20], (hands_z[20]-hands_z[19])], [hands_z[19], (hands_z[19]-hands_z[18])], [hands_z[18], (hands_z[18]-hands_z[17])], [hands_z[17], (hands_z[17]-hands_z[0])],
                    #WIRST
                    [hands_z[0], (hands_z[4]-hands_z[0])], [hands_z[0], (hands_z[8]-hands_z[0])], [hands_z[0], (hands_z[12]-hands_z[0])], [hands_z[0], (hands_z[16]-hands_z[0])], [hands_z[0], (hands_z[20]-hands_z[0])],
                    #diff-between TIP
                    [(hands_z[4]-hands_z[8]),    4], [(hands_z[8]-hands_z[12]),   8], [(hands_z[12]-hands_z[16]), 12],  [(hands_z[16]-hands_z[20]), 16],  [(hands_z[16]-hands_z[4]), 16],
                    #diff-between IP
                    [(hands_z[3]-hands_z[7]),    3], [(hands_z[7]-hands_z[11]),   7], [(hands_z[11]-hands_z[15]), 11],  [(hands_z[15]-hands_z[19]), 15],  [(hands_z[19]-hands_z[3]), 19],
                    #diff-between MCP
                    [(hands_z[2]-hands_z[6]),    2], [(hands_z[6]-hands_z[10]),   6], [(hands_z[10]-hands_z[14]), 10],  [(hands_z[14]-hands_z[18]), 14],  [(hands_z[18]-hands_z[2]), 18],
                     #diff-between 
                    [(hands_z[4]-hands_z[6]),    4], [(hands_z[4]-hands_z[10]),   4], [(hands_z[4]-hands_z[14]),   4],  [(hands_z[4]-hands_z[18]),   4],
                    [(hands_z[8]-hands_z[3]),    8], [(hands_z[8]-hands_z[10]),   8], [(hands_z[8]-hands_z[14]),   8],  [(hands_z[8]-hands_z[18]),   8],
                    [(hands_z[12]-hands_z[2]),  12], [(hands_z[12]-hands_z[6]),  12], [(hands_z[12]-hands_z[14]), 12],  [(hands_z[12]-hands_z[18]), 12],
                    [(hands_z[16]-hands_z[2]),  16], [(hands_z[16]-hands_z[6]),  16], [(hands_z[16]-hands_z[10]), 16],  [(hands_z[16]-hands_z[18]), 16],
                    [(hands_z[20]-hands_z[2]),  20], [(hands_z[20]-hands_z[6]),  20], [(hands_z[20]-hands_z[10]), 20],  [(hands_z[20]-hands_z[14]), 20],
                    #diff-between 
                    [(hands_z[4]-hands_z[7]),    4], [(hands_z[4]-hands_z[11]),   4], [(hands_z[4]-hands_z[15]),   4],  [(hands_z[4]-hands_z[19]),   4],
                    [(hands_z[8]-hands_z[3]),    8], [(hands_z[8]-hands_z[11]),   8], [(hands_z[8]-hands_z[15]),   8],  [(hands_z[8]-hands_z[19]),   8],
                    [(hands_z[12]-hands_z[3]),  12], [(hands_z[12]-hands_z[7]),  12], [(hands_z[12]-hands_z[15]), 12],  [(hands_z[12]-hands_z[19]), 12],
                    [(hands_z[16]-hands_z[3]),  16], [(hands_z[16]-hands_z[7]),  16], [(hands_z[16]-hands_z[11]), 16],  [(hands_z[16]-hands_z[19]), 16],
                    [(hands_z[20]-hands_z[3]),  20], [(hands_z[20]-hands_z[7]),  20], [(hands_z[20]-hands_z[11]), 20],  [(hands_z[20]-hands_z[15]), 20],
                    #diff-between 
                    [(hands_z[4]-hands_z[8]),    4], [(hands_z[4]-hands_z[12]),   4], [(hands_z[4]-hands_z[16]),   4],  [(hands_z[4]-hands_z[20]),   4],
                    [(hands_z[8]-hands_z[4]),    8], [(hands_z[8]-hands_z[12]),   8], [(hands_z[8]-hands_z[16]),   8],  [(hands_z[8]-hands_z[20]),   8],
                    [(hands_z[12]-hands_z[4]),  12], [(hands_z[12]-hands_z[8]),  12], [(hands_z[12]-hands_z[16]), 12],  [(hands_z[12]-hands_z[20]), 12],
                    [(hands_z[16]-hands_z[4]),  16], [(hands_z[16]-hands_z[8]),  16], [(hands_z[16]-hands_z[12]), 16],  [(hands_z[16]-hands_z[20]), 16],
                    [(hands_z[20]-hands_z[4]),  20], [(hands_z[20]-hands_z[8]),  20], [(hands_z[20]-hands_z[12]), 20],  [(hands_z[20]-hands_z[16]), 20]
                ]

            if len(hand_Left) > 0:

                hands_x = list(map(lambda a: (a['x']), hand_Left))
                hands_y = list(map(lambda a: (a['y']), hand_Left))
                hands_z = list(map(lambda a: (a['z']), hand_Left))
                

                points_hand_Left_diffX = [
                    #thumb
                    [hands_x[4], (hands_x[4]-hands_x[3])],    [hands_x[3], (hands_x[3]-hands_x[2])],    [hands_x[2], (hands_x[2]-hands_x[1])],    [hands_x[1], (hands_x[1]-hands_x[0])],
                    #index
                    [hands_x[8], (hands_x[8]-hands_x[7])],    [hands_x[7], (hands_x[7]-hands_x[6])],    [hands_x[6], (hands_x[6]-hands_x[5])],    [hands_x[5], (hands_x[5]-hands_x[0])],
                    #middle
                    [hands_x[12], (hands_x[12]-hands_x[11])], [hands_x[11], (hands_x[11]-hands_x[10])], [hands_x[10], (hands_x[10]-hands_x[9])],  [hands_x[9], (hands_x[9]-hands_x[0])],
                    #ring
                    [hands_x[16], (hands_x[16]-hands_x[15])], [hands_x[15], (hands_x[15]-hands_x[14])], [hands_x[14], (hands_x[14]-hands_x[13])], [hands_x[13], (hands_x[13]-hands_x[0])],
                    #pinky
                    [hands_x[20], (hands_x[20]-hands_x[19])], [hands_x[19], (hands_x[19]-hands_x[18])], [hands_x[18], (hands_x[18]-hands_x[17])], [hands_x[17], (hands_x[17]-hands_x[0])],
                    #WIRST
                    [hands_x[0], (hands_x[4]-hands_x[0])], [hands_x[0], (hands_x[8]-hands_x[0])], [hands_x[0], (hands_x[12]-hands_x[0])], [hands_x[0], (hands_x[16]-hands_x[0])], [hands_x[0], (hands_x[20]-hands_x[0])],
                    #diff-between TIP
                    [(hands_x[4]-hands_x[8]),    4], [(hands_x[8]-hands_x[12]),   8], [(hands_x[12]-hands_x[16]), 12],  [(hands_x[16]-hands_x[20]), 16],  [(hands_x[16]-hands_x[4]), 16],
                    #diff-between IP
                    [(hands_x[3]-hands_x[7]),    3], [(hands_x[7]-hands_x[11]),   7], [(hands_x[11]-hands_x[15]), 11],  [(hands_x[15]-hands_x[19]), 15],  [(hands_x[19]-hands_x[3]), 19],
                    #diff-between MCP
                    [(hands_x[2]-hands_x[6]),    2], [(hands_x[6]-hands_x[10]),   6], [(hands_x[10]-hands_x[14]), 10],  [(hands_x[14]-hands_x[18]), 14],  [(hands_x[18]-hands_x[2]), 18],
                    #diff-between 
                    [(hands_x[4]-hands_x[6]),    4], [(hands_x[4]-hands_x[10]),   4], [(hands_x[4]-hands_x[14]),   4],  [(hands_x[4]-hands_x[18]),   4],
                    [(hands_x[8]-hands_x[2]),    8], [(hands_x[8]-hands_x[10]),   8], [(hands_x[8]-hands_x[14]),   8],  [(hands_x[8]-hands_x[18]),   8],
                    [(hands_x[12]-hands_x[2]),  12], [(hands_x[12]-hands_x[6]),  12], [(hands_x[12]-hands_x[14]), 12],  [(hands_x[12]-hands_x[18]), 12],
                    [(hands_x[16]-hands_x[2]),  16], [(hands_x[16]-hands_x[6]),  16], [(hands_x[16]-hands_x[10]), 16],  [(hands_x[16]-hands_x[18]), 16],
                    [(hands_x[20]-hands_x[2]),  20], [(hands_x[20]-hands_x[6]),  20], [(hands_x[20]-hands_x[10]), 20],  [(hands_x[20]-hands_x[14]), 20],
                    #diff-between 
                    [(hands_x[4]-hands_x[7]),    4], [(hands_x[4]-hands_x[11]),   4], [(hands_x[4]-hands_x[15]),   4],  [(hands_x[4]-hands_x[19]),   4],
                    [(hands_x[8]-hands_x[3]),    8], [(hands_x[8]-hands_x[11]),   8], [(hands_x[8]-hands_x[15]),   8],  [(hands_x[8]-hands_x[19]),   8],
                    [(hands_x[12]-hands_x[3]),  12], [(hands_x[12]-hands_x[7]),  12], [(hands_x[12]-hands_x[15]), 12],  [(hands_x[12]-hands_x[19]), 12],
                    [(hands_x[16]-hands_x[3]),  16], [(hands_x[16]-hands_x[7]),  16], [(hands_x[16]-hands_x[11]), 16],  [(hands_x[16]-hands_x[19]), 16],
                    [(hands_x[20]-hands_x[3]),  20], [(hands_x[20]-hands_x[7]),  20], [(hands_x[20]-hands_x[11]), 20],  [(hands_x[20]-hands_x[15]), 20],
                    #diff-between 
                    [(hands_x[4]-hands_x[8]),    4], [(hands_x[4]-hands_x[12]),   4], [(hands_x[4]-hands_x[16]),   4],  [(hands_x[4]-hands_x[20]),   4],
                    [(hands_x[8]-hands_x[4]),    8], [(hands_x[8]-hands_x[12]),   8], [(hands_x[8]-hands_x[16]),   8],  [(hands_x[8]-hands_x[20]),   8],
                    [(hands_x[12]-hands_x[4]),  12], [(hands_x[12]-hands_x[8]),  12], [(hands_x[12]-hands_x[16]), 12],  [(hands_x[12]-hands_x[20]), 12],
                    [(hands_x[16]-hands_x[4]),  16], [(hands_x[16]-hands_x[8]),  16], [(hands_x[16]-hands_x[12]), 16],  [(hands_x[16]-hands_x[20]), 16],
                    [(hands_x[20]-hands_x[4]),  20], [(hands_x[20]-hands_x[8]),  20], [(hands_x[20]-hands_x[12]), 20],  [(hands_x[20]-hands_x[16]), 20]
                ]

                points_hand_Left_diffY = [
                    #thumb
                    [hands_y[4], (hands_y[4]-hands_y[3])],    [hands_y[3], (hands_y[3]-hands_y[2])],    [hands_y[2], (hands_y[2]-hands_y[1])],    [hands_y[1], (hands_y[1]-hands_y[0])],
                    #index
                    [hands_y[8], (hands_y[8]-hands_y[7])],    [hands_y[7], (hands_y[7]-hands_y[6])],    [hands_y[6], (hands_y[6]-hands_y[5])],    [hands_y[5], (hands_y[5]-hands_y[0])],
                    #middle
                    [hands_y[12], (hands_y[12]-hands_y[11])], [hands_y[11], (hands_y[11]-hands_y[10])], [hands_y[10], (hands_y[10]-hands_y[9])],  [hands_y[9], (hands_y[9]-hands_y[0])],
                    #ring
                    [hands_y[16], (hands_y[16]-hands_y[15])], [hands_y[15], (hands_y[15]-hands_y[14])], [hands_y[14], (hands_y[14]-hands_y[13])], [hands_y[13], (hands_y[13]-hands_y[0])],
                    #pinky
                    [hands_y[20], (hands_y[20]-hands_y[19])], [hands_y[19], (hands_y[19]-hands_y[18])], [hands_y[18], (hands_y[18]-hands_y[17])], [hands_y[17], (hands_y[17]-hands_y[0])],
                    #TIP
                    [hands_y[0], (hands_y[4]-hands_y[0])], [hands_y[0], (hands_y[8]-hands_y[0])], [hands_y[0], (hands_y[12]-hands_y[0])], [hands_y[0], (hands_y[16]-hands_y[0])], [hands_y[0], (hands_y[20]-hands_y[0])],
                    #diff-between TIP
                    [(hands_y[4]-hands_y[8]),    4], [(hands_y[8]-hands_y[12]),   8], [(hands_y[12]-hands_y[16]), 12],  [(hands_y[16]-hands_y[20]), 16],  [(hands_y[16]-hands_y[4]), 20],
                    #diff-between IP
                    [(hands_y[3]-hands_y[7]),    3], [(hands_y[7]-hands_y[11]),   7], [(hands_y[11]-hands_y[15]), 11],  [(hands_y[15]-hands_y[19]), 15],  [(hands_y[19]-hands_y[3]), 19],
                    #diff-between MCP
                    [(hands_y[2]-hands_y[6]),    2], [(hands_y[6]-hands_y[10]),   6], [(hands_y[10]-hands_y[14]), 10],  [(hands_y[14]-hands_y[18]), 14],  [(hands_y[18]-hands_y[2]), 18],
                    #diff-between 
                    [(hands_y[4]-hands_y[6]),    4], [(hands_y[4]-hands_y[10]),   4], [(hands_y[4]-hands_y[14]),   4],  [(hands_y[4]-hands_y[18]),   4],
                    [(hands_y[8]-hands_y[3]),    8], [(hands_y[8]-hands_y[10]),   8], [(hands_y[8]-hands_y[14]),   8],  [(hands_y[8]-hands_y[18]),   8],
                    [(hands_y[12]-hands_y[2]),  12], [(hands_y[12]-hands_y[6]),  12], [(hands_y[12]-hands_y[14]), 12],  [(hands_y[12]-hands_y[18]), 12],
                    [(hands_y[16]-hands_y[2]),  16], [(hands_y[16]-hands_y[6]),  16], [(hands_y[16]-hands_y[10]), 16],  [(hands_y[16]-hands_y[18]), 16],
                    [(hands_y[20]-hands_y[2]),  20], [(hands_y[20]-hands_y[6]),  20], [(hands_y[20]-hands_y[10]), 20],  [(hands_y[20]-hands_y[14]), 20],
                    #diff-between 
                    [(hands_y[4]-hands_y[7]),    4], [(hands_y[4]-hands_y[11]),   4], [(hands_y[4]-hands_y[15]),   4],  [(hands_y[4]-hands_y[19]),   4],
                    [(hands_y[8]-hands_y[3]),    8], [(hands_y[8]-hands_y[11]),   8], [(hands_y[8]-hands_y[15]),   8],  [(hands_y[8]-hands_y[19]),   8],
                    [(hands_y[12]-hands_y[3]),  12], [(hands_y[12]-hands_y[7]),  12], [(hands_y[12]-hands_y[15]), 12],  [(hands_y[12]-hands_y[19]), 12],
                    [(hands_y[16]-hands_y[3]),  16], [(hands_y[16]-hands_y[7]),  16], [(hands_y[16]-hands_y[11]), 16],  [(hands_y[16]-hands_y[19]), 16],
                    [(hands_y[20]-hands_y[3]),  20], [(hands_y[20]-hands_y[7]),  20], [(hands_y[20]-hands_y[11]), 20],  [(hands_y[20]-hands_y[15]), 20],
                    #diff-between 
                    [(hands_y[4]-hands_y[8]),    4], [(hands_y[4]-hands_y[12]),   4], [(hands_y[4]-hands_y[16]),   4],  [(hands_y[4]-hands_y[20]),   4],
                    [(hands_y[8]-hands_y[4]),    8], [(hands_y[8]-hands_y[12]),   8], [(hands_y[8]-hands_y[16]),   8],  [(hands_y[8]-hands_y[20]),   8],
                    [(hands_y[12]-hands_y[4]),  12], [(hands_y[12]-hands_y[8]),  12], [(hands_y[12]-hands_y[16]), 12],  [(hands_y[12]-hands_y[20]), 12],
                    [(hands_y[16]-hands_y[4]),  16], [(hands_y[16]-hands_y[8]),  16], [(hands_y[16]-hands_y[12]), 16],  [(hands_y[16]-hands_y[20]), 16],
                    [(hands_y[20]-hands_y[4]),  20], [(hands_y[20]-hands_y[8]),  20], [(hands_y[20]-hands_y[12]), 20],  [(hands_y[20]-hands_y[16]), 20]
                ]

                points_hand_Left_diffZ = [
                    #thumb
                    [hands_z[4], (hands_z[4]-hands_z[3])],    [hands_z[3], (hands_z[3]-hands_z[2])],    [hands_z[2], (hands_z[2]-hands_z[1])],    [hands_z[1], (hands_z[1]-hands_z[0])],
                    #index
                    [hands_z[8], (hands_z[8]-hands_z[7])],    [hands_z[7], (hands_z[7]-hands_z[6])],    [hands_z[6], (hands_z[6]-hands_z[5])],    [hands_z[5], (hands_z[5]-hands_z[0])],
                    #middle
                    [hands_z[12], (hands_z[12]-hands_z[11])], [hands_z[11], (hands_z[11]-hands_z[10])], [hands_z[10], (hands_z[10]-hands_z[9])],  [hands_z[9], (hands_z[9]-hands_z[0])],
                    #ring
                    [hands_z[16], (hands_z[16]-hands_z[15])], [hands_z[15], (hands_z[15]-hands_z[14])], [hands_z[14], (hands_z[14]-hands_z[13])], [hands_z[13], (hands_z[13]-hands_z[0])],
                    #pinky
                    [hands_z[20], (hands_z[20]-hands_z[19])], [hands_z[19], (hands_z[19]-hands_z[18])], [hands_z[18], (hands_z[18]-hands_z[17])], [hands_z[17], (hands_z[17]-hands_z[0])],
                    #WIRST
                    [hands_z[0], (hands_z[4]-hands_z[0])], [hands_z[0], (hands_z[8]-hands_z[0])], [hands_z[0], (hands_z[12]-hands_z[0])], [hands_z[0], (hands_z[16]-hands_z[0])], [hands_z[0], (hands_z[20]-hands_z[0])],
                    #diff-between TIP
                    [(hands_z[4]-hands_z[8]),    4], [(hands_z[8]-hands_z[12]),   8], [(hands_z[12]-hands_z[16]), 12],  [(hands_z[16]-hands_z[20]), 16],  [(hands_z[16]-hands_z[4]), 16],
                    #diff-between IP
                    [(hands_z[3]-hands_z[7]),    3], [(hands_z[7]-hands_z[11]),   7], [(hands_z[11]-hands_z[15]), 11],  [(hands_z[15]-hands_z[19]), 15],  [(hands_z[19]-hands_z[3]), 19],
                    #diff-between MCP
                    [(hands_z[2]-hands_z[6]),    2], [(hands_z[6]-hands_z[10]),   6], [(hands_z[10]-hands_z[14]), 10],  [(hands_z[14]-hands_z[18]), 14],  [(hands_z[18]-hands_z[2]), 18],
                     #diff-between 
                    [(hands_z[4]-hands_z[6]),    4], [(hands_z[4]-hands_z[10]),   4], [(hands_z[4]-hands_z[14]),   4],  [(hands_z[4]-hands_z[18]),   4],
                    [(hands_z[8]-hands_z[3]),    8], [(hands_z[8]-hands_z[10]),   8], [(hands_z[8]-hands_z[14]),   8],  [(hands_z[8]-hands_z[18]),   8],
                    [(hands_z[12]-hands_z[2]),  12], [(hands_z[12]-hands_z[6]),  12], [(hands_z[12]-hands_z[14]), 12],  [(hands_z[12]-hands_z[18]), 12],
                    [(hands_z[16]-hands_z[2]),  16], [(hands_z[16]-hands_z[6]),  16], [(hands_z[16]-hands_z[10]), 16],  [(hands_z[16]-hands_z[18]), 16],
                    [(hands_z[20]-hands_z[2]),  20], [(hands_z[20]-hands_z[6]),  20], [(hands_z[20]-hands_z[10]), 20],  [(hands_z[20]-hands_z[14]), 20],
                    #diff-between 
                    [(hands_z[4]-hands_z[7]),    4], [(hands_z[4]-hands_z[11]),   4], [(hands_z[4]-hands_z[15]),   4],  [(hands_z[4]-hands_z[19]),   4],
                    [(hands_z[8]-hands_z[3]),    8], [(hands_z[8]-hands_z[11]),   8], [(hands_z[8]-hands_z[15]),   8],  [(hands_z[8]-hands_z[19]),   8],
                    [(hands_z[12]-hands_z[3]),  12], [(hands_z[12]-hands_z[7]),  12], [(hands_z[12]-hands_z[15]), 12],  [(hands_z[12]-hands_z[19]), 12],
                    [(hands_z[16]-hands_z[3]),  16], [(hands_z[16]-hands_z[7]),  16], [(hands_z[16]-hands_z[11]), 16],  [(hands_z[16]-hands_z[19]), 16],
                    [(hands_z[20]-hands_z[3]),  20], [(hands_z[20]-hands_z[7]),  20], [(hands_z[20]-hands_z[11]), 20],  [(hands_z[20]-hands_z[15]), 20],
                    #diff-between 
                    [(hands_z[4]-hands_z[8]),    4], [(hands_z[4]-hands_z[12]),   4], [(hands_z[4]-hands_z[16]),   4],  [(hands_z[4]-hands_z[20]),   4],
                    [(hands_z[8]-hands_z[4]),    8], [(hands_z[8]-hands_z[12]),   8], [(hands_z[8]-hands_z[16]),   8],  [(hands_z[8]-hands_z[20]),   8],
                    [(hands_z[12]-hands_z[4]),  12], [(hands_z[12]-hands_z[8]),  12], [(hands_z[12]-hands_z[16]), 12],  [(hands_z[12]-hands_z[20]), 12],
                    [(hands_z[16]-hands_z[4]),  16], [(hands_z[16]-hands_z[8]),  16], [(hands_z[16]-hands_z[12]), 16],  [(hands_z[16]-hands_z[20]), 16],
                    [(hands_z[20]-hands_z[4]),  20], [(hands_z[20]-hands_z[8]),  20], [(hands_z[20]-hands_z[12]), 20],  [(hands_z[20]-hands_z[16]), 20]
                ]

            if len(hand_Right) > 0 and len(hand_Left) > 0 and hand_relation:
                ### hand Right
                hands_xR = list(map(lambda a: (a['x']), hand_Right))
                hands_yR = list(map(lambda a: (a['y']), hand_Right))
                hands_zR = list(map(lambda a: (a['z']), hand_Right))
                ### hand Left
                hands_xL = list(map(lambda a: (a['x']), hand_Left))
                hands_yL = list(map(lambda a: (a['y']), hand_Left))
                hands_zL = list(map(lambda a: (a['z']), hand_Left))

                points_hand_diffX = [
                    #WIRST
                    [0,(hands_xR[0]-hands_xL[0])],
                    #TIP
                    [1,(hands_xR[4]-hands_xL[4])], [1,(hands_xR[8]-hands_xL[8])], [1,(hands_xR[12]-hands_xL[12])],  [1,(hands_xR[16]-hands_xL[16])],  [1,(hands_xR[20]-hands_xL[20])],
                    #DIP
                    [2,(hands_xR[3]-hands_xL[3])], [2,(hands_xR[7]-hands_xL[7])], [2,(hands_xR[11]-hands_xL[11])],  [2,(hands_xR[15]-hands_xL[15])],  [2,(hands_xR[19]-hands_xL[19])],
                    #PIP
                    [3,(hands_xR[2]-hands_xL[2])], [3,(hands_xR[6]-hands_xL[6])], [3,(hands_xR[10]-hands_xL[10])],  [3,(hands_xR[14]-hands_xL[14])],  [3,(hands_xR[18]-hands_xL[18])],
                    #MCP
                    [4,(hands_xR[1]-hands_xL[1])], [4,(hands_xR[5]-hands_xL[5])], [4,(hands_xR[9]-hands_xL[9])],    [4,(hands_xR[13]-hands_xL[13])],  [4,(hands_xR[17]-hands_xL[17])]
                ]

                points_hand_diffY = [
                    #WIRST
                    [0,(hands_yR[0]-hands_yL[0])],
                    #TIP
                    [1,(hands_yR[4]-hands_yL[4])], [1,(hands_yR[8]-hands_yL[8])], [1,(hands_yR[12]-hands_yL[12])],  [1,(hands_yR[16]-hands_yL[16])],  [1,(hands_yR[20]-hands_yL[20])],
                    #DIP
                    [2,(hands_yR[3]-hands_yL[3])], [2,(hands_yR[7]-hands_yL[7])], [2,(hands_yR[11]-hands_yL[11])],  [2,(hands_yR[15]-hands_yL[15])],  [2,(hands_yR[19]-hands_yL[19])],
                    #PIP
                    [3,(hands_yR[2]-hands_yL[2])], [3,(hands_yR[6]-hands_yL[6])], [3,(hands_yR[10]-hands_yL[10])],  [3,(hands_yR[14]-hands_yL[14])],  [3,(hands_yR[18]-hands_yL[18])],
                    #MCP
                    [4,(hands_yR[1]-hands_yL[1])], [4,(hands_yR[5]-hands_yL[5])], [4,(hands_yR[9]-hands_yL[9])],    [4,(hands_yR[13]-hands_yL[13])],  [4,(hands_yR[17]-hands_yL[17])]
                ]

                points_hand_diffZ = [
                    #WIRST
                    [0,(hands_zR[0]-hands_zL[0])],
                    #TIP
                    [1,(hands_zR[4]-hands_zL[4])], [1,(hands_zR[8]-hands_zL[8])], [1,(hands_zR[12]-hands_zL[12])],  [1,(hands_zR[16]-hands_zL[16])],  [1,(hands_zR[20]-hands_zL[20])],
                    #DIP
                    [2,(hands_zR[3]-hands_zL[3])], [2,(hands_zR[7]-hands_zL[7])], [2,(hands_zR[11]-hands_zL[11])],  [2,(hands_zR[15]-hands_zL[15])],  [2,(hands_zR[19]-hands_zL[19])],
                    #PIP
                    [3,(hands_zR[2]-hands_zL[2])], [3,(hands_zR[6]-hands_zL[6])], [3,(hands_zR[10]-hands_zL[10])],  [3,(hands_zR[14]-hands_zL[14])],  [3,(hands_zR[18]-hands_zL[18])],
                    #MCP
                    [4,(hands_zR[1]-hands_zL[1])], [4,(hands_zR[5]-hands_zL[5])], [4,(hands_zR[9]-hands_zL[9])],    [4,(hands_zR[13]-hands_zL[13])],  [4,(hands_zR[17]-hands_zL[17])]
                ]

            #BODY----------------------------------------------------
            if body_relation and len(points_body)>0:

                body_x = list(map(lambda a: (a['x']), points_body))
                body_y = list(map(lambda a: (a['y']), points_body))
                body_z = list(map(lambda a: (a['z']), points_body))

                ## relation into same hands
                if len(hand_Right) > 0:
                    
                    points_body_XRight = [
                        #hombro-codo
                        [body_x[12], (body_x[12]-body_x[14])], 
                        #codo-muñeca
                        [body_x[14], (body_x[14]-body_x[16])],
                        #muñeca-indice
                        [body_x[20], (body_x[16]-body_x[20])],
                        #muñeca-meñique
                        [body_x[18], (body_x[16]-body_x[18])],
                        #muñeca-pulgar
                        [body_x[16], (body_x[16]-body_x[22])]

                    ]

                    points_body_YRight = [
                        #hombro-codo
                        [body_y[12], (body_y[12]-body_y[14])], 
                        #codo-muñeca
                        [body_y[14], (body_y[14]-body_y[16])],
                        #muñeca-indice
                        [body_y[20], (body_y[16]-body_y[20])],
                        #muñeca-meñique
                        [body_y[18], (body_y[16]-body_y[18])],
                        #muñeca-pulgar
                        [body_y[16], (body_y[16]-body_y[22])]

                    ]

                    points_body_ZRight = [
                        #hombro-codo
                        [body_z[12], (body_z[12]-body_z[14])], 
                        #codo-muñeca
                        [body_z[14], (body_z[14]-body_z[16])],
                        #muñeca-indice
                        [body_z[20], (body_z[16]-body_z[20])],
                        #muñeca-meñique
                        [body_z[18], (body_z[16]-body_z[18])],
                        #muñeca-pulgar
                        [body_z[16], (body_z[16]-body_z[22])]

                    ]

                if len(hand_Left) > 0:
                    
                    points_body_XLeft = [
                        #hombro-codo
                        [body_x[11], (body_x[11]-body_x[13])], 
                        #codo-muñeca
                        [body_x[13], (body_x[13]-body_x[15])],
                        #muñeca-indice
                        [body_x[19], (body_x[15]-body_x[19])],
                        #muñeca-meñique
                        [body_x[17], (body_x[15]-body_x[17])],
                        #muñeca-pulgar
                        [body_x[15], (body_x[15]-body_x[21])]

                    ]

                    points_body_YLeft = [
                        #hombro-codo
                        [body_y[11], (body_y[11]-body_y[13])], 
                        #codo-muñeca
                        [body_y[13], (body_y[13]-body_y[15])],
                        #muñeca-indice
                        [body_y[19], (body_y[15]-body_y[19])],
                        #muñeca-meñique
                        [body_y[17], (body_y[15]-body_y[17])],
                        #muñeca-pulgar
                        [body_y[15], (body_y[15]-body_y[21])]

                    ]

                    points_body_ZLeft = [
                        #hombro-codo
                        [body_z[11], (body_z[11]-body_z[13])], 
                        #codo-muñeca
                        [body_z[13], (body_z[13]-body_z[15])],
                        #muñeca-indice
                        [body_z[19], (body_z[15]-body_z[19])],
                        #muñeca-meñique
                        [body_z[17], (body_z[15]-body_z[17])],
                        #muñeca-pulgar
                        [body_z[15], (body_z[15]-body_z[21])]

                    ]

                ## hand_relation
                if len(hand_Left) > 0 and len(hand_Right) > 0 and hand_relation:
                    points_body_diffX = [
                        #hombro
                        [0,(body_x[12]-body_x[11])], 
                        #codo
                        [1,(body_x[14]-body_x[13])],
                        #muñeca
                        [2,(body_x[16]-body_x[15])], 
                        [6,(body_x[16]-body_x[11])], [6,(body_x[15]-body_x[12])],
                        [7,(body_x[16]-body_x[13])], [7,(body_x[15]-body_x[14])],
                        #indice
                        [3,(body_x[20]-body_x[19])],
                        [8,(body_x[20]-body_x[11])], [8,(body_x[19]-body_x[12])],
                        [9,(body_x[20]-body_x[13])], [9,(body_x[19]-body_x[14])],
                        #meñique
                        [4,(body_x[18]-body_x[17])],
                        [10,(body_x[18]-body_x[11])], [10,(body_x[17]-body_x[12])],
                        [11,(body_x[18]-body_x[13])], [11,(body_x[17]-body_x[14])],
                        #pulgar
                        [5,(body_x[22]-body_x[21])],
                        [12,(body_x[22]-body_x[11])], [12,(body_x[21]-body_x[12])],
                        [13,(body_x[22]-body_x[13])], [13,(body_x[21]-body_x[14])],                        
                    ]

                    points_body_diffY = [
                        #hombro
                        [0,(body_y[12]-body_y[11])], 
                        #codo
                        [1,(body_y[14]-body_y[13])],
                        #muñeca
                        [2,(body_y[16]-body_y[15])], 
                        [6,(body_y[16]-body_y[11])], [6,(body_y[15]-body_y[12])],
                        [7,(body_y[16]-body_y[13])], [7,(body_y[15]-body_y[14])],
                        #indice
                        [3,(body_y[20]-body_y[19])],
                        [8,(body_y[20]-body_y[11])], [8,(body_y[19]-body_y[12])],
                        [9,(body_y[20]-body_y[13])], [9,(body_y[19]-body_y[14])],
                        #meñique
                        [4,(body_y[18]-body_y[17])],
                        [10,(body_y[18]-body_y[11])], [10,(body_y[17]-body_y[12])],
                        [11,(body_y[18]-body_y[13])], [11,(body_y[17]-body_y[14])],
                        #pulgar
                        [5,(body_y[22]-body_y[21])],
                        [12,(body_y[22]-body_y[11])], [12,(body_y[21]-body_y[12])],
                        [13,(body_y[22]-body_y[13])], [13,(body_y[21]-body_y[14])],                        
                    ]

                    points_body_diffZ = [
                        #hombro
                        [0,(body_z[12]-body_z[11])], 
                        #codo
                        [1,(body_z[14]-body_z[13])],
                        #muñeca
                        [2,(body_z[16]-body_z[15])], 
                        [6,(body_z[16]-body_z[11])], [6,(body_z[15]-body_z[12])],
                        [7,(body_z[16]-body_z[13])], [7,(body_z[15]-body_z[14])],
                        #indice
                        [3,(body_z[20]-body_z[19])],
                        [8,(body_z[20]-body_z[11])], [8,(body_z[19]-body_z[12])],
                        [9,(body_z[20]-body_z[13])], [9,(body_z[19]-body_z[14])],
                        #meñique
                        [4,(body_z[18]-body_z[17])],
                        [10,(body_z[18]-body_z[11])], [10,(body_z[17]-body_z[12])],
                        [11,(body_z[18]-body_z[13])], [11,(body_z[17]-body_z[14])],
                        #pulgar
                        [5,(body_z[22]-body_z[21])],
                        [12,(body_z[22]-body_z[11])], [12,(body_z[21]-body_z[12])],
                        [13,(body_z[22]-body_z[13])], [13,(body_z[21]-body_z[14])],                        
                    ]

            #BODY_FACE----------------------------------------------------
            if (body_relation and face_relation) and len(points_body)>0:

                body_x = list(map(lambda a: (a['x']), points_body))
                body_y = list(map(lambda a: (a['y']), points_body))
                body_z = list(map(lambda a: (a['z']), points_body))

                ## relation into same hands
                if len(hand_Left) > 0:

                    points_body_face_XLeft = [
                        #muñeca------------------
                        #ear
                        [body_x[7], (body_x[15]-body_x[7])], [body_x[8], (body_x[15]-body_x[8])], 
                        #eye
                        [body_x[3], (body_x[15]-body_x[3])], [body_x[2], (body_x[15]-body_x[2])], [body_x[1], (body_x[15]-body_x[1])],
                        [body_x[4], (body_x[15]-body_x[4])], [body_x[5], (body_x[15]-body_x[5])], [body_x[6], (body_x[15]-body_x[6])],
                        #nose
                        [body_x[0], (body_x[15]-body_x[0])],
                        #mouth
                        [body_x[9], (body_x[15]-body_x[9])], [body_x[10], (body_x[15]-body_x[10])],
                        #indice------------------
                        #ear
                        [body_x[7], (body_x[19]-body_x[7])], [body_x[8], (body_x[19]-body_x[8])], 
                        #eye
                        [body_x[3], (body_x[19]-body_x[3])], [body_x[2], (body_x[19]-body_x[2])], [body_x[1], (body_x[19]-body_x[1])],
                        [body_x[4], (body_x[19]-body_x[4])], [body_x[5], (body_x[19]-body_x[5])], [body_x[6], (body_x[19]-body_x[6])],
                        #nose
                        [body_x[0], (body_x[19]-body_x[0])],
                        #mouth
                        [body_x[9], (body_x[19]-body_x[9])], [body_x[10], (body_x[19]-body_x[10])],
                        #meñique------------------
                        #ear
                        [body_x[7], (body_x[17]-body_x[7])], [body_x[8], (body_x[17]-body_x[8])], 
                        #eye
                        [body_x[3], (body_x[17]-body_x[3])], [body_x[2], (body_x[17]-body_x[2])], [body_x[1], (body_x[17]-body_x[1])],
                        [body_x[4], (body_x[17]-body_x[4])], [body_x[5], (body_x[17]-body_x[5])], [body_x[6], (body_x[17]-body_x[6])],
                        #nose
                        [body_x[0], (body_x[17]-body_x[0])],
                        #mouth
                        [body_x[9], (body_x[17]-body_x[9])], [body_x[10], (body_x[17]-body_x[10])],
                        #pulgar------------------
                        #ear
                        [body_x[7], (body_x[21]-body_x[7])], [body_x[8], (body_x[21]-body_x[8])], 
                        #eye
                        [body_x[3], (body_x[21]-body_x[3])], [body_x[2], (body_x[21]-body_x[2])], [body_x[1], (body_x[21]-body_x[1])],
                        [body_x[4], (body_x[21]-body_x[4])], [body_x[5], (body_x[21]-body_x[5])], [body_x[6], (body_x[21]-body_x[6])],
                        #nose
                        [body_x[0], (body_x[21]-body_x[0])],
                        #mouth
                        [body_x[9], (body_x[21]-body_x[9])], [body_x[10], (body_x[21]-body_x[10])]
                    ]

                    points_body_face_YLeft = [
                        #muñeca------------------
                        #ear
                        [body_y[7], (body_y[15]-body_y[7])], [body_y[8], (body_y[15]-body_y[8])], 
                        #eye
                        [body_y[3], (body_y[15]-body_y[3])], [body_y[2], (body_y[15]-body_y[2])], [body_y[1], (body_y[15]-body_y[1])],
                        [body_y[4], (body_y[15]-body_y[4])], [body_y[5], (body_y[15]-body_y[5])], [body_y[6], (body_y[15]-body_y[6])],
                        #nose
                        [body_y[0], (body_y[15]-body_y[0])],
                        #mouth
                        [body_y[9], (body_y[15]-body_y[9])], [body_y[10], (body_y[15]-body_y[10])],
                        #indice------------------
                        #ear
                        [body_y[7], (body_y[19]-body_y[7])], [body_y[8], (body_y[19]-body_y[8])], 
                        #eye
                        [body_y[3], (body_y[19]-body_y[3])], [body_y[2], (body_y[19]-body_y[2])], [body_y[1], (body_y[19]-body_y[1])],
                        [body_y[4], (body_y[19]-body_y[4])], [body_y[5], (body_y[19]-body_y[5])], [body_y[6], (body_y[19]-body_y[6])],
                        #nose
                        [body_y[0], (body_y[19]-body_y[0])],
                        #mouth
                        [body_y[9], (body_y[19]-body_y[9])], [body_y[10], (body_y[19]-body_y[10])],
                        #meñique------------------
                        #ear
                        [body_y[7], (body_y[17]-body_y[7])], [body_y[8], (body_y[17]-body_y[8])], 
                        #eye
                        [body_y[3], (body_y[17]-body_y[3])], [body_y[2], (body_y[17]-body_y[2])], [body_y[1], (body_y[17]-body_y[1])],
                        [body_y[4], (body_y[17]-body_y[4])], [body_y[5], (body_y[17]-body_y[5])], [body_y[6], (body_y[17]-body_y[6])],
                        #nose
                        [body_y[0], (body_y[17]-body_y[0])],
                        #mouth
                        [body_y[9], (body_y[17]-body_y[9])], [body_y[10], (body_y[17]-body_y[10])],
                        #pulgar------------------
                        #ear
                        [body_y[7], (body_y[21]-body_y[7])], [body_y[8], (body_y[21]-body_y[8])], 
                        #eye
                        [body_y[3], (body_y[21]-body_y[3])], [body_y[2], (body_y[21]-body_y[2])], [body_y[1], (body_y[21]-body_y[1])],
                        [body_y[4], (body_y[21]-body_y[4])], [body_y[5], (body_y[21]-body_y[5])], [body_y[6], (body_y[21]-body_y[6])],
                        #nose
                        [body_y[0], (body_y[21]-body_y[0])],
                        #mouth
                        [body_y[9], (body_y[21]-body_y[9])], [body_y[10], (body_y[21]-body_y[10])]
                    ]

                    points_body_face_ZLeft = [
                        #muñeca------------------
                        #ear
                        [body_z[7], (body_z[15]-body_z[7])], [body_z[8], (body_z[15]-body_z[8])], 
                        #eye
                        [body_z[3], (body_z[15]-body_z[3])], [body_z[2], (body_z[15]-body_z[2])], [body_z[1], (body_z[15]-body_z[1])],
                        [body_z[4], (body_z[15]-body_z[4])], [body_z[5], (body_z[15]-body_z[5])], [body_z[6], (body_z[15]-body_z[6])],
                        #nose
                        [body_z[0], (body_z[15]-body_z[0])],
                        #mouth
                        [body_z[9], (body_z[15]-body_z[9])], [body_z[10], (body_z[15]-body_z[10])],
                        #indice------------------
                        #ear
                        [body_z[7], (body_z[19]-body_z[7])], [body_z[8], (body_z[19]-body_z[8])], 
                        #eye
                        [body_z[3], (body_z[19]-body_z[3])], [body_z[2], (body_z[19]-body_z[2])], [body_z[1], (body_z[19]-body_z[1])],
                        [body_z[4], (body_z[19]-body_z[4])], [body_z[5], (body_z[19]-body_z[5])], [body_z[6], (body_z[19]-body_z[6])],
                        #nose
                        [body_z[0], (body_z[19]-body_z[0])],
                        #mouth
                        [body_z[9], (body_z[19]-body_z[9])], [body_z[10], (body_z[19]-body_z[10])],
                        #meñique------------------
                        #ear
                        [body_z[7], (body_z[17]-body_z[7])], [body_z[8], (body_z[17]-body_z[8])], 
                        #eye
                        [body_z[3], (body_z[17]-body_z[3])], [body_z[2], (body_z[17]-body_z[2])], [body_z[1], (body_z[17]-body_z[1])],
                        [body_z[4], (body_z[17]-body_z[4])], [body_z[5], (body_z[17]-body_z[5])], [body_z[6], (body_z[17]-body_z[6])],
                        #nose
                        [body_z[0], (body_z[17]-body_z[0])],
                        #mouth
                        [body_z[9], (body_z[17]-body_z[9])], [body_z[10], (body_z[17]-body_z[10])],
                        #pulgar------------------
                        #ear
                        [body_z[7], (body_z[21]-body_z[7])], [body_z[8], (body_z[21]-body_z[8])], 
                        #eye
                        [body_z[3], (body_z[21]-body_z[3])], [body_z[2], (body_z[21]-body_z[2])], [body_z[1], (body_z[21]-body_z[1])],
                        [body_z[4], (body_z[21]-body_z[4])], [body_z[5], (body_z[21]-body_z[5])], [body_z[6], (body_z[21]-body_z[6])],
                        #nose
                        [body_z[0], (body_z[21]-body_z[0])],
                        #mouth
                        [body_z[9], (body_z[21]-body_z[9])], [body_z[10], (body_z[21]-body_z[10])]
                    ]

                if len(hand_Right) > 0:

                    points_body_face_XRight = [
                        #muñeca------------------
                        #ear
                        [body_x[7], (body_x[16]-body_x[7])], [body_x[8], (body_x[16]-body_x[8])], 
                        #eye
                        [body_x[3], (body_x[16]-body_x[3])], [body_x[2], (body_x[16]-body_x[2])], [body_x[1], (body_x[16]-body_x[1])],
                        [body_x[4], (body_x[16]-body_x[4])], [body_x[5], (body_x[16]-body_x[5])], [body_x[6], (body_x[16]-body_x[6])],
                        #nose
                        [body_x[0], (body_x[16]-body_x[0])],
                        #mouth
                        [body_x[9], (body_x[16]-body_x[9])], [body_x[10], (body_x[16]-body_x[10])],
                        #indice------------------
                        #ear
                        [body_x[7], (body_x[20]-body_x[7])], [body_x[8], (body_x[20]-body_x[8])], 
                        #eye
                        [body_x[3], (body_x[20]-body_x[3])], [body_x[2], (body_x[20]-body_x[2])], [body_x[1], (body_x[20]-body_x[1])],
                        [body_x[4], (body_x[20]-body_x[4])], [body_x[5], (body_x[20]-body_x[5])], [body_x[6], (body_x[20]-body_x[6])],
                        #nose
                        [body_x[0], (body_x[20]-body_x[0])],
                        #mouth
                        [body_x[9], (body_x[20]-body_x[9])], [body_x[10], (body_x[20]-body_x[10])],
                        #meñique------------------
                        #ear
                        [body_x[7], (body_x[18]-body_x[7])], [body_x[8], (body_x[18]-body_x[8])], 
                        #eye
                        [body_x[3], (body_x[18]-body_x[3])], [body_x[2], (body_x[18]-body_x[2])], [body_x[1], (body_x[18]-body_x[1])],
                        [body_x[4], (body_x[18]-body_x[4])], [body_x[5], (body_x[18]-body_x[5])], [body_x[6], (body_x[18]-body_x[6])],
                        #nose
                        [body_x[0], (body_x[18]-body_x[0])],
                        #mouth
                        [body_x[9], (body_x[18]-body_x[9])], [body_x[10], (body_x[18]-body_x[10])],
                        #pulgar------------------
                        #ear
                        [body_x[7], (body_x[22]-body_x[7])], [body_x[8], (body_x[22]-body_x[8])], 
                        #eye
                        [body_x[3], (body_x[22]-body_x[3])], [body_x[2], (body_x[22]-body_x[2])], [body_x[1], (body_x[22]-body_x[1])],
                        [body_x[4], (body_x[22]-body_x[4])], [body_x[5], (body_x[22]-body_x[5])], [body_x[6], (body_x[22]-body_x[6])],
                        #nose
                        [body_x[0], (body_x[22]-body_x[0])],
                        #mouth
                        [body_x[9], (body_x[22]-body_x[9])], [body_x[10], (body_x[22]-body_x[10])]
                    ]
                    
                    points_body_face_YRight = [
                        #muñeca------------------
                        #ear
                        [body_y[7], (body_y[16]-body_y[7])], [body_y[8], (body_y[16]-body_y[8])], 
                        #eye
                        [body_y[3], (body_y[16]-body_y[3])], [body_y[2], (body_y[16]-body_y[2])], [body_y[1], (body_y[16]-body_y[1])],
                        [body_y[4], (body_y[16]-body_y[4])], [body_y[5], (body_y[16]-body_y[5])], [body_y[6], (body_y[16]-body_y[6])],
                        #nose
                        [body_y[0], (body_y[16]-body_y[0])],
                        #mouth
                        [body_y[9], (body_y[16]-body_y[9])], [body_y[10], (body_y[16]-body_y[10])],
                        #indice------------------
                        #ear
                        [body_y[7], (body_y[20]-body_y[7])], [body_y[8], (body_y[20]-body_y[8])], 
                        #eye
                        [body_y[3], (body_y[20]-body_y[3])], [body_y[2], (body_y[20]-body_y[2])], [body_y[1], (body_y[20]-body_y[1])],
                        [body_y[4], (body_y[20]-body_y[4])], [body_y[5], (body_y[20]-body_y[5])], [body_y[6], (body_y[20]-body_y[6])],
                        #nose
                        [body_y[0], (body_y[20]-body_y[0])],
                        #mouth
                        [body_y[9], (body_y[20]-body_y[9])], [body_y[10], (body_y[20]-body_y[10])],
                        #meñique------------------
                        #ear
                        [body_y[7], (body_y[18]-body_y[7])], [body_y[8], (body_y[18]-body_y[8])], 
                        #eye
                        [body_y[3], (body_y[18]-body_y[3])], [body_y[2], (body_y[18]-body_y[2])], [body_y[1], (body_y[18]-body_y[1])],
                        [body_y[4], (body_y[18]-body_y[4])], [body_y[5], (body_y[18]-body_y[5])], [body_y[6], (body_y[18]-body_y[6])],
                        #nose
                        [body_y[0], (body_y[18]-body_y[0])],
                        #mouth
                        [body_y[9], (body_y[18]-body_y[9])], [body_y[10], (body_y[18]-body_y[10])],
                        #pulgar------------------
                        #ear
                        [body_y[7], (body_y[22]-body_y[7])], [body_y[8], (body_y[22]-body_y[8])], 
                        #eye
                        [body_y[3], (body_y[22]-body_y[3])], [body_y[2], (body_y[22]-body_y[2])], [body_y[1], (body_y[22]-body_y[1])],
                        [body_y[4], (body_y[22]-body_y[4])], [body_y[5], (body_y[22]-body_y[5])], [body_y[6], (body_y[22]-body_y[6])],
                        #nose
                        [body_y[0], (body_y[22]-body_y[0])],
                        #mouth
                        [body_y[9], (body_y[22]-body_y[9])], [body_y[10], (body_y[22]-body_y[10])]
                    ]
                    
                    points_body_face_ZRight = [
                        #muñeca------------------
                        #ear
                        [body_z[7], (body_z[16]-body_z[7])], [body_z[8], (body_z[16]-body_z[8])], 
                        #eye
                        [body_z[3], (body_z[16]-body_z[3])], [body_z[2], (body_z[16]-body_z[2])], [body_z[1], (body_z[16]-body_z[1])],
                        [body_z[4], (body_z[16]-body_z[4])], [body_z[5], (body_z[16]-body_z[5])], [body_z[6], (body_z[16]-body_z[6])],
                        #nose
                        [body_z[0], (body_z[16]-body_z[0])],
                        #mouth
                        [body_z[9], (body_z[16]-body_z[9])], [body_z[10], (body_z[16]-body_z[10])],
                        #indice------------------
                        #ear
                        [body_z[7], (body_z[20]-body_z[7])], [body_z[8], (body_z[20]-body_z[8])], 
                        #eye
                        [body_z[3], (body_z[20]-body_z[3])], [body_z[2], (body_z[20]-body_z[2])], [body_z[1], (body_z[20]-body_z[1])],
                        [body_z[4], (body_z[20]-body_z[4])], [body_z[5], (body_z[20]-body_z[5])], [body_z[6], (body_z[20]-body_z[6])],
                        #nose
                        [body_z[0], (body_z[20]-body_z[0])],
                        #mouth
                        [body_z[9], (body_z[20]-body_z[9])], [body_z[10], (body_z[20]-body_z[10])],
                        #meñique------------------
                        #ear
                        [body_z[7], (body_z[18]-body_z[7])], [body_z[8], (body_z[18]-body_z[8])], 
                        #eye
                        [body_z[3], (body_z[18]-body_z[3])], [body_z[2], (body_z[18]-body_z[2])], [body_z[1], (body_z[18]-body_z[1])],
                        [body_z[4], (body_z[18]-body_z[4])], [body_z[5], (body_z[18]-body_z[5])], [body_z[6], (body_z[18]-body_z[6])],
                        #nose
                        [body_z[0], (body_z[18]-body_z[0])],
                        #mouth
                        [body_z[9], (body_z[18]-body_z[9])], [body_z[10], (body_z[18]-body_z[10])],
                        #pulgar------------------
                        #ear
                        [body_z[7], (body_z[22]-body_z[7])], [body_z[8], (body_z[22]-body_z[8])], 
                        #eye
                        [body_z[3], (body_z[22]-body_z[3])], [body_z[2], (body_z[22]-body_z[2])], [body_z[1], (body_z[22]-body_z[1])],
                        [body_z[4], (body_z[22]-body_z[4])], [body_z[5], (body_z[22]-body_z[5])], [body_z[6], (body_z[22]-body_z[6])],
                        #nose
                        [body_z[0], (body_z[22]-body_z[0])],
                        #mouth
                        [body_z[9], (body_z[22]-body_z[9])], [body_z[10], (body_z[22]-body_z[10])]
                    ]

            #FACE----------------------------------------------------
            if (face_relation) and not body_relation and len(points_body)>0:

                #Body
                body_x = list(map(lambda a: (a['x']), points_body))
                body_y = list(map(lambda a: (a['y']), points_body))
                body_z = list(map(lambda a: (a['z']), points_body))
                
                ## relation into same hands
                if len(hand_Left)>0:
                    #Left Hand
                    hands_x = list(map(lambda a: (a['x']), hand_Left))
                    hands_y = list(map(lambda a: (a['y']), hand_Left))
                    hands_z = list(map(lambda a: (a['z']), hand_Left))

                    hands_x = hands_x[1:]
                    hands_y = hands_y[1:]
                    hands_z = hands_z[1:]

                    ## Left Hand
                    points_face_XLeft = [[x1_elem, (x1_elem - x2_elem)] for x1_elem in hands_x for x2_elem in body_x]
                    
                    points_face_YLeft = [[x1_elem, (x1_elem - x2_elem)] for x1_elem in hands_y for x2_elem in body_y]
                    
                    points_face_ZLeft = [[x1_elem, (x1_elem - x2_elem)] for x1_elem in hands_z for x2_elem in body_z]
                    
                if len(hand_Right)>0:
                    #Right Hand
                    hands_x = list(map(lambda a: (a['x']), hand_Right))
                    hands_y = list(map(lambda a: (a['y']), hand_Right))
                    hands_z = list(map(lambda a: (a['z']), hand_Right))

                    hands_x = hands_x[1:]
                    hands_y = hands_y[1:]
                    hands_z = hands_z[1:]

                    #Right Hand
                    points_face_XRight = [[x1_elem, (x1_elem - x2_elem)] for x1_elem in hands_x for x2_elem in body_x]
                    
                    points_face_YRight = [[x1_elem, (x1_elem - x2_elem)] for x1_elem in hands_y for x2_elem in body_y]
                    
                    points_face_ZRight = [[x1_elem, (x1_elem - x2_elem)] for x1_elem in hands_z for x2_elem in body_z]
                

            #return values
            return [
                #HANDS---------------------------------------------------------
                ## hands relation  --> indepent of hand_relation, same hands
                points_hand_Right_diffX,#0
                points_hand_Right_diffY,#1
                points_hand_Right_diffZ,#2
                points_hand_Left_diffX,#3
                points_hand_Left_diffY,#4
                points_hand_Left_diffZ,#5
                ## hands difference --> when: hand_relation
                points_hand_diffX,#6
                points_hand_diffY,#7
                points_hand_diffZ,#8
                #BODY------------------------------------------------------------
                ## hands_body relation --> indepent of hand_relation, same hands
                points_body_XRight,#9
                points_body_YRight,#10
                points_body_ZRight,#11
                points_body_XLeft,#12
                points_body_YLeft,#13
                points_body_ZLeft,#14
                 ## body difference --> when: hand_relation
                points_body_diffX,#15
                points_body_diffY,#16
                points_body_diffZ,#17
                #BODY_FACE------------------------------------------------------
                ## body_face relation --> indepent of hand_relation, same hand
                points_body_face_XRight,#18
                points_body_face_YRight,#19
                points_body_face_ZRight,#20
                points_body_face_XLeft,#21
                points_body_face_YLeft,#22
                points_body_face_ZLeft,#23
                #FACE---------------------------------------------------------
                ## face relation  --> indepent of hand_relation, sane hand
                points_face_XRight,#24
                points_face_YRight,#25
                points_face_ZRight,#26
                points_face_XLeft,#27
                points_face_YLeft,#28
                points_face_ZLeft #29
            ]

        except Exception as e:
            print("Error Ocurrido [Hand model - make_model], Mensaje: {0}".format(str(e)))
            return None