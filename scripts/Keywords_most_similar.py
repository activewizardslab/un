
# coding: utf-8

# In[1]:

from gensim.models import Word2Vec
import logging
import os.path
import sys
import multiprocessing
 
from gensim.corpora import  WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence


# In[ ]:

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
 
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))
 
    # check and process input arguments
 
    if len(sys.argv) < 3:
        print globals()['__doc__'] % locals()
        sys.exit(1)
    inp, outp = sys.argv[1:3]
 
    model = Word2Vec(LineSentence(inp), size=400, window=5, min_count=5, workers=multiprocessing.cpu_count())
 
    # trim unneeded model memory = use (much) less RAM
    model.init_sims(replace=True)
 
    model.save(outp)
    
    
    SDG1 = model.most_similar(positive=['poverty'], topn=50)
    SDG2 = model.most_similar(positive=['hunger'], topn=50)
    SDG3 = model.most_similar(positive=['health', 'wells'], topn=50)
    SDG4 = model.most_similar(positive=['education'], topn=50)
    SDG5 = model.most_similar(positive=['gender', 'equality'], topn=50)
    SDG6 = model.most_similar(positive=['water', 'clean', 'sanitation'], topn=50)
    SDG7 = model.most_similar(positive=['affordable', 'clean', 'energy'], topn=50)
    SDG8 = model.most_similar(positive=['work', 'economic', 'growth'], topn=50)
    SDG9 = model.most_similar(positive=['industry', 'innovation', 'infrastructure'], topn=50)
    SDG10 = model.most_similar(positive=['reduced', 'inequalities'], topn=50)
    SDG11 = model.most_similar(positive=['cities', 'communities'], topn=50)
    SDG12 = model.most_similar(positive=['consumption', 'responsible', 'production'], topn=50)
    SDG13 = model.most_similar(positive=['climate'], topn=50)
    SDG14 = model.most_similar(positive=['life',  'below', 'water'], topn=50)
    SDG15 = model.most_similar(positive=['life', 'on', 'land'], topn=50)
    SDG16 = model.most_similar(positive=['piece', 'justice', 'institutions'], topn=50)
    SDG17 = model.most_similar(positive=['partnership',  'goals'], topn=50)
    
    
    categories_full = ['no poverty', 'zero hunger', 'good health and well beeing', 'quality education', 
                   'gender equality', 'clean water and sanitation', 'affordable and clean energy', 'decent work and economic growth',
                  'industry, innowation and infrastructure', 'reduced inequalities', 'sustainable sities and communities',
                  'responsible consumption and production', 'climate action', 'life below water', 'life on land', 
                  'piece, justice and strong institutions', 'partnership for the goals']

    
    k = [SDG1, SDG2, SDG3, SDG4, SDG5, SDG6, SDG7, SDG8, SDG9, SDG10, SDG11, SDG12, SDG13, SDG14, SDG15, SDG16, SDG17]
    
    
    keywords = dict()
    for i in xrange(len(categories_full)):
        keywords[categories_full[i]] = [l[0] for l in k[i]]
        
        
    df = pd.DataFrame.from_dict(keywords)
    df.to_csv('keywords.csv', index = False, encoding = 'utf-8')


# In[ ]:



