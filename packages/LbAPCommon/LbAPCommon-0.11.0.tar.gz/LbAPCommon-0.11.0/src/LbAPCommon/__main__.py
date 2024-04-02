###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import argparse
import asyncio
import importlib.resources
import json
import os
import subprocess
import tempfile
from pathlib import Path

import jinja2
import yaml

from LbAPCommon import parse_yaml, render_yaml, validate_yaml
from LbAPCommon.dirac_conversion import (
    group_in_to_requests,
    parse_application_string,
    step_to_production_request,
)

templates = jinja2.Environment(
    loader=jinja2.PackageLoader("LbAPCommon", "data/templates"),
    undefined=jinja2.StrictUndefined,
)


def generate_auto_configuration(prod_name, name, job_data):
    """Generate the auto-configuration for the job."""
    if "files" not in job_data["options"]:
        raise NotImplementedError(
            "generate_configuration is not yet supported for lbexec based jobs"
        )

    render_kwargs = dict(
        application_name=parse_application_string(job_data["application"])["name"],
        data_type=job_data["data_type"],
        input_type=job_data["input_type"],
        luminosity=job_data["luminosity"],
        root_in_tes=job_data["root_in_tes"],
        simulation=job_data["simulation"],
        turbo=job_data["turbo"],
    )
    if job_data["simulation"]:
        render_kwargs["conddb_tag"] = job_data["conddb_tag"]
        render_kwargs["dddb_tag"] = job_data["dddb_tag"]

    autoconf_options = templates.get_template(
        "configure-legacy-application.py.j2"
    ).render(**render_kwargs)

    dynamic_options_path = os.path.join(prod_name, f"{name}_autoconf.py")

    dynamic_options_name = os.path.join(
        "$ANALYSIS_PRODUCTIONS_DYNAMIC", dynamic_options_path
    )
    if job_data["options"].get("command") == ["python"]:
        job_data["options"]["files"].insert(1, dynamic_options_name)
    else:
        job_data["options"]["files"].insert(0, dynamic_options_name)

    return dynamic_options_path, autoconf_options


async def query_dirac(sem, query_script, name, job_data, output_path):
    """Query LHCbDIRAC to get metadata about the job's input."""
    async with sem:
        cmd = [
            "lb-dirac",
            query_script,
            json.dumps(job_data["input"]),
            f"--output={output_path}",
        ]
        if job_data["turbo"]:
            cmd += "--turbo"
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        stdout, _ = await proc.communicate()
        print(f"** Output from querying LHCbDIRAC for {name}:\n{stdout.decode()}")
        if proc.returncode != 0:
            raise RuntimeError(f"Query failed: {name}")
        result = json.loads(output_path.read_text())
        return name, job_data, result


async def main(production_name: str, input_file: Path, output_file: Path):
    """Convert info.yaml into a form which can be understood by LHCbDIRAC."""
    raw_yaml = input_file.read_text()
    sem = asyncio.Semaphore(10)

    rendered = render_yaml(raw_yaml)

    jobs_data, check_data = parse_yaml(rendered)
    validate_yaml(jobs_data, check_data, None, production_name)

    dynamic_files = {
        "__init__.py": "",
        "ap_merger.py": importlib.resources.read_text(
            "LbAPCommon.data", "ap_merger.py"
        ),
    }
    input_specs = {}
    with tempfile.TemporaryDirectory() as tmpdir:
        query_script = Path(tmpdir) / "query_dirac.py"
        query_script.write_text(
            importlib.resources.read_text("LbAPCommon.data", "query_dirac.py")
        )
        query_script.chmod(0o700)

        tasks = []
        for name, job_data in jobs_data.items():
            if "job_name" in job_data["input"]:
                # We'll handle these later
                continue
            tasks.append(
                query_dirac(
                    sem, query_script, name, job_data, Path(tmpdir) / f"{name}.json"
                )
            )

        for name, job_data, result in await asyncio.gather(*tasks):
            # Store the input specs for later use
            input_specs[name] = result["input-spec"]

            # Generate the auto-configuration options
            if job_data["automatically_configure"]:
                if result["auto-conf-error"]:
                    raise NotImplementedError(
                        "Auto-configuration failed", name, result["auto-conf-error"]
                    )

                job_data = result["auto-conf-data"] | job_data
                # Mutate the original value in jobs_data
                jobs_data[name] = job_data

                dynamic_options_path, autoconf_options = generate_auto_configuration(
                    production_name, name, job_data
                )
                if dynamic_options_path in dynamic_files:
                    raise ValueError(f"Duplicate dynamic file: {dynamic_options_path}")
                dynamic_files[dynamic_options_path] = autoconf_options

    # Apply auto-configuration to the jobs that depend on other jobs
    for job_names in group_in_to_requests(jobs_data):
        for job_name in job_names[1:]:
            if "job_name" not in jobs_data[job_name]["input"]:
                raise RuntimeError("This should be impossible")

            input_job_name = jobs_data[job_name]["input"]["job_name"]
            input_job_data = jobs_data[input_job_name]

            # If no input filetype is specified, try to set it automatically
            if "filetype" not in jobs_data[job_name]["input"]:
                if len(input_job_data["output"]) != 1:
                    raise ValueError(
                        f"No input filetype specified for {job_name} but "
                        f"{input_job_name} has multiple output files"
                    )
                jobs_data[job_name]["input"]["filetype"] = input_job_data["output"][0]

            # Validate the input filetype
            if jobs_data[job_name]["input"]["filetype"] not in input_job_data["output"]:
                raise ValueError(
                    f"Input filetype {jobs_data[job_name]['input']['filetype']} "
                    f"for {job_name} not found in {input_job_name}'s output"
                )

            # If the job is not automatically configured there is nothing left to do
            if not jobs_data[job_name]["automatically_configure"]:
                continue

            # Get information about the input job
            if not input_job_data["automatically_configure"]:
                raise ValueError(
                    "Can only automatically configure jobs with automatic input"
                )

            # Copy any missing values from the input job
            jobs_data[job_name].setdefault("input_type", input_job_data["input_type"])
            jobs_data[job_name].setdefault("simulation", input_job_data["simulation"])
            jobs_data[job_name].setdefault("data_type", input_job_data["data_type"])
            if jobs_data[job_name]["simulation"]:
                jobs_data[job_name].setdefault("dddb_tag", input_job_data["dddb_tag"])
                jobs_data[job_name].setdefault(
                    "conddb_tag", input_job_data["conddb_tag"]
                )

            # Generate the auto-configuration options
            dynamic_options_path, autoconf_options = generate_auto_configuration(
                production_name, name, job_data
            )
            if dynamic_options_path in dynamic_files:
                raise ValueError(f"Duplicate dynamic file: {dynamic_options_path}")
            dynamic_files[dynamic_options_path] = autoconf_options

    # Make sure we have at least one job
    if len(jobs_data) == 0:
        raise ValueError("No jobs found")

    # Convert the jobs data to a LHCbDIRAC production in the format expected by LbAPI
    productions = {}
    for job_names in group_in_to_requests(jobs_data):
        input_spec = input_specs[job_names[0]]
        result = {
            "raw-yaml": yaml.safe_dump(
                {x: jobs_data[x] for x in job_names}, sort_keys=False
            ),
            "request": step_to_production_request(
                production_name, jobs_data, job_names, input_spec, "v999999999999"
            ),
            "input-dataset": input_spec,
        }

        name = result["request"][0]["name"].split("#", 2)[-1]
        if name in productions:
            raise ValueError(f"Duplicate production name: {name}")
        productions[name] = result

    metadata = {
        "rendered_yaml": rendered,
        "check_data": check_data,
        "productions": productions,
        "dynamic_files": dynamic_files,
    }
    output_file.write_text(json.dumps(metadata))


def parse_args():
    """Parse the command line arguments and then call main."""
    parser = argparse.ArgumentParser()
    parser.add_argument("production_name", type=str)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--server-credentials", nargs=2)
    args = parser.parse_args()

    asyncio.run(main(args.production_name, args.input, args.output))


if __name__ == "__main__":
    parse_args()
