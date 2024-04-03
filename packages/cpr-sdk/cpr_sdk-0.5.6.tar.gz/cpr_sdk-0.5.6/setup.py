# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cpr_sdk', 'cpr_sdk.models']

package_data = \
{'': ['*'], 'cpr_sdk': ['resources/*']}

install_requires = \
['aws-error-utils>=2.7.0,<3.0.0',
 'boto3>=1.26.16,<2.0.0',
 'datasets>=2.14.0,<3.0.0',
 'deprecation>=2.1.0,<3.0.0',
 'langdetect>=1.0.9,<2.0.0',
 'numpy>=1.23.5',
 'pandas>=1.5.3,<2.0.0',
 'pydantic>=2.4.0,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

extras_require = \
{'spacy': ['spacy>=3.5.1,<4.0.0'],
 'vespa': ['pyvespa>=0.37.1,<0.38.0',
           'pyyaml>=6.0.1,<7.0.0',
           'sentence-transformers>=2.2.2,<3.0.0',
           'torch>=2.0.0,<3.0.0']}

setup_kwargs = {
    'name': 'cpr-sdk',
    'version': '0.5.6',
    'description': '',
    'long_description': '# cpr-sdk\n\nInternal library for persistent access to text data.\n\n> **Warning**\n> This library is heavily under construction and doesn\'t work with any of our open data yet. We\'re working on making it usable for anyone.\n\n## Documents and Datasets\n\nThe base document model of this library is `BaseDocument`, which contains only the metadata fields that are used in the parser.\n\n### Loading from Huggingface Hub (recommended)\n\nThe `Dataset` class is automatically configured with the Huggingface repos we use. You can optionally provide a document limit, a dataset version, and override the repo that the data is loaded from.\n\nIf the repository is private you must provide a [user access token](https://huggingface.co/docs/hub/security-tokens), either in your environment as `HUGGINGFACE_TOKEN`, or as an argument to `from_huggingface`.\n\n```py\nfrom cpr_sdk.models import Dataset, GSTDocument\n\ndataset = Dataset(GSTDocument).from_huggingface(\n    version="d8363af072d7e0f87ec281dd5084fb3d3f4583a9", # commit hash, optional\n    limit=1000,\n    token="my-huggingface-token", # required for private repos if not in env\n)\n```\n\n### Loading from local storage or s3\n\n```py\n# document_id is also the filename stem\n\ndocument = BaseDocument.load_from_local(folder_path="path/to/data/", document_id="document_1234")\n\ndocument = BaseDocument.load_from_remote(dataset_key"s3://cpr-data", document_id="document_1234")\n```\n\nTo manage metadata, documents need to be loaded into a `Dataset` object.\n\n```py\nfrom cpr_sdk.models import Dataset, CPRDocument, GSTDocument\n\ndataset = Dataset().load_from_local("path/to/data", limit=1000)\nassert all([isinstance(document, BaseDocument) for document in dataset])\n\ndataset_with_metadata = dataset.add_metadata(\n    target_model=CPRDocument,\n    metadata_csv="path/to/metadata.csv",\n)\n\nassert all([isinstance(document, CPRDocument) for document in dataset_with_metadata])\n```\n\nDatasets have a number of methods for filtering and accessing documents.\n\n```py\nlen(dataset)\n>>> 1000\n\ndataset[0]\n>>> CPRDocument(...)\n\n# Filtering\ndataset.filter("document_id", "1234")\n>>> Dataset()\n\ndataset.filter_by_language("en")\n>>> Dataset()\n\n# Filtering using a function\ndataset.filter("document_id", lambda x: x in ["1234", "5678"])\n>>> Dataset()\n```\n\n## Search\n\nThis library can also be used to run searches against CPR documents and passages in Vespa.\n\n```python\nfrom src.cpr_sdk.search_adaptors import VespaSearchAdapter\nfrom src.cpr_sdk.models.search import SearchParameters\n\nadaptor = VespaSearchAdapter(instance_url="YOUR_INSTANCE_URL")\n\nrequest = SearchParameters(query_string="forest fires")\n\nresponse = adaptor.search(request)\n```\n\nThe above example will return a `SearchResponse` object, which lists some basic information about the request, and the results, arranged as a list of Families, which each contain relevant Documents and/or Passages.\n\n### Sorting\n\nBy default, results are sorted by relevance, but can be sorted by date, or name, eg\n\n```python\nrequest = SearchParameters(\n    query_string="forest fires",\n    sort_by="date",\n    sort_order="descending",\n)\n```\n\n### Filters\n\nMatching documents can also be filtered by keyword field, and by publication date\n\n```python\nrequest = SearchParameters(\n    query_string="forest fires",\n    filters={\n        "language": ["English", "French"],\n        "category": ["Executive"],\n    },\n    year_range=(2010, 2020)\n)\n```\n\n### Search within families or documents\n\nA subset of families or documents can be retrieved for search using their ids\n\n```python\nrequest = SearchParameters(\n    query_string="forest fires",\n    family_ids=["CCLW.family.10121.0", "CCLW.family.4980.0"],\n)\n```\n\n```python\nrequest = SearchParameters(\n    query_string="forest fires",\n    document_ids=["CCLW.executive.10121.4637", "CCLW.legislative.4980.1745"],\n)\n```\n\n### Types of query\n\nThe default search approach uses a nearest neighbour search ranking.\n\nIts also possible to search for exact matches instead:\n\n```python\nrequest = SearchParameters(\n    query_string="forest fires",\n    exact_match=True,\n)\n```\n\nOr to ignore the query string and search the whole database instead:\n\n```python\nrequest = SearchParameters(\n    year_range=(2020, 2024),\n    sort_by="date",\n    sort_order="descending",\n)\n```\n\n### Continuing results\n\nThe response objects include continuation tokens, which can be used to get more results.\n\nFor the next selection of families:\n\n```python\nresponse = adaptor.search(SearchParameters(query_string="forest fires"))\n\nfollow_up_request = SearchParameters(\n    query_string="forest fires"\n    continuation_tokens=[response.continuation_token],\n\n)\nfollow_up_response = adaptor.search(follow_up_request)\n```\n\nIt is also possible to get more hits within families by using the continuation token on the family object, rather than at the responses root\n\nNote that `this_continuation_token` is used to mark the current continuation of the families, so getting more passages for a family after getting more families would look like this:\n\n```python\nfollow_up_response = adaptor.search(follow_up_request)\n\nthis_token = follow_up_response.this_continuation_token\npassage_token = follow_up_response.families[0].continuation_token\n\nfollow_up_request = SearchParameters(\n    query_string="forest fires"\n    continuation_tokens=[this_token, passage_token],\n)\n```\n\n## Get a specific document\n\nUsers can also fetch single documents directly from Vespa, by document ID\n\n```python\nadaptor.get_by_id(document_id="id:YOUR_NAMESPACE:YOUR_SCHEMA_NAME::SOME_DOCUMENT_ID")\n```\n\nAll of the above search functionality assumes that a valid set of vespa credentials is available in `~/.vespa`, or in a directory supplied to the `VespaSearchAdapter` constructor directly. See [the docs](docs/vespa-auth.md) for more information on how vespa expects credentials.\n\n# Test setup\n\nSome tests rely on a local running instance of vespa.\n\nThis requires the [vespa cli](https://docs.vespa.ai/en/vespa-cli.html) to be installed.\n\nSetup can then be run with:\n\n```\npoetry install --all-extras --with dev\npoetry shell\nmake vespa_dev_setup\nmake test\n```\n\nAlternatively, to only run non-vespa tests:\n\n```\nmake test_not_vespa\n```\n\nFor clean up:\n\n```\nmake vespa_dev_down\n```\n',
    'author': 'CPR Tech',
    'author_email': 'tech@climatepolicyradar.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
