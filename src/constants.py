# schema.org data types to Pkl type constraint https://schema.org/DataType
PACKAGE_NAME = "pkl"
data_type_map = {
    "Boolean": "Boolean",
    "False": "Boolean(this = false)",
    "True": "Boolean(this == true)",
    "Number": "Int|Float",
    "Float": "Float",
    "Integer": "Int",
    "Text": "String",
    "CssSelectorType": "String",
    "PronounceableText": "String",
    "URL": "URL",
    "XPathType": "String",
    "DateTime": "String",
    "Date": "String",
    "Time": "String",
}

data_type_specificity = {
    "Boolean": 1,
    "False": 1,
    "True": 1,
    "Date": 4,
    "DateTime": 5,
    "Time": 4,
    "Number": 3,
    "Float": 4,
    "Integer": 5,
    "Text": 1,
    "CssSelectorType": 1,
    "PronounceableText": 1,
    "URL": 2,
    "XPathType": 1,
}
