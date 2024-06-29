# Maritime Personnel Competency Correspondence analysis
Network analysis of maritime personnel competencies correspondence with the STCW code based on MSUN higher educational programs:
- 26.05.05 (Navigation),
- 26.05.06 (Operation of ship power plants),
- 26.05.07 (Operation of ship electrical and automation equipment)

pdf folder contains educational programs for specialties listed above.
data folder contains nodes and adjacency list csv files ready to import to Gephi.
competency_extractor.py by default extracts competencies (УК, ОПК, ПК) from OOP pdf files in /pdf to csv documents in /extracted.
Extractor functionality can be customised:

``` python
extract_competencies("path_to_file", 'pages', "export_file_name.csv", column_index=column_number)
```