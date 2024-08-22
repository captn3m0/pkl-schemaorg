import datetime
import os
from pathlib import Path
from typing import Union, Set, Tuple, Callable

import jinja2

from constants import data_type_map, PACKAGE_NAME
from jinja import jinja_env
from models import PklClass, PklProperty


class SchemaOrg:
    def __init__(
        self,
        schema_org: dict[str, dict],
        type_map: dict[str, tuple],
        type_specificity: dict[str, int],
    ):
        self.schema_org = schema_org
        self.pkl_classes: dict[str, Union[PklClass, tuple]] = dict()
        self._type_specificity = dict(type_specificity)

    def get_all_classes(self):
        return [
            k.strip().split(":")[-1]
            for k, v in self.schema_org.items()
            if v["@type"] != "rdf:Property"
        ]

    def get_class_by_name(self, name: str) -> dict:
        return self.schema_org[f"schema:{name}"]

    @staticmethod
    def update_imports(
        imports: list[str], type: str, class_path: str = "", classes_: set = set()
    ) -> list[str]:
        return imports.append(type) or []

    @staticmethod
    def _to_set(_object, prop="@id") -> Set[str]:
        if isinstance(_object, list):
            return set(item[prop] if prop is not None else item for item in _object)
        elif _object is None:
            return set()
        else:
            return {_object[prop] if prop is not None else _object}

    @staticmethod
    def cast_description(description):
        return description if isinstance(description, str) else description["@value"]

    def _get_including_types(self, field: dict) -> list[str]:
        return [
            incl_type.strip().split(":")[-1]
            for incl_type in self._to_set(field.get("schema:rangeIncludes"))
        ]

    # Return all fields that belong to model
    def _fields_for_model(self, name: str) -> list[Tuple[str, dict]]:
        return [
            (key.strip().split(":")[-1], field)
            for key, field in self.schema_org.items()
            if (
                field.get("@type") == "rdf:Property"
                and f"schema:{name}" in self._to_set(field.get("schema:domainIncludes"))
            )
        ]

    def extract_fields(self, name: str) -> (list[PklProperty], list[str]):
        fields: list[PklProperty] = []
        imports = []
        for key, field in self._fields_for_model(name):
            field_parent_types = self._get_including_types(field)

            field_types = [type_name for type_name in field_parent_types]
            pkl_types = ()
            for field_type in sorted(
                field_types,
                key=lambda ft: self._type_specificity.get(ft, 0),
                reverse=True,
            ):
                if field_type in data_type_map:
                    pkl_types += (data_type_map[field_type],)
                    if "." in data_type_map[field_type]:
                        imports = self.update_imports(
                            imports,
                            #class_path=f"{data_type_map[field_type][1]}",
                            #classes_={data_type_map[field_type][2]},
                            type=data_type_map[field_type],
                        )

                if name == field_type:
                    pkl_types += (field_type,)

            if field_parent_types != field_types:
                pkl_types = pkl_types + ("Any",)

            if not "String" in pkl_types:
                pkl_types += ("String",)

            type_tuple = "|".join(pkl_types)

            if not pkl_types:
                continue
            elif len(pkl_types) > 1:
                imports = []
                optional = pkl_types[-1] != "Any"
                pkl_types = f"Listing<{type_tuple}>|{type_tuple}"
                if optional:
                    pkl_types = f"({pkl_types})?"
            else:
                pkl_types = (
                    type_tuple
                    if type_tuple == "Any"
                    else f"(Listing<{type_tuple}>|{type_tuple})?"
                )
            fields.append(
                PklProperty(
                    name=key,
                    description=self.cast_description(
                        self.schema_org[f"schema:{key}"].get("rdfs:comment", "")
                    ),
                    type=pkl_types,
                )
            )
        return fields, imports

    def load_type(self, name: str) -> PklClass:
        if name in self.pkl_classes:
            # print(f"{name} exists, skipping..")
            return self.pkl_classes[name]
        try:
            node = self.get_class_by_name(name)
        except KeyError:
            raise ValueError(f"Model {name} does not exist")

        fields, imports = self.extract_fields(name)
        parents, depth = self.extract_parents(node)

        for parent in parents:
            imports = self.update_imports(
                imports,
                class_path=f"{PACKAGE_NAME}.{parent.valid_name}",
                classes_={parent.valid_name},
                type="parent",
            )

        self.pkl_classes[name] = PklClass(
            name=name,
            description=self.cast_description(node.get("rdfs:comment", "")),
            fields=list(fields),
            parents=parents,
            depth=depth,
            field_imports=list(filter(lambda x: x.type == "field", imports)),
            # forward_refs=forward_refs
        )

        with open(
            f"{PACKAGE_NAME}/{self.pkl_classes[name].valid_name}.pkl", "w"
        ) as model_file:
            with open(
                Path(__file__).parent / "templates/model.pkl.tpl"
            ) as template_file:
                template = jinja_env.from_string(template_file.read())
                template_args = dict(
                    schemaorg_version=os.getenv("SCHEMAORG_VERSION"),
                    commit=os.getenv("COMMIT"),
                    jinja2_version=jinja2.__version__,
                    timestamp=datetime.datetime.now(),
                    model=self.pkl_classes[name],
                )
            template.stream(**template_args).dump(model_file)
        # if name == "Airport":
            # breakpoint()
        return self.pkl_classes[name]

    # @staticmethod
    # def _filter_forward_refs(forward_refs: list[str]) -> list[str]:
    #     a: dict[str, Union[set, None]] = {}
    #     for forward_ref in forward_refs:
    #         if a.get(forward_ref.classPath, None):
    #             a[forward_ref.classPath].update(forward_ref.classes_)
    #         else:
    #             a[forward_ref.classPath] = forward_ref.classes_
    #     return [Import(type='forward_ref', classPath=k, classes_=v) for k, v in a.items()]

    def extract_parents(self, node) -> (list[PklClass], int):
        parent_names = set(
            reference.strip().split(":")[-1]
            for reference in self._to_set(node.get("rdfs:subClassOf", []))
        )

        node_types = node["@type"] if type(node["@type"]) == list else [node["@type"]]

        for node_type in node_types:
            if node_type.startswith("schema:"):
                parent_names.add(node_type.strip().split(":")[-1])

        parents: list[PklClass] = []

        # forward_refs = []
        for parent_name in parent_names:
            parent = self.load_type(parent_name)
            parents.append(self.load_type(parent_name))
            # forward_refs += parent.field_imports + parent.forward_refs

        parent_depth = next(
            map(lambda y: y.depth, sorted(parents, key=lambda x: x.depth)), 0
        )
        sorted_parents = list(
            map(
                lambda y: y,
                sorted(parents, key=lambda x: x.depth, reverse=True),
            )
        )
        depth = parent_depth + 1

        # if not sorted_parents:
        #     sorted_parents = [
        #         PklClass(
        #             name="SchemaOrgBase",
        #             description="",
        #             fields=[],
        #             parents=[],
        #             field_imports=[],
        #         )
        #     ]

        # return sorted_parents, self._filter_forward_refs(forward_refs), depth
        return sorted_parents, depth

    def write_init(self):
        with open(f"{PACKAGE_NAME}/PklProject", "w") as init_file:
            with open(
                Path(__file__).parent / "templates/_PklProject.tpl"
            ) as template_file:
                template = jinja_env.from_string(template_file.read())

                template_args = dict(
                    schemaorg_version=os.getenv("SCHEMAORG_VERSION"),
                    # commit=os.getenv("COMMIT"),
                    # jinja2_version=jinja2.__version__,
                    # timestamp=datetime.datetime.now(),
                    # all_classes=sorted(self.pkl_classes.values(), key=lambda x: x.depth),
                )
            template.stream(**template_args).dump(init_file)
