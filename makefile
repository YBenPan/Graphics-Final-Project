test: face.mdl main.py matrix.py mdl.py display.py draw.py gmath.py
	python3 main.py face.mdl

bear: bear.mdl main.py matrix.py mdl.py display.py draw.py gmath.py
	python3 main.py bear.mdl

hotdog: hotdog.mdl main.py matrix.py mdl.py display.py draw.py gmath.py
	python3 main.py hotdog.mdl

gallery: gallery.mdl main.py matrix.py mdl.py display.py draw.py gmath.py
	python3 main.py gallery.mdl

clean:
	rm *pyc *out parsetab.py

clear:
	rm *pyc *out parsetab.py *ppm
