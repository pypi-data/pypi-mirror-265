# 단어 전처리 및 빈도수 측정
from .base import *


class Token:
    r"""작업함수 소개"""

    regex_token  = r'[A-Za-zㄱ-ㅎ가-힣]+' # r'[A-z0-9ㄱ-힣\.\%\,]+' # 
    regex_number = r'[0-9]{1,100}[\%\,\.명년원위개억만천월일배]?'
    regex_title  = [  # 제목 필터링을 위한 정규식
        r'\[[\w]*포토[\w]*\]', 
        r'\[[\w]*사진[\w]*\]',
        r'\[스팟\]',r'\[화보\]',r'\[인사\]',
        r'\<스팟\>',r'\<화보\>',r'\<인사\>',
    ]

    def __call__(self):
        print("find_title(), filter_title(), freq()")


    def _flatten_list(self, nested_list):
        r"""다차원 list 를 평탄화"""
        return list(itertools.chain(*nested_list))


    def find_title(self, token, titles, raw=False):
        r"""`titles` 에서 `token` 검색결과 출력"""
        _lambda = lambda x : x if x.find(token) != -1 else None
        _tokens = filter(_lambda, titles)
        if raw:
            return list(_tokens)
        return len(list(_tokens))


    def filter_title(self, titles:list):
        r"""제목을 기준으로 분석 불필요한 내용 필터링"""
        _titles = []
        for _regex in self.regex_title:
            _compile  = re.compile(_regex)
            _filter   = filter(lambda x : len(_compile.findall(x)) > 0, titles)
            _filtered = list(_filter)
            _titles += _filtered
        return _titles # 불필요한 제목들


    def _token_filter(self, texts:list):
        r"""token 필터링"""
        _tokenizer = re.compile(self.regex_number)
        texts = list(map(lambda x : re.sub(r'[^\w\s\']', ' ', x), texts))     # 문자만 필터링
        texts = list(filter(lambda x : len(_tokenizer.findall(x))==0, texts)) # 숫자내용 필터링
        texts = list(filter(lambda x : len(x) > 1, texts))                    # 1글자 이상 필터링
        return texts


    # List[texts] -> [[`token1`,`token3`, ...], [`token3`,`token1` ...]]
    def _tokenizer(self, texts:list, bigrams=False, flat=True, max_length=10) -> list:
        r"""분석을 위한 한글 token 
        texts : List[`sentence`]
        flat  : 1차원 평평화 작업 적용
        bigrams : bigram 으로 Tokenizer 적용 """

        if type(texts) == str:
            texts = [texts]

        # filtering with regex
        # print("*" *8, " filtering by REGEX ", "*" *8, )
        _lambda = lambda x :" ".join(re.findall(self.regex_token, x))
        texts = list(map(_lambda, texts))                      # Token 추출
        texts = list(map(lambda x : word_tokenize(x), texts))  # uni grams

        # max_length 를 활용하여 최대길이 필터링 ...
        # print("*" *8, f" filtering by `max_length` : {max_length} ", "*" *8, )
        # _lambda = lambda x : len(x) <= max_length
        # texts = [list(filter(_lambda, x))  for x in texts]

        # 전처리 결과값 출력
        ## 단어가 아닌 문장 전체로 출력
        if flat==False:
            texts = [" ".join(self._token_filter(text))   for text in texts]
            if len(texts) > 0: return texts
            else:              return ""

        if bigrams:
            texts = list(map(lambda x : bigrams(x), texts)) # bi grams
            return texts

        texts = self._flatten_list(texts)              # list 1차원 평탄화
        # texts = self._token_filter(texts)            # Token 필터링
        texts = list(filter(lambda x : len(x.strip())>1, texts)) # 1글자 이상일 때
        texts = list(map(lambda x : x.strip(), texts)) # 공백제거
        return texts


    # Token 의 빈도수 계산
    def freq(self, texts:list, min_count=3, max_length=15):

        r"""문장내 등장하는 Token의 빈도측정
        texts  List[str] : 문장목록
        min_count  (int) : 최소 반복횟수
        max_length (int) : 최대 Token길이 """

        texts = self._tokenizer(texts)
        print(f"{len(texts):,} : Tokens Count")

        idf = dict(Counter(texts))
        idf = { k:v  
            for k, v in sorted(idf.items(),key=lambda x: x[1], reverse=True)  
            if ((v >= min_count) & (len(k) < max_length)) # `단체명` 때문에 길어짐
        }
        print(f"{len(idf):,} : idf Count")
        return idf


# texts = list(map(lambda x :re.sub('[一-龥]+',' ',x), texts)) # 한자제거
# texts = list(map(lambda x :re.sub('\[.*?\]',' ',x), texts)) # 괄호 포함된 단어제거1
# texts = list(map(lambda x :re.sub('\(.*?\)',' ',x), texts)) # 괄호 포함된 단어제거2
# texts = list(map(lambda x :re.sub('\<.*?\>',' ',x), texts)) # 괄호 포함된 단어제거2
# texts = list(map(lambda x :re.sub('ㆍ',' ',x), texts))       # 불필요한 Token 제거
# texts = list(map(lambda x :re.sub('_',' ',x), texts))       # 불필요한 Token 제거