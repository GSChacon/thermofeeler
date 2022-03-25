# 1  Data-Pre-processing

# 1.1  Import Libraries
import warnings  # for life! code to avoid warnings
import unidecode  # 1.7
import pandas as pd  # for life!
import re  # 1.5 - 1.4
import string  # Common string operations
import nltk  # 1.14
nltk.download('stopwords')
from nltk.tokenize import word_tokenize  # 1.12 - 1.19
from nltk.corpus import stopwords  # 1.12
from nltk.stem import WordNetLemmatizer # 1.14
from nltk.stem import RSLPStemmer # 1.14
nltk.download('rslp')
from autocorrect import Speller # 1.13
from bs4 import BeautifulSoup  # 1.4
import stanza  # 1.15
stanza.download('pt')  # 1.15
# import time
#from nltk.stem.api import StemmerI


# 1.4  Remove newlines & tabs
def remove_newlines_tabs(tweet):
    """
    This function will remove all the occurrences of newlines, tabs, and combinations like: \\n, \\.

    arguments:
        input_tweet: "text" of type "String".

    return:
        value: "text" after removal of newlines, tabs, \\n, \\ characters.

    Example:
    Input : This is her \\ first day at this place.\n Please,\t Be nice to her.\\n
    Output : This is her first day at this place. Please, Be nice to her.

    """
    # Replacing all the occurrences of \n,\\n,\t,\\ with a space.
    Formatted_tweet = tweet.replace('\\n', ' ').replace('\n', ' ').replace('\t',' ').replace('\\', ' ').replace('. com', '.com')
    return Formatted_tweet

# 1.5  Strip Html Tags
# DESACTIVATE
# remove_html=False
def strip_html_tags(tweet):  # '< >' for scraping
    """
    This function will remove all the occurrences of html tags from the text.

    arguments:
        input_tweet: "text" of type "String".

    return:
        value: "text" after removal of html tags.

    Example:
    Input : This is a nice place to live. <IMG>
    Output : This is a nice place to live.

    """
    # Initiating BeautifulSoup object soup.
    soup = BeautifulSoup(tweet, "html.parser")
    # Get all the text other than html tags.
    stripped_tweet = soup.get_text(separator=" ")
    return stripped_tweet

# 1.6  Remove Links
def remove_links(tweet):
    """
    This function will remove all the occurrences of links.

    arguments:
        input_tweet: "text" of type "String".

    return:
        value: "text" after removal of all types of links.

    Example:
    Input : To know more about cats and food & website: catster.com  visit: https://catster.com//how-to-feed-cats
    Output : To know more about cats and food & website: visit:

    """
    # Removing all the occurrences of links that starts with https
    remove_https = re.sub(r'http\S+', '', tweet)  # r'\1' --> Limits all the repeatation to only one character.

    # Remove all the occurrences of text that ends with .com
    remove_com = re.sub(r"\ [A-Za-z]*\.com", ' ', remove_https)
    return remove_com

# 1.7  Remove WhiteSpaces
def remove_whitespaces(tweet):
    """
    This function will remove
    extra white spaces from the text

    arguments:
        input_tweet: "text" of type "String".

    return:
        value: "text" after extra whitespaces removed .

    Example:
    Input : How   are   you   doing     ?
    Output : How are you doing ?

    """
    pattern = re.compile(r'\s+')  # r'\1' --> Limits all the repeatation to only one character.
    Without_whitespace = re.sub(pattern, ' ', tweet)
    # There are some instances where there is no space after '?' & ')',
    # So I am replacing these with one space so that It will not consider two words as one token.
    tweet = Without_whitespace.replace('?', ' ? ').replace(')', ') ')
    return tweet

# 1.8  Remove numbers
def remove_number(tweet):
    """
    This function will remove
    all numbers from the text

    arguments:
        input_tweet: "text" of type "String" with fell numbers.

    return:
        value: "text" after removal of all numbers.

    Example:
    Input : Hello my id. is 76483927 and my phone number is 67384902
    Output : Hello my id. is   and my phone number is

    """
    tweet = re.sub(r'[0-9]+',' ',tweet)
    return tweet

# 1.9  Remove Accented Characters
# Code for accented characters removal
def accented_characters_removal(tweet):
    """
    The function will remove accented characters from the
    text contained within the Dataset.

    arguments:
        input_tweet: "text" of type "String".

    return:
        value: "text" with removed accented characters.

    Example:
    Input : Málaga, àéêöhello
    Output : Malaga, aeeohello

    """
    # Remove accented characters from text using unidecode.
    # Unidecode() - It takes unicode data & tries to represent it to ASCII characters.
    tweet = unidecode.unidecode(tweet)
    return tweet

# 1.10  Case Conversion
# Code for text lowercasing
def lower_casing_text(tweet):
    """
    The function will convert text into lower case.

    arguments:
         input_tweet: "text" of type "String".

    return:
         value: text in lowercase

    Example:
    Input : The World Is Full Of Surprises!
    Output : the world is full of surprises!

    """
    # Convert text to lower case
    # lower() - It converts all upperase letter of given string to lowercase.
    tweet = tweet.lower()
    return tweet

# 1.11  Reduce repeated characters
# Code for removing repeated characters and punctuations
def reducing_error_char_repeatation(tweet):
    """
    This Function will reduce repeatition to two characters
    for alphabets.

    arguments:
         input_tweet: "text" of type "String".

    return:
        value: Finally formatted text with alphabets repeating to
        two characters & punctuations limited to one repeatition

    Example:
    Input : Realllllllllyyyyy,        Greeeeaaaatttt   !!!!?....;;;;:)
    Output : Reallyy, Greeaatt !?.;:)

    """
    # Pattern matching for all case alphabets# Pattern matching for all case alphabets
    Pattern_alpha = re.compile(r"([A-Za-z])\1{1,}", re.DOTALL)
    # Limiting all the  repeatation to two characters.
    Formatted_tweet = Pattern_alpha.sub(r"\1\1", tweet)   # r'\1\1' --> It limits all the repeatation to two characters.
    return Formatted_tweet

# 1.12  Remove punctuations
def remove_punctuation(tweet):
    """
    The function will remove all punctuaction from the
    text contained within the Dataset.

    arguments:
        input_tweet: "text" of type "String".

    return:
        value: "text" with removed accented characters.

    Example:
    Input : good morning! buen dia,\.:|;!?`~+
    Output : good morning buen dia

    """
    tweet = re.sub(r'[^\w\s]',' ',tweet)  # remove punctuation
    return tweet

# 1.13  Expand contraction words
# Portuguese Word Mapping

# The code for expanding contraction words
def expand_contractions(tweet):  #, contraction_mapping =  CONTRACTION_MAP_PT):
    """
    expand shortened words to the actual form.
    e.g. don't  to  do not

    arguments:
         input_tweet: "text" of type "String".

    return:
         value: Text with expanded form of shorthened words.

    Example:
    Input : Vamos pra praia cmg qdo vc sair do trabalho, bjs e obg
    Output : Vamos para praia comigo quando voce sair do trabalho, bjs e obrigado

    """
    CONTRACTION_MAP_PT = {'é':'ser','eh':'ser','vc':'voce','vcs':'voces','tb': 'tambem','tbm': 'tambem',
            'obg': 'obrigado','obrigada':'obrigado','gnt': 'gente', 'q': 'que', 'n': 'nao',
            'cmg': 'comigo', 'p':'para','pra' :'para','ta': 'está','tá':'está','to': 'estou',
            'vdd':'verdade','bjos':'beijo','bjo':'beijo','kd': 'cade', 'pq':'porque',
            'cmg':'comigo','cm':'com','pc':'ca','aq':'aqui','qdo':'quando','p':'para','':'que','agr':'agora'}
# Tokenizing text into tokens.
    list_Of_tokens = tweet.split(' ')
    for word in list_Of_tokens:
        if word in CONTRACTION_MAP_PT.keys():
            word_value = CONTRACTION_MAP_PT[word]
            list_Of_tokens[list_Of_tokens.index(word)] = word_value

    # Converting list of tokens to String.
    String_Of_tokens = ' '.join(i for i in list_Of_tokens)
    return String_Of_tokens

# 1.14  Remove special characters
def removing_special_characters(tweet):
    """
    Removing all the special characters except the one that is passed within
    the regex to match, as they have important meaning in the text provided.
    Also remove all hashtags but keepimg the word after (#covid)

    arguments:
         input_tweet: "text" of type "String".

    return:
        value: Text with removed special characters that don't require.

    Example:
    Input : <IMG> K-a-j-a-l. #COVID #NBA Thi*s is $100.05 : @BRASIL @Barcelona recieve! (Is this okay?)
    Output :  Hello, Kajal. This is $100.05 : the payment that you will recieve! Is this okay?

    """
    # The formatted text after removing not necessary punctuations.
    Formatted_tweet = re.sub(r'@[A-Za-z0-9_]+','',tweet)  # remove @mentions  #[^a-zA-Z0-9:$-,%.?!]
    Formatted_tweet = re.sub(r'#',' ',Formatted_tweet)  # remove hashtags
    # In the above regex expression,I am providing necessary set of punctuations that are frequent in this particular dataset.
    return Formatted_tweet

# 1.15  Remove stopwords
# The code for removing stopwords
# How to print Stopwords
# stops = set(stopwords.words('portuguese'))
# print(stops)

# Create our custom stopword list to add
# Custom StopWords portuguese


def removing_stopwords(tweet):
    """
    This function will remove stopwords which doesn't add much meaning to a sentence
    & they can be remove safely without comprimising meaning of the sentence.

    arguments:
         input_tweet: "text" of type "String".

    return:
        value: Text after omitted all stopwords.

    Example:
    Input : hoje estou Barcelona está todos estamos voces estão agente ontem estive
    Output : hoje Barcelona todos voces agente ontem

    """
    our_stopwords=['a','ah','g','h', 'd','ca','te','tu','tua','tuas','um','uma','voce','voces','vos', 'la','lo','lá',
               'as','ao','aos','aquela','aquelas','aquele','aqueles','aquilo','as','ate','com','como','da','das',
               'de','dela','delas','dele','deles','depois','do','dos','e','ela','elas','ele','eles','em','entre',
               'essa','essas','esse','esses','eu','for','isso','isto','já','lhe','lhes','me','mesmo','meu','meus',
               'minha','minhas','muito','na','nas','no','nos','nossa','nossas','nosso','nossos','num','numa',
               'nós','oh','o','os','para','pela','pelas','pelo','pelos','por','qual','quando','que','quem',
               'se','sem','seu','seus','somos','sou','sua','suas','so','tambem', 'mas','ou', 'nem',
               'este','teu','teus','estes','estas','agora','ai','alem','algo','alguém','algum','ainda',
               'alguma','algumas','alguns', 'ali','ampla','amplas', 'amplo', 'amplos','ante', 'antes','apenas',
               'apoio','após','aqui','aquilo','assim','atrás','através','bastante','breve','cada', 'cedo', 'cento',
               'certamente','certeza','cima','coisa','coisas','da','dao','daquela', 'daquelas','daquele',
               'daqueles','dentro','contudo','debaixo','demais','depois','desde','dessa','dessas','desse','desses',
               'desta','destas','deste','destes','embora','enquanto','entre','etc','feita','feitas','feito',
               'feitos','for','fora','geral','grande','grandes','hoje', 'hora', 'horas', 'longe',
               'lugar', 'maior','maioria','mais','meio', 'menor', 'menos', 'mes', 'meses','mesma', 'mesmas',
               'mesmo', 'mesmos','muita', 'muitas','muito','muitos','naquela', 'naquelas', 'naquele', 'naqueles',
               'nessa', 'nessas', 'nesse', 'nesses', 'nesta', 'nestas', 'neste', 'nestes','num', 'numa','onde',
               'ontem','perto','parte','outra', 'outras', 'outro', 'outros', 'pois', 'porém', 'porque',
               'possivel', 'possivelmente','pouca', 'poucas', 'pouco', 'poucos', 'primeira', 'primeiras',
               'primeiro', 'primeiros','propria','proprias','proprio', 'proprios', 'proxima', 'proximas',
               'proximo', 'proximos','quais', 'quanto', 'quantos','quem','sempre','si', 'sido','sob', 'sobre',
               'tal', 'talvez','tampouco', 'tanta', 'tantas','tanto', 'tao', 'tarde', 'te', 'todo', 'todos',
               'toda', 'todas','tudo', 'ultima', 'ultimas', 'ultimo', 'ultimos','vários','vez', 'vezes',]
    tweet = ' '.join([word for word in tweet.split() if word not in our_stopwords])
    return tweet

# 1.16  Correct mis-spelled words in text
# FUNCIONA MUY BIEN EN INGLES ... COMBINANDO CON EL nltk.stem.WordNetLemmatizer()
# The code for spelling corrections
def spelling_correction(tweet):
    '''
    This function will correct spellings.

    arguments:
         input_tweet: "text" of type "String".

    return:
        value: Text after corrected spellings.

    Example:
    Input : voc e eu naum gostanos de brencar na rua sin salda
    Output : você e eu num gostamos de brincar na rua se saia

    '''
    # Check for spellings in Portuguese language
    spell = Speller(lang='pt')  # English = 'en'
    Corrected_tweet = spell(tweet)
    return Corrected_tweet

# 1.17  Lemmatization
# La lematización analiza el texto circundante para
# determinar la parte del discurso de una palabra dada, no clasifica las frases.

 # set the language for Portuguese (stanza)
# Stanza it is built with highly accurate neural network components that enable efficient
# training and evaluation with your own annotated data,

# The code for lemmatization
def lemmatization(tweet):
    """
    This function converts word to their root words
    without explicitely cut down as done in stemming.

    arguments:
        input_tweet: "text" of type "String".

    return:
        value: Text having root words only, no tense form, no plural forms

    Example:
    Input : brincando treino cantei jogarei subindo agredido
    Output : 'brincar treinar cantar jogar subir agredir '

    """
    nlp = stanza.Pipeline('pt')
    lemma = ""
    for sent in nlp(tweet).sentences:
        for word in sent.words:
            lemma += word.lemma + " "
    return lemma

# 1.18  Stemming
# DESACTIVATE - We are using just Lemmatization for the moment...
# stemmezation = False
# The code for stemmezation

def stemmezation(tweet):
    """
    This function essentially chops
    off letters from the end until the stem is reached
    it helps if the search returns variations of the word

    arguments:
         input_tweet: "text" of type "String".

    return:
        value: Text having root words only, no tense form, no plural forms

    Example:
    Input : amor amante amando amar amado amei amore amamos amarei amo
    Output : am  am     am     am   am    ame  amor  am     am     amo

   """
    stemmer = RSLPStemmer()
    # Converting words to their root forms
    for token in tweet.split():
        print(stemmer.stem(token))
    return stemmer

# 1.19  Putting all in single function
# Writing main function to merge all the preprocessing steps.

def text_preprocessing(tweet, lowercase=True, links=True, remove_html=True,
                       numbers=True, special_chars=True, repeatition=True,
                       newlines_tabs=True, punctuation=True, extra_whitespace=True,
                       contractions=True, mis_spell=True, stop_words=True,
                       lemmatization_word=True, stemmezation = True,
                       accented_chars=True):
    """
    This function will preprocess input text and return
    the clean text.
    """

    if lowercase == True:  # convert all characters to lowercase.
         tweet = lower_casing_text(tweet)

    if links == True:  # remove links.
        tweet = remove_links(tweet)

    if remove_html == True: # remove html tags   # **DESACTIVATE
        Data = strip_html_tags(Data)

    if numbers == True:  # remove all numbers.
        tweet = remove_number(tweet)

    if special_chars == True:  # remove all special characters.
        tweet = removing_special_characters(tweet)

    if repeatition == True:  # reduce repeatitions.
        tweet = reducing_error_char_repeatation(tweet)

    if newlines_tabs == True:  # remove newlines & tabs.
        tweet = remove_newlines_tabs(tweet)

    if punctuation == True:  # remove punctuation.
        tweet = remove_punctuation(tweet)

    if extra_whitespace == True:  # remove extra whitespaces.
        tweet = remove_whitespaces(tweet)

    if contractions == True: # expand contractions.
        tweet = expand_contractions(tweet)

    spell = Speller(lang='pt')

    if mis_spell == True: # check for mis-spelled words & correct them.
        tweet = spelling_correction(tweet)

    stoplist = stopwords.words('portuguese')
    stoplist = set(stoplist)

    if stop_words == True:  # remove stopwords.
        tweet = removing_stopwords(tweet)

    if lemmatization_word == True:  # converts words to lemma form.
        tweet = lemmatization(tweet)

    if accented_chars == True:  # remove accented characters.
        tweet = accented_characters_removal(tweet)

    word_tokens = word_tokenize(tweet) # tokenize tweet.

    if stemmezation == True:  # converts words to stemmer form.
        tweet = stemmezation(tweet)

    return word_tokens
