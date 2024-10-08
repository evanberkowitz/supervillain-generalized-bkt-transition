
.PHONY: demo
demo: demo/scaling.pdf .WAIT demo/transition.pdf .WAIT demo/breaking.pdf
# Takes about 11 minutes on my machine.

.PHONY: demo/parallel
demo/parallel:
# Takes about 3-4 minutes on my machine.
	$(MAKE) PARALLEL=--parallel demo
# Join HDF5 files
	h5repack --merge demo/scaling-bootstrap.h5 demo/scaling-bootstrap.repacked.h5
	h5repack --merge demo/transition-bootstrap.h5 demo/transition-bootstrap.repacked.h5
	h5repack --merge demo/breaking-bootstrap.h5 demo/breaking-bootstrap.repacked.h5

demo/scaling.pdf: production.py scaling.py demo/scaling.py
	python production.py  $(PARALLEL) demo/scaling.py
	python history.py     $(PARALLEL) demo/scaling.py --pdf demo/scaling-history.pdf
	python correlators.py $(PARALLEL) demo/scaling.py --pdf demo/scaling-correlators.pdf
	python scaling.py     $(PARALLEL) demo/scaling.py --pdf demo/scaling.pdf

demo/transition.pdf: production.py transition.py demo/transition.py
	python production.py $(PARALLEL) demo/transition.py
	python history.py    $(PARALLEL) demo/transition.py --pdf demo/transition-history.pdf
	python transition.py $(PARALLEL) demo/transition.py --pdf demo/transition.pdf

demo/breaking.pdf: production.py breaking.py demo/breaking.py
	python production.py $(PARALLEL) demo/breaking.py
	python breaking.py $(PARALLEL) demo/breaking.py --pdf demo/breaking.pdf

.PHONY: demo/tidy
demo/tidy:
	$(RM) demo/{scaling,transition,breaking}*pdf

.PHONY: demo/clean
demo/clean: demo/tidy
	$(RM) demo/{scaling,transition,breaking}*h5

paper-figures.tar.gz: breaking .WAIT scaling .WAIT scaling/result
	tar -cvzf paper-figures.tar.gz Z3-breaking-N{3,7}.pdf scaling/W{1,2,3}.pdf scaling/result.pdf

.PHONY: breaking
breaking: \
	Z3-breaking-N3.pdf .WAIT \
	Z3-breaking-N7.pdf

Z3-breaking-N3.pdf: demo/breaking.pdf
	cp demo/breaking.pdf Z3-breaking-N3.pdf

Z3-breaking-N7.pdf: breaking.py Z3-breaking-N7.py
	python production.py $(PARALLEL) Z3-breaking-N7.py
	python breaking.py $(PARALLEL) Z3-breaking-N7.py --pdf Z3-breaking-N7.pdf

.PHONY: scaling
scaling: \
	scaling/W1.pdf .WAIT \
	scaling/W2.pdf .WAIT \
	scaling/W3.pdf

scaling/W%.pdf: scaling.py scaling/W=%.py
	python production.py $(PARALLEL) scaling/W=$*.py
	python history.py $(PARALLEL) scaling/W=$*.py --pdf scaling/W$*-history.pdf
	python scaling.py $(PARALLEL) scaling/W=$*.py --pdf scaling/W$*.pdf

scaling/result.pdf: result.py
	python result.py --pdf scaling/result.pdf

paper-tidy:
	$(RM) Z3-breaking.pdf

paper-clean: paper-tidy
	@ECHO "Clean the data files manually, it is too dangerous to provide a makefile target."
