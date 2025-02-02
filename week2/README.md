For question no.1, use this configuration and view the output file:

```yaml
id: postgres_taxi
namespace: de_zoomcamp
description: |
    The CSV Data used in the course: https://github.com/DataTalksClub/nyc-tlc-data/releases

inputs:
    - id: taxi
        type: SELECT
        displayName: Select taxi type
        values: [yellow, green]
        defaults: yellow

    - id: year
        type: SELECT
        displayName: Select year
        values: ["2019", "2020"]
        defaults: "2019"

    - id: month
        type: SELECT
        displayName: Select month
        values: ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        defaults: "01"

variables:
    file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"
    staging_table: "public.{{inputs.taxi}}_tripdata_staging"
    table: "public.{{inputs.taxi}}_tripdata"
    data: "{{outputs.extract.outputFiles[inputs.taxi ~ '_tripdata_' ~ inputs.year ~ '-' ~ inputs.month ~ '.csv']}}"

tasks:
    - id: set_label
        type: io.kestra.plugin.core.execution.Labels
        labels:
            file: "{{render(vars.file)}}"
            taxi: "{{inputs.taxi}}"

    - id: extract
        type: io.kestra.plugin.scripts.shell.Commands
        outputFiles:
            - "*.csv"
        taskRunner:
            type: io.kestra.plugin.core.runner.Process
        commands:
            - wget -qO- https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{{inputs.taxi}}/{{render(vars.file)}}.gz | gunzip > {{render(vars.file)}}

pluginDefaults:
    - type: io.kestra.plugin.jdbc.postgresql
        values:
            url: jdbc:postgresql://host.docker.internal:5432/postgres-zoomcamp
            username: kestra
            password: k3str4
```

For question no.2, note the following `kestra config.yml`:

```yaml
variables:
    file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"
```

The final value of `file` is `green_tripdata_2020-04.csv`.

For question no.3, this can be done using backfills, giving us `24,648,499`.

For question no.4, this can be done using backfills, giving us `1,734,051`.

For question no.5, set `year` to `2021`, `taxi` to `yellow`, and `month` to `03`, giving us `1,925,152`.

For question no.6, this can be found in the documentation:

```yaml
triggers:
    - id: daily
        type: io.kestra.plugin.core.trigger.Schedule
        cron: "@daily"
        timezone: America/New_York
```