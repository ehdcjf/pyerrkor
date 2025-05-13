### 목적
파이썬 예외 메시지를 한글로 출력해주는 라이브러리입니다. 


### 설치
```bash

```


### 사용
```python
import sibd_pyerr
sibd_pyerr.install()
```

##### 참고
https://github.com/friendly-traceback/friendly-traceback



###### 배포
1 필요한 툴 설치
pip install build twine

2 빌드 파일 생성 (dist/ 폴더 생김)
python -m build

3 PyPI 업로드
twine upload dist/*