from pureml_llm.metric_base import MetricBase
from typing import Any
from sacrebleu.metrics import TER 



class TERMetric(MetricBase):
    name:Any = 'ter'
    input_type:Any = 'text'
    output_type:Any = None
    kwargs:Any = {}


    def parse_data(self,data):
        return data
    

    def compute(self,references,predictions,normalized:bool = False,ignore_punct:bool = False,support_zh_ja_chars:bool = False,case_sensitive:bool = False):
        if (len(references) != 0) and (len(predictions) != 0):
            try:
                references_per_prediction = len(references[0])
                if any(len(refs) != references_per_prediction for refs in references):
                    raise ValueError("Sacrebleu requires the same number of references for each prediction")
                transformed_references = [[refs[i] for refs in references] for i in range(references_per_prediction)]

                sb_ter = TER(
                    normalized=normalized,
                    no_punct=ignore_punct,
                    asian_support=support_zh_ja_chars,
                    case_sensitive=case_sensitive,
                )
                output = sb_ter.corpus_score(predictions, transformed_references)
                # return {
                #     self.name: {
                #         'score' : output.score,
                #         'num_edits' : output.num_edits,
                #         'ref_length' : output.ref_length
                #     }
                # }
                return {
                    self.name  : output.score
                }

            except Exception as e:
                print(e)
    

    def risk(self, score):
        # score_threshold = 3000
        # num_edits_threshold = 10
        # ref_length_ratio_threshold = 1.0
        # ter_scores = score[self.name]
        # result = {}
        
        # if 'score' in ter_scores:
        #     result['score'] = 'pass' if ter_scores['score'] <= score_threshold else 'fail'
        
        # if 'num_edits' in ter_scores:
        #     result['num_edits'] = 'pass' if ter_scores['num_edits'] <= num_edits_threshold else 'fail'
        
        # if 'ref_length' in ter_scores:
        #     result['ref_length'] = 'pass' if ter_scores['ref_length'] <= ref_length_ratio_threshold else 'fail'
        
        # return {self.name: result}
        return {self.name: 'pass' if score[self.name] >= 3000 else 'fail'}
