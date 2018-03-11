from pyjarowinkler import distance
import soundex


def get_best_jaro_match(context, chunk):
  
    matches = [(name, distance.get_jaro_distance(name, " ".join(chunk))) for name in context]
    res = max(matches, key = lambda x: x[1])
    return res[0], res[1]
        
def get_best_soundex_match(context, chunk):
  
    instance = soundex.Soundex()
    matches = [(name, instance.compare(name, " ".join(chunk))) for name in context]
    res = min(matches, key = lambda x: x[1])
    return res[0], 1 - (float(res[1]) / len(res[0]))
  
  
def get_subchunk(chunk):
  
    subchunk = []
  
    for i in range(0, len(chunk)):
        for j in range(0, len(chunk) - i + 1):
	    subchunk.append(chunk[j : j + i])
    return subchunk
  
 
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
        name_chunks.append
        
    name_chunks.extend(get_subchunks(name_chunks))

    return [x for x in name_chunks if x]

  
def pick_best_match(context, chunk):
  
    soundex_res = get_best_soundex_match(context, chunk)
    jaro_res = get_best_jaro_match(context, chunk)
    
    if max(soundex_res[1], jaro_res[1]) < 0.9:
        return chunk
    
    return max(soundex_res, jaro_res, key = lambda x: x[1])[0]
        
  
def get_sentence_correction(context, sentence):
    
    name_chunks = get_name_chunks(sentence)
    corrections = []    
    split_names = []
    
    for name in context:
        split_names.extend(name.split())
        
    context.extend(split_names)
    
    for chunk in name_chunks:
        corrections.append(pick_best_match(context, chunk))
        
    return name_chunks, corrections
    
    


def get_corrections(context, sentences):
  
    corrections = []
    
    for sentence in sentences:
      
        names, corrections = get_sentence_correction(context, sentence)
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