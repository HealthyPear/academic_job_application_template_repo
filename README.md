# Academic job application template

[![Build PDFs](https://github.com/HealthyPear/academic_job_application_template_repo/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/HealthyPear/academic_job_application_template_repo/actions/workflows/build.yml)
[![Download PDFs](https://img.shields.io/badge/download-PDFs-2ea44f?logo=adobeacrobatreader)](https://github.com/HealthyPear/academic_job_application_template_repo/actions/workflows/build.yml?query=branch%3Amain)
[![Snakemake](https://img.shields.io/badge/Snakemake-9.26.1-239120?logo=snakemake)](https://snakemake.readthedocs.io/)
[![RenderCV](https://img.shields.io/badge/RenderCV-2.8-4051b5)](https://rendercv.com/)
[![Tectonic](https://img.shields.io/badge/Tectonic-0.17.0-555555)](https://tectonic-typesetting.github.io/)

This is a template repository for building academic application documents:

- CV generated with [RenderCV](https://rendercv.com/)
- Motivation letter generated with [Tectonic](https://tectonic-typesetting.github.io/)
- Research plan generated with Tectonic

## Requirements

For the intended workflow, install:

- [VS Code](https://code.visualstudio.com/)
- The [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- A container runtime: [Docker Desktop](https://www.docker.com/products/docker-desktop/) on macOS or Windows, Docker Engine on Linux, or a compatible Podman setup

The repository supplies the Miniforge-based development container and creates the
`dev` Conda environment automatically. The container definition is in
`.devcontainer/devcontainer.json`; `.devcontainer/devcontainer-lock.json` pins
the Dev Container feature versions.

The workflow creates its Snakemake environments from the files in `envs/`.

The workflow dependencies are pinned in those files:

- Snakemake `9.26.1` in `envs/devcontainer.yaml`
- RenderCV `2.8`, BibTeX parser `2.0.0`, PyYAML `6.0.3`, and yq in `envs/rendercv.yaml`
- Tectonic `0.17.0` in `envs/tectonic.yaml`

## Start the Workspace

Open the repository directory in VS Code, then choose **Reopen in Container** when prompted, or run **Dev Containers: Reopen in Container** from the Command Palette. The container setup installs the required VS Code extensions, creates or updates the `dev` environment, and selects its Python interpreter.

Once the container has finished building, no manual package installation or
environment activation is required. The first build may take longer while
Snakemake creates its rule-specific Conda environments.

## Build

From the repository root, run this only when you want to build manually:

```sh
conda run --no-capture-output -n dev snakemake --use-conda -c 3
```

The default target builds all documents and copies the final PDFs to `build/`:

- `build/FOO_BAR_CV.pdf`
- `build/motivation_letter_FOOBAR.pdf`
- `build/research_plan_FOOBAR.pdf`

Intermediate outputs are kept in:

- `src/CV/rendercv_output/`
- `src/motivation_letter/build/`
- `src/research_plan/build/`

## VS Code

The workspace includes a `Snakemake: build` task in `.vscode/tasks.json`, which uses the `dev` environment. The recommended `gruntfuggly.triggertaskonsave` extension runs this task automatically when a workflow input is saved, and the command output appears in the integrated **Terminal** panel.

Saving any workflow input automatically runs the build. This includes the `Snakefile`,
all files under `src/CV/bibs/`, the bibliography conversion script, editable CV config
files under `src/CV/configs/`, the motivation letter and research plan sources, and the
environment YAMLs under `envs/`:

```sh
conda run --no-capture-output -n dev snakemake --use-conda -c 3
```

The save behavior is configured in `.vscode/settings.json`. The task watches:

- `Snakefile`
- BibTeX files under `src/CV/bibs/`
- `src/CV/scripts/test_bib2rendercv.py`
- `src/CV/configs/template.yaml`, `src/CV/configs/cv.yaml`, `src/CV/configs/design.yaml`, and `src/CV/configs/locale.yml`
- Motivation letter and research plan sources
- Environment files under `envs/`

Generated files such as `src/CV/config.yml`, the rendered CV files, and final PDFs are
not save triggers.

The generated CV configuration is `src/CV/config.yml`. It combines the editable
`src/CV/configs/cv.yaml` and `src/CV/configs/template.yaml` with generated bibliography
files under `src/CV/`. Do not edit generated `src/CV/*.yml` files or `src/CV/config.yml`; edit
the BibTeX files or source configuration files instead.

To control automatic builds, open the Command Palette (`Ctrl+Shift+P`) and choose:

- **Trigger Task on Save: Enable** to enable builds after matching files are saved
- **Trigger Task on Save: Disable** to disable automatic builds
- **Trigger Task on Save: Toggle** to switch between enabled and disabled

To build manually, open the Command Palette and choose **Tasks: Run Task**, then **Snakemake: build**. You can also run the same command directly in a terminal:

```sh
conda run --no-capture-output -n dev snakemake --use-conda -c 3
```

To remove workflow-generated outputs from VS Code, choose **Tasks: Run Task**,
then **Snakemake: clean outputs**. This runs Snakemake's `--delete-all-output`
option and does not remove source files or cached rule environments.

To reproduce the workflow from a clean output state, let Snakemake remove all
outputs declared by the workflow, then run the build again:

```sh
find build src/CV/rendercv_output src/motivation_letter/build src/research_plan/build \
	-type f -exec chmod u+w {} + 2>/dev/null
find src/CV -maxdepth 1 -type f \( -name 'bib_*.yml' -o -name 'config.yml' \) \
	-exec chmod u+w {} + 2>/dev/null
conda run --no-capture-output -n dev snakemake --use-conda -c 3 --delete-all-output
conda run --no-capture-output -n dev snakemake --use-conda -c 3
```

Use `--dry-run` with `--delete-all-output` first if you want to preview the
files that will be removed. This command does not remove source files under
`src/CV/configs/`, `src/CV/bibs/`, `src/motivation_letter/src/`, or
`src/research_plan/src/`, and it does not clear Snakemake's `.snakemake/`
metadata or cached rule environments.

## Repository Layout

```text
Snakefile                 Snakemake workflow
src/CV/                    CV source files and RenderCV output
src/motivation_letter/     Motivation letter sources and build output
src/research_plan/         Research plan sources and build output
envs/                      Conda environment definitions
build/                     Final copied PDFs
.vscode/                   Workspace tasks and save automation
```
