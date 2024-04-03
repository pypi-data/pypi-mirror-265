# Running TuxTrigger

## Create Configuration File

To make TuxTrigger work you have to provide configuration .yaml file with declared SQUAD details and repositories data
(url to tracked repository, selected branches and plan.yaml file for TuxSuite Plan).

Example of basic config.yaml

```yaml
repositories:
- url: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
  squad_group: ~pawel.szymaszek
  branches:
    - name: master
      squad_project: tuxtrigger-torvalds-v5.19
      plan: stable.yaml
    - name: v5.19-rc6
      squad_project: tuxtrigger-torvalds-v5.19
      plan: stable_next.yaml
      lava_test_plans_project: lkft
      lab: https://lkft.validation.linaro.org
```

Tuxtrigger enables dynamically generated branch list in config file:

- 'regex' - match branch names in selected repository
- 'default_plan' - plan to be assigned for matched branches
- 'squad_project_prefix' - prefix added to 'squad_project' value in matched branches
- 'default_squad_project' - Use this squad_project value in matched branches
- 'default_lava_test_plans_project' - Use to set value in matched branches
- 'default_lab' - Use to set lab for all matched branches
- 'lava_test_plans_project' - Use to say what project in lava-test-plans to use
- 'lab' - Use to say what LAVA lab to submit jobs to

```yaml
repositories:
- url: https://git.kernel.org/pub/scm/linux/kernel/git/arm64/linux.git
  squad_group: ~pawel.szymaszek
  regex: for-next/*
  default_plan: stable.yaml
  squad_project_prefix: generator
  default_lava_test_plans_project: lkft
  default_lab: https://lkft.validation.linaro.org
  branches:
  - name: for-next/acpi # hardcoded values won't be overwritten
    squad_project: generator-linux-for-next-acpi
    plan: stable_next.yaml
```

Tuxtrigger enables SQAUD project configuration. By setting values in config file you are able to 
create or update squad project.
- in ```config``` section you are able to specify one or more options from listed below

```yaml
config:
  plugins: linux_log_parser,ltp
  wait_before_notification_timeout: 600
  notification_timeout: 28800
  force_finishing_builds_on_timeout: False
  important_metadata_keys: build-url,git_ref,git_describe,git_repo,kernel_version
  thresholds: build/*-warnings
  data_retention: 0
repositories:
- url: https://git.kernel.org/pub/scm/linux/kernel/git/arm64/linux.git
  squad_group: ~pawel.szymaszek
  regex: for-next/*
  default_plan: stable.yaml
  squad_project_prefix: generator
  default_lava_test_plans_project: lkft
  default_lab: https://lkft.validation.linaro.org
  branches:
  - name: for-next/acpi # hardcoded values won't be overwritten
    squad_project: generator-linux-for-next-acpi
    plan: stable_next.yaml
```
To check results of dynamically generated config use "--generate-config" argument.
Tuxtrigger will perform 'dry-run' and prompt generated config.

```shell
tuxtrigger /path/to/config.yaml --generate-config
```

## Create Plan for TuxSuite

!!! note
    TuxTrigger requires valid TuxSuite account with TUXSUITE_TOKEN declared as env var

For sending plan to TuxSuite you must provide relevant plan (and include that in the configuration file)

Example of a plan file
```yaml
version: 1
name: stable_plan
description: stable_plan
jobs:
- tests:
    - {device: qemu-x86_64, tests: [ltp-smoke]}
```
For further information about plans and TuxSuite configuration please Visit: [TuxSuite Home](https://docs.tuxsuite.com/)

!!! note "Usage"
    By default TuxTrigger takes plans from `share/plans` folder Custom path can be set by argument --plan `<path>`
    ```shell
    tuxtrigger path/to/config.yaml --plan=path/to/plan/folder

    ```

## Running TuxTrigger

To run tuxtrigger with the default configuration file:
```shell
tuxtrigger /path/to/config.yaml --plan /path/to/plan_directory
```


