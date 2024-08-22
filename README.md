# pydantic2_schemaorg

[![PyPi version](https://img.shields.io/pypi/v/pydantic2-schemaorg.svg)](https://pypi.python.org/pypi/pydantic2-schemaorg/)
[![](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![](https://img.shields.io/github/license/blurry-dev/pydantic2_schemaorg.svg)](https://github.com/blurry-dev/pydantic2_schemaorg/blob/master/LICENSE)

Use [Schema.org](https://schema.org) types in [pydantic](https://pydantic-docs.helpmanual.io/)!

**pydantic2_schemaorg** contains all the models defined by schema.org. The pydantic classes are auto-generated from the
schema.org model definitions that can be found
on [https://schema.org/version/latest/schemaorg-current-https.jsonld](https://schema.org/version/latest/schemaorg-current-https.jsonld)

## Requirements

Works with python >= 3.10

## How to install

```python
pip install pydantic2-schemaorg
```

Import any class you want to use by with the following convention

```python
from pydantic2_schemaorg.<SCHEMAORG_MODEL_NAME> import <SCHEMAORG_MODEL_NAME>
```

A full (hierarchical) list of Schema.org model names can be found [here](https://schema.org/docs/full.html)

## Example usages

```python
from pydantic2_schemaorg.ScholarlyArticle import ScholarlyArticle

scholarly_article = ScholarlyArticle(
    url='https://github.com/blurry-dev/pydantic2-schemaorg/pydantic2_schemaorg',
    sameAs='https://github.com/blurry-dev/pydantic2-schemaorg/pydantic2_schemaorg',
    copyrightNotice='Free to use under the MIT license',
    dateCreated='15-12-2021'
)
print(scholarly_article.json())
```

```json
{"@type": "ScholarlyArticle", "url": "https://github.com/blurry-dev/pydantic2-schemaorg/pydantic2_schemaorg", "sameAs": "https://github.com/blurry-dev/pydantic2-schemaorg/pydantic2_schemaorg", "copyrightNotice": "Free to use under the MIT license", "dateCreated": "15-12-2021"}
```
