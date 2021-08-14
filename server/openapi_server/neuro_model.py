from neuroner import neuromodel


class Neuroner:
    def __init__(self):
        self.nn = neuromodel. \
                  NeuroNER(train_model=False,
                           use_pretrained_model=True,
                           dataset_text_folder="openapi_server/data/example_unannotated_texts",
                           pretrained_model_folder="openapi_server/trained_models/i2b2_2014_glove_spacy_bioes",
                           parameters_filepath='.',
                           spacylanguage="en_core_web_sm",
                           token_pretrained_embedding_filepath='openapi_server/data/word_vectors/glove.6B.100d.txt',
                           load_all_pretrained_token_embeddings=1,
                           maximum_number_of_epochs=500)
       

model = Neuroner().nn


def predict(text):
    result = model.predict(text)
    return result
