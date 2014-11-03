SOURCE = mombench.txt

TARGET_ODT = $(SOURCE:.txt=.odt)
TARGET_HTML = $(SOURCE:.txt=.html)

all: odt html
odt: $(TARGET_ODT)
html: $(TARGET_HTML)

$(TARGET_ODT): $(SOURCE)
	rst2odt $< $@

$(TARGET_HTML): $(SOURCE)
	rst2html $< $@

.PHONY: clean
clean:
	rm -rf $(TARGET_ODT) $(TARGET_HTML)
