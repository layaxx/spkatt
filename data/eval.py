import json  
import sys 
 
#################################################
# Evaluate results for speaker attribution:     #
# Usage: python eval.py <gold file> <pred file> #
#################################################


def read_json(infile):
   with open(infile) as jfile:
      dic = json.load(jfile)
   return dic   

   

def read_jsonl(infile):
   data = []
   with open(infile, "r") as inf:
      for line in inf:
         data.append(json.loads(line))
   return data



def list2dic(pred_list):
   dic = {}
   for item in pred_list:
      dic[item["sentence_id"]] = item["annotations"]
   return dic


def get_pred_labels(annot):
   dic = {}
   role_labels = ['Source', 'Message', 'Addr', 'Topic', 'Medium',  'Evidence', 'PTC', 'V']
   for file in annot:
      for id in annot[file]:
         dic[file + "_" + id] = {"predicate": annot[file][id]["predicate"]}
         dic[file + "_" + id]['cues'] = []
         for role in role_labels: 
            dic[file + "_" + id][role] = []
            if role == 'V':
               for idx in range(len(annot[file][id]["roles"])):
                  if annot[file][id]["roles"][idx] == "B-V":
                     dic[file + "_" + id]['cues'].append(idx)
                  elif annot[file][id]["roles"][idx].endswith("-" + role):
                     if role not in dic[file + "_" + id]:
                        dic[file + "_" + id][role] = []
                     dic[file + "_" + id][role].append(idx)
            else:    
               for idx in range(len(annot[file][id]["roles"])): 
                  if annot[file][id]["roles"][idx].endswith("-" + role): 
                     dic[file + "_" + id][role].append(idx)
   return dic




def get_labels(annot):
   dic = {}
   role_labels = ['Source', 'Message', 'Addr', 'Topic', 'Medium',  'Evidence', 'PTC', 'V']
   for file in annot:
      for id in annot[file]["annotations"]:
         dic[file + "_" + id] = {"predicate": annot[file]["annotations"][id]["predicate"]}
         dic[file + "_" + id]['cues'] = []

         for role in role_labels:
            dic[file + "_" + id][role] = []
            if role == 'V':
               for idx in range(len(annot[file]["annotations"][id]["roles"])):
                  if annot[file]["annotations"][id]["roles"][idx] == "B-V":
                     dic[file + "_" + id]['cues'].append(idx)
                  elif annot[file]["annotations"][id]["roles"][idx] == "I-V":
                     if role not in dic[file+ "_" + id]:
                        dic[file + "_" + id][role] = []
                     dic[file + "_" + id][role].append(idx)

            else:
               for idx in range(len(annot[file]["annotations"][id]["roles"])):
                  if annot[file]["annotations"][id]["roles"][idx].endswith("-" + role):
                     dic[file + "_" + id][role].append(idx) 

   return dic


def get_predicate(pred_string):
   if pred_string.startswith('SE'):
      return 'SE'
   return pred_string


# compute precision, recall and f1 
def prec_rec_f1(dic):
   prec, rec, f1 = 0, 0, 0
   if (dic['tp'] + dic['fp']) > 0:
      prec = dic['tp'] / (dic['tp'] + dic['fp'])
   if (dic['tp'] + dic['fn']):
      rec  = dic['tp'] / (dic['tp'] + dic['fn'])
   if (prec + rec) > 0:
      f1   = 2 * prec * rec / (prec + rec)
   return prec, rec, f1
   

      
def eval_dics_strict(gold, pred):
   role_labels = ['Source', 'Message', 'Addr', 'Topic', 'Medium',  'Evidence', 'PTC', 'V']
   gdic = get_labels(gold)
   pdic = get_pred_labels(pred)

   cue_dic = { 'trigger': {'tp':0, 'fp':0, 'fn':0},
               'preds':{'correct':0, 'false':0}} 
   all_roles_strict = {'tp':0, 'fp':0, 'fn':0}
   each_role_strict = {r:{'tp':0, 'fp':0, 'fn':0} for r in role_labels} 
   
   for fname in gdic:
      # sanity check: all instances should have a predicted label
      if fname not in gdic:
         print("Error: missing file", fname)

      # eval cues
      gpred = get_predicate(gdic[fname]['predicate'])
      ppred = get_predicate(pdic[fname]['predicate'])

      # eval predicate labels 
      if gpred == ppred:
         cue_dic['preds']['correct'] += 1
      else:
         cue_dic['preds']['false'] += 1

      # eval B-V (we use B-V for role evaluation)
      if gdic[fname]['cues'] == pdic[fname]['cues']: 
         cue_dic['trigger']['tp'] += 1
      
         # strict 
         for role in role_labels:
            groles = gdic[fname][role]
            proles = pdic[fname][role]
            
            if groles == proles:
               # skip empty roles
               if groles == []:
                  continue
               all_roles_strict['tp'] += 1
               each_role_strict[role]['tp'] += 1

            # fp, fn
            else:
               all_roles_strict['fp'] += 1 
               each_role_strict[role]['fp'] += 1
               if groles != []:
                  all_roles_strict['fn'] += 1 
                  each_role_strict[role]['fn'] += 1
  
      else: 
         if gdic[fname]['cues'] == 'B-V':
            cue_dic['trigger']['fn'] += 1
         else:
            cue_dic['trigger']['fp'] += 1

         # wrong SE => count all roles in gold as fn
         # and all predicted role as fp 
         # (even if they match the gold roles)
         for role in role_labels: 
            groles = gdic[fname][role]
            proles = pdic[fname][role] 

            # fn
            if gdic[fname][role] != []:
               all_roles_strict['fn'] += 1 
               each_role_strict[role]['fn'] += 1 

            # fp
            if pdic[fname][role] != []:
               all_roles_strict['fp'] += 1 
               each_role_strict[role]['fp'] += 1 

   print()
   print("STRICT CUES\t", cue_dic)
   print("STRICT ROLES\t", all_roles_strict) 
   print()

   print()
   cue_prec = cue_dic['trigger']['tp'] / (cue_dic['trigger']['tp']+cue_dic['trigger']['fp'])
   cue_rec  = cue_dic['trigger']['tp'] / (cue_dic['trigger']['tp']+cue_dic['trigger']['fn'])
   cue_f1   = 2 * cue_prec * cue_rec / (cue_prec + cue_rec)
   print("CUES (prec/rec/f1):\t", cue_prec, "\t", cue_rec, "\t", cue_f1)
   
   print()
   print("ROLES (all, strict):")
   role_prec = all_roles_strict['tp'] / (all_roles_strict['tp']+all_roles_strict['fp'])
   role_rec  = all_roles_strict['tp'] / (all_roles_strict['tp']+all_roles_strict['fn'])
   role_f1   = 2 * role_prec * role_rec / (role_prec + role_rec)
   print("All roles:\t", role_prec, "\t", role_rec, "\t", role_f1)
   
   print()
   print("ROLES (each, strict):")
   for role in role_labels: 
      prec, rec, f1 = prec_rec_f1(each_role_strict[role])
      print(role, "\t", prec,"\t",  rec,"\t",  f1) 




def eval_dics_overlap(gold, pred):
   role_labels = ['Source', 'Message', 'Addr', 'Topic', 'Medium',  'Evidence', 'PTC', 'V']
   gdic = get_labels(gold)
   pdic = get_pred_labels(pred)
   cue_dic = { 'trigger': {'tp':0, 'fp':0, 'fn':0},
               'preds':{'correct':0, 'false':0}} 
   all_roles_overlap = {'tp':0, 'fp':0, 'fn':0}
   each_role_overlap = {r:{'tp':0, 'fp':0, 'fn':0} for r in role_labels} 
   
   for fname in gdic: 
      # sanity check: all instances should have a predicted label
      if fname not in gdic:
         print("Error: missing file", fname)

      # Evaluate the subjective expressions 
      gpred = get_predicate(gdic[fname]['predicate'])
      ppred = get_predicate(pdic[fname]['predicate'])

      # eval predicate labels 
      if gpred == ppred:
         cue_dic['preds']['correct'] += 1
      else:
         cue_dic['preds']['false'] += 1

      # Evaluate B-V (we use B-V for role evaluation:
      # not the predicate but the V in the role list
      # has to be set correctly to consider a token as a SE
      # and its corresponding roles as correct).
      if gdic[fname]['cues'] == pdic[fname]['cues']: 
         cue_dic['trigger']['tp'] += 1
      
         # Here we count token overlap for role eval. 
         for role in role_labels:
            groles = gdic[fname][role]
            proles = pdic[fname][role]
      
            for g in groles:
               if g in proles:
                  all_roles_overlap['tp'] += 1
                  each_role_overlap[role]['tp'] += 1
               # fn
               else:
                  all_roles_overlap['fn'] += 1 
                  each_role_overlap[role]['fn'] += 1

            # fp
            for p in proles:
               if p not in groles:
                  all_roles_overlap['fp'] += 1 
                  each_role_overlap[role]['fp'] += 1
  
      # SE has not been predicted correctly (position of V in roles set)
      else: 
         if gdic[fname]['cues'] == 'B-V':
            cue_dic['trigger']['fn'] += 1
         else:
            cue_dic['trigger']['fp'] += 1
 
         for role in role_labels: 
            # get the gold/pred token positions for this role 
            groles = gdic[fname][role]
            proles = pdic[fname][role]
         
            # we count all gold roles as fn 
            for g in groles:
               # fn
               all_roles_overlap['fn'] += 1 
               each_role_overlap[role]['fn'] += 1

            # we count all predicted roles as fp
            for p in proles:
               # fp
               all_roles_overlap['fp'] += 1 
               each_role_overlap[role]['fp'] += 1

   print()
   print()
   print("OVERLAP CUES\t", cue_dic)
   print("OVERLAP ROLES\t", all_roles_overlap) 
   print()

   cue_prec = cue_dic['trigger']['tp'] / (cue_dic['trigger']['tp']+cue_dic['trigger']['fp'])
   cue_rec  = cue_dic['trigger']['tp'] / (cue_dic['trigger']['tp']+cue_dic['trigger']['fn'])
   cue_f1   = 2 * cue_prec * cue_rec / (cue_prec + cue_rec)
   print("CUES:(prec/rec/f1)\t", cue_prec, "\t", cue_rec, "\t", cue_f1)
   
   print()
   print("ROLES (all, overlap):")
   role_prec = all_roles_overlap['tp'] / (all_roles_overlap['tp']+all_roles_overlap['fp'])
   role_rec  = all_roles_overlap['tp'] / (all_roles_overlap['tp']+all_roles_overlap['fn'])
   role_f1   = 2 * role_prec * role_rec / (role_prec + role_rec)
   print("All roles:\t", role_prec, "\t", role_rec, "\t", role_f1)
   
   print()
   print("ROLES (each, overlap):")
   for role in role_labels:
      prec, rec, f1 = prec_rec_f1(each_role_overlap[role])
      print(role, "\t", prec,"\t",  rec,"\t",  f1) 

   return      



#########################################
# read in gold and system output files
# and print results for strict evaluation
# and for token overlap

goldfile = sys.argv[1]
predfile = sys.argv[2]

print("reading gold input:", goldfile)
gold_dic  = read_json(goldfile)
 
print("reading system output:", predfile)
pred_list = read_jsonl(predfile)
pred_dic = list2dic(pred_list) 

eval_dics_strict(gold_dic, pred_dic)
print()
eval_dics_overlap(gold_dic, pred_dic) 

