PY_SRC = platform.py scaling.py submodels.py
PY_OUT = $(PY_SRC:.py=.pdf)

INK_SRC = snake.svg ladder.svg
INK_OUT = $(INK_SRC:.svg=.pdf)

all: $(INK_OUT) $(PY_OUT)

$(PY_OUT): %.pdf : %.py
	python $<

$(INK_OUT): %.pdf : %.svg
	inkscape -D -f $< -A $@

.PHONY: clean
clean:
	rm -rf $(INK_OUT) $(PY_OUT)
