module org.schema.experimental
import "package://pkg.pkl-lang.org/pkl-pantry/pkl.experimental.uri@1.0.3#/URI.pkl" as URL
{%- if model.field_imports %}
{%- for _import in model.field_imports %}
import "{{_import}}.pkl"
{%- endfor %}
{%- endif %}

{%- set ALLPARENTS = model.parents | sort(attribute='depth', reverse=True) | map(attribute='valid_name') %}
{%- for p in ALLPARENTS %}
import "{{p}}.pkl"
{%- endfor %}

{%- set parents2 = model.parents | sort(attribute='depth', reverse=True) | map(attribute='valid_name') %}
/// {{ model.description | format_description(space=0)}}
///
/// See: <https://schema.org/{{ model.name }}>
/// Model depth: {{model.depth}}
{%- if model.parents %}
open class {{ model.valid_name }} extends{%- for p in parents2 %} {{p}}.{{p}}{%-endfor%} {
{%- else %}
open class {{ model.valid_name }} {
{%- endif %}
    {% for field in model.fields %}    
    /// {{ field.description | replace('\\n','\n') | format_description }}
    {{ field.name }}: {{ field.type }}
    {% endfor %}
}