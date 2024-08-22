from typing import Optional


class PklProperty:
    name: str
    type: str
    description: Optional[str]
    default: Optional[str]
    required: bool

    def __init__(
        self,
        name: str,
        type: str,
        description: Optional[str],
        default: Optional[str] = None,
        required: bool = False,
    ):
        self.name = name
        self.type = type
        self.description = description
        self.default = default
        self.required = required


class PklClass:
    name: str
    fields: list[PklProperty]
    parents: list[str]
    depth: int = 1
    parent_imports: list[str]
    field_imports: list[str]
    filename: str = ""
    description: str
    valid_name: str

    def __init__(
        self,
        name: str,
        description: str,
        fields: list[PklProperty],
        parents: list[str],
        depth: int = 1,
        parent_imports: list[str] = [],
        field_imports: list[str] = [],
        forward_refs: list[str] = [],
        filename: str = "",
        valid_name: Optional[str] = None,
    ):
        self.name = name
        if valid_name:
            self.valid_name = valid_name
        else:
            self.valid_name = name
        self.description = description
        self.fields = fields
        self.parents = parents
        self.depth = depth
        self.parent_imports = parent_imports
        self.field_imports = field_imports
        # self.forward_refs = forward_refs
        self.filename = filename

    # TODO: @validator("filename", always=True)
    def filename_val(cls, v, values) -> str:
        if not values["valid_name"]:
            raise ValueError()
        filename = values["valid_name"]
        if filename in {
            "class",
            "def",
            "from",
            "import",
            "return",
            "yield",
        }:
            return f"{filename}_"
        return values["valid_name"]
