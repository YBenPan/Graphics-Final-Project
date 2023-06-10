test: face.mdl main.py matrix.py mdl.py display.py draw.py gmath.py
	python main.py face.mdl

bear: bear.mdl main.py matrix.py mdl.py display.py draw.py gmath.py
	python main.py bear.mdl

hotdog: hotdog.mdl main.py matrix.py mdl.py display.py draw.py gmath.py
	python main.py hotdog.mdl

clean:
	rm *pyc *out parsetab.py

clear:
	rm *pyc *out parsetab.py *ppm
