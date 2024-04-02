from typing import Dict 


framework_list: Dict = {
    "pureml_llm" : {
        'rouge_score_precision' : 0.7,
        'rouge_score_recall' : 0.7,
        'rouge_score_fmeasure' : 0.7,
    },
    "pureml_genai" : {
    'rouge_score_precision' : 0.7,
    'rouge_score_recall' : 0.7,
    'rouge_score_fmeasure' : 0.5,
    'quasi_exact_match' : 0.5,
    'f1' : 0.7,
    'rr_10' : 0.4,
    'bert_score_precision' : 0.5,
    'bert_score_recall' : 0.6,
    'bert_score_f1' : 0.4,
    'fluency' : 0.5,
    'sentiment' : 0.7,
    'flesch_reading_ease' : 0.5,
    'flesch_kincaid_grade' : 0.4,
    'ai_disclaimer_similarity' : 0.6,
    'character' : 0.5,
    'wer' : 0.3,
    'ter' : 0.4,
    'charcut' : 0.5,
    'chrf' : 0.6,
    'GoogleBLEU' : 0.5,
    'Mauve' : 0.5,
    'Meteor' : 0.6,
    'nltk_mt' : 0.4,
    'Hallucination' : 0.5,
    'bias'  : 0.4,
    'toxicity' : 0.001,
    'insult' : 0.01,
    'severe_toxicity' : 0.01,
    'profanity' :0.01,
    'identity_attack' : 0.01  
    },
    "pureml_test" : {
        'ban_topics' : 0.5,
        'gibberish' : 0.5,
        'relevance' : 0.5
    }
}