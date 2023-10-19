# Copyright 2023
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" This script implements the main function.
"""

import sys
import os
import argparse
import checkov_fix_chart
import kubescape_fix_chart
import kics_fix_chart
import count_checks


# Define the argument parser
parser = argparse.ArgumentParser(description='Script to fix Helm Charts based on results from \
                                 security tools and add required functionalities.')

# Add the --check argument
parser.add_argument('--check', action='store_true', help='Fix the chart based on the results \
                                                        of a tool.')
# Add the --add-func argument
parser.add_argument('--add-func', action='store_true', help='Add required functionality to \
                                                            the chart.')

# Add the --add-func argument
parser.add_argument('--docker-run', action='store_true', help='Generate Docker run command')

# Add the --add-func argument
parser.add_argument('--count-checks', action='store_true', help='Count final checks')

# Parse the arguments
args = parser.parse_args()


def main():
    """ The main function.
    """

    # Get chart_folder from ENV
    # For local testing on macOS, add env variables to ~/.zshrc
    chart_folder = os.environ.get("chart_folder")

    tool = os.environ.get("first_tool")

    # Fix the chart based on the results of a tool
    if args.check:
        # Get ENV variables
        iteration = os.environ.get("iteration")
        result_path = f"scan_results_{iteration}.json"

        if iteration == "1":
            chart_folder = f"templates/{chart_folder}"
        elif iteration == "2" or iteration == "3":
            chart_folder = f"fixed_templates/{chart_folder}"

        # Check if there are any failed tests
        if tool == "checkov" or tool == "Checkov":
            checkov_fix_chart.iterate_checks(chart_folder, result_path)

        elif tool == "kics" or tool == "KICS":
            kics_fix_chart.iterate_checks(chart_folder, result_path)

        elif tool == "kubescape" or tool == "Kubescape":
            kubescape_fix_chart.iterate_checks(chart_folder, result_path)

        else:
            print("Tool not supported. Exiting...")
            sys.exit(1)

    # Count final checks
    elif args.count_checks:
        # Get ENV variables
        tool = os.environ.get("second_tool")
        iteration = os.environ.get("iteration")
        result_path = f"scan_results_{iteration}.json"
        count_checks.count_checks(result_path, tool)

    else:
        print("No arguments passed. Exiting...")
        sys.exit(1)


if __name__ == "__main__":
    main()
