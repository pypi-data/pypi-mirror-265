from .base import *
kiwi = Kiwi()


# 품사 재조정을 위한 클래스
# Mecab(dicpath='/home/buffet/Coding/venv/mecab-ko-dic-2.1.1-20180720')
class Morph:

    r"""Mecab 품사분류기 활용 함수모음"""

    def __init__(self, path:str=None):
        self.dic_path = path
        self.mecab = None
        if self.dic_path:
            self.mecab = Mecab(dicpath=self.dic_path)
        else:
            self.mecab = Mecab()


    # Mecab 의 활용 ====================================================
    def _nouns(self, token:str):
        r"""1개 단어에서 명사 추출하기 by Mecab"""
        assert type(token) == str, f"`{type(token)}` only allowd `str` data"
        result = self.mecab.nouns(token)
        return (token, result)


    def _pos(self, token):
        r"""품사태그 추가하기 by Mecab"""
        assert type(token) == str, f"`{type(token)}` only allowd `str` data"
        result = self.mecab.pos(token)
        return (token, result)


    def _kiwi_post(self, tokens):
        r"""Kiwi 품사 분류기 활용"""
        result = {}
        if type(tokens) == list:
            for token in tqdm(tokens):
                pos = [(_.form, _.tag)  for _ in kiwi.tokenize(token)]
                result[token] = pos

        elif type(tokens) == str:
            return tokens, [(_.form, _.tag)  for _ in kiwi.tokenize(tokens)]
        return result


    def nouns_dict(self, texts:list=None, tokens_nouns:dict=None, kiwi=False):

        r""" 명사태그 추출하기
        texts (List[])      : 태그 추출작업을 위한 단어목록
        tokens_nouns (Dict) : 품사 Tag 내용이 추가된 데이터 
        kiwi  (bool)        : Mecab 대신 Kiwi 태크사용 """

        print("*"*8," Create Nouns Dict ...")
        if texts is not None:
            assert type(texts) == list,\
                f"`{type(texts)}` only allowd `list` data"

        if ((tokens_nouns is None) & (type(texts) == list)):
            if kiwi: # Kiwi 활용한 품사태그
                tokens_nouns = self._kiwi_post(texts)
            else:    # Mecab 활용한 품사태그
                tokens_nouns = [self._pos(_)  for _ in tqdm(texts)]
                tokens_nouns = {_[0]:_[1]     for _ in tokens_nouns}
        else:
            assert type(tokens_nouns) == dict,\
                f"`{type(tokens_nouns)}` only allowd `dict` data"

        # Pre Processing ...
        tokens_nouns = { # 'NN' 태그가 포함된 내용만 필터링
            k : list(filter(lambda x : x[1].find('NN') != -1, v))  
            for k,v in tokens_nouns.items()
        }
        tokens_nouns = {k:v   for k,v in tokens_nouns.items()  if len(v)>0}

        # 발견된 마지막 Nouns 단어를 기준으로 Token 필터링
        nouns_dict = {}
        for _token, _tags in tqdm(tokens_nouns.items()):
            _last_noun = _tags[-1][0]
            _idx       = _token.find(_last_noun)
            _new_token = _token[:_idx] + _last_noun
            # 추출된 명사가 1글자 이상일 때
            if len(_new_token) > 1:
                nouns_dict[_token] = _new_token
        return nouns_dict


    # Josa 의 활용 ==================================================
    def _josa(self):
        r"""Josa 단어목록 확인"""
        particles  = "이,가,을,를,은,는,도,만,부터,이,가,께서,에서,이다,의,이며,과의,"
        particles += "들,인들,엔들,밖에,뿐만,뿐,만,을,를,로,로써,로서,으로,와,과,에,"
        particles += "에서,에다,에다가,에게,께,한테,한테서,보다,에게서,서,랑,이랑,"
        particles += "와의,과의,로부터,에다,에다가,에게,께,한테,한테서,보다,에게서,"
        particles += "써,서,랑,이랑,함으로써,으로써,으로서,에서도,에서의,만의,"
        particles += "에서는,에서도,에서만,에선,에는,으로부터,으로선,로부터,라는"
        particles  = particles.split(',')
        return particles



    # def _token_index(self, 
    #         tokens=None, mecab=False, items=None, min_length=2
    #     ):
    #     r"""한글단어 Tag 추가 및 인덱싱 값 출력
    #     token : list => 작업 시작 tokens
    #     items : list(tuple) => mecab=True 작업 결과를 함수에 재입력"""

    #     # Multiprocessing ... 이 더 느림....
    #     if tokens:
    #         items = list(self._pos(_)  for _ in tqdm(tokens))
    #         # 명사태그 Index 추출 :1글자 이상 & 명사품사가 포함된 단어
    #         _lambda = lambda x : x if x[1] in ['NNG','NNP','NNB'] else None 
    #         if mecab:
    #             items = {
    #                 _[0]:_[1]  
    #                 for _ in items   
    #                 if ((len(_[0]) >= min_length) & (len(list(filter(_lambda, _[1])))>0))
    #             }
    #             return items

    #     # 외부에서 items 를 입력한 경우로 아랫 추가작업이 필요한 경우
    #     if items:
    #         items = items

    #     result  = {}
    #     for token, morph_tokens in tqdm(items):
    #         _lambda     = lambda x : x[1].find('NN') != -1
    #         _lambda     = lambda x : x[1] in ['NNG','NNP','NNB']
    #         _morph_list = list(filter(_lambda, morph_tokens))
    #         _lambda     = lambda x :morph_tokens.index(x)
    #         _morph_idx  = list(map(_lambda, _morph_list))
    #         if len(_morph_idx) >= min_length:
    #             result[token] = _morph_idx
    #     return result

# if self.worker:
#     print("MultiPr ocessing ...")
#     with multiprocessing.Pool(processes=self.worker) as pool:
#         items = list(tqdm(
#             pool.imap(self._nouns, tokens), 
#             total=len(tokens)
#         ))
# else: