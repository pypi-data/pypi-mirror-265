import re
from typing import Optional

from yamllint import linter, config

from gha_ci_detector.Job import Job
from gha_ci_detector.Step import Step
from gha_ci_detector.Workflow import Workflow


def files_should_be_indented_correctly(workflow: Workflow) -> None:
    yaml_config = config.YamlLintConfig("{extends: default, rules: {document-start: false}}")
    problems = list(linter.run(workflow.file_content, yaml_config))
    if len(problems) > 0:
        workflow.smells.add("Avoid incorrectly indented workflows")
        # Maybe this needs to be renamed to correctly formatted workflows?


def external_actions_must_have_permissions_workflow(workflow: Workflow) -> None:
    """
    Check if the change adds 'permission' and if we are using an external action.
    Make sure we distinguish between job and workflow
    # TODO: Do gh default actions also require permissions?
    :param workflow:
    :return:
    """
    if "permissions" in workflow.yaml.keys():
        return

    # Are we using secrets?
    jobs_using_secrets = []
    if ("secrets.GITHUB_TOKEN" in str(workflow.yaml) or
            "secrets.GH_BOT_ACCESS_TOKEN" in str(workflow.yaml)):
        jobs_using_secrets = list(filter(lambda j: "secrets.GITHUB_TOKEN" in str(j.yaml)
                                                   or "secrets.GH_BOT_ACCESS_TOKEN" in str(j.yaml),
                                         workflow.get_jobs()))
    # We have jobs with secrets.GITHUB_TOKEN
    if len(jobs_using_secrets) > 0:
        # There is no global permissions set
        for job in jobs_using_secrets:
            if not job.has_permissions():
                workflow.smells.add("Use permissions whenever using Github Token")

    for job in workflow.get_jobs():
        if job.has_permissions():
            continue
        for step in job.get_steps():
            if "uses" in step.yaml.keys():
                workflow.smells.add("Define permissions for workflows with external actions")


def pull_based_actions_on_fork(workflow: Workflow) -> None:
    """
    Check if the 'if' statement is added somewhere, also make sure that the action we are doing
    is 'the correct one'
    TODO: There is a paper classifying workflows, check what they did?
    :param workflow:
    :return:
    """

    def is_pull_based_name(name) -> bool:
        return ("pr" in name or "issue" in name or "issues" in name or "review" in
                name or "branch" in name or "pull request" in name
                or "pull_request" in name or "pull-request" in name or "label" in name)

    pull_based_workflow = ("name" in workflow.yaml.keys()
                           and is_pull_based_name(workflow.yaml["name"]))

    for job in workflow.get_jobs():
        job_has_if = job.get_if() is not None and ("github.repository" in job.get_if() or
                                                   "github.repository_owner" in job.get_if())
        if is_pull_based_name(job.name) or pull_based_workflow:
            # We expect an if statement on the job
            if not job_has_if:
                workflow.smells.add("Prevent running issue/PR actions on forks")
        # Otherwise we need to check
        elif not job_has_if:
            for step in job.get_steps():
                step_has_if = step.get_if() is not None and ("github.repository" in step.get_if() or
                                                             "github.repository_owner" in step.get_if())
                if is_pull_based_name(str(step.yaml)) and not step_has_if:
                    workflow.smells.add("Prevent running issue/PR actions on forks")

            # TODO: Maybe we can extend this further?


def running_ci_when_nothing_changed(workflow: Workflow) -> None:
    """
    CI includes building, testing, linting.
    TODO: Double check that we are actually doing some CI
    related tasks
    :param workflow:
    :return:
    """
    ci_list = ["lint", "build", "test", "compile", "style", "ci", "codeql", "cypress"]
    is_ci_file_name = any(word in workflow.name.lower() for word in ci_list)
    is_ci_in_workflow = any(
        word in str(workflow.yaml).lower() for word in ci_list)
    if is_ci_in_workflow or is_ci_file_name:
        if "on" not in workflow.get_keys():
            workflow.smells.add("Avoid running CI related actions when no source code has changed")
        elif (isinstance(workflow.yaml["on"], dict) and ("paths-ignore" not in str(workflow.yaml[
                                                                                       "on"])) and (
                      "paths" not in str(workflow.yaml["on"]))):
            workflow.smells.add("Avoid running CI related actions when no source code has changed")


def use_fixed_version_runs_on(workflow: Workflow) -> None:
    """
    Runs on should use a fixed version and not 'latest'
    :param workflow:
    :return:
    """
    lines = workflow.file_content.split("\n")
    runs_on_lines = list(filter(lambda x: "runs-on" in x and "latest" in x, lines))
    for line in runs_on_lines:
        line_nr = lines.index(line)
        workflow.smells.add(f"Use fixed version for runs-on argument (line {line_nr})")


def use_specific_version_instead_of_dynamic(workflow: Workflow) -> None:
    """
    Check if a version is updated to contain more dots or is changed from latest to something
    else or is updated to be a hash value
    Using tags is as versions for actions is a known security problem
    :param workflow:
    :return:
    """
    lines = workflow.file_content.split("\n")
    uses_lines = filter(lambda x: "uses:" in x, lines)
    for line in uses_lines:
        line_nr = lines.index(line)
        versions = line.split("@")
        if len(versions) == 1:
            workflow.smells.add(f"Use commit hash instead of tags for action versions (line "
                                f"{line_nr})")
            continue
        if "v" in versions[1] or "." in versions[1]:
            workflow.smells.add(f"Use commit hash instead of tags for action versions (line "
                                f"{line_nr})")


def action_should_have_timeout(workflow: Workflow) -> None:
    """
    TODO: Try to compile a list of actions on github which tend to run long?
          Or try to compile a list of actions which access the outside world?
          Differentiate between jobs having a timeout and steps having a timeout.
          Jobs should be good practice and specific steps should be smell?
    :param change:
    :return:
    """
    for job in workflow.get_jobs():
        if "timeout-minutes" not in job.yaml.keys():
            workflow.smells.add("Avoid jobs without timeouts")


def use_cache_from_setup(workflow: Workflow) -> None:
    """
    Many setup/install actions such as `setup-node` already provide a cache for the downloaded libraries
    Should it be desirable to have the cache param even when they are not yet doing caching?
    :param workflow:
    :return:
    """
    cacheable_actions = ["actions/setup-python", "actions/setup-java", "actions/setup-node"]
    for job in workflow.get_jobs():
        is_cachable_action = False
        is_cache_action = False
        for index, step in enumerate(job.get_steps()):
            is_cachable_action = ("uses" in step.yaml.keys() and any(action in str(step.yaml) for
                                                                     action in cacheable_actions)
                                  or is_cachable_action)
            is_cache_action = is_cache_action or "cache" in str(step.yaml)

        if is_cache_action and is_cachable_action:
            workflow.smells.add("Use cache parameter instead of cache option")


def scheduled_workflows_on_forks(workflow: Workflow) -> None:
    on_dict = workflow.get_on()
    if on_dict is not None and isinstance(on_dict, dict) and "schedule" in on_dict.keys():
        # We are dealing with a cron workflow
        for job in workflow.get_jobs():
            if_statements = ["github.repository", "github.repository_owner"]
            if job.get_if() is None:
                workflow.smells.add("Avoid executing  scheduled workflows on forks")
                continue
            if not any(word in job.get_if() for word in if_statements):
                workflow.smells.add("Avoid executing  scheduled workflows on forks")


def use_name_for_step(workflow: Workflow) -> None:
    for job in workflow.get_jobs():
        for step in job.get_steps():
            if "name" not in step.yaml.keys():
                (start, end) = step.get_line_numbers(workflow.get_line_number)
                workflow.smells.add(f"Use names for run steps (lines {start}:{end})")


def stop_workflows_for_old_commit(workflow: Workflow) -> None:
    """
    TODO: How to differentiate between branch and PR?
          Should this apply for every kind of workflow?
    :param workflow:
    :return:
    """
    if "concurrency" not in workflow.yaml.keys():
        workflow.smells.add("Avoid starting new workflow whilst the previous one is still running")
        workflow.smells.add("Stop running workflows when there is a newer commit in branch")
        workflow.smells.add("Stop running workflows when there is a newer commit in PR")


def upload_artifact_must_have_if(workflow: Workflow) -> None:
    for job in workflow.get_jobs():
        for step in job.get_steps():
            if "uses" in step.yaml.keys() and ("actions/upload-artifact" in step.yaml["uses"] or
                                               "coverallsapp/github-action" in step.yaml["uses"]):
                if step.get_if() is None:
                    stripped = step.yaml["uses"].strip()
                    line_nr = workflow.get_line_number(f"uses: {stripped}".replace(" ", ""),
                                                       use_whitespace=False)
                    workflow.smells.add(f"Use 'if' for upload-artifact action (line {line_nr})")
                else:
                    if not (("github.repository" in step.get_if() or "github.repository_owner"
                             in step.get_if()) and (
                                    job.get_if() is not None and (
                                    "github.repository" in job.get_if()
                                    or "github.repository_owner" in job.get_if()))):
                        workflow.smells.add("Avoid uploading artifacts on forks")
            elif step.get_name() is not None and "upload" in step.get_name().lower():
                if (step.get_if() is None) or not (("github.repository" in step.get_if() or
                                                    "github.repository_owner"
                                                    in step.get_if()) and (
                                                           job.get_if() is not None and (
                                                           "github.repository" in job.get_if()
                                                           or "github.repository_owner" in job.get_if()))):
                    (start, end) = step.get_line_numbers(workflow.get_line_number)
                    workflow.smells.add(f"Avoid uploading artifacts on forks (line {start}:{end})")


def multi_line_steps(workflow: Workflow) -> None:
    """
    TODO: This smell still needs to be renamed
    :param workflow:
    :return:
    """
    for job in workflow.get_jobs():
        for step in job.get_steps():
            if "run" in step.yaml.keys():
                run = step.yaml["run"]
                if "\n" in run or "&&" in run:
                    line_nr = workflow.get_line_number(run.split("\n")[0])
                    workflow.smells.add(f"Steps should only perform a single command (line "
                                        f"{line_nr})")


def comment_in_workflow(workflow: Workflow) -> None:
    source_code = workflow.file_content
    if not source_code.startswith("#"):
        workflow.smells.add("Avoid workflows without comments")


def deploy_from_fork(workflow: Workflow) -> None:
    if "deploy" in workflow.name:
        for job in workflow.get_jobs():
            if job.get_if() is None and ("github.repository" in job.get_if() or
                                         "github.repository_owner"
                                         in job.get_if()):
                workflow.smells.add("Avoid deploying from forks")

    for job in workflow.get_jobs():
        if "deploy" in job.name:
            if job.get_if() is None and ("github.repository" in job.get_if() or
                                         "github.repository_owner"
                                         in job.get_if()):
                workflow.smells.add("Avoid deploying from forks")


def run_multiple_versions(workflow: Workflow) -> None:
    def job_has_setup_action_with_version(job: Job) -> bool:
        setup_step: list[Step] = filter(lambda s: s.get_uses() is not None and "actions/setup" in
                                                  s.get_uses(), job.get_steps())
        for step in setup_step:
            if "node" in step.get_uses():
                if "with" in step.yaml.keys() and "node-version" in step.yaml["with"].keys():
                    if "matrix" in step.yaml["with"]["node-version"]:
                        return True
                    else:
                        return False
                else:
                    return False
            if "java" in step.get_uses():
                if "with" in step.yaml.keys() and "java-version" in step.yaml["with"].keys():
                    if "matrix" in step.yaml["with"]["java-version"]:
                        return True
                    else:
                        return False
                else:
                    return False

    has_build = "build" in workflow.name.lower() or "test" in workflow.name.lower()
    for job in workflow.get_jobs():
        if has_build or "build" in str(job.yaml).lower() or "test" in str(job.yaml).lower():
            if not ("matrix" in job.yaml.keys() and "matrix" in job.yaml["runs-on"]):
                workflow.smells.add("Run tests on multiple OS's")
            if not ("matrix" in job.yaml.keys() and job_has_setup_action_with_version(job)):
                workflow.smells.add("Run CI on multiple language versions")


def installing_packages_without_version(workflow: Workflow) -> None:
    for job in workflow.get_jobs():
        for step in job.get_steps():
            if "run" in step.yaml.keys():
                run = step.yaml["run"]
                lines = run.split("\n")
                for l in lines:
                    if "install" in l:
                        version = re.search("(==[0-9]+.[0-9]+.[0-9]+)", l)
                        if version is None:
                            line_nr = workflow.get_line_number(l.strip())
                            workflow.smells.add("Avoid installing packages without version (line "
                                                f"{line_nr})")


def running_workflow_through_bot(workflow: Workflow) -> None:
    for job in workflow.get_jobs():
        if job.get_if() is None or "github.actor !=" in job.get_if():
            workflow.smells.add("Avoid running workflow when a bot has made a change in the repo")


def detect_yaml_duplication(workflows: list[Workflow]) -> Optional[str]:
    jobs = {}
    for w in workflows:
        for j in w.get_jobs():
            key = w.name + "-" + j.name
            step_list = []
            for index in range(0, len(j.get_steps()) - 2):
                step_list.append([j.get_steps()[index], j.get_steps()[index + 1], j.get_steps()[
                    index + 2]])
            jobs[key] = step_list
    for key in jobs.keys():
        for key1 in jobs.keys():
            if key == key1:
                continue
            else:
                l1 = jobs[key]
                for l in l1:
                    if l in jobs[key1]:
                        return "Avoid job duplication"
    return None
