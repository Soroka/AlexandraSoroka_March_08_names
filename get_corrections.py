from pyjarowinkler import distance
import soundex


def get_best_jaro_match(context, chunk):
  
    matches = [(name, distance.get_jaro_distance(name, " ".join(chunk))) for name in context]
    res = max(matches, key = lambda x: x[1])
    return res[0], res[1]
        
def get_best_soundex_match(context, chunk, instance):
  
    matches = [(name, instance.compare(name, " ".join(chunk))) for name in context]
    res = min(matches, key = lambda x: x[1])
    return res[0], 1 - (float(res[1]) / len(res[0]))
  
  
def get_subchunk(chunk):
  
    subchunk = []
  
    for i in range(0, len(chunk)):
        for j in range(0, len(chunk) - i + 1):
	    subchunk.append(chunk[j : j + i])
    return [x for x in subchunk if x]
  
 
def get_subchunks(chunks):
  
    subchunks = []
    
    for chunk in chunks:
        if len(chunk) > 1:
	   subchunks.extend(get_subchunk(chunk))
	   
    return subchunks
  

def get_name_chunks(sentence):

    words = sentence.split()    
    name_chunks = []    
    chunk = []    
    
    for word in words:
      
        if len(word) < 2:
	  continue
	
        if word[0].isupper() and len(chunk) < 2:
	    chunk.append(word)
	else:
	    if chunk:
	        name_chunks.append(chunk)
	        chunk = []
	        
	    if word[0].isupper():
	        chunk.append(word)
    
    if chunk:
        name_chunks.append(chunk)
        
    return [x for x in name_chunks if x]
  
def compose(reslist):  
    avg_res_score = sum([x[1] for x in reslist]) / len(reslist)
    res = " ".join([x[0] for x in reslist])
    return avg_res_score, res

  
def pick_best_match(context, split_context, chunk, soundex_instance):
  

    subchunks = get_subchunk(chunk)
    
    if subchunks:
    
        subchunk_soundex_res = [get_best_soundex_match(split_context, subchunk, soundex_instance) for subchunk in subchunks]
        subchunk_jaro_res = [get_best_jaro_match(split_context, subchunk, soundex_instance) for subchunk in subchunks]

    else:
        subchunk_soundex_res = []
        subchunk_jaro_res = []
        
    avg_subchunk_soundex_res = compose(subchunk_soundex_res)
    avg_subchunk_jaro_res = compose(subchunk_jaro_res)

    soundex_res = get_best_soundex_match(context, chunk, soundex_instance)
    jaro_res = get_best_jaro_match(context, chunk)
    
    if max(soundex_res[1], jaro_res[1], avg_subchunk_soundex_res, avg_subchunk_jaro_res) < 0.9:
        return " ".join(chunk)
    
    return max(soundex_res, jaro_res, avg_subchunk_soundex_res, avg_subchunk_jaro_res, key = lambda x: x[1])[0]
        
  
def get_sentence_correction(context, sentence, soundex_instance):
    
    name_chunks = get_name_chunks(sentence)
    corrections = []    
    split_names = []
    
    context.extend(split_names)
    
    for chunk in name_chunks:
        corrections.append(pick_best_match(context, split_names, chunk, soundex_instance))
        
    return name_chunks, corrections
    
    


def get_corrections(context, sentences):
  
    corrections = []
    soundex_instance = soundex.Soundex()
    
    for sentence in sentences:
      
        names, corrections = get_sentence_correction(context, sentence, soundex_instance)
        print names
        print corrections
        corrections.append((names, corrections))
        
    return corrections
        
        
# TODO: sliding similarity with context - if a word was misclassified with NER



sentences = [ 'tomorrow I have a meeting with Tim Hanks Tom Crus and Eastwud',
              'Michael likes movies with Jon Way and Client East',
              'Jonn invited me Jon Ham and Jon Wane, over for a lunch']


context = ['John Wayne',
           'Tom Hanks',
           'Tom Cruise',
           'Clint Eastwood',
           'Jon Hamm',
           'John Nolan',
           'William',
           'Fitcher'
           ]

get_corrections(context, sentences)