from pyjarowinkler import distance
import soundex


def get_best_soundex_match(context, chunk):
  
    matches = [(name, distance.get_jaro_distance(name, " ".join(chunk))) for name in context]
    return min(matches, key = lambda x: x[1])
        
def get_best_jaro_match(context, chunk):
  
    instance = soundex.Soundex()
    matches = [(name, instance.compare(name, " ".join(chunk))) for name in context]
    return min(matches, key = lambda x: x[1])

def get_name_chunks(sentence):

    words = sentence.split()    
    name_chunks = []    
    chunk = []    
    
    for word in words:
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

    return name_chunks
  
  
def get_sentence_correction(context, sentence):
    
    name_chunks = get_name_chunks(sentence)
    
    print name_chunks
    
    for chunk in name_chunks:
        print chunk
        print get_best_soundex_match(context, chunk)
        print get_best_jaro_match(context, chunk)
    
    


def get_corrections(context, sentences):
    
    for sentence in sentences:
      
        get_sentence_correction(context, sentence)



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