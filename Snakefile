CV_BIB_DATASETS = glob_wildcards("src/CV/bibs/{dataset}.bib").dataset
CV_BIB_CONFIGS = expand("src/CV/bib_{dataset}.yml", dataset=CV_BIB_DATASETS)


rule make_bib_configs:
    input:
        bib="src/CV/bibs/{dataset}.bib",
        script="src/CV/scripts/test_bib2rendercv.py",
    output:
        "src/CV/bib_{dataset}.yml",
    conda:
        "envs/rendercv.yaml"
    shell:
        "python {input.script} {input.bib} {output} --user-name 'Bar, F.'"


rule combine_CV_configs:
    input:
        template="src/CV/configs/template.yaml",
        cv="src/CV/configs/cv.yaml",
        bibs=CV_BIB_CONFIGS,
    output:
        "src/CV/config.yml",
    conda:
        "envs/rendercv.yaml"
    shell:
        'yq -n \'load("{input.template}") as $template | '
        'load("{input.cv}").cv as $cv | '
        "($cv | .sections = (.sections * $template.cv.sections)) as $merged | "
        "($template | .cv = $merged) | "
        '(.. | select(has("file"))) |= load(.file)\' > {output}'


rule make_CV:
    input:
        config=rules.combine_CV_configs.output,
        design="src/CV/configs/design.yaml",
        locale="src/CV/configs/locale.yml",
    output:
        directory("src/CV/rendercv_output"),
        "src/CV/rendercv_output/FOO_BAR_CV.pdf",
    conda:
        "envs/rendercv.yaml"
    shell:
        "rendercv render {input.config} --design {input.design} --locale-catalog {input.locale}"


rule make_motivation_letter:
    input:
        "src/motivation_letter/Tectonic.toml",
        "src/motivation_letter/src/_postamble.tex",
        "src/motivation_letter/src/_preamble.tex",
        "src/motivation_letter/src/index.tex",
    output:
        "src/motivation_letter/build/motivation_letter_FOOBAR/motivation_letter_FOOBAR.pdf",
    conda:
        "envs/tectonic.yaml"
    shell:
        "cd src/motivation_letter && tectonic -X build --keep-logs --print"


rule make_research_plan:
    input:
        "src/research_plan/Tectonic.toml",
        "src/research_plan/src/_postamble.tex",
        "src/research_plan/src/_preamble.tex",
        "src/research_plan/src/index.tex",
    output:
        "src/research_plan/build/research_plan_FOOBAR/research_plan_FOOBAR.pdf",
    conda:
        "envs/tectonic.yaml"
    shell:
        "cd src/research_plan && tectonic -X build --keep-logs --print"


rule copy_final_build:
    default_target: True
    input:
        "src/CV/rendercv_output/FOO_BAR_CV.pdf",
        rules.make_motivation_letter.output,
        rules.make_research_plan.output,
    output:
        "build/FOO_BAR_CV.pdf",
        "build/motivation_letter_FOOBAR.pdf",
        "build/research_plan_FOOBAR.pdf",
    shell:
        "cp {input[0]} {output[0]} && "
        "cp {input[1]} {output[1]} && "
        "cp {input[2]} {output[2]}"
