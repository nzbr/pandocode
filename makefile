## Options
PY=python3
ZIP=zip -0 -q
PYLINT=pylint -E
PYC=$(PY) -c "from py_compile import compile; from sys import argv; compile(argv[1], cfile=argv[1]+'c', doraise=True, optimize=2)"

DESTDIR=/usr
PREFIX=$(DESTDIR)

NAME=pandocode
OUT=$(NAME).pyz

## Files
SRC = $(wildcard *.py) $(wildcard pandocode/*.py)
OBJ = $(SRC:%.py=%.pyc)
CLEAN = $(wildcard *.pyc) $(wildcard *.pyz.zip) $(wildcard *.pyz) $(wildcard *.py.lint)

## Build Targets
$(OUT) : $(OUT).zip
	@printf "  PYZ\t$@  <=  $<\n"
	@echo "#!$$(which $(PY))" | cat - $(OUT).zip >$(OUT)
	@chmod +x $(OUT)

$(OUT).zip : $(OBJ) LICENSE
	@printf "  ZIP\t$@  <=  $+\n"
	@$(ZIP) $(OUT).zip $(OBJ)

%.py.lint : %.py
	@printf "  LINT  $<\n"
	@$(PYLINT) $<

%.pyc : %.py %.py.lint
	@printf "  PYC\t$@\n"
	@$(PYC) $<

## Phony Targets
.PHONY: clean all dist check install
clean :
	@for x in $(CLEAN); do printf "  RM\t$$x\n"; rm -rf $$x; done

all : dist

dist : $(OUT)

check : dist
	@printf "  CHK\t$(OUT).zip\n"
	@zip -T $(OUT).zip

install : dist
	@printf "  INST\t$(OUT) => $(PREFIX)/bin/$(NAME)\n"
	@install -D -m 755 $(OUT) $(PREFIX)/bin/$(NAME)
