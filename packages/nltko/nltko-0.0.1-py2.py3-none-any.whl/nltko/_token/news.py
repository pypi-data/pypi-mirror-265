from .base import *
from .token import Token


# Post Processing of News
class News(Token):

    rate_eng = .8
    tokenizer_eng = re.compile(r'[ A-z0-9]+')
    tokenizer_kor = re.compile(r'[ ㄱ-힣0-9]+')

    # 제목을 기준으로 영어가사 필터링
    def titles_of_eng(self, titles):

        assert type(titles) == list, "`titles` only allowed : List[str]"
        _lambda = lambda x : x  if len("".join(
            self.tokenizer_eng.findall(x))) > len(x) * self.rate_eng else None
        _eng = list(filter(_lambda, titles)) 
        return _eng

    # 코딩내용 삽입부분 제거하기
    def content_coding(self, df):

        # 코딩영역 인덱스 확인 후 필터링
        def _filter1(content):
            _check  = '/* iframe resize for nate news */'    
            _idx    = content.find(_check)
            return content[:_idx]

        def _filter2(content):
            _check  = 'window.dicnf ='    
            _idx    = content.find(_check)
            return content[:_idx]

        # 본문에서 불필요한 부분 필터링
        _check  = '\/\* iframe resize for nate news \*\/'
        _df     = df[df.content.str.contains(_check)] # 2만개 추출
        _items  = _df.to_dict()['content']        # {index: content, ...}
        _items  = {key: (lambda x : _filter1(x))(value)  for key, value in _items.items()}
        _indexs = list(_items.keys())
        df.loc[_indexs, 'content'] = list(_items.values())

        _check  = 'window.dicnf ='
        _df     = df[df.content.str.contains(_check)] # 2만개 추출
        _items  = _df.to_dict()['content']        # {index: content, ...}
        _items  = {key: (lambda x : _filter2(x))(value)  for key, value in _items.items()}
        _indexs = list(_items.keys())
        df.loc[_indexs, 'content'] = list(_items.values())
        return df

    # 본문 외국어 비중으로 외국어 기사 찾기
    def contents_filter(self, contents):
        assert type(contents) == list, "`contents` only allowed : List[str]"
        _lambda  = lambda x : (x, 
            len("".join(re.findall(r'[ㄱ-힣]+', x))), # 한글비중
            len("".join(re.findall(r'[A-z0-9]+', x))), # 외국어 비중
            len(x), # 전체길이
        )  # 위 값들 중 `0` 을 출력하는 경우가 있어서 연산에 문제가 발생함
        # ==> 외국어 , 전체길이 0 인 데이터 필터링
        # ==> 필터링 결과로 비중연산 재실행 하기
        result = list(map(_lambda, tqdm(contents)))
        return result