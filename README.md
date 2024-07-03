# Network analysis of maritime educational programs
Network analysis of maritime educational program elements in correspondence with the STCW code based on data from Admiral Nevelskoy Maritime State University educational programs of higher education:
- 26.05.05 Navigation;
- 26.05.06 Operation of ship power plants;
- 26.05.07 Operation of ship electrical and automation equipment.

pdf folder contains educational programs for training programs listed above.
data folder contains nodes.csv and adjacency_list.csv datasets for importing to Gephi graph software.
competency_extractor.py (by default) extracts competencies (УК, ОПК, ПК) from files in /pdf to CSV documents in /extracted.
Extractor functionality can be customised:

``` python
extract_competencies("path_to_file", 'pages', "export_file_name.csv", column_index=column_number)
```
