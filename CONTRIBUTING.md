# Contributing to CloudGoat-GCP

Thanks for helping improve this lab — contributions are welcome and appreciated. Follow these guidelines so the repo doesn't explode.

## How to contribute
1. Fork the repository and create a branch: `feature/<short-desc>` from `dev`.
2. Make small, focused commits. Use clear commit messages.
3. Open a Pull Request to `dev` with a description of the change, any infra side-effects, and a test plan.
4. A reviewer will evaluate code quality, security implications, and documentation coverage.

## PR checklist
- [ ] Includes updated documentation (if behavior or interfaces changed).
- [ ] No secrets or credentials committed.
- [ ] Terraform changes include `terraform plan` output as an artifact or comment.
- [ ] K8s manifests validated with `kubectl apply --dry-run=client`.
- [ ] Portal UI changes include component-level tests or manual testing steps.

## Coding style
- JavaScript/TypeScript: follow ESLint + Prettier rules.
- Terraform: follow `terraform fmt` and pin module/provider versions.
- Shell scripts: include `set -euo pipefail` and comments.
- YAML/JSON: use 2-space indentation.

## Reporting security issues
If you discover a real security issue outside this intentionally vulnerable lab (e.g., an accidental secret leak), do **not** open a public issue. Contact the repo owner or send an email to the maintainer listed in `MAINTAINERS.md`.

