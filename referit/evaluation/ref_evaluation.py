
from tokenizer.ptbtokenizer import PTBTokenizer
from bleu.bleu import Bleu
from meteor.meteor import Meteor
from rouge.rouge import Rouge
from cider.cider import Cider

"""
Input: refer and res = [{ref_id, sent}]

Things of interest
eval_refs  - list of ['ref_id', 'CIDEr', 'Bleu_1', 'Bleu_2',
                      'Bleu_3', 'Bleu_4', 'ROUGE_L', 'METEOR']
eval      - dict of {metric: score}
ref_to_eval - dict of {ref_id: ['ref_id', 'CIDEr', 'Bleu_1',
                                'Bleu_2', 'Bleu_3', 'Bleu_4',
                                'ROUGE_L', 'METEOR']}
"""


class RefEvaluation:
    def __init__(self, refer, res):
        """
        :param refer: refer class of current dataset
        :param res: [{'ref_id', 'sent'}]
        """
        self.eval_refs = []
        self.eval = {}
        self.ref_to_eval = {}
        self.refer = refer
        self.res = res

    def evaluate(self):

        evalRefIds = [ann['ref_id'] for ann in self.res]

        refToGts = {}
        for ref_id in evalRefIds:
            ref = self.refer.refs[ref_id]
            # up to 3 expressions
            gt_sents = [sent['sent'] for sent in ref['sentences']]
            refToGts[ref_id] = gt_sents
        refTores = {ann['ref_id']: [ann['sent']] for ann in self.res}

        print('tokenization...')
        tokenizer = PTBTokenizer()
        self.refTores = tokenizer.tokenize(refTores)
        self.refToGts = tokenizer.tokenize(refToGts)

        # =================================================
        # Set up scorers
        # =================================================
        print('setting up scorers...')
        scorers = [
            (Bleu(4), ["Bleu_1", "Bleu_2", "Bleu_3", "Bleu_4"]),
            (Meteor(), "METEOR"),
            (Rouge(), "ROUGE_L"),
            (Cider(), "CIDEr")
        ]

        # =================================================
        # Compute scores
        # =================================================
        for scorer, method in scorers:
            print('computing %s score...' % (scorer.method()))
            score, scores = scorer.compute_score(self.refToGts, self.refTores)
            if type(method) == list:
                for sc, scs, m in zip(score, scores, method):
                    self.set_eval(sc, m)
                    self.set_ref_to_eval_refs(scs, self.refToGts.keys(), m)
                    print("%s: %0.3f" % (m, sc))
            else:
                self.set_eval(score, method)
                self.set_ref_to_eval_refs(scores, self.refToGts.keys(), method)
                print("%s: %0.3f" % (method, score))
        self.set_eval_refs()

    def set_eval(self, score, method):
        self.eval[method] = score

    def set_ref_to_eval_refs(self, scores, refIds, method):
        for refId, score in zip(refIds, scores):
            if refId not in self.ref_to_eval:
                self.ref_to_eval[refId] = {}
                self.ref_to_eval[refId]["ref_id"] = refId
            self.ref_to_eval[refId][method] = score

    def set_eval_refs(self):
        self.eval_refs = [eval for refId, eval in self.ref_to_eval.items()]


if __name__ == '__main__':

    import os.path as osp
    import sys
    ROOT_DIR = osp.abspath(osp.join(osp.dirname(__file__), '..', '..'))
    sys.path.insert(0, osp.join(ROOT_DIR, 'lib', 'datasets'))
    from referit import REFER

    # load refer of dataset
    dataset = 'refcoco'
    refer = REFER(dataset, split_by='google')

    # mimic some res
    val_refIds = refer.getRefIds(split='test')
    ref_id = 49767
    print("GD: %s" % refer.refs[ref_id]['sentences'])
    res = [{'ref_id': ref_id, 'sent': 'left bottle'}]

    # evaluate some refer expressions
    refEval = RefEvaluation(refer, res)
    refEval.evaluate()

    # print output evaluation scores
    for metric, score in refEval.eval.items():
        print('%s: %.3f' % (metric, score))

    # demo how to use evalImgs to retrieve low score result
    # evals = [eva for eva in refEval.eval_refs if eva['CIDEr']<30]
    # print 'ground truth sents'
    # refId = evals[0]['ref_id']
    # print 'refId: %s' % refId
    # print [sent['sent'] for sent in refer.refs[refId]['sentences']]
    #
    # print 'generated sent (CIDEr score %0.1f)' % (evals[0]['CIDEr'])

    # print refEval.ref_to_eval[8]
