# Wolf catcher

## Requirements

- pyenv 
  - local version : 3.8.10
  - [GitHub - pyenv/pyenv: Simple Python version management](https://github.com/pyenv/pyenv)
- poetry
  - https://python-poetry.org/docs/

## Before start

```bash
peotry install
```

> 🚀 See below for PySide6 installation error in poety </br>
> https://github.com/python-poetry/poetry/issues/1413#issuecomment-557195997

## 빌드
콘솔 창이 뜨지 않게 하기 위해서는 아래와 같은 작업을 해 줘야 한다.
* [Pyinstaller 사용시 selenium의 chromedriver 콘솔창 제거하는 방법](https://hydragon-cv.info/entry/Pyinstaller-%EC%82%AC%EC%9A%A9%EC%8B%9C-selenium%EC%9D%98-chromedriver-%EC%BD%98%EC%86%94%EC%B0%BD-%EC%A0%9C%EA%B1%B0%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95?category=960692)

## TODO
- [x] 다운로드 목록 관리 - SQLite로 해 보자
- [x] ID 저장 데이터 베이스 제작
- [x] 페이지 로딩 속도 개선
- [x] 처음 로딩 시 상태 텍스트 

---


## References
### Python 기본 문법
* [파이썬 - 기본을 갈고 닦자!](https://wikidocs.net/book/1553)
* [파이썬 코딩 도장](https://dojang.io/course/view.php?id=7)
* [레벨업 파이썬](https://wikidocs.net/book/4170)

### PySide Or PyQT
* [Qt for Python](https://doc.qt.io/qtforpython/index.html)
* [The complete PyQt5 tutorial — Create GUI applications with Python](https://www.pythonguis.com/pyqt5-tutorial/#qt-creator)
* [Qt Designer and Python: Build Your GUI Applications Faster](https://realpython.com/qt-designer-python/)
* [PyQt5 Tutorial - 파이썬으로 만드는 나만의 GUI 프로그램 - WikiDocs](https://wikidocs.net/book/2165) (2020)
* [초보자를 위한 Python GUI 프로그래밍 - PyQt5 - WikiDocs](https://wikidocs.net/book/2944) (2021)
* [공학자를 위한 PySide2](https://wikidocs.net/book/2957) (2019)