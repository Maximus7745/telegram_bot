import spacy
import random
from spacy.lang.en import English

TRAINING_DATA = [
    ("What to expect at Apple's 10 November event", 
    {"entities": [(18,23,"COMPANY")]})
    # Другие примеры...
]

nlp = English()

for i in range(10):
    random.shuffle(TRAINING_DATA)
    for batch in spacy.util.minibatch(TRAINING_DATA):
        texts = [text for text, annotation in batch]
        annotations = [annotation for text, annotation in batch]
        nlp.update(texts, annotations)
        
nlp.to_disk("model")