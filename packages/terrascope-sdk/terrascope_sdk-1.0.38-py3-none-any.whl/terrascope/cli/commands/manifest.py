import click
import asyncio
import pandas as pd
import yaml
import os
import json
import terrascope.cli.lib.utils as tsu
from terrascope.cli.lib.aliased_group import AliasedGroup
import terrascope.cli.lib.workflow as wf
from google.protobuf.json_format import MessageToDict


@click.command(cls=AliasedGroup, help="'manifest' command group")
@click.pass_context
def manifest(ctx):
    pass


@manifest.command('get')
@click.pass_context
@click.option('-ia', '--algorithm_id', type=str,
              help="UUID of the algorithm to look up the algorithm_versions.")
@click.option('-iv', '--algorithm_version_id', type=str,
              help="UUID of the algorithm_version to look up.")
@click.option('-n', '--algorithm_name', type=str,
              help="Name of the algorithm to look up the algorithm_versions.  All matching algos will be queries")
@click.option('-om', '--output_manifest', type=str,
              help="Write manifest to this filename.", default=None)
def algorithm_version_get(
        ctx,
        algorithm_id,
        algorithm_version_id,
        algorithm_name,
        output_manifest=None,
):
    columns = ['id', 'created_on', 'algorithm.name', 'algorithm.author']

    # if they provide an explicit algo version ID, get it.
    algo_versions = []
    if algorithm_version_id:
        algo_versions += asyncio.run(wf.get_algorithm_versions(algorithm_version_id=algorithm_version_id))

    # if they provide a algorithm_id or name, look up the algo versions and get them.
    algorithm_ids = []
    if algorithm_id is not None:
        algorithm_ids = [algorithm_id]
    if algorithm_name is not None:
        algos = asyncio.run(wf.list_algorithms(algorithm_name))
        algorithm_ids += [algo.id for algo in algos]

    for algorithm_id in algorithm_ids:
        algo_versions += asyncio.run(wf.get_algorithm_versions(algorithm_id=algorithm_id))

    # print the results
    if algo_versions:
        data = []
        for algo_version in algo_versions:
            algo_version_dict = tsu.protobuf_to_dict(algo_version)
            data.append(algo_version_dict)

        df = pd.DataFrame(data=data)
        if 'all' not in columns:
            df = df[tsu.match_columns(df.columns, columns)]
        df = df.rename(columns={'id': 'algorithm_version_id'})
        tsu.set_pandas_display()
        click.secho(f"algorithm_id: {algorithm_id}", fg='cyan')
        click.echo(df)

    if output_manifest:
        n_versions = len(algo_versions)
        for algo_version in algo_versions:

            manifest = MessageToDict(algo_version.manifest)
            algorithm_id = algo_version.algorithm.id
            manifest['algorithm_id'] = algorithm_id
            manifest['algorithm_name'] = algo_version.algorithm.name

            output_manifest_fname = output_manifest
            if n_versions > 1:
                fname, ext = os.path.splitext(output_manifest)
                output_manifest_fname = f"{fname}_{algorithm_id[:8]}.{ext}"
            with open(output_manifest_fname, 'w') as fp:
                if output_manifest.endswith('json'):
                    json.dump(manifest, fp, indent=4)
                else:
                    yaml.dump(manifest, fp)
