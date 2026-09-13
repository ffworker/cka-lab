PYTHON ?= python3
TRAINER := $(PYTHON) -m trainer

.PHONY: status lab-up mission validate hint solution reset lab-down profile

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
