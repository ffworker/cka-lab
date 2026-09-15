PYTHON ?= python3
TRAINER := $(PYTHON) -m trainer

.PHONY: requirements requirements-check status lab-up mission validate hint solution reset lab-down profile

requirements:
	@./scripts/install-requirements.sh --install

requirements-check:
	@./scripts/install-requirements.sh --check

status:
	@$(TRAINER) status

lab-up:
	@$(TRAINER) lab-up

mission:
	@$(TRAINER) mission

validate:
	@$(TRAINER) validate

hint:
	@$(TRAINER) hint

solution:
	@$(TRAINER) solution

reset:
	@$(TRAINER) reset

lab-down:
	@$(TRAINER) lab-down

profile:
	@$(TRAINER) profile
