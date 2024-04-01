import sys #line:58
import time #line:59
import copy #line:60
from time import strftime #line:62
from time import gmtime #line:63
import pandas as pd #line:65
import numpy #line:66
from pandas .api .types import CategoricalDtype #line:67
import progressbar #line:69
import re #line:70
class cleverminer :#line:71
    version_string ="1.0.11"#line:73
    def __init__ (O00OOO000O0O0OOOO ,**O0OO0O0O0OO0OO0O0 ):#line:75
        O00OOO000O0O0OOOO ._print_disclaimer ()#line:76
        O00OOO000O0O0OOOO .stats ={'total_cnt':0 ,'total_ver':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:85
        O00OOO000O0O0OOOO .options ={'max_categories':100 ,'max_rules':None ,'optimizations':True ,'automatic_data_conversions':True ,'progressbar':True ,'keep_df':False }#line:93
        O00OOO000O0O0OOOO .df =None #line:94
        O00OOO000O0O0OOOO .kwargs =None #line:95
        if len (O0OO0O0O0OO0OO0O0 )>0 :#line:96
            O00OOO000O0O0OOOO .kwargs =O0OO0O0O0OO0OO0O0 #line:97
        O00OOO000O0O0OOOO .verbosity ={}#line:98
        O00OOO000O0O0OOOO .verbosity ['debug']=False #line:99
        O00OOO000O0O0OOOO .verbosity ['print_rules']=False #line:100
        O00OOO000O0O0OOOO .verbosity ['print_hashes']=True #line:101
        O00OOO000O0O0OOOO .verbosity ['last_hash_time']=0 #line:102
        O00OOO000O0O0OOOO .verbosity ['hint']=False #line:103
        if "opts"in O0OO0O0O0OO0OO0O0 :#line:104
            O00OOO000O0O0OOOO ._set_opts (O0OO0O0O0OO0OO0O0 .get ("opts"))#line:105
        if "opts"in O0OO0O0O0OO0OO0O0 :#line:106
            if "verbose"in O0OO0O0O0OO0OO0O0 .get ('opts'):#line:107
                O0000OO000OO00OO0 =O0OO0O0O0OO0OO0O0 .get ('opts').get ('verbose')#line:108
                if O0000OO000OO00OO0 .upper ()=='FULL':#line:109
                    O00OOO000O0O0OOOO .verbosity ['debug']=True #line:110
                    O00OOO000O0O0OOOO .verbosity ['print_rules']=True #line:111
                    O00OOO000O0O0OOOO .verbosity ['print_hashes']=False #line:112
                    O00OOO000O0O0OOOO .verbosity ['hint']=True #line:113
                    O00OOO000O0O0OOOO .options ['progressbar']=False #line:114
                elif O0000OO000OO00OO0 .upper ()=='RULES':#line:115
                    O00OOO000O0O0OOOO .verbosity ['debug']=False #line:116
                    O00OOO000O0O0OOOO .verbosity ['print_rules']=True #line:117
                    O00OOO000O0O0OOOO .verbosity ['print_hashes']=True #line:118
                    O00OOO000O0O0OOOO .verbosity ['hint']=True #line:119
                    O00OOO000O0O0OOOO .options ['progressbar']=False #line:120
                elif O0000OO000OO00OO0 .upper ()=='HINT':#line:121
                    O00OOO000O0O0OOOO .verbosity ['debug']=False #line:122
                    O00OOO000O0O0OOOO .verbosity ['print_rules']=False #line:123
                    O00OOO000O0O0OOOO .verbosity ['print_hashes']=True #line:124
                    O00OOO000O0O0OOOO .verbosity ['last_hash_time']=0 #line:125
                    O00OOO000O0O0OOOO .verbosity ['hint']=True #line:126
                    O00OOO000O0O0OOOO .options ['progressbar']=False #line:127
                elif O0000OO000OO00OO0 .upper ()=='DEBUG':#line:128
                    O00OOO000O0O0OOOO .verbosity ['debug']=True #line:129
                    O00OOO000O0O0OOOO .verbosity ['print_rules']=True #line:130
                    O00OOO000O0O0OOOO .verbosity ['print_hashes']=True #line:131
                    O00OOO000O0O0OOOO .verbosity ['last_hash_time']=0 #line:132
                    O00OOO000O0O0OOOO .verbosity ['hint']=True #line:133
                    O00OOO000O0O0OOOO .options ['progressbar']=False #line:134
        O00OOO000O0O0OOOO ._is_py310 =sys .version_info [0 ]>=4 or (sys .version_info [0 ]>=3 and sys .version_info [1 ]>=10 )#line:135
        if not (O00OOO000O0O0OOOO ._is_py310 ):#line:136
            print ("Warning: Python 3.10+ NOT detected. You should upgrade to Python 3.10 or greater to get better performance")#line:137
        else :#line:138
            if (O00OOO000O0O0OOOO .verbosity ['debug']):#line:139
                print ("Python 3.10+ detected.")#line:140
        O00OOO000O0O0OOOO ._initialized =False #line:141
        O00OOO000O0O0OOOO ._init_data ()#line:142
        O00OOO000O0O0OOOO ._init_task ()#line:143
        if len (O0OO0O0O0OO0OO0O0 )>0 :#line:144
            if "df"in O0OO0O0O0OO0OO0O0 :#line:145
                O00OOO000O0O0OOOO ._prep_data (O0OO0O0O0OO0OO0O0 .get ("df"))#line:146
            else :#line:147
                print ("Missing dataframe. Cannot initialize.")#line:148
                O00OOO000O0O0OOOO ._initialized =False #line:149
                return #line:150
            O0OOOOOO00OOO0000 =O0OO0O0O0OO0OO0O0 .get ("proc",None )#line:151
            if not (O0OOOOOO00OOO0000 ==None ):#line:152
                O00OOO000O0O0OOOO ._calculate (**O0OO0O0O0OO0OO0O0 )#line:153
            else :#line:155
                if O00OOO000O0O0OOOO .verbosity ['debug']:#line:156
                    print ("INFO: just initialized")#line:157
                OOOO0OOOOO0O0O00O ={}#line:158
                OOO00O00O0OOO0OOO ={}#line:159
                OOO00O00O0OOO0OOO ["varname"]=O00OOO000O0O0OOOO .data ["varname"]#line:160
                OOO00O00O0OOO0OOO ["catnames"]=O00OOO000O0O0OOOO .data ["catnames"]#line:161
                OOOO0OOOOO0O0O00O ["datalabels"]=OOO00O00O0OOO0OOO #line:162
                O00OOO000O0O0OOOO .result =OOOO0OOOOO0O0O00O #line:163
        O00OOO000O0O0OOOO ._initialized =True #line:165
    def _set_opts (OOOO00O0OOOOO0O00 ,OO0O0O000000OOOOO ):#line:167
        if "no_optimizations"in OO0O0O000000OOOOO :#line:168
            OOOO00O0OOOOO0O00 .options ['optimizations']=not (OO0O0O000000OOOOO ['no_optimizations'])#line:169
            print ("No optimization will be made.")#line:170
        if "disable_progressbar"in OO0O0O000000OOOOO :#line:171
            OOOO00O0OOOOO0O00 .options ['progressbar']=False #line:172
            print ("Progressbar will not be shown.")#line:173
        if "max_rules"in OO0O0O000000OOOOO :#line:174
            OOOO00O0OOOOO0O00 .options ['max_rules']=OO0O0O000000OOOOO ['max_rules']#line:175
        if "max_categories"in OO0O0O000000OOOOO :#line:176
            OOOO00O0OOOOO0O00 .options ['max_categories']=OO0O0O000000OOOOO ['max_categories']#line:177
            if OOOO00O0OOOOO0O00 .verbosity ['debug']==True :#line:178
                print (f"Maximum number of categories set to {OOOO00O0OOOOO0O00.options['max_categories']}")#line:179
        if "no_automatic_data_conversions"in OO0O0O000000OOOOO :#line:180
            OOOO00O0OOOOO0O00 .options ['automatic_data_conversions']=not (OO0O0O000000OOOOO ['no_automatic_data_conversions'])#line:181
            print ("No automatic data conversions will be made.")#line:182
        if "keep_df"in OO0O0O000000OOOOO :#line:183
            OOOO00O0OOOOO0O00 .options ['keep_df']=OO0O0O000000OOOOO ['keep_df']#line:184
    def _init_data (OOOO00O0O0O0OO0O0 ):#line:187
        OOOO00O0O0O0OO0O0 .data ={}#line:189
        OOOO00O0O0O0OO0O0 .data ["varname"]=[]#line:190
        OOOO00O0O0O0OO0O0 .data ["catnames"]=[]#line:191
        OOOO00O0O0O0OO0O0 .data ["vtypes"]=[]#line:192
        OOOO00O0O0O0OO0O0 .data ["dm"]=[]#line:193
        OOOO00O0O0O0OO0O0 .data ["rows_count"]=int (0 )#line:194
        OOOO00O0O0O0OO0O0 .data ["data_prepared"]=0 #line:195
    def _init_task (OOOOOOOOO000O0O00 ):#line:197
        if "opts"in OOOOOOOOO000O0O00 .kwargs :#line:199
            OOOOOOOOO000O0O00 ._set_opts (OOOOOOOOO000O0O00 .kwargs .get ("opts"))#line:200
        OOOOOOOOO000O0O00 .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'trace_cedent_asindata':[],'traces':[],'generated_string':'','rule':{},'filter_value':int (0 )}#line:210
        OOOOOOOOO000O0O00 .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:214
        OOOOOOOOO000O0O00 .rulelist =[]#line:215
        OOOOOOOOO000O0O00 .stats ['total_cnt']=0 #line:217
        OOOOOOOOO000O0O00 .stats ['total_valid']=0 #line:218
        OOOOOOOOO000O0O00 .stats ['control_number']=0 #line:219
        OOOOOOOOO000O0O00 .result ={}#line:220
        OOOOOOOOO000O0O00 ._opt_base =None #line:221
        OOOOOOOOO000O0O00 ._opt_relbase =None #line:222
        OOOOOOOOO000O0O00 ._opt_base1 =None #line:223
        OOOOOOOOO000O0O00 ._opt_relbase1 =None #line:224
        OOOOOOOOO000O0O00 ._opt_base2 =None #line:225
        OOOOOOOOO000O0O00 ._opt_relbase2 =None #line:226
        O0O0OO0OOO000O000 =None #line:227
        if not (OOOOOOOOO000O0O00 .kwargs ==None ):#line:228
            O0O0OO0OOO000O000 =OOOOOOOOO000O0O00 .kwargs .get ("quantifiers",None )#line:229
            if not (O0O0OO0OOO000O000 ==None ):#line:230
                for O000O00O0000O0000 in O0O0OO0OOO000O000 .keys ():#line:231
                    if O000O00O0000O0000 .upper ()=='BASE':#line:232
                        OOOOOOOOO000O0O00 ._opt_base =O0O0OO0OOO000O000 .get (O000O00O0000O0000 )#line:233
                    if O000O00O0000O0000 .upper ()=='RELBASE':#line:234
                        OOOOOOOOO000O0O00 ._opt_relbase =O0O0OO0OOO000O000 .get (O000O00O0000O0000 )#line:235
                    if (O000O00O0000O0000 .upper ()=='FRSTBASE')|(O000O00O0000O0000 .upper ()=='BASE1'):#line:236
                        OOOOOOOOO000O0O00 ._opt_base1 =O0O0OO0OOO000O000 .get (O000O00O0000O0000 )#line:237
                    if (O000O00O0000O0000 .upper ()=='SCNDBASE')|(O000O00O0000O0000 .upper ()=='BASE2'):#line:238
                        OOOOOOOOO000O0O00 ._opt_base2 =O0O0OO0OOO000O000 .get (O000O00O0000O0000 )#line:239
                    if (O000O00O0000O0000 .upper ()=='FRSTRELBASE')|(O000O00O0000O0000 .upper ()=='RELBASE1'):#line:240
                        OOOOOOOOO000O0O00 ._opt_relbase1 =O0O0OO0OOO000O000 .get (O000O00O0000O0000 )#line:241
                    if (O000O00O0000O0000 .upper ()=='SCNDRELBASE')|(O000O00O0000O0000 .upper ()=='RELBASE2'):#line:242
                        OOOOOOOOO000O0O00 ._opt_relbase2 =O0O0OO0OOO000O000 .get (O000O00O0000O0000 )#line:243
            else :#line:244
                print ("Warning: no quantifiers found. Optimization will not take place (1)")#line:245
        else :#line:246
            print ("Warning: no quantifiers found. Optimization will not take place (2)")#line:247
    def mine (O000OO00OOO0OOO00 ,**O00OOO0OO0OO0OO00 ):#line:250
        if not (O000OO00OOO0OOO00 ._initialized ):#line:251
            print ("Class NOT INITIALIZED. Please call constructor with dataframe first")#line:252
            return #line:253
        O000OO00OOO0OOO00 .kwargs =None #line:254
        if len (O00OOO0OO0OO0OO00 )>0 :#line:255
            O000OO00OOO0OOO00 .kwargs =O00OOO0OO0OO0OO00 #line:256
        O000OO00OOO0OOO00 ._init_task ()#line:257
        if len (O00OOO0OO0OO0OO00 )>0 :#line:258
            OO0O000O0OOOOOOO0 =O00OOO0OO0OO0OO00 .get ("proc",None )#line:259
            if not (OO0O000O0OOOOOOO0 ==None ):#line:260
                O000OO00OOO0OOO00 ._calc_all (**O00OOO0OO0OO0OO00 )#line:261
            else :#line:262
                print ("Rule mining procedure missing")#line:263
    def _get_ver (O0OOOOOO0000O00O0 ):#line:266
        return O0OOOOOO0000O00O0 .version_string #line:267
    def _print_disclaimer (OOOOOOOOOOO0O00OO ):#line:269
        print (f"Cleverminer version {OOOOOOOOOOO0O00OO._get_ver()}.")#line:271
    def _automatic_data_conversions (O0OOO0O00O0OOOOO0 ,O0OO0O0OOO0O000OO ):#line:277
        print ("Automatically reordering numeric categories ...")#line:278
        for OOO00O0O00O000O0O in range (len (O0OO0O0OOO0O000OO .columns )):#line:279
            if O0OOO0O00O0OOOOO0 .verbosity ['debug']:#line:280
                print (f"#{OOO00O0O00O000O0O}: {O0OO0O0OOO0O000OO.columns[OOO00O0O00O000O0O]} : {O0OO0O0OOO0O000OO.dtypes[OOO00O0O00O000O0O]}.")#line:281
            try :#line:282
                O0OO0O0OOO0O000OO [O0OO0O0OOO0O000OO .columns [OOO00O0O00O000O0O ]]=O0OO0O0OOO0O000OO [O0OO0O0OOO0O000OO .columns [OOO00O0O00O000O0O ]].astype (str ).astype (float )#line:283
                if O0OOO0O00O0OOOOO0 .verbosity ['debug']:#line:284
                    print (f"CONVERTED TO FLOATS #{OOO00O0O00O000O0O}: {O0OO0O0OOO0O000OO.columns[OOO00O0O00O000O0O]} : {O0OO0O0OOO0O000OO.dtypes[OOO00O0O00O000O0O]}.")#line:285
                O000OO0OOOOO00000 =pd .unique (O0OO0O0OOO0O000OO [O0OO0O0OOO0O000OO .columns [OOO00O0O00O000O0O ]])#line:286
                OOOOO000O0O00OO0O =True #line:287
                for OO0OO0O0OOO000O00 in O000OO0OOOOO00000 :#line:288
                    if OO0OO0O0OOO000O00 %1 !=0 :#line:289
                        OOOOO000O0O00OO0O =False #line:290
                if OOOOO000O0O00OO0O :#line:291
                    O0OO0O0OOO0O000OO [O0OO0O0OOO0O000OO .columns [OOO00O0O00O000O0O ]]=O0OO0O0OOO0O000OO [O0OO0O0OOO0O000OO .columns [OOO00O0O00O000O0O ]].astype (int )#line:292
                    if O0OOO0O00O0OOOOO0 .verbosity ['debug']:#line:293
                        print (f"CONVERTED TO INT #{OOO00O0O00O000O0O}: {O0OO0O0OOO0O000OO.columns[OOO00O0O00O000O0O]} : {O0OO0O0OOO0O000OO.dtypes[OOO00O0O00O000O0O]}.")#line:294
                O00O0OO00OOOOOO00 =pd .unique (O0OO0O0OOO0O000OO [O0OO0O0OOO0O000OO .columns [OOO00O0O00O000O0O ]])#line:295
                OO0OO0OOO00OO0000 =CategoricalDtype (categories =O00O0OO00OOOOOO00 .sort (),ordered =True )#line:296
                O0OO0O0OOO0O000OO [O0OO0O0OOO0O000OO .columns [OOO00O0O00O000O0O ]]=O0OO0O0OOO0O000OO [O0OO0O0OOO0O000OO .columns [OOO00O0O00O000O0O ]].astype (OO0OO0OOO00OO0000 )#line:297
                if O0OOO0O00O0OOOOO0 .verbosity ['debug']:#line:298
                    print (f"CONVERTED TO CATEGORY #{OOO00O0O00O000O0O}: {O0OO0O0OOO0O000OO.columns[OOO00O0O00O000O0O]} : {O0OO0O0OOO0O000OO.dtypes[OOO00O0O00O000O0O]}.")#line:299
            except :#line:301
                if O0OOO0O00O0OOOOO0 .verbosity ['debug']:#line:302
                    print ("...cannot be converted to int")#line:303
                try :#line:304
                    OO0000O0O00OOOOOO =O0OO0O0OOO0O000OO [O0OO0O0OOO0O000OO .columns [OOO00O0O00O000O0O ]].unique ()#line:305
                    if O0OOO0O00O0OOOOO0 .verbosity ['debug']:#line:306
                        print (f"Values: {OO0000O0O00OOOOOO}")#line:307
                    OO0OO00OOO0OO00OO =True #line:308
                    O00OO0OOOO0000000 =[]#line:309
                    for OO0OO0O0OOO000O00 in OO0000O0O00OOOOOO :#line:310
                        O00O000O00O0000O0 =re .findall (r"-?\d+",OO0OO0O0OOO000O00 )#line:313
                        if len (O00O000O00O0000O0 )>0 :#line:315
                            O00OO0OOOO0000000 .append (int (O00O000O00O0000O0 [0 ]))#line:316
                        else :#line:317
                            OO0OO00OOO0OO00OO =False #line:318
                    if O0OOO0O00O0OOOOO0 .verbosity ['debug']:#line:319
                        print (f"Is ok: {OO0OO00OOO0OO00OO}, extracted {O00OO0OOOO0000000}")#line:320
                    if OO0OO00OOO0OO00OO :#line:321
                        OOO0OOOO00000OOOO =copy .deepcopy (O00OO0OOOO0000000 )#line:322
                        OOO0OOOO00000OOOO .sort ()#line:323
                        O0OOO000O000O0OO0 =[]#line:325
                        for OO0OOOO00O000O00O in OOO0OOOO00000OOOO :#line:326
                            OOOO00000O000000O =O00OO0OOOO0000000 .index (OO0OOOO00O000O00O )#line:327
                            O0OOO000O000O0OO0 .append (OO0000O0O00OOOOOO [OOOO00000O000000O ])#line:329
                        if O0OOO0O00O0OOOOO0 .verbosity ['debug']:#line:330
                            print (f"Sorted list: {O0OOO000O000O0OO0}")#line:331
                        OO0OO0OOO00OO0000 =CategoricalDtype (categories =O0OOO000O000O0OO0 ,ordered =True )#line:332
                        O0OO0O0OOO0O000OO [O0OO0O0OOO0O000OO .columns [OOO00O0O00O000O0O ]]=O0OO0O0OOO0O000OO [O0OO0O0OOO0O000OO .columns [OOO00O0O00O000O0O ]].astype (OO0OO0OOO00OO0000 )#line:333
                except :#line:336
                    if O0OOO0O00O0OOOOO0 .verbosity ['debug']:#line:337
                        print ("...cannot extract numbers from all categories")#line:338
    print ("Automatically reordering numeric categories ...done")#line:340
    def _prep_data (OO000O00000OO000O ,OO0O0O0O00000OOOO ):#line:342
        print ("Starting data preparation ...")#line:343
        OO000O00000OO000O ._init_data ()#line:344
        OO000O00000OO000O .stats ['start_prep_time']=time .time ()#line:345
        if OO000O00000OO000O .options ['automatic_data_conversions']:#line:346
            OO000O00000OO000O ._automatic_data_conversions (OO0O0O0O00000OOOO )#line:347
        OO000O00000OO000O .data ["rows_count"]=OO0O0O0O00000OOOO .shape [0 ]#line:348
        for OO000OO000O00O00O in OO0O0O0O00000OOOO .select_dtypes (exclude =['category']).columns :#line:349
            OO0O0O0O00000OOOO [OO000OO000O00O00O ]=OO0O0O0O00000OOOO [OO000OO000O00O00O ].apply (str )#line:350
        try :#line:351
            OO0O0000OO0OO000O =pd .DataFrame .from_records ([(O0O0O0OOO000O0O0O ,OO0O0O0O00000OOOO [O0O0O0OOO000O0O0O ].nunique ())for O0O0O0OOO000O0O0O in OO0O0O0O00000OOOO .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:353
        except :#line:354
            print ("Error in input data, probably unsupported data type. Will try to scan for column with unsupported type.")#line:355
            OOOO00OOO0OO000OO =""#line:356
            try :#line:357
                for OO000OO000O00O00O in OO0O0O0O00000OOOO .columns :#line:358
                    OOOO00OOO0OO000OO =OO000OO000O00O00O #line:359
                    print (f"...column {OO000OO000O00O00O} has {int(OO0O0O0O00000OOOO[OO000OO000O00O00O].nunique())} values")#line:360
            except :#line:361
                print (f"... detected : column {OOOO00OOO0OO000OO} has unsupported type: {type(OO0O0O0O00000OOOO[OO000OO000O00O00O])}.")#line:362
                exit (1 )#line:363
            print (f"Error in data profiling - attribute with unsupported type not detected. Please profile attributes manually, only simple attributes are supported.")#line:364
            exit (1 )#line:365
        if OO000O00000OO000O .verbosity ['hint']:#line:368
            print ("Quick profile of input data: unique value counts are:")#line:369
            print (OO0O0000OO0OO000O )#line:370
            for OO000OO000O00O00O in OO0O0O0O00000OOOO .columns :#line:371
                if OO0O0O0O00000OOOO [OO000OO000O00O00O ].nunique ()<OO000O00000OO000O .options ['max_categories']:#line:372
                    OO0O0O0O00000OOOO [OO000OO000O00O00O ]=OO0O0O0O00000OOOO [OO000OO000O00O00O ].astype ('category')#line:373
                else :#line:374
                    print (f"WARNING: attribute {OO000OO000O00O00O} has more than {OO000O00000OO000O.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:375
                    del OO0O0O0O00000OOOO [OO000OO000O00O00O ]#line:376
        for OO000OO000O00O00O in OO0O0O0O00000OOOO .columns :#line:378
            if OO0O0O0O00000OOOO [OO000OO000O00O00O ].nunique ()>OO000O00000OO000O .options ['max_categories']:#line:379
                print (f"WARNING: attribute {OO000OO000O00O00O} has more than {OO000O00000OO000O.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:380
                del OO0O0O0O00000OOOO [OO000OO000O00O00O ]#line:381
        if OO000O00000OO000O .options ['keep_df']:#line:382
            if OO000O00000OO000O .verbosity ['debug']:#line:383
                print ("Keeping df.")#line:384
            OO000O00000OO000O .df =OO0O0O0O00000OOOO #line:385
        print ("Encoding columns into bit-form...")#line:386
        OO0000000O000O000 =0 #line:387
        O0OO00O00OOO0OOOO =0 #line:388
        for OOOO0OO000O00O00O in OO0O0O0O00000OOOO :#line:389
            if OO000O00000OO000O .verbosity ['debug']:#line:391
                print ('Column: '+OOOO0OO000O00O00O )#line:392
            OO000O00000OO000O .data ["varname"].append (OOOO0OO000O00O00O )#line:393
            O0O00O00O0OOO000O =pd .get_dummies (OO0O0O0O00000OOOO [OOOO0OO000O00O00O ])#line:394
            O0OOO0OO0OOOO0O0O =0 #line:395
            if (OO0O0O0O00000OOOO .dtypes [OOOO0OO000O00O00O ].name =='category'):#line:396
                O0OOO0OO0OOOO0O0O =1 #line:397
            OO000O00000OO000O .data ["vtypes"].append (O0OOO0OO0OOOO0O0O )#line:398
            OO000O0000O000OO0 =0 #line:401
            O00000O00O0O000O0 =[]#line:402
            OO0OOO0O00OO00OO0 =[]#line:403
            for OOOO000OOOO00OO00 in O0O00O00O0OOO000O :#line:405
                if OO000O00000OO000O .verbosity ['debug']:#line:407
                    print ('....category : '+str (OOOO000OOOO00OO00 )+" @ "+str (time .time ()))#line:408
                O00000O00O0O000O0 .append (OOOO000OOOO00OO00 )#line:409
                O0OOOO00000OO00OO =int (0 )#line:410
                OOOOO0OO000000OO0 =O0O00O00O0OOO000O [OOOO000OOOO00OO00 ].values #line:411
                O0OOO000OOO0O0000 =numpy .packbits (OOOOO0OO000000OO0 ,bitorder ='little')#line:413
                O0OOOO00000OO00OO =int .from_bytes (O0OOO000OOO0O0000 ,byteorder ='little')#line:414
                OO0OOO0O00OO00OO0 .append (O0OOOO00000OO00OO )#line:415
                OO000O0000O000OO0 +=1 #line:433
                O0OO00O00OOO0OOOO +=1 #line:434
            OO000O00000OO000O .data ["catnames"].append (O00000O00O0O000O0 )#line:436
            OO000O00000OO000O .data ["dm"].append (OO0OOO0O00OO00OO0 )#line:437
        print ("Encoding columns into bit-form...done")#line:439
        if OO000O00000OO000O .verbosity ['hint']:#line:440
            print (f"List of attributes for analysis is: {OO000O00000OO000O.data['varname']}")#line:441
            print (f"List of category names for individual attributes is : {OO000O00000OO000O.data['catnames']}")#line:442
        if OO000O00000OO000O .verbosity ['debug']:#line:443
            print (f"List of vtypes is (all should be 1) : {OO000O00000OO000O.data['vtypes']}")#line:444
        OO000O00000OO000O .data ["data_prepared"]=1 #line:446
        print ("Data preparation finished.")#line:447
        if OO000O00000OO000O .verbosity ['debug']:#line:448
            print ('Number of variables : '+str (len (OO000O00000OO000O .data ["dm"])))#line:449
            print ('Total number of categories in all variables : '+str (O0OO00O00OOO0OOOO ))#line:450
        OO000O00000OO000O .stats ['end_prep_time']=time .time ()#line:451
        if OO000O00000OO000O .verbosity ['debug']:#line:452
            print ('Time needed for data preparation : ',str (OO000O00000OO000O .stats ['end_prep_time']-OO000O00000OO000O .stats ['start_prep_time']))#line:453
    def _bitcount (O00OOO00000O0OO00 ,O00000OOOO0O0OOOO ):#line:455
        O0OO0OOO00000OOO0 =None #line:456
        if (O00OOO00000O0OO00 ._is_py310 ):#line:457
            O0OO0OOO00000OOO0 =O00000OOOO0O0OOOO .bit_count ()#line:458
        else :#line:459
            O0OO0OOO00000OOO0 =bin (O00000OOOO0O0OOOO ).count ("1")#line:460
        return O0OO0OOO00000OOO0 #line:461
    def _verifyCF (OO0000OOO000OOO00 ,_OO00OOOOO00O0OO00 ):#line:464
        OO0O00O0OOO0OOOOO =OO0000OOO000OOO00 ._bitcount (_OO00OOOOO00O0OO00 )#line:465
        OO000O00O00O0OO0O =[]#line:466
        O0OOOOO0OOOO0OO0O =[]#line:467
        OO0OOOOO0000O00O0 =0 #line:468
        OOO0O0OO0000O00O0 =0 #line:469
        OO0OO0OO00OO0O0O0 =0 #line:470
        OOOOO000OOO00000O =0 #line:471
        O00O0OO0O0O000O0O =0 #line:472
        O000O0OO00OOO0O0O =0 #line:473
        O0OOO000O0O000000 =0 #line:474
        O0OO0000O0O0O0OOO =0 #line:475
        O00OOOOO000OO0OO0 =0 #line:476
        OO00O0OO0OOO00OOO =None #line:477
        O0OOO0O00O0OO0OOO =None #line:478
        O00O0O00OO00OOO00 =None #line:479
        if ('min_step_size'in OO0000OOO000OOO00 .quantifiers ):#line:480
            OO00O0OO0OOO00OOO =OO0000OOO000OOO00 .quantifiers .get ('min_step_size')#line:481
        if ('min_rel_step_size'in OO0000OOO000OOO00 .quantifiers ):#line:482
            O0OOO0O00O0OO0OOO =OO0000OOO000OOO00 .quantifiers .get ('min_rel_step_size')#line:483
            if O0OOO0O00O0OO0OOO >=1 and O0OOO0O00O0OO0OOO <100 :#line:484
                O0OOO0O00O0OO0OOO =O0OOO0O00O0OO0OOO /100 #line:485
        OOO0O0OOOO0O00OOO =0 #line:486
        OO0OO0O0O0000OOO0 =0 #line:487
        OO00OO0000000OOOO =[]#line:488
        if ('aad_weights'in OO0000OOO000OOO00 .quantifiers ):#line:489
            OOO0O0OOOO0O00OOO =1 #line:490
            OO0OO0O00OO00O0O0 =[]#line:491
            OO00OO0000000OOOO =OO0000OOO000OOO00 .quantifiers .get ('aad_weights')#line:492
        O0OOOO00OOO000OO0 =OO0000OOO000OOO00 .data ["dm"][OO0000OOO000OOO00 .data ["varname"].index (OO0000OOO000OOO00 .kwargs .get ('target'))]#line:493
        def OOO0OO0OOOOO00OO0 (OOOOOOOOO00000000 ,O000O000OOO0O0OOO ):#line:494
            O000OOO0O00OOO0OO =True #line:495
            if (OOOOOOOOO00000000 >O000O000OOO0O0OOO ):#line:496
                if not (OO00O0OO0OOO00OOO is None or OOOOOOOOO00000000 >=O000O000OOO0O0OOO +OO00O0OO0OOO00OOO ):#line:497
                    O000OOO0O00OOO0OO =False #line:498
                if not (O0OOO0O00O0OO0OOO is None or OOOOOOOOO00000000 >=O000O000OOO0O0OOO *(1 +O0OOO0O00O0OO0OOO )):#line:499
                    O000OOO0O00OOO0OO =False #line:500
            if (OOOOOOOOO00000000 <O000O000OOO0O0OOO ):#line:501
                if not (OO00O0OO0OOO00OOO is None or OOOOOOOOO00000000 <=O000O000OOO0O0OOO -OO00O0OO0OOO00OOO ):#line:502
                    O000OOO0O00OOO0OO =False #line:503
                if not (O0OOO0O00O0OO0OOO is None or OOOOOOOOO00000000 <=O000O000OOO0O0OOO *(1 -O0OOO0O00O0OO0OOO )):#line:504
                    O000OOO0O00OOO0OO =False #line:505
            return O000OOO0O00OOO0OO #line:506
        for OOOOOOO00O0O00O00 in range (len (O0OOOO00OOO000OO0 )):#line:507
            OOO0O0OO0000O00O0 =OO0OOOOO0000O00O0 #line:509
            OO0OOOOO0000O00O0 =OO0000OOO000OOO00 ._bitcount (_OO00OOOOO00O0OO00 &O0OOOO00OOO000OO0 [OOOOOOO00O0O00O00 ])#line:510
            OO000O00O00O0OO0O .append (OO0OOOOO0000O00O0 )#line:511
            if OOOOOOO00O0O00O00 >0 :#line:512
                if (OO0OOOOO0000O00O0 >OOO0O0OO0000O00O0 ):#line:513
                    if (OO0OO0OO00OO0O0O0 ==1 )and (OOO0OO0OOOOO00OO0 (OO0OOOOO0000O00O0 ,OOO0O0OO0000O00O0 )):#line:514
                        O0OO0000O0O0O0OOO +=1 #line:515
                    else :#line:516
                        if OOO0OO0OOOOO00OO0 (OO0OOOOO0000O00O0 ,OOO0O0OO0000O00O0 ):#line:517
                            O0OO0000O0O0O0OOO =1 #line:518
                        else :#line:519
                            O0OO0000O0O0O0OOO =0 #line:520
                    if O0OO0000O0O0O0OOO >OOOOO000OOO00000O :#line:521
                        OOOOO000OOO00000O =O0OO0000O0O0O0OOO #line:522
                    OO0OO0OO00OO0O0O0 =1 #line:523
                    if OOO0OO0OOOOO00OO0 (OO0OOOOO0000O00O0 ,OOO0O0OO0000O00O0 ):#line:524
                        O000O0OO00OOO0O0O +=1 #line:525
                if (OO0OOOOO0000O00O0 <OOO0O0OO0000O00O0 ):#line:526
                    if (OO0OO0OO00OO0O0O0 ==-1 )and (OOO0OO0OOOOO00OO0 (OO0OOOOO0000O00O0 ,OOO0O0OO0000O00O0 )):#line:527
                        O00OOOOO000OO0OO0 +=1 #line:528
                    else :#line:529
                        if OOO0OO0OOOOO00OO0 (OO0OOOOO0000O00O0 ,OOO0O0OO0000O00O0 ):#line:530
                            O00OOOOO000OO0OO0 =1 #line:531
                        else :#line:532
                            O00OOOOO000OO0OO0 =0 #line:533
                    if O00OOOOO000OO0OO0 >O00O0OO0O0O000O0O :#line:534
                        O00O0OO0O0O000O0O =O00OOOOO000OO0OO0 #line:535
                    OO0OO0OO00OO0O0O0 =-1 #line:536
                    if OOO0OO0OOOOO00OO0 (OO0OOOOO0000O00O0 ,OOO0O0OO0000O00O0 ):#line:537
                        O0OOO000O0O000000 +=1 #line:538
                if (OO0OOOOO0000O00O0 ==OOO0O0OO0000O00O0 ):#line:539
                    OO0OO0OO00OO0O0O0 =0 #line:540
                    O00OOOOO000OO0OO0 =0 #line:541
                    O0OO0000O0O0O0OOO =0 #line:542
            if (OOO0O0OOOO0O00OOO ):#line:544
                O0OOO000OO000O000 =OO0000OOO000OOO00 ._bitcount (O0OOOO00OOO000OO0 [OOOOOOO00O0O00O00 ])#line:545
                OO0OO0O00OO00O0O0 .append (O0OOO000OO000O000 )#line:546
        if (OOO0O0OOOO0O00OOO &sum (OO000O00O00O0OO0O )>0 ):#line:548
            for OOOOOOO00O0O00O00 in range (len (O0OOOO00OOO000OO0 )):#line:549
                if OO0OO0O00OO00O0O0 [OOOOOOO00O0O00O00 ]>0 :#line:550
                    if OO000O00O00O0OO0O [OOOOOOO00O0O00O00 ]/sum (OO000O00O00O0OO0O )>OO0OO0O00OO00O0O0 [OOOOOOO00O0O00O00 ]/sum (OO0OO0O00OO00O0O0 ):#line:552
                        OO0OO0O0O0000OOO0 +=OO00OO0000000OOOO [OOOOOOO00O0O00O00 ]*((OO000O00O00O0OO0O [OOOOOOO00O0O00O00 ]/sum (OO000O00O00O0OO0O ))/(OO0OO0O00OO00O0O0 [OOOOOOO00O0O00O00 ]/sum (OO0OO0O00OO00O0O0 ))-1 )#line:553
        O0O0O000OO0O0O0O0 =True #line:556
        for O00O00O000OOOO000 in OO0000OOO000OOO00 .quantifiers .keys ():#line:557
            if O00O00O000OOOO000 .upper ()=='BASE':#line:558
                O0O0O000OO0O0O0O0 =O0O0O000OO0O0O0O0 and (OO0000OOO000OOO00 .quantifiers .get (O00O00O000OOOO000 )<=OO0O00O0OOO0OOOOO )#line:559
            if O00O00O000OOOO000 .upper ()=='RELBASE':#line:560
                O0O0O000OO0O0O0O0 =O0O0O000OO0O0O0O0 and (OO0000OOO000OOO00 .quantifiers .get (O00O00O000OOOO000 )<=OO0O00O0OOO0OOOOO *1.0 /OO0000OOO000OOO00 .data ["rows_count"])#line:561
            if O00O00O000OOOO000 .upper ()=='S_UP':#line:562
                O0O0O000OO0O0O0O0 =O0O0O000OO0O0O0O0 and (OO0000OOO000OOO00 .quantifiers .get (O00O00O000OOOO000 )<=OOOOO000OOO00000O )#line:563
            if O00O00O000OOOO000 .upper ()=='S_DOWN':#line:564
                O0O0O000OO0O0O0O0 =O0O0O000OO0O0O0O0 and (OO0000OOO000OOO00 .quantifiers .get (O00O00O000OOOO000 )<=O00O0OO0O0O000O0O )#line:565
            if O00O00O000OOOO000 .upper ()=='S_ANY_UP':#line:566
                O0O0O000OO0O0O0O0 =O0O0O000OO0O0O0O0 and (OO0000OOO000OOO00 .quantifiers .get (O00O00O000OOOO000 )<=OOOOO000OOO00000O )#line:567
            if O00O00O000OOOO000 .upper ()=='S_ANY_DOWN':#line:568
                O0O0O000OO0O0O0O0 =O0O0O000OO0O0O0O0 and (OO0000OOO000OOO00 .quantifiers .get (O00O00O000OOOO000 )<=O00O0OO0O0O000O0O )#line:569
            if O00O00O000OOOO000 .upper ()=='MAX':#line:570
                O0O0O000OO0O0O0O0 =O0O0O000OO0O0O0O0 and (OO0000OOO000OOO00 .quantifiers .get (O00O00O000OOOO000 )<=max (OO000O00O00O0OO0O ))#line:571
            if O00O00O000OOOO000 .upper ()=='MIN':#line:572
                O0O0O000OO0O0O0O0 =O0O0O000OO0O0O0O0 and (OO0000OOO000OOO00 .quantifiers .get (O00O00O000OOOO000 )<=min (OO000O00O00O0OO0O ))#line:573
            if O00O00O000OOOO000 .upper ()=='RELMAX':#line:574
                if sum (OO000O00O00O0OO0O )>0 :#line:575
                    O0O0O000OO0O0O0O0 =O0O0O000OO0O0O0O0 and (OO0000OOO000OOO00 .quantifiers .get (O00O00O000OOOO000 )<=max (OO000O00O00O0OO0O )*1.0 /sum (OO000O00O00O0OO0O ))#line:576
                else :#line:577
                    O0O0O000OO0O0O0O0 =False #line:578
            if O00O00O000OOOO000 .upper ()=='RELMAX_LEQ':#line:579
                if sum (OO000O00O00O0OO0O )>0 :#line:580
                    O0O0O000OO0O0O0O0 =O0O0O000OO0O0O0O0 and (OO0000OOO000OOO00 .quantifiers .get (O00O00O000OOOO000 )>=max (OO000O00O00O0OO0O )*1.0 /sum (OO000O00O00O0OO0O ))#line:581
                else :#line:582
                    O0O0O000OO0O0O0O0 =False #line:583
            if O00O00O000OOOO000 .upper ()=='RELMIN':#line:584
                if sum (OO000O00O00O0OO0O )>0 :#line:585
                    O0O0O000OO0O0O0O0 =O0O0O000OO0O0O0O0 and (OO0000OOO000OOO00 .quantifiers .get (O00O00O000OOOO000 )<=min (OO000O00O00O0OO0O )*1.0 /sum (OO000O00O00O0OO0O ))#line:586
                else :#line:587
                    O0O0O000OO0O0O0O0 =False #line:588
            if O00O00O000OOOO000 .upper ()=='RELMIN_LEQ':#line:589
                if sum (OO000O00O00O0OO0O )>0 :#line:590
                    O0O0O000OO0O0O0O0 =O0O0O000OO0O0O0O0 and (OO0000OOO000OOO00 .quantifiers .get (O00O00O000OOOO000 )>=min (OO000O00O00O0OO0O )*1.0 /sum (OO000O00O00O0OO0O ))#line:591
                else :#line:592
                    O0O0O000OO0O0O0O0 =False #line:593
            if O00O00O000OOOO000 .upper ()=='AAD':#line:594
                O0O0O000OO0O0O0O0 =O0O0O000OO0O0O0O0 and (OO0000OOO000OOO00 .quantifiers .get (O00O00O000OOOO000 )<=OO0OO0O0O0000OOO0 )#line:595
            if O00O00O000OOOO000 .upper ()=='RELRANGE_LEQ':#line:597
                O00OO0000000O0OOO =OO0000OOO000OOO00 .quantifiers .get (O00O00O000OOOO000 )#line:598
                if O00OO0000000O0OOO >=1 and O00OO0000000O0OOO <100 :#line:599
                    O00OO0000000O0OOO =O00OO0000000O0OOO *1.0 /100 #line:600
                OO00OOOO0OOO0O0OO =min (OO000O00O00O0OO0O )*1.0 /sum (OO000O00O00O0OO0O )#line:601
                O000OOOOOOOOO00O0 =max (OO000O00O00O0OO0O )*1.0 /sum (OO000O00O00O0OO0O )#line:602
                O0O0O000OO0O0O0O0 =O0O0O000OO0O0O0O0 and (O00OO0000000O0OOO >=O000OOOOOOOOO00O0 -OO00OOOO0OOO0O0OO )#line:603
        O00OOOOOOOO0000OO ={}#line:604
        if O0O0O000OO0O0O0O0 ==True :#line:605
            OO0000OOO000OOO00 .stats ['total_valid']+=1 #line:607
            O00OOOOOOOO0000OO ["base"]=OO0O00O0OOO0OOOOO #line:608
            O00OOOOOOOO0000OO ["rel_base"]=OO0O00O0OOO0OOOOO *1.0 /OO0000OOO000OOO00 .data ["rows_count"]#line:609
            O00OOOOOOOO0000OO ["s_up"]=OOOOO000OOO00000O #line:610
            O00OOOOOOOO0000OO ["s_down"]=O00O0OO0O0O000O0O #line:611
            O00OOOOOOOO0000OO ["s_any_up"]=O000O0OO00OOO0O0O #line:612
            O00OOOOOOOO0000OO ["s_any_down"]=O0OOO000O0O000000 #line:613
            O00OOOOOOOO0000OO ["max"]=max (OO000O00O00O0OO0O )#line:614
            O00OOOOOOOO0000OO ["min"]=min (OO000O00O00O0OO0O )#line:615
            if sum (OO000O00O00O0OO0O )>0 :#line:618
                O00OOOOOOOO0000OO ["rel_max"]=max (OO000O00O00O0OO0O )*1.0 /sum (OO000O00O00O0OO0O )#line:619
                O00OOOOOOOO0000OO ["rel_min"]=min (OO000O00O00O0OO0O )*1.0 /sum (OO000O00O00O0OO0O )#line:620
            else :#line:621
                O00OOOOOOOO0000OO ["rel_max"]=0 #line:622
                O00OOOOOOOO0000OO ["rel_min"]=0 #line:623
            O00OOOOOOOO0000OO ["hist"]=OO000O00O00O0OO0O #line:624
            if OOO0O0OOOO0O00OOO :#line:625
                O00OOOOOOOO0000OO ["aad"]=OO0OO0O0O0000OOO0 #line:626
                O00OOOOOOOO0000OO ["hist_full"]=OO0OO0O00OO00O0O0 #line:627
                O00OOOOOOOO0000OO ["rel_hist"]=[O0000O00O0O000000 /sum (OO000O00O00O0OO0O )for O0000O00O0O000000 in OO000O00O00O0OO0O ]#line:628
                O00OOOOOOOO0000OO ["rel_hist_full"]=[OOO0OOO00OO00OO0O /sum (OO0OO0O00OO00O0O0 )for OOO0OOO00OO00OO0O in OO0OO0O00OO00O0O0 ]#line:629
        return O0O0O000OO0O0O0O0 ,O00OOOOOOOO0000OO #line:631
    def _verifyUIC (OOO00OO0OOO00OOO0 ,_O0O0O00OO00O00O00 ):#line:633
        OO000000O0O0000OO ={}#line:634
        OO0O0000OO00OOO00 =0 #line:635
        for O0O00OO00O0OO0OOO in OOO00OO0OOO00OOO0 .task_actinfo ['cedents']:#line:636
            OO000000O0O0000OO [O0O00OO00O0OO0OOO ['cedent_type']]=O0O00OO00O0OO0OOO ['filter_value']#line:638
            OO0O0000OO00OOO00 =OO0O0000OO00OOO00 +1 #line:639
        OO0000OO0O0000O0O =OOO00OO0OOO00OOO0 ._bitcount (_O0O0O00OO00O00O00 )#line:641
        OO0OOO0OOO0000OOO =[]#line:642
        O0O0O0OOO0OOOO0OO =0 #line:643
        OO0OO00OOO000000O =0 #line:644
        OO0O00O00OOOO0O00 =0 #line:645
        O00O0OOO0OO0O0OO0 =[]#line:646
        OO00OO00OO0OOO000 =[]#line:647
        if ('aad_weights'in OOO00OO0OOO00OOO0 .quantifiers ):#line:648
            O00O0OOO0OO0O0OO0 =OOO00OO0OOO00OOO0 .quantifiers .get ('aad_weights')#line:649
            OO0OO00OOO000000O =1 #line:650
        O0O000O0OO000OO00 =OOO00OO0OOO00OOO0 .data ["dm"][OOO00OO0OOO00OOO0 .data ["varname"].index (OOO00OO0OOO00OOO0 .kwargs .get ('target'))]#line:651
        for OOOO0O0OO0O0OO000 in range (len (O0O000O0OO000OO00 )):#line:652
            OO0000O000OOO0000 =O0O0O0OOO0OOOO0OO #line:654
            O0O0O0OOO0OOOO0OO =OOO00OO0OOO00OOO0 ._bitcount (_O0O0O00OO00O00O00 &O0O000O0OO000OO00 [OOOO0O0OO0O0OO000 ])#line:655
            OO0OOO0OOO0000OOO .append (O0O0O0OOO0OOOO0OO )#line:656
            O0O0OO0O0O0OOOO0O =OOO00OO0OOO00OOO0 ._bitcount (OO000000O0O0000OO ['cond']&O0O000O0OO000OO00 [OOOO0O0OO0O0OO000 ])#line:659
            OO00OO00OO0OOO000 .append (O0O0OO0O0O0OOOO0O )#line:660
        if (OO0OO00OOO000000O &sum (OO0OOO0OOO0000OOO )>0 ):#line:662
            for OOOO0O0OO0O0OO000 in range (len (O0O000O0OO000OO00 )):#line:663
                if OO00OO00OO0OOO000 [OOOO0O0OO0O0OO000 ]>0 :#line:664
                    if OO0OOO0OOO0000OOO [OOOO0O0OO0O0OO000 ]/sum (OO0OOO0OOO0000OOO )>OO00OO00OO0OOO000 [OOOO0O0OO0O0OO000 ]/sum (OO00OO00OO0OOO000 ):#line:666
                        OO0O00O00OOOO0O00 +=O00O0OOO0OO0O0OO0 [OOOO0O0OO0O0OO000 ]*((OO0OOO0OOO0000OOO [OOOO0O0OO0O0OO000 ]/sum (OO0OOO0OOO0000OOO ))/(OO00OO00OO0OOO000 [OOOO0O0OO0O0OO000 ]/sum (OO00OO00OO0OOO000 ))-1 )#line:667
        OOOO00O0OO0000OO0 =True #line:670
        for O0O0OOOO0OOO0OO00 in OOO00OO0OOO00OOO0 .quantifiers .keys ():#line:671
            if O0O0OOOO0OOO0OO00 .upper ()=='BASE':#line:672
                OOOO00O0OO0000OO0 =OOOO00O0OO0000OO0 and (OOO00OO0OOO00OOO0 .quantifiers .get (O0O0OOOO0OOO0OO00 )<=OO0000OO0O0000O0O )#line:673
            if O0O0OOOO0OOO0OO00 .upper ()=='RELBASE':#line:674
                OOOO00O0OO0000OO0 =OOOO00O0OO0000OO0 and (OOO00OO0OOO00OOO0 .quantifiers .get (O0O0OOOO0OOO0OO00 )<=OO0000OO0O0000O0O *1.0 /OOO00OO0OOO00OOO0 .data ["rows_count"])#line:675
            if O0O0OOOO0OOO0OO00 .upper ()=='AAD_SCORE':#line:676
                OOOO00O0OO0000OO0 =OOOO00O0OO0000OO0 and (OOO00OO0OOO00OOO0 .quantifiers .get (O0O0OOOO0OOO0OO00 )<=OO0O00O00OOOO0O00 )#line:677
        O0O0O00O0O0O0O000 ={}#line:679
        if OOOO00O0OO0000OO0 ==True :#line:680
            OOO00OO0OOO00OOO0 .stats ['total_valid']+=1 #line:682
            O0O0O00O0O0O0O000 ["base"]=OO0000OO0O0000O0O #line:683
            O0O0O00O0O0O0O000 ["rel_base"]=OO0000OO0O0000O0O *1.0 /OOO00OO0OOO00OOO0 .data ["rows_count"]#line:684
            O0O0O00O0O0O0O000 ["hist"]=OO0OOO0OOO0000OOO #line:685
            O0O0O00O0O0O0O000 ["aad_score"]=OO0O00O00OOOO0O00 #line:687
            O0O0O00O0O0O0O000 ["hist_cond"]=OO00OO00OO0OOO000 #line:688
            O0O0O00O0O0O0O000 ["rel_hist"]=[O00000OOOO000OOO0 /sum (OO0OOO0OOO0000OOO )for O00000OOOO000OOO0 in OO0OOO0OOO0000OOO ]#line:689
            O0O0O00O0O0O0O000 ["rel_hist_cond"]=[OO00OOO0O0OO00000 /sum (OO00OO00OO0OOO000 )for OO00OOO0O0OO00000 in OO00OO00OO0OOO000 ]#line:690
        return OOOO00O0OO0000OO0 ,O0O0O00O0O0O0O000 #line:692
    def _verify4ft (O0O00OO00OO00O000 ,_O00O0OOO00O0O0OOO ):#line:694
        OO0O000O00OO000OO ={}#line:695
        OO0000O00OOO0O0O0 =0 #line:696
        for O00O00O0OO00O00OO in O0O00OO00OO00O000 .task_actinfo ['cedents']:#line:697
            OO0O000O00OO000OO [O00O00O0OO00O00OO ['cedent_type']]=O00O00O0OO00O00OO ['filter_value']#line:699
            OO0000O00OOO0O0O0 =OO0000O00OOO0O0O0 +1 #line:700
        OOOOO00O0O00O0OO0 =O0O00OO00OO00O000 ._bitcount (OO0O000O00OO000OO ['ante']&OO0O000O00OO000OO ['succ']&OO0O000O00OO000OO ['cond'])#line:702
        O00O00O0OO0OOO000 =None #line:703
        O00O00O0OO0OOO000 =0 #line:704
        if OOOOO00O0O00O0OO0 >0 :#line:713
            O00O00O0OO0OOO000 =O0O00OO00OO00O000 ._bitcount (OO0O000O00OO000OO ['ante']&OO0O000O00OO000OO ['succ']&OO0O000O00OO000OO ['cond'])*1.0 /O0O00OO00OO00O000 ._bitcount (OO0O000O00OO000OO ['ante']&OO0O000O00OO000OO ['cond'])#line:714
        OO00O00OOO00O0OOO =1 <<O0O00OO00OO00O000 .data ["rows_count"]#line:716
        OO0OO0000OO0O0OOO =O0O00OO00OO00O000 ._bitcount (OO0O000O00OO000OO ['ante']&OO0O000O00OO000OO ['succ']&OO0O000O00OO000OO ['cond'])#line:717
        O0O0OOOOO00O0O0OO =O0O00OO00OO00O000 ._bitcount (OO0O000O00OO000OO ['ante']&~(OO00O00OOO00O0OOO |OO0O000O00OO000OO ['succ'])&OO0O000O00OO000OO ['cond'])#line:718
        O00O00O0OO00O00OO =O0O00OO00OO00O000 ._bitcount (~(OO00O00OOO00O0OOO |OO0O000O00OO000OO ['ante'])&OO0O000O00OO000OO ['succ']&OO0O000O00OO000OO ['cond'])#line:719
        O0OOO0OOO00O0OO0O =O0O00OO00OO00O000 ._bitcount (~(OO00O00OOO00O0OOO |OO0O000O00OO000OO ['ante'])&~(OO00O00OOO00O0OOO |OO0O000O00OO000OO ['succ'])&OO0O000O00OO000OO ['cond'])#line:720
        O0000OO00OO00OO00 =0 #line:721
        if (OO0OO0000OO0O0OOO +O0O0OOOOO00O0O0OO )*(OO0OO0000OO0O0OOO +O00O00O0OO00O00OO )>0 :#line:722
            O0000OO00OO00OO00 =OO0OO0000OO0O0OOO *(OO0OO0000OO0O0OOO +O0O0OOOOO00O0O0OO +O00O00O0OO00O00OO +O0OOO0OOO00O0OO0O )/(OO0OO0000OO0O0OOO +O0O0OOOOO00O0O0OO )/(OO0OO0000OO0O0OOO +O00O00O0OO00O00OO )-1 #line:723
        else :#line:724
            O0000OO00OO00OO00 =None #line:725
        OO0O0000000O0O0OO =0 #line:726
        if (OO0OO0000OO0O0OOO +O0O0OOOOO00O0O0OO )*(OO0OO0000OO0O0OOO +O00O00O0OO00O00OO )>0 :#line:727
            OO0O0000000O0O0OO =1 -OO0OO0000OO0O0OOO *(OO0OO0000OO0O0OOO +O0O0OOOOO00O0O0OO +O00O00O0OO00O00OO +O0OOO0OOO00O0OO0O )/(OO0OO0000OO0O0OOO +O0O0OOOOO00O0O0OO )/(OO0OO0000OO0O0OOO +O00O00O0OO00O00OO )#line:728
        else :#line:729
            OO0O0000000O0O0OO =None #line:730
        O0000OOO0O0O000OO =True #line:731
        for O00O0OOO0O00OOOOO in O0O00OO00OO00O000 .quantifiers .keys ():#line:732
            if O00O0OOO0O00OOOOO .upper ()=='BASE':#line:733
                O0000OOO0O0O000OO =O0000OOO0O0O000OO and (O0O00OO00OO00O000 .quantifiers .get (O00O0OOO0O00OOOOO )<=OOOOO00O0O00O0OO0 )#line:734
            if O00O0OOO0O00OOOOO .upper ()=='RELBASE':#line:735
                O0000OOO0O0O000OO =O0000OOO0O0O000OO and (O0O00OO00OO00O000 .quantifiers .get (O00O0OOO0O00OOOOO )<=OOOOO00O0O00O0OO0 *1.0 /O0O00OO00OO00O000 .data ["rows_count"])#line:736
            if (O00O0OOO0O00OOOOO .upper ()=='PIM')or (O00O0OOO0O00OOOOO .upper ()=='CONF'):#line:737
                O0000OOO0O0O000OO =O0000OOO0O0O000OO and (O0O00OO00OO00O000 .quantifiers .get (O00O0OOO0O00OOOOO )<=O00O00O0OO0OOO000 )#line:738
            if O00O0OOO0O00OOOOO .upper ()=='AAD':#line:739
                if O0000OO00OO00OO00 !=None :#line:740
                    O0000OOO0O0O000OO =O0000OOO0O0O000OO and (O0O00OO00OO00O000 .quantifiers .get (O00O0OOO0O00OOOOO )<=O0000OO00OO00OO00 )#line:741
                else :#line:742
                    O0000OOO0O0O000OO =False #line:743
            if O00O0OOO0O00OOOOO .upper ()=='BAD':#line:744
                if OO0O0000000O0O0OO !=None :#line:745
                    O0000OOO0O0O000OO =O0000OOO0O0O000OO and (O0O00OO00OO00O000 .quantifiers .get (O00O0OOO0O00OOOOO )<=OO0O0000000O0O0OO )#line:746
                else :#line:747
                    O0000OOO0O0O000OO =False #line:748
            O00000O00O0O0O00O ={}#line:749
        if O0000OOO0O0O000OO ==True :#line:750
            O0O00OO00OO00O000 .stats ['total_valid']+=1 #line:752
            O00000O00O0O0O00O ["base"]=OOOOO00O0O00O0OO0 #line:753
            O00000O00O0O0O00O ["rel_base"]=OOOOO00O0O00O0OO0 *1.0 /O0O00OO00OO00O000 .data ["rows_count"]#line:754
            O00000O00O0O0O00O ["conf"]=O00O00O0OO0OOO000 #line:755
            O00000O00O0O0O00O ["aad"]=O0000OO00OO00OO00 #line:756
            O00000O00O0O0O00O ["bad"]=OO0O0000000O0O0OO #line:757
            O00000O00O0O0O00O ["fourfold"]=[OO0OO0000OO0O0OOO ,O0O0OOOOO00O0O0OO ,O00O00O0OO00O00OO ,O0OOO0OOO00O0OO0O ]#line:758
        return O0000OOO0O0O000OO ,O00000O00O0O0O00O #line:762
    def _verifysd4ft (O000OOOOOOOO0OO0O ,_O000O0O0O0OOOO0O0 ):#line:764
        OO00O000O0O000O0O ={}#line:765
        OO00O000O00OO00OO =0 #line:766
        for O000O000O00OO0000 in O000OOOOOOOO0OO0O .task_actinfo ['cedents']:#line:767
            OO00O000O0O000O0O [O000O000O00OO0000 ['cedent_type']]=O000O000O00OO0000 ['filter_value']#line:769
            OO00O000O00OO00OO =OO00O000O00OO00OO +1 #line:770
        O0000OOO0OO0000OO =O000OOOOOOOO0OO0O ._bitcount (OO00O000O0O000O0O ['ante']&OO00O000O0O000O0O ['succ']&OO00O000O0O000O0O ['cond']&OO00O000O0O000O0O ['frst'])#line:772
        O00O0OOOOO000OO0O =O000OOOOOOOO0OO0O ._bitcount (OO00O000O0O000O0O ['ante']&OO00O000O0O000O0O ['succ']&OO00O000O0O000O0O ['cond']&OO00O000O0O000O0O ['scnd'])#line:773
        O0OO0OOOO0OO0OO0O =None #line:774
        OOOOO0OOOOO0OOOO0 =0 #line:775
        O0OO0OOOOOO0OO0OO =0 #line:776
        if O0000OOO0OO0000OO >0 :#line:785
            OOOOO0OOOOO0OOOO0 =O000OOOOOOOO0OO0O ._bitcount (OO00O000O0O000O0O ['ante']&OO00O000O0O000O0O ['succ']&OO00O000O0O000O0O ['cond']&OO00O000O0O000O0O ['frst'])*1.0 /O000OOOOOOOO0OO0O ._bitcount (OO00O000O0O000O0O ['ante']&OO00O000O0O000O0O ['cond']&OO00O000O0O000O0O ['frst'])#line:786
        if O00O0OOOOO000OO0O >0 :#line:787
            O0OO0OOOOOO0OO0OO =O000OOOOOOOO0OO0O ._bitcount (OO00O000O0O000O0O ['ante']&OO00O000O0O000O0O ['succ']&OO00O000O0O000O0O ['cond']&OO00O000O0O000O0O ['scnd'])*1.0 /O000OOOOOOOO0OO0O ._bitcount (OO00O000O0O000O0O ['ante']&OO00O000O0O000O0O ['cond']&OO00O000O0O000O0O ['scnd'])#line:788
        O0O00O00000OO0O00 =1 <<O000OOOOOOOO0OO0O .data ["rows_count"]#line:790
        O0O0O0O0O0OO0O000 =O000OOOOOOOO0OO0O ._bitcount (OO00O000O0O000O0O ['ante']&OO00O000O0O000O0O ['succ']&OO00O000O0O000O0O ['cond']&OO00O000O0O000O0O ['frst'])#line:791
        O000OO0O0O0OOO0OO =O000OOOOOOOO0OO0O ._bitcount (OO00O000O0O000O0O ['ante']&~(O0O00O00000OO0O00 |OO00O000O0O000O0O ['succ'])&OO00O000O0O000O0O ['cond']&OO00O000O0O000O0O ['frst'])#line:792
        OOO0O00OO000O0OOO =O000OOOOOOOO0OO0O ._bitcount (~(O0O00O00000OO0O00 |OO00O000O0O000O0O ['ante'])&OO00O000O0O000O0O ['succ']&OO00O000O0O000O0O ['cond']&OO00O000O0O000O0O ['frst'])#line:793
        O0O0O000OO000OOO0 =O000OOOOOOOO0OO0O ._bitcount (~(O0O00O00000OO0O00 |OO00O000O0O000O0O ['ante'])&~(O0O00O00000OO0O00 |OO00O000O0O000O0O ['succ'])&OO00O000O0O000O0O ['cond']&OO00O000O0O000O0O ['frst'])#line:794
        OO0O0O0O0O00000O0 =O000OOOOOOOO0OO0O ._bitcount (OO00O000O0O000O0O ['ante']&OO00O000O0O000O0O ['succ']&OO00O000O0O000O0O ['cond']&OO00O000O0O000O0O ['scnd'])#line:795
        OO0O000O0O0OO0OOO =O000OOOOOOOO0OO0O ._bitcount (OO00O000O0O000O0O ['ante']&~(O0O00O00000OO0O00 |OO00O000O0O000O0O ['succ'])&OO00O000O0O000O0O ['cond']&OO00O000O0O000O0O ['scnd'])#line:796
        O0O00O0000OOOOOOO =O000OOOOOOOO0OO0O ._bitcount (~(O0O00O00000OO0O00 |OO00O000O0O000O0O ['ante'])&OO00O000O0O000O0O ['succ']&OO00O000O0O000O0O ['cond']&OO00O000O0O000O0O ['scnd'])#line:797
        OOOOOO0OO000000O0 =O000OOOOOOOO0OO0O ._bitcount (~(O0O00O00000OO0O00 |OO00O000O0O000O0O ['ante'])&~(O0O00O00000OO0O00 |OO00O000O0O000O0O ['succ'])&OO00O000O0O000O0O ['cond']&OO00O000O0O000O0O ['scnd'])#line:798
        OOO0O0O0O0OOO0O00 =True #line:799
        for OO00O0O0O0OO0O0OO in O000OOOOOOOO0OO0O .quantifiers .keys ():#line:800
            if (OO00O0O0O0OO0O0OO .upper ()=='FRSTBASE')|(OO00O0O0O0OO0O0OO .upper ()=='BASE1'):#line:801
                OOO0O0O0O0OOO0O00 =OOO0O0O0O0OOO0O00 and (O000OOOOOOOO0OO0O .quantifiers .get (OO00O0O0O0OO0O0OO )<=O0000OOO0OO0000OO )#line:802
            if (OO00O0O0O0OO0O0OO .upper ()=='SCNDBASE')|(OO00O0O0O0OO0O0OO .upper ()=='BASE2'):#line:803
                OOO0O0O0O0OOO0O00 =OOO0O0O0O0OOO0O00 and (O000OOOOOOOO0OO0O .quantifiers .get (OO00O0O0O0OO0O0OO )<=O00O0OOOOO000OO0O )#line:804
            if (OO00O0O0O0OO0O0OO .upper ()=='FRSTRELBASE')|(OO00O0O0O0OO0O0OO .upper ()=='RELBASE1'):#line:805
                OOO0O0O0O0OOO0O00 =OOO0O0O0O0OOO0O00 and (O000OOOOOOOO0OO0O .quantifiers .get (OO00O0O0O0OO0O0OO )<=O0000OOO0OO0000OO *1.0 /O000OOOOOOOO0OO0O .data ["rows_count"])#line:806
            if (OO00O0O0O0OO0O0OO .upper ()=='SCNDRELBASE')|(OO00O0O0O0OO0O0OO .upper ()=='RELBASE2'):#line:807
                OOO0O0O0O0OOO0O00 =OOO0O0O0O0OOO0O00 and (O000OOOOOOOO0OO0O .quantifiers .get (OO00O0O0O0OO0O0OO )<=O00O0OOOOO000OO0O *1.0 /O000OOOOOOOO0OO0O .data ["rows_count"])#line:808
            if (OO00O0O0O0OO0O0OO .upper ()=='FRSTPIM')|(OO00O0O0O0OO0O0OO .upper ()=='PIM1')|(OO00O0O0O0OO0O0OO .upper ()=='FRSTCONF')|(OO00O0O0O0OO0O0OO .upper ()=='CONF1'):#line:809
                OOO0O0O0O0OOO0O00 =OOO0O0O0O0OOO0O00 and (O000OOOOOOOO0OO0O .quantifiers .get (OO00O0O0O0OO0O0OO )<=OOOOO0OOOOO0OOOO0 )#line:810
            if (OO00O0O0O0OO0O0OO .upper ()=='SCNDPIM')|(OO00O0O0O0OO0O0OO .upper ()=='PIM2')|(OO00O0O0O0OO0O0OO .upper ()=='SCNDCONF')|(OO00O0O0O0OO0O0OO .upper ()=='CONF2'):#line:811
                OOO0O0O0O0OOO0O00 =OOO0O0O0O0OOO0O00 and (O000OOOOOOOO0OO0O .quantifiers .get (OO00O0O0O0OO0O0OO )<=O0OO0OOOOOO0OO0OO )#line:812
            if (OO00O0O0O0OO0O0OO .upper ()=='DELTAPIM')|(OO00O0O0O0OO0O0OO .upper ()=='DELTACONF'):#line:813
                OOO0O0O0O0OOO0O00 =OOO0O0O0O0OOO0O00 and (O000OOOOOOOO0OO0O .quantifiers .get (OO00O0O0O0OO0O0OO )<=OOOOO0OOOOO0OOOO0 -O0OO0OOOOOO0OO0OO )#line:814
            if (OO00O0O0O0OO0O0OO .upper ()=='RATIOPIM')|(OO00O0O0O0OO0O0OO .upper ()=='RATIOCONF'):#line:817
                if (O0OO0OOOOOO0OO0OO >0 ):#line:818
                    OOO0O0O0O0OOO0O00 =OOO0O0O0O0OOO0O00 and (O000OOOOOOOO0OO0O .quantifiers .get (OO00O0O0O0OO0O0OO )<=OOOOO0OOOOO0OOOO0 *1.0 /O0OO0OOOOOO0OO0OO )#line:819
                else :#line:820
                    OOO0O0O0O0OOO0O00 =False #line:821
            if (OO00O0O0O0OO0O0OO .upper ()=='RATIOPIM_LEQ')|(OO00O0O0O0OO0O0OO .upper ()=='RATIOCONF_LEQ'):#line:822
                if (O0OO0OOOOOO0OO0OO >0 ):#line:823
                    OOO0O0O0O0OOO0O00 =OOO0O0O0O0OOO0O00 and (O000OOOOOOOO0OO0O .quantifiers .get (OO00O0O0O0OO0O0OO )>=OOOOO0OOOOO0OOOO0 *1.0 /O0OO0OOOOOO0OO0OO )#line:824
                else :#line:825
                    OOO0O0O0O0OOO0O00 =False #line:826
        O00O0OOO0OO0OOOO0 ={}#line:827
        if OOO0O0O0O0OOO0O00 ==True :#line:828
            O000OOOOOOOO0OO0O .stats ['total_valid']+=1 #line:830
            O00O0OOO0OO0OOOO0 ["base1"]=O0000OOO0OO0000OO #line:831
            O00O0OOO0OO0OOOO0 ["base2"]=O00O0OOOOO000OO0O #line:832
            O00O0OOO0OO0OOOO0 ["rel_base1"]=O0000OOO0OO0000OO *1.0 /O000OOOOOOOO0OO0O .data ["rows_count"]#line:833
            O00O0OOO0OO0OOOO0 ["rel_base2"]=O00O0OOOOO000OO0O *1.0 /O000OOOOOOOO0OO0O .data ["rows_count"]#line:834
            O00O0OOO0OO0OOOO0 ["conf1"]=OOOOO0OOOOO0OOOO0 #line:835
            O00O0OOO0OO0OOOO0 ["conf2"]=O0OO0OOOOOO0OO0OO #line:836
            O00O0OOO0OO0OOOO0 ["deltaconf"]=OOOOO0OOOOO0OOOO0 -O0OO0OOOOOO0OO0OO #line:837
            if (O0OO0OOOOOO0OO0OO >0 ):#line:838
                O00O0OOO0OO0OOOO0 ["ratioconf"]=OOOOO0OOOOO0OOOO0 *1.0 /O0OO0OOOOOO0OO0OO #line:839
            else :#line:840
                O00O0OOO0OO0OOOO0 ["ratioconf"]=None #line:841
            O00O0OOO0OO0OOOO0 ["fourfold1"]=[O0O0O0O0O0OO0O000 ,O000OO0O0O0OOO0OO ,OOO0O00OO000O0OOO ,O0O0O000OO000OOO0 ]#line:842
            O00O0OOO0OO0OOOO0 ["fourfold2"]=[OO0O0O0O0O00000O0 ,OO0O000O0O0OO0OOO ,O0O00O0000OOOOOOO ,OOOOOO0OO000000O0 ]#line:843
        return OOO0O0O0O0OOO0O00 ,O00O0OOO0OO0OOOO0 #line:847
    def _verifynewact4ft (O0OOO0OO00OOO0O0O ,_OO00OOO00OO0O0000 ):#line:849
        OO00OOOOO0OO0OO0O ={}#line:850
        for O0000000OOOO0OOO0 in O0OOO0OO00OOO0O0O .task_actinfo ['cedents']:#line:851
            OO00OOOOO0OO0OO0O [O0000000OOOO0OOO0 ['cedent_type']]=O0000000OOOO0OOO0 ['filter_value']#line:853
        O0O0O00O000OOO000 =O0OOO0OO00OOO0O0O ._bitcount (OO00OOOOO0OO0OO0O ['ante']&OO00OOOOO0OO0OO0O ['succ']&OO00OOOOO0OO0OO0O ['cond'])#line:855
        OOOOOOO0OO0OOO00O =O0OOO0OO00OOO0O0O ._bitcount (OO00OOOOO0OO0OO0O ['ante']&OO00OOOOO0OO0OO0O ['succ']&OO00OOOOO0OO0OO0O ['cond']&OO00OOOOO0OO0OO0O ['antv']&OO00OOOOO0OO0OO0O ['sucv'])#line:856
        O00O0000OOO00O000 =None #line:857
        O000OOOOOOOO0OO00 =0 #line:858
        OO0O0OOOO0OOO0O0O =0 #line:859
        if O0O0O00O000OOO000 >0 :#line:868
            O000OOOOOOOO0OO00 =O0OOO0OO00OOO0O0O ._bitcount (OO00OOOOO0OO0OO0O ['ante']&OO00OOOOO0OO0OO0O ['succ']&OO00OOOOO0OO0OO0O ['cond'])*1.0 /O0OOO0OO00OOO0O0O ._bitcount (OO00OOOOO0OO0OO0O ['ante']&OO00OOOOO0OO0OO0O ['cond'])#line:869
        if OOOOOOO0OO0OOO00O >0 :#line:870
            OO0O0OOOO0OOO0O0O =O0OOO0OO00OOO0O0O ._bitcount (OO00OOOOO0OO0OO0O ['ante']&OO00OOOOO0OO0OO0O ['succ']&OO00OOOOO0OO0OO0O ['cond']&OO00OOOOO0OO0OO0O ['antv']&OO00OOOOO0OO0OO0O ['sucv'])*1.0 /O0OOO0OO00OOO0O0O ._bitcount (OO00OOOOO0OO0OO0O ['ante']&OO00OOOOO0OO0OO0O ['cond']&OO00OOOOO0OO0OO0O ['antv'])#line:872
        O0OOOO00OOO0OO0OO =1 <<O0OOO0OO00OOO0O0O .rows_count #line:874
        OOOO0O000OO0O0O00 =O0OOO0OO00OOO0O0O ._bitcount (OO00OOOOO0OO0OO0O ['ante']&OO00OOOOO0OO0OO0O ['succ']&OO00OOOOO0OO0OO0O ['cond'])#line:875
        O0O0OOO0O000O0O00 =O0OOO0OO00OOO0O0O ._bitcount (OO00OOOOO0OO0OO0O ['ante']&~(O0OOOO00OOO0OO0OO |OO00OOOOO0OO0OO0O ['succ'])&OO00OOOOO0OO0OO0O ['cond'])#line:876
        OOOO00OOOOO0000O0 =O0OOO0OO00OOO0O0O ._bitcount (~(O0OOOO00OOO0OO0OO |OO00OOOOO0OO0OO0O ['ante'])&OO00OOOOO0OO0OO0O ['succ']&OO00OOOOO0OO0OO0O ['cond'])#line:877
        O0OOOO0000OO0OO0O =O0OOO0OO00OOO0O0O ._bitcount (~(O0OOOO00OOO0OO0OO |OO00OOOOO0OO0OO0O ['ante'])&~(O0OOOO00OOO0OO0OO |OO00OOOOO0OO0OO0O ['succ'])&OO00OOOOO0OO0OO0O ['cond'])#line:878
        OOO0OO00OO00OO000 =O0OOO0OO00OOO0O0O ._bitcount (OO00OOOOO0OO0OO0O ['ante']&OO00OOOOO0OO0OO0O ['succ']&OO00OOOOO0OO0OO0O ['cond']&OO00OOOOO0OO0OO0O ['antv']&OO00OOOOO0OO0OO0O ['sucv'])#line:879
        O0OO0O0O00O0O0OOO =O0OOO0OO00OOO0O0O ._bitcount (OO00OOOOO0OO0OO0O ['ante']&~(O0OOOO00OOO0OO0OO |(OO00OOOOO0OO0OO0O ['succ']&OO00OOOOO0OO0OO0O ['sucv']))&OO00OOOOO0OO0OO0O ['cond'])#line:880
        OOO0OO00000OO0O00 =O0OOO0OO00OOO0O0O ._bitcount (~(O0OOOO00OOO0OO0OO |(OO00OOOOO0OO0OO0O ['ante']&OO00OOOOO0OO0OO0O ['antv']))&OO00OOOOO0OO0OO0O ['succ']&OO00OOOOO0OO0OO0O ['cond']&OO00OOOOO0OO0OO0O ['sucv'])#line:881
        O0O0OOO00O0OOOOOO =O0OOO0OO00OOO0O0O ._bitcount (~(O0OOOO00OOO0OO0OO |(OO00OOOOO0OO0OO0O ['ante']&OO00OOOOO0OO0OO0O ['antv']))&~(O0OOOO00OOO0OO0OO |(OO00OOOOO0OO0OO0O ['succ']&OO00OOOOO0OO0OO0O ['sucv']))&OO00OOOOO0OO0OO0O ['cond'])#line:882
        OO000OO0O00000OO0 =True #line:883
        for O0O0000000OO00O00 in O0OOO0OO00OOO0O0O .quantifiers .keys ():#line:884
            if (O0O0000000OO00O00 =='PreBase')|(O0O0000000OO00O00 =='Base1'):#line:885
                OO000OO0O00000OO0 =OO000OO0O00000OO0 and (O0OOO0OO00OOO0O0O .quantifiers .get (O0O0000000OO00O00 )<=O0O0O00O000OOO000 )#line:886
            if (O0O0000000OO00O00 =='PostBase')|(O0O0000000OO00O00 =='Base2'):#line:887
                OO000OO0O00000OO0 =OO000OO0O00000OO0 and (O0OOO0OO00OOO0O0O .quantifiers .get (O0O0000000OO00O00 )<=OOOOOOO0OO0OOO00O )#line:888
            if (O0O0000000OO00O00 =='PreRelBase')|(O0O0000000OO00O00 =='RelBase1'):#line:889
                OO000OO0O00000OO0 =OO000OO0O00000OO0 and (O0OOO0OO00OOO0O0O .quantifiers .get (O0O0000000OO00O00 )<=O0O0O00O000OOO000 *1.0 /O0OOO0OO00OOO0O0O .data ["rows_count"])#line:890
            if (O0O0000000OO00O00 =='PostRelBase')|(O0O0000000OO00O00 =='RelBase2'):#line:891
                OO000OO0O00000OO0 =OO000OO0O00000OO0 and (O0OOO0OO00OOO0O0O .quantifiers .get (O0O0000000OO00O00 )<=OOOOOOO0OO0OOO00O *1.0 /O0OOO0OO00OOO0O0O .data ["rows_count"])#line:892
            if (O0O0000000OO00O00 =='Prepim')|(O0O0000000OO00O00 =='pim1')|(O0O0000000OO00O00 =='PreConf')|(O0O0000000OO00O00 =='conf1'):#line:893
                OO000OO0O00000OO0 =OO000OO0O00000OO0 and (O0OOO0OO00OOO0O0O .quantifiers .get (O0O0000000OO00O00 )<=O000OOOOOOOO0OO00 )#line:894
            if (O0O0000000OO00O00 =='Postpim')|(O0O0000000OO00O00 =='pim2')|(O0O0000000OO00O00 =='PostConf')|(O0O0000000OO00O00 =='conf2'):#line:895
                OO000OO0O00000OO0 =OO000OO0O00000OO0 and (O0OOO0OO00OOO0O0O .quantifiers .get (O0O0000000OO00O00 )<=OO0O0OOOO0OOO0O0O )#line:896
            if (O0O0000000OO00O00 =='Deltapim')|(O0O0000000OO00O00 =='DeltaConf'):#line:897
                OO000OO0O00000OO0 =OO000OO0O00000OO0 and (O0OOO0OO00OOO0O0O .quantifiers .get (O0O0000000OO00O00 )<=O000OOOOOOOO0OO00 -OO0O0OOOO0OOO0O0O )#line:898
            if (O0O0000000OO00O00 =='Ratiopim')|(O0O0000000OO00O00 =='RatioConf'):#line:901
                if (OO0O0OOOO0OOO0O0O >0 ):#line:902
                    OO000OO0O00000OO0 =OO000OO0O00000OO0 and (O0OOO0OO00OOO0O0O .quantifiers .get (O0O0000000OO00O00 )<=O000OOOOOOOO0OO00 *1.0 /OO0O0OOOO0OOO0O0O )#line:903
                else :#line:904
                    OO000OO0O00000OO0 =False #line:905
        OOOO00000OO0O0OO0 ={}#line:906
        if OO000OO0O00000OO0 ==True :#line:907
            O0OOO0OO00OOO0O0O .stats ['total_valid']+=1 #line:909
            OOOO00000OO0O0OO0 ["base1"]=O0O0O00O000OOO000 #line:910
            OOOO00000OO0O0OO0 ["base2"]=OOOOOOO0OO0OOO00O #line:911
            OOOO00000OO0O0OO0 ["rel_base1"]=O0O0O00O000OOO000 *1.0 /O0OOO0OO00OOO0O0O .data ["rows_count"]#line:912
            OOOO00000OO0O0OO0 ["rel_base2"]=OOOOOOO0OO0OOO00O *1.0 /O0OOO0OO00OOO0O0O .data ["rows_count"]#line:913
            OOOO00000OO0O0OO0 ["conf1"]=O000OOOOOOOO0OO00 #line:914
            OOOO00000OO0O0OO0 ["conf2"]=OO0O0OOOO0OOO0O0O #line:915
            OOOO00000OO0O0OO0 ["deltaconf"]=O000OOOOOOOO0OO00 -OO0O0OOOO0OOO0O0O #line:916
            if (OO0O0OOOO0OOO0O0O >0 ):#line:917
                OOOO00000OO0O0OO0 ["ratioconf"]=O000OOOOOOOO0OO00 *1.0 /OO0O0OOOO0OOO0O0O #line:918
            else :#line:919
                OOOO00000OO0O0OO0 ["ratioconf"]=None #line:920
            OOOO00000OO0O0OO0 ["fourfoldpre"]=[OOOO0O000OO0O0O00 ,O0O0OOO0O000O0O00 ,OOOO00OOOOO0000O0 ,O0OOOO0000OO0OO0O ]#line:921
            OOOO00000OO0O0OO0 ["fourfoldpost"]=[OOO0OO00OO00OO000 ,O0OO0O0O00O0O0OOO ,OOO0OO00000OO0O00 ,O0O0OOO00O0OOOOOO ]#line:922
        return OO000OO0O00000OO0 ,OOOO00000OO0O0OO0 #line:924
    def _verifyact4ft (OOOO0OO00OOOOOO00 ,_O0OO0OO00OOO0000O ):#line:926
        O0OOOO000000O0OO0 ={}#line:927
        for O0O0OO00OO00OO0O0 in OOOO0OO00OOOOOO00 .task_actinfo ['cedents']:#line:928
            O0OOOO000000O0OO0 [O0O0OO00OO00OO0O0 ['cedent_type']]=O0O0OO00OO00OO0O0 ['filter_value']#line:930
        OOOO0OOOOOO0OO000 =OOOO0OO00OOOOOO00 ._bitcount (O0OOOO000000O0OO0 ['ante']&O0OOOO000000O0OO0 ['succ']&O0OOOO000000O0OO0 ['cond']&O0OOOO000000O0OO0 ['antv-']&O0OOOO000000O0OO0 ['sucv-'])#line:932
        OOO00O0000O00OOO0 =OOOO0OO00OOOOOO00 ._bitcount (O0OOOO000000O0OO0 ['ante']&O0OOOO000000O0OO0 ['succ']&O0OOOO000000O0OO0 ['cond']&O0OOOO000000O0OO0 ['antv+']&O0OOOO000000O0OO0 ['sucv+'])#line:933
        OO0OO0OOOO0OOO0O0 =None #line:934
        OO0O0O0O0OOOO0000 =0 #line:935
        O00000OO0000OOO00 =0 #line:936
        if OOOO0OOOOOO0OO000 >0 :#line:945
            OO0O0O0O0OOOO0000 =OOOO0OO00OOOOOO00 ._bitcount (O0OOOO000000O0OO0 ['ante']&O0OOOO000000O0OO0 ['succ']&O0OOOO000000O0OO0 ['cond']&O0OOOO000000O0OO0 ['antv-']&O0OOOO000000O0OO0 ['sucv-'])*1.0 /OOOO0OO00OOOOOO00 ._bitcount (O0OOOO000000O0OO0 ['ante']&O0OOOO000000O0OO0 ['cond']&O0OOOO000000O0OO0 ['antv-'])#line:947
        if OOO00O0000O00OOO0 >0 :#line:948
            O00000OO0000OOO00 =OOOO0OO00OOOOOO00 ._bitcount (O0OOOO000000O0OO0 ['ante']&O0OOOO000000O0OO0 ['succ']&O0OOOO000000O0OO0 ['cond']&O0OOOO000000O0OO0 ['antv+']&O0OOOO000000O0OO0 ['sucv+'])*1.0 /OOOO0OO00OOOOOO00 ._bitcount (O0OOOO000000O0OO0 ['ante']&O0OOOO000000O0OO0 ['cond']&O0OOOO000000O0OO0 ['antv+'])#line:950
        O0OOOO00OO0OOOOO0 =1 <<OOOO0OO00OOOOOO00 .data ["rows_count"]#line:952
        OOO000O00OO0OOO0O =OOOO0OO00OOOOOO00 ._bitcount (O0OOOO000000O0OO0 ['ante']&O0OOOO000000O0OO0 ['succ']&O0OOOO000000O0OO0 ['cond']&O0OOOO000000O0OO0 ['antv-']&O0OOOO000000O0OO0 ['sucv-'])#line:953
        O0OO0OOOO000O0OOO =OOOO0OO00OOOOOO00 ._bitcount (O0OOOO000000O0OO0 ['ante']&O0OOOO000000O0OO0 ['antv-']&~(O0OOOO00OO0OOOOO0 |(O0OOOO000000O0OO0 ['succ']&O0OOOO000000O0OO0 ['sucv-']))&O0OOOO000000O0OO0 ['cond'])#line:954
        OO0OO0000OOOO0O00 =OOOO0OO00OOOOOO00 ._bitcount (~(O0OOOO00OO0OOOOO0 |(O0OOOO000000O0OO0 ['ante']&O0OOOO000000O0OO0 ['antv-']))&O0OOOO000000O0OO0 ['succ']&O0OOOO000000O0OO0 ['cond']&O0OOOO000000O0OO0 ['sucv-'])#line:955
        OO0OOO00OOOOOOO0O =OOOO0OO00OOOOOO00 ._bitcount (~(O0OOOO00OO0OOOOO0 |(O0OOOO000000O0OO0 ['ante']&O0OOOO000000O0OO0 ['antv-']))&~(O0OOOO00OO0OOOOO0 |(O0OOOO000000O0OO0 ['succ']&O0OOOO000000O0OO0 ['sucv-']))&O0OOOO000000O0OO0 ['cond'])#line:956
        O000000OOOOOOOO00 =OOOO0OO00OOOOOO00 ._bitcount (O0OOOO000000O0OO0 ['ante']&O0OOOO000000O0OO0 ['succ']&O0OOOO000000O0OO0 ['cond']&O0OOOO000000O0OO0 ['antv+']&O0OOOO000000O0OO0 ['sucv+'])#line:957
        O00000O000OO00OOO =OOOO0OO00OOOOOO00 ._bitcount (O0OOOO000000O0OO0 ['ante']&O0OOOO000000O0OO0 ['antv+']&~(O0OOOO00OO0OOOOO0 |(O0OOOO000000O0OO0 ['succ']&O0OOOO000000O0OO0 ['sucv+']))&O0OOOO000000O0OO0 ['cond'])#line:958
        O00O000O00OOOO0O0 =OOOO0OO00OOOOOO00 ._bitcount (~(O0OOOO00OO0OOOOO0 |(O0OOOO000000O0OO0 ['ante']&O0OOOO000000O0OO0 ['antv+']))&O0OOOO000000O0OO0 ['succ']&O0OOOO000000O0OO0 ['cond']&O0OOOO000000O0OO0 ['sucv+'])#line:959
        O000O0OOO00OOO000 =OOOO0OO00OOOOOO00 ._bitcount (~(O0OOOO00OO0OOOOO0 |(O0OOOO000000O0OO0 ['ante']&O0OOOO000000O0OO0 ['antv+']))&~(O0OOOO00OO0OOOOO0 |(O0OOOO000000O0OO0 ['succ']&O0OOOO000000O0OO0 ['sucv+']))&O0OOOO000000O0OO0 ['cond'])#line:960
        O0OO00000O0OOOO00 =True #line:961
        for O0O000OOOOO000O00 in OOOO0OO00OOOOOO00 .quantifiers .keys ():#line:962
            if (O0O000OOOOO000O00 =='PreBase')|(O0O000OOOOO000O00 =='Base1'):#line:963
                O0OO00000O0OOOO00 =O0OO00000O0OOOO00 and (OOOO0OO00OOOOOO00 .quantifiers .get (O0O000OOOOO000O00 )<=OOOO0OOOOOO0OO000 )#line:964
            if (O0O000OOOOO000O00 =='PostBase')|(O0O000OOOOO000O00 =='Base2'):#line:965
                O0OO00000O0OOOO00 =O0OO00000O0OOOO00 and (OOOO0OO00OOOOOO00 .quantifiers .get (O0O000OOOOO000O00 )<=OOO00O0000O00OOO0 )#line:966
            if (O0O000OOOOO000O00 =='PreRelBase')|(O0O000OOOOO000O00 =='RelBase1'):#line:967
                O0OO00000O0OOOO00 =O0OO00000O0OOOO00 and (OOOO0OO00OOOOOO00 .quantifiers .get (O0O000OOOOO000O00 )<=OOOO0OOOOOO0OO000 *1.0 /OOOO0OO00OOOOOO00 .data ["rows_count"])#line:968
            if (O0O000OOOOO000O00 =='PostRelBase')|(O0O000OOOOO000O00 =='RelBase2'):#line:969
                O0OO00000O0OOOO00 =O0OO00000O0OOOO00 and (OOOO0OO00OOOOOO00 .quantifiers .get (O0O000OOOOO000O00 )<=OOO00O0000O00OOO0 *1.0 /OOOO0OO00OOOOOO00 .data ["rows_count"])#line:970
            if (O0O000OOOOO000O00 =='Prepim')|(O0O000OOOOO000O00 =='pim1')|(O0O000OOOOO000O00 =='PreConf')|(O0O000OOOOO000O00 =='conf1'):#line:971
                O0OO00000O0OOOO00 =O0OO00000O0OOOO00 and (OOOO0OO00OOOOOO00 .quantifiers .get (O0O000OOOOO000O00 )<=OO0O0O0O0OOOO0000 )#line:972
            if (O0O000OOOOO000O00 =='Postpim')|(O0O000OOOOO000O00 =='pim2')|(O0O000OOOOO000O00 =='PostConf')|(O0O000OOOOO000O00 =='conf2'):#line:973
                O0OO00000O0OOOO00 =O0OO00000O0OOOO00 and (OOOO0OO00OOOOOO00 .quantifiers .get (O0O000OOOOO000O00 )<=O00000OO0000OOO00 )#line:974
            if (O0O000OOOOO000O00 =='Deltapim')|(O0O000OOOOO000O00 =='DeltaConf'):#line:975
                O0OO00000O0OOOO00 =O0OO00000O0OOOO00 and (OOOO0OO00OOOOOO00 .quantifiers .get (O0O000OOOOO000O00 )<=OO0O0O0O0OOOO0000 -O00000OO0000OOO00 )#line:976
            if (O0O000OOOOO000O00 =='Ratiopim')|(O0O000OOOOO000O00 =='RatioConf'):#line:979
                if (OO0O0O0O0OOOO0000 >0 ):#line:980
                    O0OO00000O0OOOO00 =O0OO00000O0OOOO00 and (OOOO0OO00OOOOOO00 .quantifiers .get (O0O000OOOOO000O00 )<=O00000OO0000OOO00 *1.0 /OO0O0O0O0OOOO0000 )#line:981
                else :#line:982
                    O0OO00000O0OOOO00 =False #line:983
        OOO00O0O0OO0O0O0O ={}#line:984
        if O0OO00000O0OOOO00 ==True :#line:985
            OOOO0OO00OOOOOO00 .stats ['total_valid']+=1 #line:987
            OOO00O0O0OO0O0O0O ["base1"]=OOOO0OOOOOO0OO000 #line:988
            OOO00O0O0OO0O0O0O ["base2"]=OOO00O0000O00OOO0 #line:989
            OOO00O0O0OO0O0O0O ["rel_base1"]=OOOO0OOOOOO0OO000 *1.0 /OOOO0OO00OOOOOO00 .data ["rows_count"]#line:990
            OOO00O0O0OO0O0O0O ["rel_base2"]=OOO00O0000O00OOO0 *1.0 /OOOO0OO00OOOOOO00 .data ["rows_count"]#line:991
            OOO00O0O0OO0O0O0O ["conf1"]=OO0O0O0O0OOOO0000 #line:992
            OOO00O0O0OO0O0O0O ["conf2"]=O00000OO0000OOO00 #line:993
            OOO00O0O0OO0O0O0O ["deltaconf"]=OO0O0O0O0OOOO0000 -O00000OO0000OOO00 #line:994
            if (OO0O0O0O0OOOO0000 >0 ):#line:995
                OOO00O0O0OO0O0O0O ["ratioconf"]=O00000OO0000OOO00 *1.0 /OO0O0O0O0OOOO0000 #line:996
            else :#line:997
                OOO00O0O0OO0O0O0O ["ratioconf"]=None #line:998
            OOO00O0O0OO0O0O0O ["fourfoldpre"]=[OOO000O00OO0OOO0O ,O0OO0OOOO000O0OOO ,OO0OO0000OOOO0O00 ,OO0OOO00OOOOOOO0O ]#line:999
            OOO00O0O0OO0O0O0O ["fourfoldpost"]=[O000000OOOOOOOO00 ,O00000O000OO00OOO ,O00O000O00OOOO0O0 ,O000O0OOO00OOO000 ]#line:1000
        return O0OO00000O0OOOO00 ,OOO00O0O0OO0O0O0O #line:1002
    def _verify_opt (O0OO00O0O000O0O00 ,O0O00O0O0O0OOO00O ,OOO0000O00O0O000O ):#line:1004
        O0OO00O0O000O0O00 .stats ['total_ver']+=1 #line:1005
        O000OOOOO00O00O00 =False #line:1006
        if not (O0O00O0O0O0OOO00O ['optim'].get ('only_con')):#line:1009
            return False #line:1010
        if not (O0OO00O0O000O0O00 .options ['optimizations']):#line:1013
            return False #line:1015
        OOOOO0O0OO0000O0O ={}#line:1017
        for O0OOOOOO00OO000OO in O0OO00O0O000O0O00 .task_actinfo ['cedents']:#line:1018
            OOOOO0O0OO0000O0O [O0OOOOOO00OO000OO ['cedent_type']]=O0OOOOOO00OO000OO ['filter_value']#line:1020
        OOOOOOOO0OOO00O00 =1 <<O0OO00O0O000O0O00 .data ["rows_count"]#line:1022
        OO00O000OOO0000OO =OOOOOOOO0OOO00O00 -1 #line:1023
        O000000OO0O00OO00 =""#line:1024
        O0OOOO0O0OO0000O0 =0 #line:1025
        if (OOOOO0O0OO0000O0O .get ('ante')!=None ):#line:1026
            OO00O000OOO0000OO =OO00O000OOO0000OO &OOOOO0O0OO0000O0O ['ante']#line:1027
        if (OOOOO0O0OO0000O0O .get ('succ')!=None ):#line:1028
            OO00O000OOO0000OO =OO00O000OOO0000OO &OOOOO0O0OO0000O0O ['succ']#line:1029
        if (OOOOO0O0OO0000O0O .get ('cond')!=None ):#line:1030
            OO00O000OOO0000OO =OO00O000OOO0000OO &OOOOO0O0OO0000O0O ['cond']#line:1031
        O00O00O0OO0O00000 =None #line:1034
        if (O0OO00O0O000O0O00 .proc =='CFMiner')|(O0OO00O0O000O0O00 .proc =='4ftMiner')|(O0OO00O0O000O0O00 .proc =='UICMiner'):#line:1059
            OOOO0O00O000000OO =O0OO00O0O000O0O00 ._bitcount (OO00O000OOO0000OO )#line:1060
            if not (O0OO00O0O000O0O00 ._opt_base ==None ):#line:1061
                if not (O0OO00O0O000O0O00 ._opt_base <=OOOO0O00O000000OO ):#line:1062
                    O000OOOOO00O00O00 =True #line:1063
            if not (O0OO00O0O000O0O00 ._opt_relbase ==None ):#line:1065
                if not (O0OO00O0O000O0O00 ._opt_relbase <=OOOO0O00O000000OO *1.0 /O0OO00O0O000O0O00 .data ["rows_count"]):#line:1066
                    O000OOOOO00O00O00 =True #line:1067
        if (O0OO00O0O000O0O00 .proc =='SD4ftMiner'):#line:1069
            OOOO0O00O000000OO =O0OO00O0O000O0O00 ._bitcount (OO00O000OOO0000OO )#line:1070
            if (not (O0OO00O0O000O0O00 ._opt_base1 ==None ))&(not (O0OO00O0O000O0O00 ._opt_base2 ==None )):#line:1071
                if not (max (O0OO00O0O000O0O00 ._opt_base1 ,O0OO00O0O000O0O00 ._opt_base2 )<=OOOO0O00O000000OO ):#line:1072
                    O000OOOOO00O00O00 =True #line:1074
            if (not (O0OO00O0O000O0O00 ._opt_relbase1 ==None ))&(not (O0OO00O0O000O0O00 ._opt_relbase2 ==None )):#line:1075
                if not (max (O0OO00O0O000O0O00 ._opt_relbase1 ,O0OO00O0O000O0O00 ._opt_relbase2 )<=OOOO0O00O000000OO *1.0 /O0OO00O0O000O0O00 .data ["rows_count"]):#line:1076
                    O000OOOOO00O00O00 =True #line:1077
        return O000OOOOO00O00O00 #line:1079
        if O0OO00O0O000O0O00 .proc =='CFMiner':#line:1082
            if (OOO0000O00O0O000O ['cedent_type']=='cond')&(OOO0000O00O0O000O ['defi'].get ('type')=='con'):#line:1083
                OOOO0O00O000000OO =bin (OOOOO0O0OO0000O0O ['cond']).count ("1")#line:1084
                O0OO0000O0OOOO00O =True #line:1085
                for O00O0000O00O0OOO0 in O0OO00O0O000O0O00 .quantifiers .keys ():#line:1086
                    if O00O0000O00O0OOO0 =='Base':#line:1087
                        O0OO0000O0OOOO00O =O0OO0000O0OOOO00O and (O0OO00O0O000O0O00 .quantifiers .get (O00O0000O00O0OOO0 )<=OOOO0O00O000000OO )#line:1088
                        if not (O0OO0000O0OOOO00O ):#line:1089
                            print (f"...optimization : base is {OOOO0O00O000000OO} for {OOO0000O00O0O000O['generated_string']}")#line:1090
                    if O00O0000O00O0OOO0 =='RelBase':#line:1091
                        O0OO0000O0OOOO00O =O0OO0000O0OOOO00O and (O0OO00O0O000O0O00 .quantifiers .get (O00O0000O00O0OOO0 )<=OOOO0O00O000000OO *1.0 /O0OO00O0O000O0O00 .data ["rows_count"])#line:1092
                        if not (O0OO0000O0OOOO00O ):#line:1093
                            print (f"...optimization : base is {OOOO0O00O000000OO} for {OOO0000O00O0O000O['generated_string']}")#line:1094
                O000OOOOO00O00O00 =not (O0OO0000O0OOOO00O )#line:1095
        elif O0OO00O0O000O0O00 .proc =='4ftMiner':#line:1096
            if (OOO0000O00O0O000O ['cedent_type']=='cond')&(OOO0000O00O0O000O ['defi'].get ('type')=='con'):#line:1097
                OOOO0O00O000000OO =bin (OOOOO0O0OO0000O0O ['cond']).count ("1")#line:1098
                O0OO0000O0OOOO00O =True #line:1099
                for O00O0000O00O0OOO0 in O0OO00O0O000O0O00 .quantifiers .keys ():#line:1100
                    if O00O0000O00O0OOO0 =='Base':#line:1101
                        O0OO0000O0OOOO00O =O0OO0000O0OOOO00O and (O0OO00O0O000O0O00 .quantifiers .get (O00O0000O00O0OOO0 )<=OOOO0O00O000000OO )#line:1102
                        if not (O0OO0000O0OOOO00O ):#line:1103
                            print (f"...optimization : base is {OOOO0O00O000000OO} for {OOO0000O00O0O000O['generated_string']}")#line:1104
                    if O00O0000O00O0OOO0 =='RelBase':#line:1105
                        O0OO0000O0OOOO00O =O0OO0000O0OOOO00O and (O0OO00O0O000O0O00 .quantifiers .get (O00O0000O00O0OOO0 )<=OOOO0O00O000000OO *1.0 /O0OO00O0O000O0O00 .data ["rows_count"])#line:1106
                        if not (O0OO0000O0OOOO00O ):#line:1107
                            print (f"...optimization : base is {OOOO0O00O000000OO} for {OOO0000O00O0O000O['generated_string']}")#line:1108
                O000OOOOO00O00O00 =not (O0OO0000O0OOOO00O )#line:1109
            if (OOO0000O00O0O000O ['cedent_type']=='ante')&(OOO0000O00O0O000O ['defi'].get ('type')=='con'):#line:1110
                OOOO0O00O000000OO =bin (OOOOO0O0OO0000O0O ['ante']&OOOOO0O0OO0000O0O ['cond']).count ("1")#line:1111
                O0OO0000O0OOOO00O =True #line:1112
                for O00O0000O00O0OOO0 in O0OO00O0O000O0O00 .quantifiers .keys ():#line:1113
                    if O00O0000O00O0OOO0 =='Base':#line:1114
                        O0OO0000O0OOOO00O =O0OO0000O0OOOO00O and (O0OO00O0O000O0O00 .quantifiers .get (O00O0000O00O0OOO0 )<=OOOO0O00O000000OO )#line:1115
                        if not (O0OO0000O0OOOO00O ):#line:1116
                            print (f"...optimization : ANTE: base is {OOOO0O00O000000OO} for {OOO0000O00O0O000O['generated_string']}")#line:1117
                    if O00O0000O00O0OOO0 =='RelBase':#line:1118
                        O0OO0000O0OOOO00O =O0OO0000O0OOOO00O and (O0OO00O0O000O0O00 .quantifiers .get (O00O0000O00O0OOO0 )<=OOOO0O00O000000OO *1.0 /O0OO00O0O000O0O00 .data ["rows_count"])#line:1119
                        if not (O0OO0000O0OOOO00O ):#line:1120
                            print (f"...optimization : ANTE:  base is {OOOO0O00O000000OO} for {OOO0000O00O0O000O['generated_string']}")#line:1121
                O000OOOOO00O00O00 =not (O0OO0000O0OOOO00O )#line:1122
            if (OOO0000O00O0O000O ['cedent_type']=='succ')&(OOO0000O00O0O000O ['defi'].get ('type')=='con'):#line:1123
                OOOO0O00O000000OO =bin (OOOOO0O0OO0000O0O ['ante']&OOOOO0O0OO0000O0O ['cond']&OOOOO0O0OO0000O0O ['succ']).count ("1")#line:1124
                O00O00O0OO0O00000 =0 #line:1125
                if OOOO0O00O000000OO >0 :#line:1126
                    O00O00O0OO0O00000 =bin (OOOOO0O0OO0000O0O ['ante']&OOOOO0O0OO0000O0O ['succ']&OOOOO0O0OO0000O0O ['cond']).count ("1")*1.0 /bin (OOOOO0O0OO0000O0O ['ante']&OOOOO0O0OO0000O0O ['cond']).count ("1")#line:1127
                OOOOOOOO0OOO00O00 =1 <<O0OO00O0O000O0O00 .data ["rows_count"]#line:1128
                OOO0OO00O0OO0O00O =bin (OOOOO0O0OO0000O0O ['ante']&OOOOO0O0OO0000O0O ['succ']&OOOOO0O0OO0000O0O ['cond']).count ("1")#line:1129
                O0000OOO0O0000O0O =bin (OOOOO0O0OO0000O0O ['ante']&~(OOOOOOOO0OOO00O00 |OOOOO0O0OO0000O0O ['succ'])&OOOOO0O0OO0000O0O ['cond']).count ("1")#line:1130
                O0OOOOOO00OO000OO =bin (~(OOOOOOOO0OOO00O00 |OOOOO0O0OO0000O0O ['ante'])&OOOOO0O0OO0000O0O ['succ']&OOOOO0O0OO0000O0O ['cond']).count ("1")#line:1131
                OO000O00O000000O0 =bin (~(OOOOOOOO0OOO00O00 |OOOOO0O0OO0000O0O ['ante'])&~(OOOOOOOO0OOO00O00 |OOOOO0O0OO0000O0O ['succ'])&OOOOO0O0OO0000O0O ['cond']).count ("1")#line:1132
                O0OO0000O0OOOO00O =True #line:1133
                for O00O0000O00O0OOO0 in O0OO00O0O000O0O00 .quantifiers .keys ():#line:1134
                    if O00O0000O00O0OOO0 =='pim':#line:1135
                        O0OO0000O0OOOO00O =O0OO0000O0OOOO00O and (O0OO00O0O000O0O00 .quantifiers .get (O00O0000O00O0OOO0 )<=O00O00O0OO0O00000 )#line:1136
                    if not (O0OO0000O0OOOO00O ):#line:1137
                        print (f"...optimization : SUCC:  pim is {O00O00O0OO0O00000} for {OOO0000O00O0O000O['generated_string']}")#line:1138
                    if O00O0000O00O0OOO0 =='aad':#line:1140
                        if (OOO0OO00O0OO0O00O +O0000OOO0O0000O0O )*(OOO0OO00O0OO0O00O +O0OOOOOO00OO000OO )>0 :#line:1141
                            O0OO0000O0OOOO00O =O0OO0000O0OOOO00O and (O0OO00O0O000O0O00 .quantifiers .get (O00O0000O00O0OOO0 )<=OOO0OO00O0OO0O00O *(OOO0OO00O0OO0O00O +O0000OOO0O0000O0O +O0OOOOOO00OO000OO +OO000O00O000000O0 )/(OOO0OO00O0OO0O00O +O0000OOO0O0000O0O )/(OOO0OO00O0OO0O00O +O0OOOOOO00OO000OO )-1 )#line:1142
                        else :#line:1143
                            O0OO0000O0OOOO00O =False #line:1144
                        if not (O0OO0000O0OOOO00O ):#line:1145
                            OO00OO00OO00OO000 =OOO0OO00O0OO0O00O *(OOO0OO00O0OO0O00O +O0000OOO0O0000O0O +O0OOOOOO00OO000OO +OO000O00O000000O0 )/(OOO0OO00O0OO0O00O +O0000OOO0O0000O0O )/(OOO0OO00O0OO0O00O +O0OOOOOO00OO000OO )-1 #line:1146
                            print (f"...optimization : SUCC:  aad is {OO00OO00OO00OO000} for {OOO0000O00O0O000O['generated_string']}")#line:1147
                    if O00O0000O00O0OOO0 =='bad':#line:1148
                        if (OOO0OO00O0OO0O00O +O0000OOO0O0000O0O )*(OOO0OO00O0OO0O00O +O0OOOOOO00OO000OO )>0 :#line:1149
                            O0OO0000O0OOOO00O =O0OO0000O0OOOO00O and (O0OO00O0O000O0O00 .quantifiers .get (O00O0000O00O0OOO0 )<=1 -OOO0OO00O0OO0O00O *(OOO0OO00O0OO0O00O +O0000OOO0O0000O0O +O0OOOOOO00OO000OO +OO000O00O000000O0 )/(OOO0OO00O0OO0O00O +O0000OOO0O0000O0O )/(OOO0OO00O0OO0O00O +O0OOOOOO00OO000OO ))#line:1150
                        else :#line:1151
                            O0OO0000O0OOOO00O =False #line:1152
                        if not (O0OO0000O0OOOO00O ):#line:1153
                            OOOO0OOO00O0O00OO =1 -OOO0OO00O0OO0O00O *(OOO0OO00O0OO0O00O +O0000OOO0O0000O0O +O0OOOOOO00OO000OO +OO000O00O000000O0 )/(OOO0OO00O0OO0O00O +O0000OOO0O0000O0O )/(OOO0OO00O0OO0O00O +O0OOOOOO00OO000OO )#line:1154
                            print (f"...optimization : SUCC:  bad is {OOOO0OOO00O0O00OO} for {OOO0000O00O0O000O['generated_string']}")#line:1155
                O000OOOOO00O00O00 =not (O0OO0000O0OOOO00O )#line:1156
        if (O000OOOOO00O00O00 ):#line:1157
            print (f"... OPTIMALIZATION - SKIPPING BRANCH at cedent {OOO0000O00O0O000O['cedent_type']}")#line:1158
        return O000OOOOO00O00O00 #line:1159
    def _print (O0O0O0OOOO0OO000O ,OOOOOO0000OOO0O0O ,_O0O0OO0OO0OOOO0O0 ,_O00OO0000OOO0OO00 ):#line:1162
        if (len (_O0O0OO0OO0OOOO0O0 ))!=len (_O00OO0000OOO0OO00 ):#line:1163
            print ("DIFF IN LEN for following cedent : "+str (len (_O0O0OO0OO0OOOO0O0 ))+" vs "+str (len (_O00OO0000OOO0OO00 )))#line:1164
            print ("trace cedent : "+str (_O0O0OO0OO0OOOO0O0 )+", traces "+str (_O00OO0000OOO0OO00 ))#line:1165
        OO0O000O0OOO00000 =''#line:1166
        O0O0O00OOO00000OO ={}#line:1167
        O00O0OOO0O0O0O0O0 =[]#line:1168
        for OOO00O0000OO0OOOO in range (len (_O0O0OO0OO0OOOO0O0 )):#line:1169
            OO0OO0OOOO00O0O0O =O0O0O0OOOO0OO000O .data ["varname"].index (OOOOOO0000OOO0O0O ['defi'].get ('attributes')[_O0O0OO0OO0OOOO0O0 [OOO00O0000OO0OOOO ]].get ('name'))#line:1170
            OO0O000O0OOO00000 =OO0O000O0OOO00000 +O0O0O0OOOO0OO000O .data ["varname"][OO0OO0OOOO00O0O0O ]+'('#line:1172
            O00O0OOO0O0O0O0O0 .append (OO0OO0OOOO00O0O0O )#line:1173
            OOOO00OO000OO00OO =[]#line:1174
            for O0OO00O0OO0OOOOO0 in _O00OO0000OOO0OO00 [OOO00O0000OO0OOOO ]:#line:1175
                OO0O000O0OOO00000 =OO0O000O0OOO00000 +str (O0O0O0OOOO0OO000O .data ["catnames"][OO0OO0OOOO00O0O0O ][O0OO00O0OO0OOOOO0 ])+" "#line:1176
                OOOO00OO000OO00OO .append (str (O0O0O0OOOO0OO000O .data ["catnames"][OO0OO0OOOO00O0O0O ][O0OO00O0OO0OOOOO0 ]))#line:1177
            OO0O000O0OOO00000 =OO0O000O0OOO00000 [:-1 ]+')'#line:1178
            O0O0O00OOO00000OO [O0O0O0OOOO0OO000O .data ["varname"][OO0OO0OOOO00O0O0O ]]=OOOO00OO000OO00OO #line:1179
            if OOO00O0000OO0OOOO +1 <len (_O0O0OO0OO0OOOO0O0 ):#line:1180
                OO0O000O0OOO00000 =OO0O000O0OOO00000 +' & '#line:1181
        return OO0O000O0OOO00000 ,O0O0O00OOO00000OO ,O00O0OOO0O0O0O0O0 #line:1185
    def _print_hypo (O00O000OO00000OOO ,O0OOOOOO0OOOO00O0 ):#line:1187
        O00O000OO00000OOO .print_rule (O0OOOOOO0OOOO00O0 )#line:1188
    def _print_rule (O0O00OOOOO00OOOO0 ,OO000OOO00OOO00O0 ):#line:1190
        if O0O00OOOOO00OOOO0 .verbosity ['print_rules']:#line:1191
            print ('Rules info : '+str (OO000OOO00OOO00O0 ['params']))#line:1192
            for OO000OOOO00000OOO in O0O00OOOOO00OOOO0 .task_actinfo ['cedents']:#line:1193
                print (OO000OOOO00000OOO ['cedent_type']+' = '+OO000OOOO00000OOO ['generated_string'])#line:1194
    def _genvar (O0OOO00OO00O0OOOO ,OOO0OO0OO0000OOOO ,O000O00OO0OO0OO0O ,_O0OOO0OOOOOO0000O ,_O0OOO0OO00OO00O00 ,_O000O0OOO00O000O0 ,_O0O00O0O000O0O0O0 ,_OOOO0000O000000O0 ,_O0000O0O000O0O0O0 ,_O0OO0OO000OO0OOO0 ):#line:1196
        _OOO0O0O0000O0O000 =0 #line:1197
        if O000O00OO0OO0OO0O ['num_cedent']>0 :#line:1198
            _OOO0O0O0000O0O000 =(_O0OO0OO000OO0OOO0 -_O0000O0O000O0O0O0 )/O000O00OO0OO0OO0O ['num_cedent']#line:1199
        for O0OO0OO0000O0OOOO in range (O000O00OO0OO0OO0O ['num_cedent']):#line:1200
            if len (_O0OOO0OOOOOO0000O )==0 or O0OO0OO0000O0OOOO >_O0OOO0OOOOOO0000O [-1 ]:#line:1201
                _O0OOO0OOOOOO0000O .append (O0OO0OO0000O0OOOO )#line:1202
                OO00O0O00OO0OO0OO =O0OOO00OO00O0OOOO .data ["varname"].index (O000O00OO0OO0OO0O ['defi'].get ('attributes')[O0OO0OO0000O0OOOO ].get ('name'))#line:1203
                _OOO00OOO0OOOO0OO0 =O000O00OO0OO0OO0O ['defi'].get ('attributes')[O0OO0OO0000O0OOOO ].get ('minlen')#line:1204
                _OO0000O00O0OOO000 =O000O00OO0OO0OO0O ['defi'].get ('attributes')[O0OO0OO0000O0OOOO ].get ('maxlen')#line:1205
                _O000O0OO0O00OOO0O =O000O00OO0OO0OO0O ['defi'].get ('attributes')[O0OO0OO0000O0OOOO ].get ('type')#line:1206
                O00OO0O0O0OOO0O00 =len (O0OOO00OO00O0OOOO .data ["dm"][OO00O0O00OO0OO0OO ])#line:1207
                _OOO0OO000O00OOO0O =[]#line:1208
                _O0OOO0OO00OO00O00 .append (_OOO0OO000O00OOO0O )#line:1209
                _OOO0O0O000OO0O0OO =int (0 )#line:1210
                O0OOO00OO00O0OOOO ._gencomb (OOO0OO0OO0000OOOO ,O000O00OO0OO0OO0O ,_O0OOO0OOOOOO0000O ,_O0OOO0OO00OO00O00 ,_OOO0OO000O00OOO0O ,_O000O0OOO00O000O0 ,_OOO0O0O000OO0O0OO ,O00OO0O0O0OOO0O00 ,_O000O0OO0O00OOO0O ,_O0O00O0O000O0O0O0 ,_OOOO0000O000000O0 ,_OOO00OOO0OOOO0OO0 ,_OO0000O00O0OOO000 ,_O0000O0O000O0O0O0 +O0OO0OO0000O0OOOO *_OOO0O0O0000O0O000 ,_O0000O0O000O0O0O0 +(O0OO0OO0000O0OOOO +1 )*_OOO0O0O0000O0O000 )#line:1211
                _O0OOO0OO00OO00O00 .pop ()#line:1212
                _O0OOO0OOOOOO0000O .pop ()#line:1213
    def _gencomb (O0OO0O0OO0O00O0O0 ,O000O0OOOO00OO000 ,OOO0OO0O0O0OO0OOO ,_OO0O0000OO00O0O00 ,_OOOO0O0000O0OOOO0 ,_OOO000O0O0O0O00O0 ,_O0OOO0O0O0000000O ,_OOO00OOO0OO0O0OO0 ,O0O0O0O0000OO0OO0 ,_OO0OO0OO000000O00 ,_O00OOO0OOO00000O0 ,_O0000O00000OO0000 ,_O0OO00000OO0O0OO0 ,_O00OOOOO00O0OO00O ,_O0OO000O0O0O0O00O ,_O00O0OOO0OOO0OOOO ):#line:1215
        _O0O0OOOOOO0OO0O0O =[]#line:1216
        if _OO0OO0OO000000O00 =="subset":#line:1217
            if len (_OOO000O0O0O0O00O0 )==0 :#line:1218
                _O0O0OOOOOO0OO0O0O =range (O0O0O0O0000OO0OO0 )#line:1219
            else :#line:1220
                _O0O0OOOOOO0OO0O0O =range (_OOO000O0O0O0O00O0 [-1 ]+1 ,O0O0O0O0000OO0OO0 )#line:1221
        elif _OO0OO0OO000000O00 =="seq":#line:1222
            if len (_OOO000O0O0O0O00O0 )==0 :#line:1223
                _O0O0OOOOOO0OO0O0O =range (O0O0O0O0000OO0OO0 -_O0OO00000OO0O0OO0 +1 )#line:1224
            else :#line:1225
                if _OOO000O0O0O0O00O0 [-1 ]+1 ==O0O0O0O0000OO0OO0 :#line:1226
                    return #line:1227
                OO0OO00OO0OO0OO0O =_OOO000O0O0O0O00O0 [-1 ]+1 #line:1228
                _O0O0OOOOOO0OO0O0O .append (OO0OO00OO0OO0OO0O )#line:1229
        elif _OO0OO0OO000000O00 =="lcut":#line:1230
            if len (_OOO000O0O0O0O00O0 )==0 :#line:1231
                OO0OO00OO0OO0OO0O =0 ;#line:1232
            else :#line:1233
                if _OOO000O0O0O0O00O0 [-1 ]+1 ==O0O0O0O0000OO0OO0 :#line:1234
                    return #line:1235
                OO0OO00OO0OO0OO0O =_OOO000O0O0O0O00O0 [-1 ]+1 #line:1236
            _O0O0OOOOOO0OO0O0O .append (OO0OO00OO0OO0OO0O )#line:1237
        elif _OO0OO0OO000000O00 =="rcut":#line:1238
            if len (_OOO000O0O0O0O00O0 )==0 :#line:1239
                OO0OO00OO0OO0OO0O =O0O0O0O0000OO0OO0 -1 ;#line:1240
            else :#line:1241
                if _OOO000O0O0O0O00O0 [-1 ]==0 :#line:1242
                    return #line:1243
                OO0OO00OO0OO0OO0O =_OOO000O0O0O0O00O0 [-1 ]-1 #line:1244
            _O0O0OOOOOO0OO0O0O .append (OO0OO00OO0OO0OO0O )#line:1246
        elif _OO0OO0OO000000O00 =="one":#line:1247
            if len (_OOO000O0O0O0O00O0 )==0 :#line:1248
                O0OO000OOO0O0OO0O =O0OO0O0OO0O00O0O0 .data ["varname"].index (OOO0OO0O0O0OO0OOO ['defi'].get ('attributes')[_OO0O0000OO00O0O00 [-1 ]].get ('name'))#line:1249
                try :#line:1250
                    OO0OO00OO0OO0OO0O =O0OO0O0OO0O00O0O0 .data ["catnames"][O0OO000OOO0O0OO0O ].index (OOO0OO0O0O0OO0OOO ['defi'].get ('attributes')[_OO0O0000OO00O0O00 [-1 ]].get ('value'))#line:1251
                except :#line:1252
                    print (f"ERROR: attribute '{OOO0OO0O0O0OO0OOO['defi'].get('attributes')[_OO0O0000OO00O0O00[-1]].get('name')}' has not value '{OOO0OO0O0O0OO0OOO['defi'].get('attributes')[_OO0O0000OO00O0O00[-1]].get('value')}'")#line:1253
                    exit (1 )#line:1254
                _O0O0OOOOOO0OO0O0O .append (OO0OO00OO0OO0OO0O )#line:1255
                _O0OO00000OO0O0OO0 =1 #line:1256
                _O00OOOOO00O0OO00O =1 #line:1257
            else :#line:1258
                print ("DEBUG: one category should not have more categories")#line:1259
                return #line:1260
        else :#line:1261
            print ("Attribute type "+_OO0OO0OO000000O00 +" not supported.")#line:1262
            return #line:1263
        if len (_O0O0OOOOOO0OO0O0O )>0 :#line:1265
            _OO0OO0OOOO00000OO =(_O00O0OOO0OOO0OOOO -_O0OO000O0O0O0O00O )/len (_O0O0OOOOOO0OO0O0O )#line:1266
        else :#line:1267
            _OO0OO0OOOO00000OO =0 #line:1268
        _OO000000O0O00O00O =0 #line:1270
        for O00O0O00OO000O0OO in _O0O0OOOOOO0OO0O0O :#line:1272
                _OOO000O0O0O0O00O0 .append (O00O0O00OO000O0OO )#line:1274
                _OOOO0O0000O0OOOO0 .pop ()#line:1275
                _OOOO0O0000O0OOOO0 .append (_OOO000O0O0O0O00O0 )#line:1276
                _OOOOOO0OOO00OOOO0 =_OOO00OOO0OO0O0OO0 |O0OO0O0OO0O00O0O0 .data ["dm"][O0OO0O0OO0O00O0O0 .data ["varname"].index (OOO0OO0O0O0OO0OOO ['defi'].get ('attributes')[_OO0O0000OO00O0O00 [-1 ]].get ('name'))][O00O0O00OO000O0OO ]#line:1280
                _O0O00O0O0O000OOO0 =1 #line:1282
                if (len (_OO0O0000OO00O0O00 )<_O00OOO0OOO00000O0 ):#line:1283
                    _O0O00O0O0O000OOO0 =-1 #line:1284
                if (len (_OOOO0O0000O0OOOO0 [-1 ])<_O0OO00000OO0O0OO0 ):#line:1286
                    _O0O00O0O0O000OOO0 =0 #line:1287
                _OOOO0OO00O0OOO0OO =0 #line:1289
                if OOO0OO0O0O0OO0OOO ['defi'].get ('type')=='con':#line:1290
                    _OOOO0OO00O0OOO0OO =_O0OOO0O0O0000000O &_OOOOOO0OOO00OOOO0 #line:1291
                else :#line:1292
                    _OOOO0OO00O0OOO0OO =_O0OOO0O0O0000000O |_OOOOOO0OOO00OOOO0 #line:1293
                OOO0OO0O0O0OO0OOO ['trace_cedent']=_OO0O0000OO00O0O00 #line:1294
                OOO0OO0O0O0OO0OOO ['traces']=_OOOO0O0000O0OOOO0 #line:1295
                OO0OO0OOO0O0OO00O ,OO0OOOO00OOO00O00 ,O000O0O0OO0O0O00O =O0OO0O0OO0O00O0O0 ._print (OOO0OO0O0O0OO0OOO ,_OO0O0000OO00O0O00 ,_OOOO0O0000O0OOOO0 )#line:1296
                OOO0OO0O0O0OO0OOO ['generated_string']=OO0OO0OOO0O0OO00O #line:1297
                OOO0OO0O0O0OO0OOO ['rule']=OO0OOOO00OOO00O00 #line:1298
                OOO0OO0O0O0OO0OOO ['filter_value']=_OOOO0OO00O0OOO0OO #line:1299
                OOO0OO0O0O0OO0OOO ['traces']=copy .deepcopy (_OOOO0O0000O0OOOO0 )#line:1300
                OOO0OO0O0O0OO0OOO ['trace_cedent']=copy .deepcopy (_OO0O0000OO00O0O00 )#line:1301
                OOO0OO0O0O0OO0OOO ['trace_cedent_asindata']=copy .deepcopy (O000O0O0OO0O0O00O )#line:1302
                O000O0OOOO00OO000 ['cedents'].append (OOO0OO0O0O0OO0OOO )#line:1304
                O000O00OOO000000O =O0OO0O0OO0O00O0O0 ._verify_opt (O000O0OOOO00OO000 ,OOO0OO0O0O0OO0OOO )#line:1305
                if not (O000O00OOO000000O ):#line:1311
                    if _O0O00O0O0O000OOO0 ==1 :#line:1312
                        if len (O000O0OOOO00OO000 ['cedents_to_do'])==len (O000O0OOOO00OO000 ['cedents']):#line:1314
                            if O0OO0O0OO0O00O0O0 .proc =='CFMiner':#line:1315
                                OO0O0O000O0O00O00 ,O00OOO0OO00OO0000 =O0OO0O0OO0O00O0O0 ._verifyCF (_OOOO0OO00O0OOO0OO )#line:1316
                            elif O0OO0O0OO0O00O0O0 .proc =='UICMiner':#line:1317
                                OO0O0O000O0O00O00 ,O00OOO0OO00OO0000 =O0OO0O0OO0O00O0O0 ._verifyUIC (_OOOO0OO00O0OOO0OO )#line:1318
                            elif O0OO0O0OO0O00O0O0 .proc =='4ftMiner':#line:1319
                                OO0O0O000O0O00O00 ,O00OOO0OO00OO0000 =O0OO0O0OO0O00O0O0 ._verify4ft (_OOOOOO0OOO00OOOO0 )#line:1320
                            elif O0OO0O0OO0O00O0O0 .proc =='SD4ftMiner':#line:1321
                                OO0O0O000O0O00O00 ,O00OOO0OO00OO0000 =O0OO0O0OO0O00O0O0 ._verifysd4ft (_OOOOOO0OOO00OOOO0 )#line:1322
                            elif O0OO0O0OO0O00O0O0 .proc =='NewAct4ftMiner':#line:1323
                                OO0O0O000O0O00O00 ,O00OOO0OO00OO0000 =O0OO0O0OO0O00O0O0 ._verifynewact4ft (_OOOOOO0OOO00OOOO0 )#line:1324
                            elif O0OO0O0OO0O00O0O0 .proc =='Act4ftMiner':#line:1325
                                OO0O0O000O0O00O00 ,O00OOO0OO00OO0000 =O0OO0O0OO0O00O0O0 ._verifyact4ft (_OOOOOO0OOO00OOOO0 )#line:1326
                            else :#line:1327
                                print ("Unsupported procedure : "+O0OO0O0OO0O00O0O0 .proc )#line:1328
                                exit (0 )#line:1329
                            if OO0O0O000O0O00O00 ==True :#line:1330
                                O0O0OO00OO00O0000 ={}#line:1331
                                O0O0OO00OO00O0000 ["rule_id"]=O0OO0O0OO0O00O0O0 .stats ['total_valid']#line:1332
                                O0O0OO00OO00O0000 ["cedents_str"]={}#line:1333
                                O0O0OO00OO00O0000 ["cedents_struct"]={}#line:1334
                                O0O0OO00OO00O0000 ['traces']={}#line:1335
                                O0O0OO00OO00O0000 ['trace_cedent_taskorder']={}#line:1336
                                O0O0OO00OO00O0000 ['trace_cedent_dataorder']={}#line:1337
                                for O0OOO00O0OOO00OO0 in O000O0OOOO00OO000 ['cedents']:#line:1338
                                    O0O0OO00OO00O0000 ['cedents_str'][O0OOO00O0OOO00OO0 ['cedent_type']]=O0OOO00O0OOO00OO0 ['generated_string']#line:1340
                                    O0O0OO00OO00O0000 ['cedents_struct'][O0OOO00O0OOO00OO0 ['cedent_type']]=O0OOO00O0OOO00OO0 ['rule']#line:1341
                                    O0O0OO00OO00O0000 ['traces'][O0OOO00O0OOO00OO0 ['cedent_type']]=O0OOO00O0OOO00OO0 ['traces']#line:1342
                                    O0O0OO00OO00O0000 ['trace_cedent_taskorder'][O0OOO00O0OOO00OO0 ['cedent_type']]=O0OOO00O0OOO00OO0 ['trace_cedent']#line:1343
                                    O0O0OO00OO00O0000 ['trace_cedent_dataorder'][O0OOO00O0OOO00OO0 ['cedent_type']]=O0OOO00O0OOO00OO0 ['trace_cedent_asindata']#line:1344
                                O0O0OO00OO00O0000 ["params"]=O00OOO0OO00OO0000 #line:1346
                                O0OO0O0OO0O00O0O0 ._print_rule (O0O0OO00OO00O0000 )#line:1348
                                O0OO0O0OO0O00O0O0 .rulelist .append (O0O0OO00OO00O0000 )#line:1354
                            O0OO0O0OO0O00O0O0 .stats ['total_cnt']+=1 #line:1356
                            O0OO0O0OO0O00O0O0 .stats ['total_ver']+=1 #line:1357
                    if _O0O00O0O0O000OOO0 >=0 :#line:1358
                        if len (O000O0OOOO00OO000 ['cedents_to_do'])>len (O000O0OOOO00OO000 ['cedents']):#line:1359
                            O0OO0O0OO0O00O0O0 ._start_cedent (O000O0OOOO00OO000 ,_O0OO000O0O0O0O00O +_OO000000O0O00O00O *_OO0OO0OOOO00000OO ,_O0OO000O0O0O0O00O +(_OO000000O0O00O00O +0.33 )*_OO0OO0OOOO00000OO )#line:1360
                    O000O0OOOO00OO000 ['cedents'].pop ()#line:1361
                    if (len (_OO0O0000OO00O0O00 )<_O0000O00000OO0000 ):#line:1362
                        O0OO0O0OO0O00O0O0 ._genvar (O000O0OOOO00OO000 ,OOO0OO0O0O0OO0OOO ,_OO0O0000OO00O0O00 ,_OOOO0O0000O0OOOO0 ,_OOOO0OO00O0OOO0OO ,_O00OOO0OOO00000O0 ,_O0000O00000OO0000 ,_O0OO000O0O0O0O00O +(_OO000000O0O00O00O +0.33 )*_OO0OO0OOOO00000OO ,_O0OO000O0O0O0O00O +(_OO000000O0O00O00O +0.66 )*_OO0OO0OOOO00000OO )#line:1363
                else :#line:1364
                    O000O0OOOO00OO000 ['cedents'].pop ()#line:1365
                if len (_OOO000O0O0O0O00O0 )<_O00OOOOO00O0OO00O :#line:1366
                    O0OO0O0OO0O00O0O0 ._gencomb (O000O0OOOO00OO000 ,OOO0OO0O0O0OO0OOO ,_OO0O0000OO00O0O00 ,_OOOO0O0000O0OOOO0 ,_OOO000O0O0O0O00O0 ,_O0OOO0O0O0000000O ,_OOOOOO0OOO00OOOO0 ,O0O0O0O0000OO0OO0 ,_OO0OO0OO000000O00 ,_O00OOO0OOO00000O0 ,_O0000O00000OO0000 ,_O0OO00000OO0O0OO0 ,_O00OOOOO00O0OO00O ,_O0OO000O0O0O0O00O +_OO0OO0OOOO00000OO *(_OO000000O0O00O00O +0.66 ),_O0OO000O0O0O0O00O +_OO0OO0OOOO00000OO *(_OO000000O0O00O00O +1 ))#line:1367
                _OOO000O0O0O0O00O0 .pop ()#line:1368
                _OO000000O0O00O00O +=1 #line:1369
                if O0OO0O0OO0O00O0O0 .options ['progressbar']:#line:1370
                    O0OO0O0OO0O00O0O0 .bar .update (min (100 ,_O0OO000O0O0O0O00O +_OO0OO0OOOO00000OO *_OO000000O0O00O00O ))#line:1371
    def _start_cedent (OOO00OOO00000O0O0 ,OO0O0O000OO0OO0OO ,_O00O0OO000OOO0OO0 ,_OOO00OOOO0000000O ):#line:1374
        if len (OO0O0O000OO0OO0OO ['cedents_to_do'])>len (OO0O0O000OO0OO0OO ['cedents']):#line:1375
            _OO000O000000O00OO =[]#line:1376
            _OO0OOOO00O0OOOOO0 =[]#line:1377
            OO0O00OOOO00O000O ={}#line:1378
            OO0O00OOOO00O000O ['cedent_type']=OO0O0O000OO0OO0OO ['cedents_to_do'][len (OO0O0O000OO0OO0OO ['cedents'])]#line:1379
            OO0O0OO0O0OO00000 =OO0O00OOOO00O000O ['cedent_type']#line:1380
            if ((OO0O0OO0O0OO00000 [-1 ]=='-')|(OO0O0OO0O0OO00000 [-1 ]=='+')):#line:1381
                OO0O0OO0O0OO00000 =OO0O0OO0O0OO00000 [:-1 ]#line:1382
            OO0O00OOOO00O000O ['defi']=OOO00OOO00000O0O0 .kwargs .get (OO0O0OO0O0OO00000 )#line:1384
            if (OO0O00OOOO00O000O ['defi']==None ):#line:1385
                print ("Error getting cedent ",OO0O00OOOO00O000O ['cedent_type'])#line:1386
            _OO000O00O0O0OOO00 =int (0 )#line:1387
            OO0O00OOOO00O000O ['num_cedent']=len (OO0O00OOOO00O000O ['defi'].get ('attributes'))#line:1394
            if (OO0O00OOOO00O000O ['defi'].get ('type')=='con'):#line:1395
                _OO000O00O0O0OOO00 =(1 <<OOO00OOO00000O0O0 .data ["rows_count"])-1 #line:1396
            OOO00OOO00000O0O0 ._genvar (OO0O0O000OO0OO0OO ,OO0O00OOOO00O000O ,_OO000O000000O00OO ,_OO0OOOO00O0OOOOO0 ,_OO000O00O0O0OOO00 ,OO0O00OOOO00O000O ['defi'].get ('minlen'),OO0O00OOOO00O000O ['defi'].get ('maxlen'),_O00O0OO000OOO0OO0 ,_OOO00OOOO0000000O )#line:1397
    def _calc_all (OO0OO0000O0OO0O00 ,**OO0O0OOO0OO0O00O0 ):#line:1400
        if "df"in OO0O0OOO0OO0O00O0 :#line:1401
            OO0OO0000O0OO0O00 ._prep_data (OO0OO0000O0OO0O00 .kwargs .get ("df"))#line:1402
        if not (OO0OO0000O0OO0O00 ._initialized ):#line:1403
            print ("ERROR: dataframe is missing and not initialized with dataframe")#line:1404
        else :#line:1405
            OO0OO0000O0OO0O00 ._calculate (**OO0O0OOO0OO0O00O0 )#line:1406
    def _check_cedents (O0O0OOO0OOOO0OOOO ,OO0O00O00OO00O0OO ,**OOOOO0OOOOOOOOOO0 ):#line:1408
        OO0O00O00O0O00000 =True #line:1409
        if (OOOOO0OOOOOOOOOO0 .get ('quantifiers',None )==None ):#line:1410
            print (f"Error: missing quantifiers.")#line:1411
            OO0O00O00O0O00000 =False #line:1412
            return OO0O00O00O0O00000 #line:1413
        if (type (OOOOO0OOOOOOOOOO0 .get ('quantifiers'))!=dict ):#line:1414
            print (f"Error: quantifiers are not dictionary type.")#line:1415
            OO0O00O00O0O00000 =False #line:1416
            return OO0O00O00O0O00000 #line:1417
        for OOOOOO0OOO00000O0 in OO0O00O00OO00O0OO :#line:1419
            if (OOOOO0OOOOOOOOOO0 .get (OOOOOO0OOO00000O0 ,None )==None ):#line:1420
                print (f"Error: cedent {OOOOOO0OOO00000O0} is missing in parameters.")#line:1421
                OO0O00O00O0O00000 =False #line:1422
                return OO0O00O00O0O00000 #line:1423
            O0O00O0O00O0OO0O0 =OOOOO0OOOOOOOOOO0 .get (OOOOOO0OOO00000O0 )#line:1424
            if (O0O00O0O00O0OO0O0 .get ('minlen'),None )==None :#line:1425
                print (f"Error: cedent {OOOOOO0OOO00000O0} has no minimal length specified.")#line:1426
                OO0O00O00O0O00000 =False #line:1427
                return OO0O00O00O0O00000 #line:1428
            if not (type (O0O00O0O00O0OO0O0 .get ('minlen'))is int ):#line:1429
                print (f"Error: cedent {OOOOOO0OOO00000O0} has invalid type of minimal length ({type(O0O00O0O00O0OO0O0.get('minlen'))}).")#line:1430
                OO0O00O00O0O00000 =False #line:1431
                return OO0O00O00O0O00000 #line:1432
            if (O0O00O0O00O0OO0O0 .get ('maxlen'),None )==None :#line:1433
                print (f"Error: cedent {OOOOOO0OOO00000O0} has no maximal length specified.")#line:1434
                OO0O00O00O0O00000 =False #line:1435
                return OO0O00O00O0O00000 #line:1436
            if not (type (O0O00O0O00O0OO0O0 .get ('maxlen'))is int ):#line:1437
                print (f"Error: cedent {OOOOOO0OOO00000O0} has invalid type of maximal length.")#line:1438
                OO0O00O00O0O00000 =False #line:1439
                return OO0O00O00O0O00000 #line:1440
            if (O0O00O0O00O0OO0O0 .get ('type'),None )==None :#line:1441
                print (f"Error: cedent {OOOOOO0OOO00000O0} has no type specified.")#line:1442
                OO0O00O00O0O00000 =False #line:1443
                return OO0O00O00O0O00000 #line:1444
            if not ((O0O00O0O00O0OO0O0 .get ('type'))in (['con','dis'])):#line:1445
                print (f"Error: cedent {OOOOOO0OOO00000O0} has invalid type. Allowed values are 'con' and 'dis'.")#line:1446
                OO0O00O00O0O00000 =False #line:1447
                return OO0O00O00O0O00000 #line:1448
            if (O0O00O0O00O0OO0O0 .get ('attributes'),None )==None :#line:1449
                print (f"Error: cedent {OOOOOO0OOO00000O0} has no attributes specified.")#line:1450
                OO0O00O00O0O00000 =False #line:1451
                return OO0O00O00O0O00000 #line:1452
            for OO000OO00000OOOOO in O0O00O0O00O0OO0O0 .get ('attributes'):#line:1453
                if (OO000OO00000OOOOO .get ('name'),None )==None :#line:1454
                    print (f"Error: cedent {OOOOOO0OOO00000O0} / attribute {OO000OO00000OOOOO} has no 'name' attribute specified.")#line:1455
                    OO0O00O00O0O00000 =False #line:1456
                    return OO0O00O00O0O00000 #line:1457
                if not ((OO000OO00000OOOOO .get ('name'))in O0O0OOO0OOOO0OOOO .data ["varname"]):#line:1458
                    print (f"Error: cedent {OOOOOO0OOO00000O0} / attribute {OO000OO00000OOOOO.get('name')} not in variable list. Please check spelling.")#line:1459
                    OO0O00O00O0O00000 =False #line:1460
                    return OO0O00O00O0O00000 #line:1461
                if (OO000OO00000OOOOO .get ('type'),None )==None :#line:1462
                    print (f"Error: cedent {OOOOOO0OOO00000O0} / attribute {OO000OO00000OOOOO.get('name')} has no 'type' attribute specified.")#line:1463
                    OO0O00O00O0O00000 =False #line:1464
                    return OO0O00O00O0O00000 #line:1465
                if not ((OO000OO00000OOOOO .get ('type'))in (['rcut','lcut','seq','subset','one'])):#line:1466
                    print (f"Error: cedent {OOOOOO0OOO00000O0} / attribute {OO000OO00000OOOOO.get('name')} has unsupported type {OO000OO00000OOOOO.get('type')}. Supported types are 'subset','seq','lcut','rcut','one'.")#line:1467
                    OO0O00O00O0O00000 =False #line:1468
                    return OO0O00O00O0O00000 #line:1469
                if (OO000OO00000OOOOO .get ('minlen'),None )==None :#line:1470
                    print (f"Error: cedent {OOOOOO0OOO00000O0} / attribute {OO000OO00000OOOOO.get('name')} has no minimal length specified.")#line:1471
                    OO0O00O00O0O00000 =False #line:1472
                    return OO0O00O00O0O00000 #line:1473
                if not (type (OO000OO00000OOOOO .get ('minlen'))is int ):#line:1474
                    if not (OO000OO00000OOOOO .get ('type')=='one'):#line:1475
                        print (f"Error: cedent {OOOOOO0OOO00000O0} / attribute {OO000OO00000OOOOO.get('name')} has invalid type of minimal length.")#line:1476
                        OO0O00O00O0O00000 =False #line:1477
                        return OO0O00O00O0O00000 #line:1478
                if (OO000OO00000OOOOO .get ('maxlen'),None )==None :#line:1479
                    print (f"Error: cedent {OOOOOO0OOO00000O0} / attribute {OO000OO00000OOOOO.get('name')} has no maximal length specified.")#line:1480
                    OO0O00O00O0O00000 =False #line:1481
                    return OO0O00O00O0O00000 #line:1482
                if not (type (OO000OO00000OOOOO .get ('maxlen'))is int ):#line:1483
                    if not (OO000OO00000OOOOO .get ('type')=='one'):#line:1484
                        print (f"Error: cedent {OOOOOO0OOO00000O0} / attribute {OO000OO00000OOOOO.get('name')} has invalid type of maximal length.")#line:1485
                        OO0O00O00O0O00000 =False #line:1486
                        return OO0O00O00O0O00000 #line:1487
        return OO0O00O00O0O00000 #line:1488
    def _calculate (O00O0O0OOOO000OO0 ,**OOO00O0OO0O00000O ):#line:1490
        if O00O0O0OOOO000OO0 .data ["data_prepared"]==0 :#line:1491
            print ("Error: data not prepared")#line:1492
            return #line:1493
        O00O0O0OOOO000OO0 .kwargs =OOO00O0OO0O00000O #line:1494
        O00O0O0OOOO000OO0 .proc =OOO00O0OO0O00000O .get ('proc')#line:1495
        O00O0O0OOOO000OO0 .quantifiers =OOO00O0OO0O00000O .get ('quantifiers')#line:1496
        O00O0O0OOOO000OO0 ._init_task ()#line:1498
        O00O0O0OOOO000OO0 .stats ['start_proc_time']=time .time ()#line:1499
        O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do']=[]#line:1500
        O00O0O0OOOO000OO0 .task_actinfo ['cedents']=[]#line:1501
        if OOO00O0OO0O00000O .get ("proc")=='UICMiner':#line:1504
            if not (O00O0O0OOOO000OO0 ._check_cedents (['ante'],**OOO00O0OO0O00000O )):#line:1505
                return #line:1506
            _O0OOOO0O0O000O000 =OOO00O0OO0O00000O .get ("cond")#line:1508
            if _O0OOOO0O0O000O000 !=None :#line:1509
                O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1510
            else :#line:1511
                OOO0OOO0O0OOOO0O0 =O00O0O0OOOO000OO0 .cedent #line:1512
                OOO0OOO0O0OOOO0O0 ['cedent_type']='cond'#line:1513
                OOO0OOO0O0OOOO0O0 ['filter_value']=(1 <<O00O0O0OOOO000OO0 .data ["rows_count"])-1 #line:1514
                OOO0OOO0O0OOOO0O0 ['generated_string']='---'#line:1515
                O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1517
                O00O0O0OOOO000OO0 .task_actinfo ['cedents'].append (OOO0OOO0O0OOOO0O0 )#line:1518
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1519
            if OOO00O0OO0O00000O .get ('target',None )==None :#line:1520
                print ("ERROR: no succedent/target variable defined for UIC Miner")#line:1521
                return #line:1522
            if not (OOO00O0OO0O00000O .get ('target')in O00O0O0OOOO000OO0 .data ["varname"]):#line:1523
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1524
                return #line:1525
            if ("aad_score"in O00O0O0OOOO000OO0 .quantifiers ):#line:1526
                if not ("aad_weights"in O00O0O0OOOO000OO0 .quantifiers ):#line:1527
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:1528
                    return #line:1529
                if not (len (O00O0O0OOOO000OO0 .quantifiers .get ("aad_weights"))==len (O00O0O0OOOO000OO0 .data ["dm"][O00O0O0OOOO000OO0 .data ["varname"].index (O00O0O0OOOO000OO0 .kwargs .get ('target'))])):#line:1530
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:1531
                    return #line:1532
        elif OOO00O0OO0O00000O .get ("proc")=='CFMiner':#line:1533
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do']=['cond']#line:1534
            if OOO00O0OO0O00000O .get ('target',None )==None :#line:1535
                print ("ERROR: no target variable defined for CF Miner")#line:1536
                return #line:1537
            if not (O00O0O0OOOO000OO0 ._check_cedents (['cond'],**OOO00O0OO0O00000O )):#line:1538
                return #line:1539
            if not (OOO00O0OO0O00000O .get ('target')in O00O0O0OOOO000OO0 .data ["varname"]):#line:1540
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1541
                return #line:1542
            if ("aad"in O00O0O0OOOO000OO0 .quantifiers ):#line:1543
                if not ("aad_weights"in O00O0O0OOOO000OO0 .quantifiers ):#line:1544
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:1545
                    return #line:1546
                if not (len (O00O0O0OOOO000OO0 .quantifiers .get ("aad_weights"))==len (O00O0O0OOOO000OO0 .data ["dm"][O00O0O0OOOO000OO0 .data ["varname"].index (O00O0O0OOOO000OO0 .kwargs .get ('target'))])):#line:1547
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:1548
                    return #line:1549
        elif OOO00O0OO0O00000O .get ("proc")=='4ftMiner':#line:1552
            if not (O00O0O0OOOO000OO0 ._check_cedents (['ante','succ'],**OOO00O0OO0O00000O )):#line:1553
                return #line:1554
            _O0OOOO0O0O000O000 =OOO00O0OO0O00000O .get ("cond")#line:1556
            if _O0OOOO0O0O000O000 !=None :#line:1557
                O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1558
            else :#line:1559
                OOO0OOO0O0OOOO0O0 =O00O0O0OOOO000OO0 .cedent #line:1560
                OOO0OOO0O0OOOO0O0 ['cedent_type']='cond'#line:1561
                OOO0OOO0O0OOOO0O0 ['filter_value']=(1 <<O00O0O0OOOO000OO0 .data ["rows_count"])-1 #line:1562
                OOO0OOO0O0OOOO0O0 ['generated_string']='---'#line:1563
                O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1565
                O00O0O0OOOO000OO0 .task_actinfo ['cedents'].append (OOO0OOO0O0OOOO0O0 )#line:1566
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1570
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('succ')#line:1571
        elif OOO00O0OO0O00000O .get ("proc")=='NewAct4ftMiner':#line:1572
            _O0OOOO0O0O000O000 =OOO00O0OO0O00000O .get ("cond")#line:1575
            if _O0OOOO0O0O000O000 !=None :#line:1576
                O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1577
            else :#line:1578
                OOO0OOO0O0OOOO0O0 =O00O0O0OOOO000OO0 .cedent #line:1579
                OOO0OOO0O0OOOO0O0 ['cedent_type']='cond'#line:1580
                OOO0OOO0O0OOOO0O0 ['filter_value']=(1 <<O00O0O0OOOO000OO0 .data ["rows_count"])-1 #line:1581
                OOO0OOO0O0OOOO0O0 ['generated_string']='---'#line:1582
                print (OOO0OOO0O0OOOO0O0 ['filter_value'])#line:1583
                O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1584
                O00O0O0OOOO000OO0 .task_actinfo ['cedents'].append (OOO0OOO0O0OOOO0O0 )#line:1585
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('antv')#line:1586
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('sucv')#line:1587
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1588
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('succ')#line:1589
        elif OOO00O0OO0O00000O .get ("proc")=='Act4ftMiner':#line:1590
            _O0OOOO0O0O000O000 =OOO00O0OO0O00000O .get ("cond")#line:1593
            if _O0OOOO0O0O000O000 !=None :#line:1594
                O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1595
            else :#line:1596
                OOO0OOO0O0OOOO0O0 =O00O0O0OOOO000OO0 .cedent #line:1597
                OOO0OOO0O0OOOO0O0 ['cedent_type']='cond'#line:1598
                OOO0OOO0O0OOOO0O0 ['filter_value']=(1 <<O00O0O0OOOO000OO0 .data ["rows_count"])-1 #line:1599
                OOO0OOO0O0OOOO0O0 ['generated_string']='---'#line:1600
                print (OOO0OOO0O0OOOO0O0 ['filter_value'])#line:1601
                O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1602
                O00O0O0OOOO000OO0 .task_actinfo ['cedents'].append (OOO0OOO0O0OOOO0O0 )#line:1603
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('antv-')#line:1604
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('antv+')#line:1605
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('sucv-')#line:1606
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('sucv+')#line:1607
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1608
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('succ')#line:1609
        elif OOO00O0OO0O00000O .get ("proc")=='SD4ftMiner':#line:1610
            if not (O00O0O0OOOO000OO0 ._check_cedents (['ante','succ','frst','scnd'],**OOO00O0OO0O00000O )):#line:1613
                return #line:1614
            _O0OOOO0O0O000O000 =OOO00O0OO0O00000O .get ("cond")#line:1615
            if _O0OOOO0O0O000O000 !=None :#line:1616
                O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1617
            else :#line:1618
                OOO0OOO0O0OOOO0O0 =O00O0O0OOOO000OO0 .cedent #line:1619
                OOO0OOO0O0OOOO0O0 ['cedent_type']='cond'#line:1620
                OOO0OOO0O0OOOO0O0 ['filter_value']=(1 <<O00O0O0OOOO000OO0 .data ["rows_count"])-1 #line:1621
                OOO0OOO0O0OOOO0O0 ['generated_string']='---'#line:1622
                O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1624
                O00O0O0OOOO000OO0 .task_actinfo ['cedents'].append (OOO0OOO0O0OOOO0O0 )#line:1625
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('frst')#line:1626
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('scnd')#line:1627
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1628
            O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do'].append ('succ')#line:1629
        else :#line:1630
            print ("Unsupported procedure")#line:1631
            return #line:1632
        print ("Will go for ",OOO00O0OO0O00000O .get ("proc"))#line:1633
        O00O0O0OOOO000OO0 .task_actinfo ['optim']={}#line:1636
        O0O0O0O000O000O00 =True #line:1637
        for OOOOOOOOOO0000OO0 in O00O0O0OOOO000OO0 .task_actinfo ['cedents_to_do']:#line:1638
            try :#line:1639
                OOO00O00OO00O00OO =O00O0O0OOOO000OO0 .kwargs .get (OOOOOOOOOO0000OO0 )#line:1640
                if OOO00O00OO00O00OO .get ('type')!='con':#line:1644
                    O0O0O0O000O000O00 =False #line:1645
            except :#line:1647
                O00O0OOO00O0OOOOO =1 <2 #line:1648
        if O00O0O0OOOO000OO0 .options ['optimizations']==False :#line:1650
            O0O0O0O000O000O00 =False #line:1651
        O0OOO0O000OO0OOOO ={}#line:1652
        O0OOO0O000OO0OOOO ['only_con']=O0O0O0O000O000O00 #line:1653
        O00O0O0OOOO000OO0 .task_actinfo ['optim']=O0OOO0O000OO0OOOO #line:1654
        print ("Starting to mine rules.")#line:1662
        sys .stdout .flush ()#line:1663
        time .sleep (0.01 )#line:1664
        if O00O0O0OOOO000OO0 .options ['progressbar']:#line:1665
            OOOOOOO0000O0OO00 =[progressbar .Percentage (),progressbar .Bar (),progressbar .Timer ()]#line:1666
            O00O0O0OOOO000OO0 .bar =progressbar .ProgressBar (widgets =OOOOOOO0000O0OO00 ,max_value =100 ,fd =sys .stdout ).start ()#line:1667
            O00O0O0OOOO000OO0 .bar .update (0 )#line:1668
        O00O0O0OOOO000OO0 .progress_lower =0 #line:1669
        O00O0O0OOOO000OO0 .progress_upper =100 #line:1670
        O00O0O0OOOO000OO0 ._start_cedent (O00O0O0OOOO000OO0 .task_actinfo ,O00O0O0OOOO000OO0 .progress_lower ,O00O0O0OOOO000OO0 .progress_upper )#line:1671
        if O00O0O0OOOO000OO0 .options ['progressbar']:#line:1672
            O00O0O0OOOO000OO0 .bar .update (100 )#line:1673
            O00O0O0OOOO000OO0 .bar .finish ()#line:1674
        O00O0O0OOOO000OO0 .stats ['end_proc_time']=time .time ()#line:1676
        print ("Done. Total verifications : "+str (O00O0O0OOOO000OO0 .stats ['total_cnt'])+", rules "+str (O00O0O0OOOO000OO0 .stats ['total_valid'])+", times: prep "+"{:.2f}".format (O00O0O0OOOO000OO0 .stats ['end_prep_time']-O00O0O0OOOO000OO0 .stats ['start_prep_time'])+"sec, processing "+"{:.2f}".format (O00O0O0OOOO000OO0 .stats ['end_proc_time']-O00O0O0OOOO000OO0 .stats ['start_proc_time'])+"sec")#line:1680
        OOO00OO00OOO0000O ={}#line:1681
        OOOOO0O0000O0OOOO ={}#line:1682
        OOOOO0O0000O0OOOO ["task_type"]=OOO00O0OO0O00000O .get ('proc')#line:1683
        OOOOO0O0000O0OOOO ["target"]=OOO00O0OO0O00000O .get ('target')#line:1685
        OOOOO0O0000O0OOOO ["self.quantifiers"]=O00O0O0OOOO000OO0 .quantifiers #line:1686
        if OOO00O0OO0O00000O .get ('cond')!=None :#line:1688
            OOOOO0O0000O0OOOO ['cond']=OOO00O0OO0O00000O .get ('cond')#line:1689
        if OOO00O0OO0O00000O .get ('ante')!=None :#line:1690
            OOOOO0O0000O0OOOO ['ante']=OOO00O0OO0O00000O .get ('ante')#line:1691
        if OOO00O0OO0O00000O .get ('succ')!=None :#line:1692
            OOOOO0O0000O0OOOO ['succ']=OOO00O0OO0O00000O .get ('succ')#line:1693
        if OOO00O0OO0O00000O .get ('opts')!=None :#line:1694
            OOOOO0O0000O0OOOO ['opts']=OOO00O0OO0O00000O .get ('opts')#line:1695
        if O00O0O0OOOO000OO0 .df is None :#line:1696
            OOOOO0O0000O0OOOO ['rowcount']=len (OOO00O0OO0O00000O .get ('df').index )#line:1697
        else :#line:1698
            OOOOO0O0000O0OOOO ['rowcount']=len (O00O0O0OOOO000OO0 .df .index )#line:1699
        OOO00OO00OOO0000O ["taskinfo"]=OOOOO0O0000O0OOOO #line:1700
        O0OOOO000OOOOO000 ={}#line:1701
        O0OOOO000OOOOO000 ["total_verifications"]=O00O0O0OOOO000OO0 .stats ['total_cnt']#line:1702
        O0OOOO000OOOOO000 ["valid_rules"]=O00O0O0OOOO000OO0 .stats ['total_valid']#line:1703
        O0OOOO000OOOOO000 ["total_verifications_with_opt"]=O00O0O0OOOO000OO0 .stats ['total_ver']#line:1704
        O0OOOO000OOOOO000 ["time_prep"]=O00O0O0OOOO000OO0 .stats ['end_prep_time']-O00O0O0OOOO000OO0 .stats ['start_prep_time']#line:1705
        O0OOOO000OOOOO000 ["time_processing"]=O00O0O0OOOO000OO0 .stats ['end_proc_time']-O00O0O0OOOO000OO0 .stats ['start_proc_time']#line:1706
        O0OOOO000OOOOO000 ["time_total"]=O00O0O0OOOO000OO0 .stats ['end_prep_time']-O00O0O0OOOO000OO0 .stats ['start_prep_time']+O00O0O0OOOO000OO0 .stats ['end_proc_time']-O00O0O0OOOO000OO0 .stats ['start_proc_time']#line:1707
        OOO00OO00OOO0000O ["summary_statistics"]=O0OOOO000OOOOO000 #line:1708
        OOO00OO00OOO0000O ["rules"]=O00O0O0OOOO000OO0 .rulelist #line:1709
        OOOO0O0OO00000OOO ={}#line:1710
        OOOO0O0OO00000OOO ["varname"]=O00O0O0OOOO000OO0 .data ["varname"]#line:1711
        OOOO0O0OO00000OOO ["catnames"]=O00O0O0OOOO000OO0 .data ["catnames"]#line:1712
        OOO00OO00OOO0000O ["datalabels"]=OOOO0O0OO00000OOO #line:1713
        O00O0O0OOOO000OO0 .result =OOO00OO00OOO0000O #line:1714
    def print_summary (O0O000OO00O00O0OO ):#line:1716
        ""#line:1719
        if not (O0O000OO00O00O0OO ._is_calculated ()):#line:1720
            print ("ERROR: Task has not been calculated.")#line:1721
            return #line:1722
        print ("")#line:1723
        print ("CleverMiner task processing summary:")#line:1724
        print ("")#line:1725
        print (f"Task type : {O0O000OO00O00O0OO.result['taskinfo']['task_type']}")#line:1726
        print (f"Number of verifications : {O0O000OO00O00O0OO.result['summary_statistics']['total_verifications']}")#line:1727
        print (f"Number of rules : {O0O000OO00O00O0OO.result['summary_statistics']['valid_rules']}")#line:1728
        print (f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(O0O000OO00O00O0OO.result['summary_statistics']['time_total']))}")#line:1729
        print (f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(O0O000OO00O00O0OO.result['summary_statistics']['time_prep']))}")#line:1731
        print (f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(O0O000OO00O00O0OO.result['summary_statistics']['time_processing']))}")#line:1732
        print ("")#line:1733
    def print_hypolist (OOOOO0O00O0OOOOOO ):#line:1735
        OOOOO0O00O0OOOOOO .print_rulelist ();#line:1736
    def print_rulelist (O00OOO00O0OO0O0OO ,sortby =None ,storesorted =False ):#line:1738
        if not (O00OOO00O0OO0O0OO ._is_calculated ()):#line:1739
            print ("ERROR: Task has not been calculated.")#line:1740
            return #line:1741
        def OOO00O00O0O0O0000 (OO0OO0O0OOO00OO0O ):#line:1742
            O0OO0000000O0O0O0 =OO0OO0O0OOO00OO0O ["params"]#line:1743
            return O0OO0000000O0O0O0 .get (sortby ,0 )#line:1744
        print ("")#line:1746
        print ("List of rules:")#line:1747
        if O00OOO00O0OO0O0OO .result ['taskinfo']['task_type']=="4ftMiner":#line:1748
            print ("RULEID BASE  CONF  AAD    Rule")#line:1749
        elif O00OOO00O0OO0O0OO .result ['taskinfo']['task_type']=="UICMiner":#line:1750
            print ("RULEID BASE  AAD_SCORE  Rule")#line:1751
        elif O00OOO00O0OO0O0OO .result ['taskinfo']['task_type']=="CFMiner":#line:1752
            print ("RULEID BASE  S_UP  S_DOWN Condition")#line:1753
        elif O00OOO00O0OO0O0OO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1754
            print ("RULEID BASE1 BASE2 RatioConf DeltaConf Rule")#line:1755
        else :#line:1756
            print ("Unsupported task type for rulelist")#line:1757
            return #line:1758
        OOOOOO0OO0O00O0O0 =O00OOO00O0OO0O0OO .result ["rules"]#line:1759
        if sortby is not None :#line:1760
            OOOOOO0OO0O00O0O0 =sorted (OOOOOO0OO0O00O0O0 ,key =OOO00O00O0O0O0000 ,reverse =True )#line:1761
            if storesorted :#line:1762
                O00OOO00O0OO0O0OO .result ["rules"]=OOOOOO0OO0O00O0O0 #line:1763
        for O0000O00OO000OOO0 in OOOOOO0OO0O00O0O0 :#line:1765
            OOO0O00O0O0OOOO0O ="{:6d}".format (O0000O00OO000OOO0 ["rule_id"])#line:1766
            if O00OOO00O0OO0O0OO .result ['taskinfo']['task_type']=="4ftMiner":#line:1767
                OOO0O00O0O0OOOO0O =OOO0O00O0O0OOOO0O +" "+"{:5d}".format (O0000O00OO000OOO0 ["params"]["base"])+" "+"{:.3f}".format (O0000O00OO000OOO0 ["params"]["conf"])+" "+"{:+.3f}".format (O0000O00OO000OOO0 ["params"]["aad"])#line:1769
                OOO0O00O0O0OOOO0O =OOO0O00O0O0OOOO0O +" "+O0000O00OO000OOO0 ["cedents_str"]["ante"]+" => "+O0000O00OO000OOO0 ["cedents_str"]["succ"]+" | "+O0000O00OO000OOO0 ["cedents_str"]["cond"]#line:1770
            elif O00OOO00O0OO0O0OO .result ['taskinfo']['task_type']=="UICMiner":#line:1771
                OOO0O00O0O0OOOO0O =OOO0O00O0O0OOOO0O +" "+"{:5d}".format (O0000O00OO000OOO0 ["params"]["base"])+" "+"{:.3f}".format (O0000O00OO000OOO0 ["params"]["aad_score"])#line:1772
                OOO0O00O0O0OOOO0O =OOO0O00O0O0OOOO0O +"     "+O0000O00OO000OOO0 ["cedents_str"]["ante"]+" => "+O00OOO00O0OO0O0OO .result ['taskinfo']['target']+"(*) | "+O0000O00OO000OOO0 ["cedents_str"]["cond"]#line:1773
            elif O00OOO00O0OO0O0OO .result ['taskinfo']['task_type']=="CFMiner":#line:1774
                OOO0O00O0O0OOOO0O =OOO0O00O0O0OOOO0O +" "+"{:5d}".format (O0000O00OO000OOO0 ["params"]["base"])+" "+"{:5d}".format (O0000O00OO000OOO0 ["params"]["s_up"])+" "+"{:5d}".format (O0000O00OO000OOO0 ["params"]["s_down"])#line:1775
                OOO0O00O0O0OOOO0O =OOO0O00O0O0OOOO0O +" "+O0000O00OO000OOO0 ["cedents_str"]["cond"]#line:1776
            elif O00OOO00O0OO0O0OO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1777
                OOO0O00O0O0OOOO0O =OOO0O00O0O0OOOO0O +" "+"{:5d}".format (O0000O00OO000OOO0 ["params"]["base1"])+" "+"{:5d}".format (O0000O00OO000OOO0 ["params"]["base2"])+"    "+"{:.3f}".format (O0000O00OO000OOO0 ["params"]["ratioconf"])+"    "+"{:+.3f}".format (O0000O00OO000OOO0 ["params"]["deltaconf"])#line:1778
                OOO0O00O0O0OOOO0O =OOO0O00O0O0OOOO0O +"  "+O0000O00OO000OOO0 ["cedents_str"]["ante"]+" => "+O0000O00OO000OOO0 ["cedents_str"]["succ"]+" | "+O0000O00OO000OOO0 ["cedents_str"]["cond"]+" : "+O0000O00OO000OOO0 ["cedents_str"]["frst"]+" x "+O0000O00OO000OOO0 ["cedents_str"]["scnd"]#line:1779
            print (OOO0O00O0O0OOOO0O )#line:1781
        print ("")#line:1782
    def print_hypo (O00OO0O00OOO00000 ,OOO0O00O00OOO00O0 ):#line:1784
        O00OO0O00OOO00000 .print_rule (OOO0O00O00OOO00O0 )#line:1785
    def print_rule (O00O0O0000000OOO0 ,OO0O0O00OOOOO0000 ):#line:1788
        if not (O00O0O0000000OOO0 ._is_calculated ()):#line:1789
            print ("ERROR: Task has not been calculated.")#line:1790
            return #line:1791
        print ("")#line:1792
        if (OO0O0O00OOOOO0000 <=len (O00O0O0000000OOO0 .result ["rules"])):#line:1793
            if O00O0O0000000OOO0 .result ['taskinfo']['task_type']=="4ftMiner":#line:1794
                print ("")#line:1795
                O00OO00O0OO0O00OO =O00O0O0000000OOO0 .result ["rules"][OO0O0O00OOOOO0000 -1 ]#line:1796
                print (f"Rule id : {O00OO00O0OO0O00OO['rule_id']}")#line:1797
                print ("")#line:1798
                print (f"Base : {'{:5d}'.format(O00OO00O0OO0O00OO['params']['base'])}  Relative base : {'{:.3f}'.format(O00OO00O0OO0O00OO['params']['rel_base'])}  CONF : {'{:.3f}'.format(O00OO00O0OO0O00OO['params']['conf'])}  AAD : {'{:+.3f}'.format(O00OO00O0OO0O00OO['params']['aad'])}  BAD : {'{:+.3f}'.format(O00OO00O0OO0O00OO['params']['bad'])}")#line:1799
                print ("")#line:1800
                print ("Cedents:")#line:1801
                print (f"  antecedent : {O00OO00O0OO0O00OO['cedents_str']['ante']}")#line:1802
                print (f"  succcedent : {O00OO00O0OO0O00OO['cedents_str']['succ']}")#line:1803
                print (f"  condition  : {O00OO00O0OO0O00OO['cedents_str']['cond']}")#line:1804
                print ("")#line:1805
                print ("Fourfold table")#line:1806
                print (f"    |  S  |  ¬S |")#line:1807
                print (f"----|-----|-----|")#line:1808
                print (f" A  |{'{:5d}'.format(O00OO00O0OO0O00OO['params']['fourfold'][0])}|{'{:5d}'.format(O00OO00O0OO0O00OO['params']['fourfold'][1])}|")#line:1809
                print (f"----|-----|-----|")#line:1810
                print (f"¬A  |{'{:5d}'.format(O00OO00O0OO0O00OO['params']['fourfold'][2])}|{'{:5d}'.format(O00OO00O0OO0O00OO['params']['fourfold'][3])}|")#line:1811
                print (f"----|-----|-----|")#line:1812
            elif O00O0O0000000OOO0 .result ['taskinfo']['task_type']=="CFMiner":#line:1813
                print ("")#line:1814
                O00OO00O0OO0O00OO =O00O0O0000000OOO0 .result ["rules"][OO0O0O00OOOOO0000 -1 ]#line:1815
                print (f"Rule id : {O00OO00O0OO0O00OO['rule_id']}")#line:1816
                print ("")#line:1817
                O0O000O00O0O0O0OO =""#line:1818
                if ('aad'in O00OO00O0OO0O00OO ['params']):#line:1819
                    O0O000O00O0O0O0OO ="aad : "+str (O00OO00O0OO0O00OO ['params']['aad'])#line:1820
                print (f"Base : {'{:5d}'.format(O00OO00O0OO0O00OO['params']['base'])}  Relative base : {'{:.3f}'.format(O00OO00O0OO0O00OO['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(O00OO00O0OO0O00OO['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(O00OO00O0OO0O00OO['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(O00OO00O0OO0O00OO['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(O00OO00O0OO0O00OO['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(O00OO00O0OO0O00OO['params']['max'])}  Histogram minimum : {'{:5d}'.format(O00OO00O0OO0O00OO['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(O00OO00O0OO0O00OO['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(O00OO00O0OO0O00OO['params']['rel_min'])} {O0O000O00O0O0O0OO}")#line:1822
                print ("")#line:1823
                print (f"Condition  : {O00OO00O0OO0O00OO['cedents_str']['cond']}")#line:1824
                print ("")#line:1825
                OO00O00OOOO000O0O =O00O0O0000000OOO0 .get_category_names (O00O0O0000000OOO0 .result ["taskinfo"]["target"])#line:1826
                print (f"Categories in target variable  {OO00O00OOOO000O0O}")#line:1827
                print (f"Histogram                      {O00OO00O0OO0O00OO['params']['hist']}")#line:1828
                if ('aad'in O00OO00O0OO0O00OO ['params']):#line:1829
                    print (f"Histogram on full set          {O00OO00O0OO0O00OO['params']['hist_full']}")#line:1830
                    print (f"Relative histogram             {O00OO00O0OO0O00OO['params']['rel_hist']}")#line:1831
                    print (f"Relative histogram on full set {O00OO00O0OO0O00OO['params']['rel_hist_full']}")#line:1832
            elif O00O0O0000000OOO0 .result ['taskinfo']['task_type']=="UICMiner":#line:1833
                print ("")#line:1834
                O00OO00O0OO0O00OO =O00O0O0000000OOO0 .result ["rules"][OO0O0O00OOOOO0000 -1 ]#line:1835
                print (f"Rule id : {O00OO00O0OO0O00OO['rule_id']}")#line:1836
                print ("")#line:1837
                O0O000O00O0O0O0OO =""#line:1838
                if ('aad_score'in O00OO00O0OO0O00OO ['params']):#line:1839
                    O0O000O00O0O0O0OO ="aad score : "+str (O00OO00O0OO0O00OO ['params']['aad_score'])#line:1840
                print (f"Base : {'{:5d}'.format(O00OO00O0OO0O00OO['params']['base'])}  Relative base : {'{:.3f}'.format(O00OO00O0OO0O00OO['params']['rel_base'])}   {O0O000O00O0O0O0OO}")#line:1842
                print ("")#line:1843
                print (f"Condition  : {O00OO00O0OO0O00OO['cedents_str']['cond']}")#line:1844
                print (f"Antecedent : {O00OO00O0OO0O00OO['cedents_str']['ante']}")#line:1845
                print ("")#line:1846
                print (f"Histogram                                        {O00OO00O0OO0O00OO['params']['hist']}")#line:1847
                if ('aad_score'in O00OO00O0OO0O00OO ['params']):#line:1848
                    print (f"Histogram on full set with condition             {O00OO00O0OO0O00OO['params']['hist_cond']}")#line:1849
                    print (f"Relative histogram                               {O00OO00O0OO0O00OO['params']['rel_hist']}")#line:1850
                    print (f"Relative histogram on full set with condition    {O00OO00O0OO0O00OO['params']['rel_hist_cond']}")#line:1851
                O0OOOOOOOOOOOO0O0 =O00O0O0000000OOO0 .result ['datalabels']['catnames'][O00O0O0000000OOO0 .result ['datalabels']['varname'].index (O00O0O0000000OOO0 .result ['taskinfo']['target'])]#line:1852
                print (" ")#line:1854
                print ("Interpretation:")#line:1855
                for O000OOOO0OOOOOOO0 in range (len (O0OOOOOOOOOOOO0O0 )):#line:1856
                  OO00O000OOO00OO0O =0 #line:1857
                  if O00OO00O0OO0O00OO ['params']['rel_hist'][O000OOOO0OOOOOOO0 ]>0 :#line:1858
                      OO00O000OOO00OO0O =O00OO00O0OO0O00OO ['params']['rel_hist'][O000OOOO0OOOOOOO0 ]/O00OO00O0OO0O00OO ['params']['rel_hist_cond'][O000OOOO0OOOOOOO0 ]#line:1859
                  OOOOOOO000O0OOOO0 =''#line:1860
                  if not (O00OO00O0OO0O00OO ['cedents_str']['cond']=='---'):#line:1861
                      OOOOOOO000O0OOOO0 ="For "+O00OO00O0OO0O00OO ['cedents_str']['cond']+": "#line:1862
                  print (f"    {OOOOOOO000O0OOOO0}{O00O0O0000000OOO0.result['taskinfo']['target']}({O0OOOOOOOOOOOO0O0[O000OOOO0OOOOOOO0]}) has an occurrence of {'{:.1%}'.format(O00OO00O0OO0O00OO['params']['rel_hist_cond'][O000OOOO0OOOOOOO0])}, with antecedent it has an occurrence of {'{:.1%}'.format(O00OO00O0OO0O00OO['params']['rel_hist'][O000OOOO0OOOOOOO0])}, that is {'{:.3f}'.format(OO00O000OOO00OO0O)} times more.")#line:1864
            elif O00O0O0000000OOO0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1865
                print ("")#line:1866
                O00OO00O0OO0O00OO =O00O0O0000000OOO0 .result ["rules"][OO0O0O00OOOOO0000 -1 ]#line:1867
                print (f"Rule id : {O00OO00O0OO0O00OO['rule_id']}")#line:1868
                print ("")#line:1869
                print (f"Base1 : {'{:5d}'.format(O00OO00O0OO0O00OO['params']['base1'])} Base2 : {'{:5d}'.format(O00OO00O0OO0O00OO['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(O00OO00O0OO0O00OO['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(O00OO00O0OO0O00OO['params']['rel_base2'])} CONF1 : {'{:.3f}'.format(O00OO00O0OO0O00OO['params']['conf1'])}  CONF2 : {'{:+.3f}'.format(O00OO00O0OO0O00OO['params']['conf2'])}  Delta Conf : {'{:+.3f}'.format(O00OO00O0OO0O00OO['params']['deltaconf'])} Ratio Conf : {'{:+.3f}'.format(O00OO00O0OO0O00OO['params']['ratioconf'])}")#line:1870
                print ("")#line:1871
                print ("Cedents:")#line:1872
                print (f"  antecedent : {O00OO00O0OO0O00OO['cedents_str']['ante']}")#line:1873
                print (f"  succcedent : {O00OO00O0OO0O00OO['cedents_str']['succ']}")#line:1874
                print (f"  condition  : {O00OO00O0OO0O00OO['cedents_str']['cond']}")#line:1875
                print (f"  first set  : {O00OO00O0OO0O00OO['cedents_str']['frst']}")#line:1876
                print (f"  second set : {O00OO00O0OO0O00OO['cedents_str']['scnd']}")#line:1877
                print ("")#line:1878
                print ("Fourfold tables:")#line:1879
                print (f"FRST|  S  |  ¬S |  SCND|  S  |  ¬S |");#line:1880
                print (f"----|-----|-----|  ----|-----|-----| ")#line:1881
                print (f" A  |{'{:5d}'.format(O00OO00O0OO0O00OO['params']['fourfold1'][0])}|{'{:5d}'.format(O00OO00O0OO0O00OO['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(O00OO00O0OO0O00OO['params']['fourfold2'][0])}|{'{:5d}'.format(O00OO00O0OO0O00OO['params']['fourfold2'][1])}|")#line:1882
                print (f"----|-----|-----|  ----|-----|-----|")#line:1883
                print (f"¬A  |{'{:5d}'.format(O00OO00O0OO0O00OO['params']['fourfold1'][2])}|{'{:5d}'.format(O00OO00O0OO0O00OO['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(O00OO00O0OO0O00OO['params']['fourfold2'][2])}|{'{:5d}'.format(O00OO00O0OO0O00OO['params']['fourfold2'][3])}|")#line:1884
                print (f"----|-----|-----|  ----|-----|-----|")#line:1885
            else :#line:1886
                print ("Unsupported task type for rule details")#line:1887
            print ("")#line:1891
        else :#line:1892
            print ("No such rule.")#line:1893
    def get_rulecount (O0O00O00OOOO00000 ):#line:1895
        if not (O0O00O00OOOO00000 ._is_calculated ()):#line:1896
            print ("ERROR: Task has not been calculated.")#line:1897
            return #line:1898
        return len (O0O00O00OOOO00000 .result ["rules"])#line:1899
    def get_ruletext (O00O00O000O0O0O0O ,OOOO0O00OOOO00OO0 ):#line:1901
        ""#line:1907
        if not (O00O00O000O0O0O0O ._is_calculated ()):#line:1908
            print ("ERROR: Task has not been calculated.")#line:1909
            return #line:1910
        if OOOO0O00OOOO00OO0 <=0 or OOOO0O00OOOO00OO0 >O00O00O000O0O0O0O .get_rulecount ():#line:1911
            if O00O00O000O0O0O0O .get_rulecount ()==0 :#line:1912
                print ("No such rule. There are no rules in result.")#line:1913
            else :#line:1914
                print (f"No such rule ({OOOO0O00OOOO00OO0}). Available rules are 1 to {O00O00O000O0O0O0O.get_rulecount()}")#line:1915
            return None #line:1916
        OO0O00OOOO0OO0OO0 =""#line:1917
        OO0OO0O000OO0OO00 =O00O00O000O0O0O0O .result ["rules"][OOOO0O00OOOO00OO0 -1 ]#line:1918
        if O00O00O000O0O0O0O .result ['taskinfo']['task_type']=="4ftMiner":#line:1919
            OO0O00OOOO0OO0OO0 =OO0O00OOOO0OO0OO0 +" "+OO0OO0O000OO0OO00 ["cedents_str"]["ante"]+" => "+OO0OO0O000OO0OO00 ["cedents_str"]["succ"]+" | "+OO0OO0O000OO0OO00 ["cedents_str"]["cond"]#line:1921
        elif O00O00O000O0O0O0O .result ['taskinfo']['task_type']=="UICMiner":#line:1922
            OO0O00OOOO0OO0OO0 =OO0O00OOOO0OO0OO0 +"     "+OO0OO0O000OO0OO00 ["cedents_str"]["ante"]+" => "+O00O00O000O0O0O0O .result ['taskinfo']['target']+"(*) | "+OO0OO0O000OO0OO00 ["cedents_str"]["cond"]#line:1924
        elif O00O00O000O0O0O0O .result ['taskinfo']['task_type']=="CFMiner":#line:1925
            OO0O00OOOO0OO0OO0 =OO0O00OOOO0OO0OO0 +" "+OO0OO0O000OO0OO00 ["cedents_str"]["cond"]#line:1926
        elif O00O00O000O0O0O0O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1927
            OO0O00OOOO0OO0OO0 =OO0O00OOOO0OO0OO0 +"  "+OO0OO0O000OO0OO00 ["cedents_str"]["ante"]+" => "+OO0OO0O000OO0OO00 ["cedents_str"]["succ"]+" | "+OO0OO0O000OO0OO00 ["cedents_str"]["cond"]+" : "+OO0OO0O000OO0OO00 ["cedents_str"]["frst"]+" x "+OO0OO0O000OO0OO00 ["cedents_str"]["scnd"]#line:1929
        return OO0O00OOOO0OO0OO0 #line:1930
    def get_fourfold (O0OOOO000000000O0 ,OO0O0OO0O0O0O0OOO ,order =0 ):#line:1932
        if not (O0OOOO000000000O0 ._is_calculated ()):#line:1933
            print ("ERROR: Task has not been calculated.")#line:1934
            return #line:1935
        if (OO0O0OO0O0O0O0OOO <=len (O0OOOO000000000O0 .result ["rules"])):#line:1936
            if O0OOOO000000000O0 .result ['taskinfo']['task_type']=="4ftMiner":#line:1937
                O00OOO0OO0OOO0O00 =O0OOOO000000000O0 .result ["rules"][OO0O0OO0O0O0O0OOO -1 ]#line:1938
                return O00OOO0OO0OOO0O00 ['params']['fourfold']#line:1939
            elif O0OOOO000000000O0 .result ['taskinfo']['task_type']=="CFMiner":#line:1940
                print ("Error: fourfold for CFMiner is not defined")#line:1941
                return None #line:1942
            elif O0OOOO000000000O0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1943
                O00OOO0OO0OOO0O00 =O0OOOO000000000O0 .result ["rules"][OO0O0OO0O0O0O0OOO -1 ]#line:1944
                if order ==1 :#line:1945
                    return O00OOO0OO0OOO0O00 ['params']['fourfold1']#line:1946
                if order ==2 :#line:1947
                    return O00OOO0OO0OOO0O00 ['params']['fourfold2']#line:1948
                print ("Error: for SD4ft-Miner, you need to provide order of fourfold table in order= parameter (valid values are 1,2).")#line:1949
                return None #line:1950
            else :#line:1951
                print ("Unsupported task type for rule details")#line:1952
        else :#line:1953
            print ("No such rule.")#line:1954
    def get_hist (O000O0O0O0O0O0OO0 ,O0000O0O00O0O0000 ):#line:1956
        if not (O000O0O0O0O0O0OO0 ._is_calculated ()):#line:1957
            print ("ERROR: Task has not been calculated.")#line:1958
            return #line:1959
        if (O0000O0O00O0O0000 <=len (O000O0O0O0O0O0OO0 .result ["rules"])):#line:1960
            if O000O0O0O0O0O0OO0 .result ['taskinfo']['task_type']=="CFMiner":#line:1961
                O00OO0OOOOOO00O00 =O000O0O0O0O0O0OO0 .result ["rules"][O0000O0O00O0O0000 -1 ]#line:1962
                return O00OO0OOOOOO00O00 ['params']['hist']#line:1963
            elif O000O0O0O0O0O0OO0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1964
                print ("Error: SD4ft-Miner has no histogram")#line:1965
                return None #line:1966
            elif O000O0O0O0O0O0OO0 .result ['taskinfo']['task_type']=="4ftMiner":#line:1967
                print ("Error: 4ft-Miner has no histogram")#line:1968
                return None #line:1969
            else :#line:1970
                print ("Unsupported task type for rule details")#line:1971
        else :#line:1972
            print ("No such rule.")#line:1973
    def get_hist_cond (O00000O00OOOO0O00 ,O0OO0OO00O0OO0000 ):#line:1976
        if not (O00000O00OOOO0O00 ._is_calculated ()):#line:1977
            print ("ERROR: Task has not been calculated.")#line:1978
            return #line:1979
        if (O0OO0OO00O0OO0000 <=len (O00000O00OOOO0O00 .result ["rules"])):#line:1980
            if O00000O00OOOO0O00 .result ['taskinfo']['task_type']=="UICMiner":#line:1981
                OOO0O0O0O0000OOOO =O00000O00OOOO0O00 .result ["rules"][O0OO0OO00O0OO0000 -1 ]#line:1982
                return OOO0O0O0O0000OOOO ['params']['hist_cond']#line:1983
            elif O00000O00OOOO0O00 .result ['taskinfo']['task_type']=="CFMiner":#line:1984
                OOO0O0O0O0000OOOO =O00000O00OOOO0O00 .result ["rules"][O0OO0OO00O0OO0000 -1 ]#line:1985
                return OOO0O0O0O0000OOOO ['params']['hist']#line:1986
            elif O00000O00OOOO0O00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1987
                print ("Error: SD4ft-Miner has no histogram")#line:1988
                return None #line:1989
            elif O00000O00OOOO0O00 .result ['taskinfo']['task_type']=="4ftMiner":#line:1990
                print ("Error: 4ft-Miner has no histogram")#line:1991
                return None #line:1992
            else :#line:1993
                print ("Unsupported task type for rule details")#line:1994
        else :#line:1995
            print ("No such rule.")#line:1996
    def get_quantifiers (OO0000OOO000OO0O0 ,OO0O0O0OOO0OOO0O0 ,order =0 ):#line:1998
        if not (OO0000OOO000OO0O0 ._is_calculated ()):#line:1999
            print ("ERROR: Task has not been calculated.")#line:2000
            return #line:2001
        if (OO0O0O0OOO0OOO0O0 <=len (OO0000OOO000OO0O0 .result ["rules"])):#line:2002
            OOOOO00O00O0OOO00 =OO0000OOO000OO0O0 .result ["rules"][OO0O0O0OOO0OOO0O0 -1 ]#line:2003
            if OO0000OOO000OO0O0 .result ['taskinfo']['task_type']=="4ftMiner":#line:2004
                return OOOOO00O00O0OOO00 ['params']#line:2005
            elif OO0000OOO000OO0O0 .result ['taskinfo']['task_type']=="CFMiner":#line:2006
                return OOOOO00O00O0OOO00 ['params']#line:2007
            elif OO0000OOO000OO0O0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:2008
                return OOOOO00O00O0OOO00 ['params']#line:2009
            else :#line:2010
                print ("Unsupported task type for rule details")#line:2011
        else :#line:2012
            print ("No such rule.")#line:2013
    def get_varlist (O00OOO0OOOOOO00O0 ):#line:2015
        return O00OOO0OOOOOO00O0 .result ["datalabels"]["varname"]#line:2016
    def get_category_names (OO00OO00OO00O00O0 ,varname =None ,varindex =None ):#line:2018
        OOO0O00OO0O00OOO0 =0 #line:2019
        if varindex is not None :#line:2020
            if OOO0O00OO0O00OOO0 >=0 &OOO0O00OO0O00OOO0 <len (OO00OO00OO00O00O0 .get_varlist ()):#line:2021
                OOO0O00OO0O00OOO0 =varindex #line:2022
            else :#line:2023
                print ("Error: no such variable.")#line:2024
                return #line:2025
        if (varname is not None ):#line:2026
            OO00O0O0000OOOOO0 =OO00OO00OO00O00O0 .get_varlist ()#line:2027
            OOO0O00OO0O00OOO0 =OO00O0O0000OOOOO0 .index (varname )#line:2028
            if OOO0O00OO0O00OOO0 ==-1 |OOO0O00OO0O00OOO0 <0 |OOO0O00OO0O00OOO0 >=len (OO00OO00OO00O00O0 .get_varlist ()):#line:2029
                print ("Error: no such variable.")#line:2030
                return #line:2031
        return OO00OO00OO00O00O0 .result ["datalabels"]["catnames"][OOO0O00OO0O00OOO0 ]#line:2032
    def print_data_definition (OOO0OOO0O0OO0OO0O ):#line:2034
        OO00O00OOOOO00O0O =OOO0OOO0O0OO0OO0O .get_varlist ()#line:2035
        for O0O0O0OO0OO0OO000 in OO00O00OOOOO00O0O :#line:2036
            OOO0O0OOOO000O00O =OOO0OOO0O0OO0OO0O .get_category_names (O0O0O0OO0OO0OO000 )#line:2037
            O0OOO00OO00O00OO0 =""#line:2038
            for O0OO0000000OOO0OO in OOO0O0OOOO000O00O :#line:2039
                O0OOO00OO00O00OO0 =O0OOO00OO00O00OO0 +str (O0OO0000000OOO0OO )+" "#line:2040
            O0OOO00OO00O00OO0 =O0OOO00OO00O00OO0 [:-1 ]#line:2041
            print (f"Variable {O0O0O0OO0OO0OO000} has {len(OOO0O0OOOO000O00O)} categories: {O0OOO00OO00O00OO0}")#line:2042
    def _is_calculated (O0OOOOOO0OO00OO0O ):#line:2044
        ""#line:2049
        OO000OOO000OOOO00 =False #line:2050
        if 'taskinfo'in O0OOOOOO0OO00OO0O .result :#line:2051
            OO000OOO000OOOO00 =True #line:2052
        return OO000OOO000OOOO00 