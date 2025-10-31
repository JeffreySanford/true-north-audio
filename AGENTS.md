<!-- nx configuration start-->
<!-- Leave the start & end comments to automatically receive updates. -->



# General Guidelines for Working with Nx (True North Audio)


- **Nx-First Workflow:** All build, lint, test, serve, and e2e tasks must be run through Nx (`nx run`, `nx run-many`, `nx affected`) or the provided pnpm scripts. Never use underlying tooling directly (e.g., do not run `eslint` or `jest` directly).
- **Strict Linting:** Lint targets are configured to *never* lint build artifacts (dist, build, out, test-output, etc.). Only source files are linted. This is enforced at both the Nx target and ESLint config level for all projects.
- **Project Analysis:** Use the `nx_workspace` tool to understand the workspace architecture. For individual projects, use the `nx_project_details` tool to analyze structure and dependencies.
- **Configuration & Best Practices:** For Nx configuration, best practices, or uncertainty, always use the `nx_docs` tool for up-to-date documentation. Never assume or guess Nx config details.
- **Feature Development:** For new features (such as multi-section song generation), always update documentation, tests, and ensure strict linting before merging. Use modular Nx libraries for extensibility.
- **CI/CD:** If you encounter CI errors, follow the CI Error Guidelines below. Always validate fixes by re-running the relevant Nx task.


# CI Error Guidelines

If you need to fix an error in the CI pipeline, follow this process:
1. Retrieve the list of current CI Pipeline Executions (CIPEs) using the `nx_cloud_cipe_details` tool.
2. If there are errors, use the `nx_cloud_fix_cipe_failure` tool to get logs for the failed task.
3. Use the logs to diagnose and fix the problem. Use Nx tools and scripts to apply fixes.
4. Always re-run the relevant Nx task to validate the fix. Only mark the issue resolved when the task passes and no build artifacts are linted.


<!-- nx configuration end-->