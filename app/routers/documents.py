from fastapi import Body, APIRouter
from ..models.document import Document
import spacy
from spacy.matcher import Matcher
from spacy.lang.en import English

# Preflight load up NLP modules, vocabulary, and rules
# More elaborate rule to capture more context for return string (passive subject) if detected
PASSIVE_WITH_SUBJECT = [{'DEP':'nsubjpass'},{'DEP':'advmod','OP':'*'},{'DEP':'aux','OP':'*'},{'DEP':'auxpass'},{'TAG':'VBN'}]
# Simpler rule if only passive auxillary & verb in past participle are detected
PASSIVE_WITH_AUX_ONLY = [{'DEP':'auxpass'},{'TAG':'VBN'}]
TRAINED_MODEL = 'en_core_web_lg'
NLP = spacy.load(TRAINED_MODEL)
matcher = Matcher(NLP.vocab)
matcher.add('passives', [PASSIVE_WITH_SUBJECT, PASSIVE_WITH_AUX_ONLY])

SENT = English()
SENT.add_pipe('sentencizer')

router = APIRouter()

@router.post("/passives", tags=["documents"])
async def postPassive(document: Document):
  processedText = NLP(document.text)
  passiveSpans = matcher(processedText, as_spans=True)
  passivePhrases = []
  # filter_spans removes duplicates/overlapping spans, prefering the longest one
  for span in spacy.util.filter_spans(passiveSpans):
    phraseString = span.text
    passivePhrases.append([phraseString, span.start, span.end])
  return { "passives": passivePhrases }


@router.post("/sentences", tags=["documents"])
async def postSentence(document: Document):
  text = document.text
  processed = SENT(text)
  sentences = []
  for sent in processed.sents:
    print(str(sent))
    sentence = sent.text
    sentences.append(sentence)
  return { "sentences": sentences }
