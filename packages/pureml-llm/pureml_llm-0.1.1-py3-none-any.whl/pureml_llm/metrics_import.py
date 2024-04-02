from .accuracy.rouge_precision import RougeScorePrecision
from .accuracy.rouge_recall import RougeScoreRecall
from .accuracy.rouge_fmeasure import RougeScoreFmeasure
from .accuracy.quasi_exact_match import QuasiExactMatch
from .accuracy.f1 import F1
from .accuracy.rr_10 import RR10
from .accuracy.bert_score_precision import BertScorePrecision
from .accuracy.bert_score_recall import BertScoreRecall
from .accuracy.bert_score_f1 import BertScoreF1
from .accuracy.fluency import Fluency
from .accuracy.sentiment import Sentiment
from .accuracy.flesch_reading_ease import Flesch_Reading_Ease
from .accuracy.flesch_kincaid_grade import Flesch_Kincaid_Grade
#from .accuracy.ai_disclaimer_similarity import AI_Disclaimer_Similarity
from .accuracy.character import Character
from .accuracy.wer import WER
from .accuracy.ter import TERMetric
from .accuracy.charcut_mt import Charcut
from .accuracy.chrf import Chrf
from .accuracy.google_bleu import GoogleBLUE
from .accuracy.mauve_score import Mauve
from .accuracy.meteor import Meteor
from .accuracy.nltk_mt import NltkMT
from .hallicunation.hallicunation_hugging_face import HallucinationMetric
from .bias.bias import Bias

from .toxicity.toxicity_from_prespective import ToxicityAPI
from .toxicity.insult import ToxicityAPIInsult
from .toxicity.severe_toxicity import ToxicityAPISEVERE_TOXICITY
from .toxicity.profanity import ToxicityAPIPROFANITY
from .toxicity.identity_attack import ToxicityAPIIDENTITY_ATTACK
from typing import Any

# from .accuracy.ban_topics import BanTopics
# from .accuracy.gibberish import Gibberish
# from .accuracy.relevance import Relevance

accuracy_metrics: Any = {
    'rouge_score_precision' : RougeScorePrecision(),
    'rouge_score_recall' : RougeScoreRecall(),
    'rouge_score_fmeasure' : RougeScoreFmeasure(),
    'quasi_exact_match' : QuasiExactMatch(),
    'f1' : F1(),
    'rr_10' : RR10(),
    'bert_score_precision' : BertScorePrecision(),
    'bert_score_recall' : BertScoreRecall(),
    'bert_score_f1' : BertScoreF1(),
    'fluency' : Fluency(),
    'sentiment' : Sentiment(),
    'flesch_reading_ease' : Flesch_Reading_Ease(),
    'flesch_kincaid_grade' : Flesch_Kincaid_Grade(),
    #'ai_disclaimer_similarity' : AI_Disclaimer_Similarity(),
    'character' : Character(),
    'wer' : WER(),
    'ter' : TERMetric(),
    'charcut' : Charcut(),
    'chrf' : Chrf(),
    'GoogleBLEU' : GoogleBLUE(),
    'Mauve' : Mauve(),
    'Meteor' : Meteor(),
    'nltk_mt' : NltkMT(),
    # 'ban_topics' : BanTopics(),
    # 'gibberish' : Gibberish(),
    # 'relevance' : Relevance()
}

hallucination_metrics: Any = {
    'Hallucination' : HallucinationMetric()
}


bias_metrics: Any = {
    'bias' : Bias()
}


toxicity_metrics: Any = {
    'toxicity' : ToxicityAPI(),
    'insult' : ToxicityAPIInsult(),
    'severe_toxicity' : ToxicityAPISEVERE_TOXICITY(),
    'profanity' : ToxicityAPIPROFANITY(),
    'identity_attack' : ToxicityAPIIDENTITY_ATTACK()
}