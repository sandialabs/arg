# HEADER
#                     arg/Aggregation/argAggregate.py
#               Automatic Report Generator (ARG) v. 1.0
#
# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC
# (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
# Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Questions? Visit gitlab.com/AutomaticReportGenerator/arg
#
# HEADER

import os
import yaml

from arg.Common.argMultiFontStringHelper import argMultiFontStringHelper
from arg.DataInterface.argDataInterface import argDataInterface
from arg.Aggregation.argAggregator import argAggregator


# Load supported types
common_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(common_dir, "../Common/argTypes.yml"), 'r', encoding="utf-8") as t_file:
    supported_types = yaml.safe_load(t_file)

# Retrieve supported verbosity levels
verbosity_levels = supported_types.get("VerbosityLevels")



def arg_aggregate(backend, request_params):
    """Decide which aggregation operation is to be performed
    """

    # Switch between different aggregation types
    request_name = request_params["name"]
    print("[argAggregate] Processing {} request".format(request_name))

    # Instantiate aggregator
    aggregator = argAggregator(backend)

    # Operation show_all_blocks: one 4-view figure and one table per mesh block
    if request_name.startswith("show_all_blocks"):
        # Decide whether mesh edges are to be shown or not
        request_params["edges"] = request_name.endswith("with_edges")

        # Add specific request parameters
        request_params.setdefault("view_direction", ())

        # Retrieve model file
        model_file = request_params.get("model")
        file_names = {"model": model_file}

        # Try to retrieve model data
        if model_file:
            model_data = argDataInterface.factory(
                "ExodusII",
                os.path.join(backend.Parameters.DataDir, model_file),
                request_params.get("var_name", ''))
        else:
            model_data = None
        data = {"model": model_data}

        # Aggregate
        if model_data:
            aggregator.show_all_blocks(
                request_params, data, file_names,
                (int(request_params.get("verbosity", 0)) > 0))

    # Operation show_enumerated_fields: one figure page per field
    elif request_name == "show_enumerated_fields":
        # Decide whether mesh edges are to be shown or not
        request_params["edges"] = request_name.endswith("with_edges")

        # Add specific request parameters
        request_params.setdefault("view_direction", ())
        var_names = request_params.get("var_names")
        if not var_names:
            print("*  WARNING: no variable names provided for {}".format(
                request_name))
            return

        # Get handle on data
        file_name = request_params["model"]
        data = [argDataInterface.factory(
            "ExodusII",
            os.path.join(backend.Parameters.DataDir, file_name), v, False)
            for v in var_names]

        # Aggregate
        if data:
            aggregator.show_enumerated_fields(
                request_params, data, file_name)

    # Operation show_all_modes: one figure every n_cols x n_rows modes
    elif request_name.startswith("show_all_modes"):
        # Decide whether mesh edges are to be shown or not
        request_params["edges"] = request_name.endswith("with_edges")

        # Add specific request parameters
        request_params.setdefault("view_direction", ())
        request_params.setdefault("displacement", 2.)
        request_params.setdefault("n_cols", 4)
        request_params.setdefault("n_rows", 4)

        # Get handle on data
        file_name = request_params["model"]
        data = argDataInterface.factory(
            "ExodusII",
            os.path.join(backend.Parameters.DataDir, file_name),
            request_params.get("var_name", "Disp"),
            False)

        # Aggregate
        aggregate.show_all_modes(
            request_params, data, file_name)

    # Operation show_mesh_surface: create one figure for the entire mesh
    elif request_name.startswith("show_mesh_surface"):
        # Decide whether mesh edges are to be shown or not
        request_params["edges"] = request_name.endswith("with_edges")

        # Add specific request parameters
        request_params.setdefault("view_direction", ())

        # Get handle on data
        file_name = request_params["model"]
        file_type = request_params["type"]
        if file_type == "ExodusII":
            third_param = request_params.get("var_name", '')
        elif file_type == "vtkSTL":
            third_param = request_params.get("merge", "True")
        else:
            third_param = None
        data = argDataInterface.factory(
            file_type,
            os.path.join(backend.Parameters.DataDir, file_name),
            third_param)

        # Aggregate
        if data:
            aggregator.show_mesh_surface(
                request_params, data, file_name)

    # Operation show_CAD_metadata: create one table per reported CAD metadata
    elif request_name == "show_CAD_metadata":

        # Get handle on data and ensure it has the right type
        metadata = request_params.get("metadata")

        # Aggregate
        if metadata:
            aggregator.show_CAD_metadata(request_params, metadata)
