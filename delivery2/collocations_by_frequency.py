from nltk.util import ngrams
from nltk import word_tokenize
from nltk.corpus import stopwords 
from nltk.tag import pos_tag
from collections import Counter
from zemberek import TurkishMorphology

class CollocationsByFrequency():

    def __init__(self):
        self.pos_tagger = TurkishMorphology.create_with_defaults()

    def get_pos_tags(self, word):
        
        r_tags = []
        tags = self.pos_tagger.analyze(word.strip())
        tags_str = str(tags)
        
        if ":Adj" in tags_str:
            r_tags.append("A")
        
        if ":Noun" in tags_str:
            r_tags.append("N")


        if len(r_tags) > 0:
            return r_tags[0]
        return ''


    def tag_collocations(self, bigrams_with_freqs):
        
        ''' part of speech tagging for all the collocations passed'''
        
        freq_collocation_tag = []
        for collocation in bigrams_with_freqs:
            frequency_of_collocation = bigrams_with_freqs[collocation]
            tag_of_collocation = self.get_pos_tags(collocation[0])+ self.get_pos_tags(collocation[1])
            freq_collocation_tag_tuple = frequency_of_collocation, collocation, tag_of_collocation
            freq_collocation_tag.append(freq_collocation_tag_tuple)
            
        return freq_collocation_tag


    def pos_filter(self, tagged_collocations, filter_tags_list):
        
        ''' Takes a set of tuples  containing the tags to be filtered and returns
            filtered version of the collocations
        '''
        filtered_collocations = []
        for collocation in tagged_collocations:
            tag = collocation[2] 
            if tag in filter_tags_list:
                filtered_collocations.append(collocation)
        return filtered_collocations
    
    def get_collocations(self, bigrams_with_freqs):
        
        """Returns bigrams(collocations) list given a donem_text """
        tagged_collocations = self.tag_collocations(bigrams_with_freqs)
        pos_filter_list = set(['AN', 'NN'])
        filtered_collocations = self.pos_filter(tagged_collocations, pos_filter_list)
        return filtered_collocations