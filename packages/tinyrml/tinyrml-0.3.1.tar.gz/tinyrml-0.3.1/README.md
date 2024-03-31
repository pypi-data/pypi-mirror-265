# Tiny RML

The package `tinyrml` is an implementation of a subset of [RML](https://rml.io/specs/rml/) and [R2RML](https://www.w3.org/TR/r2rml/) with some helpful extended features. It is intended to be used as a Python package/library, and accepts Python *iterables* (of `dict`s) as input. It has the following limitations:

  + Mappings cannot specify their sources (tables or SQL queries, or RML's logical sources). Instead, data sources are assigned externally when data is mapped.
  + None of the join-related features are supported. Only a single tabular data source can be mapped at a time.
  + Inverse expressions (`rr:inverseExpression`) are not supported, but similar functionality can be achieved via `rre:expression` (see below).
  + Named graphs are not supported.

The package supports the following extensions to R2RML (note that a special namespace `rre:` is reserved for these extensions):

  + A `dict` key whose value is a Python list is automatically expanded as multiple values/rows.
  + Object maps accept the property `rre:expandAsList`; if true, the value (which is assumed to be a string) is split (using `re.split`) with commas and semicolons acting as separators, and expanded as multiple values/rows. This makes it possible to (say) have a comma-separated list as a quoted value in a cell in your CSV file, read the file using [`csv.DictReader`](https://docs.python.org/3/library/csv.html?highlight=dictreader#csv.DictReader), and expand the list as separate values. Splitting and expansion happens only if `rr:template` has a value in the object map (in cases where you would have used `rr:column`, you can instead introduce a template like `{field}`).
  + Term maps accept the property `rre:expression`, the value of which is a string containing a Python expression. During the mapping process, this expression is evaluated with dict keys ("column names") as variables in the expression.
  + Also object maps accept `rr:class`, allowing objects of generated triples to be typed (the R2RML only supports this for subject maps).
  + In term maps, `rr:column` and `rml:reference` can be used interchangeably (in the original [RML specification](https://rml.io/specs/rml/) `rr:column` is reserved for SQL data sources whereas `rml:reference` is used for all other sources, but very much in a similar role). See notes on template formatting below.

Tiny RML was originally part of [`rdfhelpers`](https://gitlab.com/somanyaircraft/rdfhelpers), but is now split off as its own project. It has no dependencies to `rdfhelpers`.

## Installation

Tiny RML can be installed [from PyPI](https://pypi.org/project/tinyrml/):

```commandline
pip install tinyrml
```

## Usage

Tiny RML exposes the class `Mapper` which is the basic implementation of the mapping functionality. Instances of `Mapper` represent individual mappings (i.e., specific mapping definitions). The class constructor takes the following parameters:

  + `mapping`: a graph (an `rdflib.Graph`) containing the mapping, or a path to a file which, when parsed, yields the mapping graph. This is a required (positional) parameter, the rest are optional.
 + `triples_map_uri=`, when provided (as a `URIRef`), identifies the actual triples map to be used. This is useful when the mapping graph contains several mappings. If the parameter is not provided, `Mapper` will pick the first triples map it finds, and because of the way RDF is parsed and subsequently accessed, this may or may not be the lexically first triples map in the source file.
 + `ignore_field_keys=` is a set of names of keys/fields that are ignored when determining the likely candidate for a key in a template. It defaults to an empty set.
 + `empty_string_is_none=`, when `True` (the default), makes the mapper treat empty strings as missing values.
 + `allow_expressions=`, when `True` (the default), lets the mapper use Python expressions embedded in the mapping graph.
 + `global_bindings=`, when provided, is passed to the `eval()` function (as the parameter `globals=`; see [Python documentation](https://docs.python.org/3/library/functions.html?highlight=eval#eval)) when embedded Python expressions are evaluated. If not provided, "global globals" (default global bindings) are used.
 + `allow_object_map_classes=`, when `True` (the default), lets mappings specify `rr:class` properties for _object maps also_ (the R2RML specification only allows those for subject maps).
 + `input_is_json=`, when `True` (it defaults to `False`), allows the processed input data to consists of JSON objects - say, objects from `json.load()`. The objects are "flattened" so that simplistic JSONPath references (e.g., `a.b.c`) can be used in mappings. The flattening is done using the method `Mapper.flatten()` (see below).

The method `Mapper.process(self, rows, result_graph=)` invokes a mapper. The parameter `rows` is an iterable of `dict`s used as the "rows" to be mapped; dictionary keys take the role of column names. If provided, `result_graph=` is a graph where results are added; otherwise a new graph is created. Regardless, the result graph is returned.

The method `Mapper.processCSVFile(self, source, result_graph=, skip_unicode_marker=)` takes a CSV file (provided as the parameter `source` and passed to `open`) and maps its contents. The parameter `result_graph` is passed to `process`. If `skip_unicode_marker` is `True` (the default), the initial character in the source file is skipped (otherwise it becomes part of the name of the first column). The result graph is returned.

The package exposes `RR`, `RML`, and `RRE` as the namespaces (instances of `rdflib.Namespace`) for R2RML, RML, and the Tiny RML extensions, respectively. By convention, we use the prefixes `rr:`, `rml:`, and `rre:` for these.

### Template Formatting

Template strings (values of `rr:template`) do not support full JSONPath references. Paths like `a.b.c` are supported (see below); other features of JSONPath will be added in the future. The template mechanism is currently implemented using the `string.Formatter` class, so technically the [format string syntax](https://docs.python.org/3/library/string.html?highlight=format#formatstrings) is available; this is likely to change in the future, though.

### JSON object "flattening"

JSON objects, when processed, are first "flattened" into non-nested `dict`s. For example, the object
```python
{ "a": {"b": 1}, "c": 2 }
```
becomes
```python
{ "a.b": 1, "c": 2 }
```
and now the simplistic JSONPath `"a.b"` could be used in templates as a field reference.

"Flattening" is done using the method `Mapper.flatten()` which subclasses of `Mapper` can override if they so choose.

### Recipies

If you have an RDF source file (say, `mappings.ttl`) with multiple mappings (i.e., triples maps), you can parse the file and create multiple `Mapper` instances. For example, assuming triples maps `ex:tm_1` and `ex:tm_2` (corresponding to `EX.tm_1` and `EX.tm_2`), you could do this:
```python
mappings = rdflib.Graph()
mappings.parse("mappings.ttl")
mapping_1 = tinyrml.Mapper(mappings, triples_map_uri=EX.tm_1)
mapping_2 = tinyrml.Mapper(mappings, triples_map_uri=EX.tm_2)
```

To create an `rdflib.Composable` instance by mapping some tabular data, you can do the following (assuming `mapper` contains a `Mapper` instance and `rows` contains data to be mapped):

```python
composable = rdflib.Composable(mapper.process(rows))
```