#!/usr/bin/env python3

from aws_cdk import core

from glue_datacatalog.glue_datacatalog_stack import GlueDatacatalogStack


app = core.App()
GlueDatacatalogStack(app, "glue-datacatalog")

app.synth()
