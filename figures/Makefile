PY_SRC = platform.py scaling.py submodels.py
PY_SVG = $(PY_SRC:.py=.svg)
PY_EPS = $(PY_SRC:.py=.eps)
PY_PDF = $(PY_SRC:.py=.pdf)

INK_SRC = snake.svg ladder.svg tofu.svg
INK_OUT = $(INK_SRC:.svg=.pdf)
INK_EPS = $(INK_SRC:.svg=.eps)

all: $(INK_OUT) $(INK_EPS) $(PY_PDF) $(PY_SVG)

$(PY_SVG): $(PY_PDF)
$(PY_EPS): $(PY_PDF)
$(PY_PDF): %.pdf : %.py
	python $<

$(INK_OUT): %.pdf : %.svg
	inkscape -D -f $< -A $@

$(INK_EPS): %.eps : %.svg
	inkscape -D -f $< -E $@

.PHONY: clean
clean:
	rm -rf $(INK_OUT) $(INK_EPS) $(PY_SVG) $(PY_EPS) $(PY_PDF)
