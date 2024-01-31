### Transforming from YAML format to other formats

#### CSV

```bash
linkml-convert -t csv -s linkml/schema/peh.yaml -S observable_property_groups linkml/data/ObservablePropertyGroupList_data.yaml > ObservablePropertiesList.csv
```

#### TSV

```bash
linkml-convert -t tsv -s linkml/schema/peh.yaml -S observable_property_groups linkml/data/ObservablePropertyGroupList_data.yaml > ObservablePropertiesList.tsv
```
