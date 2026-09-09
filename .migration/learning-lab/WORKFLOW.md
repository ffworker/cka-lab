# Branch Workflow for This Course Repo

## Rule of thumb
- `main` = current active lab (work in progress)
- `lab/NN-topic` = finished snapshot of one lab

## After finishing a lab on main
1. Commit all final lab changes on `main` (including report + tracker + README overview update).
2. Create/update the dedicated branch for that lab:
   - `git checkout -b lab/03-persistence` (or `git checkout lab/03-persistence` if it exists)
3. Push the lab branch:
   - `git push -u origin lab/03-persistence`
4. Go back to `main`:
   - `git checkout main`
5. Scaffold the next lab on `main` (new README instructions, bug scenario, templates).
6. Commit and push `main`.

## Important safety checks
- Before pushing, run: `git status` and `git branch --show-current`
- Never merge old lab branches back into `main` unless explicitly intended.
- If a lab branch gets polluted, reset it to the intended lab commit and force-push once.
