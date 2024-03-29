### Cycle Enrichr

Enrichment of gene sets with no gene annotations leveraging ARCHS4 and PrismExp gene function prediction.


## Usage

#### Installation
```
pip3 install cycleenrichr
```
#### Download Prediction File
```python
# download precomputed predictions file from PrismExp

import cycleenrichr as cycle
cycle.load.download("predictions.h5")
```

### Run Set Enrichment for Gene Set Library

```python
import cycleenrichr as cycle

# load gene set libary from Enrichr
library = cycle.enrichr.get_library("KEGG_2021_Human")

predictions_path = "predictions.h5"

result = cycle.enrichment.enrich(library, predictions_path)
```
