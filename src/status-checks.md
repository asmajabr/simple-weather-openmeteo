
# Status checks & branch protection mapping

- Require pull request before merge
- Require at least 1 approval and conversation resolution
- Require status checks to pass:
  - CI / lint (ruff)
  - CI / tests (pytest + coverage)
  - CI / bandit (security)
  - CI / docker-build (image compiles)
  - CodeQL / analyze (Python)
- (Optional) Require signed commits
- (Optional) Require review from CODEOWNERS
