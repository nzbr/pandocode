## Options
PY=python3
ZIP=zip -0 -q
PYLINT=pylint -E
PYC=$(PY) -c "from py_compile import compile; from sys import argv; compile(argv[1], cfile=argv[1]+'c', doraise=True, optimize=2)"

PREFIX=/usr/bin

NAME=pandocode
OUT=$(NAME).pyz

## Files
SRC = $(wildcard *.py)
OBJ = $(SRC:%.py=%.pyc)
CLEAN = $(wildcard *.pyc) $(wildcard *.pyz.zip) $(wildcard *.pyz) $(wildcard *.py.lint)

## Build Targets
$(OUT) : $(OUT).zip
	@printf "  PYZ\t$@  <=  $<\n"
	@echo "#!$$(which $(PY))" | cat - $(OUT).zip >$(OUT)
	@chmod +x $(OUT)

$(OUT).zip : $(OBJ)
	@printf "  ZIP\t$@  <=  $+\n"
	@$(ZIP) $(OUT).zip $(OBJ) -x pyc.pyc

%.py.lint : %.py
	@printf "  LINT  $<\n"
	@$(PYLINT) $<

%.pyc : %.py %.py.lint
	@printf "  PYC\t$<\n"
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
	@printf "  INST\t$(OUT) => $(PREFIX)/$(NAME)\n"
	@install -m 755 $(OUT) $(PREFIX)/$(NAME)

