# MIMIC-Cardio
Master's thesis by Jakub Wierzchowiec, Wroclaw University of Science and Technology, 2025

## Instalation
The instruction focuses on UNIX-based systems, equivalent commands on Windows should be similar.

To create and activate virtual environment use:
```shell
python3 -m venv .venv
source .venv/bin/activate
```
To install dependencies use:
```shell
pip install -e .
```
## Running applications
### Prerequisites
- Register on OpenAI API platform, setup organization and generate API key
- Sign up on PhysioNet and become a credentialed user, make sure you can access this [resource](https://physionet.org/content/mimic-iv-echo/0.1/)

To perform experiments:
```shell
export OPENAI_API_KEY=<token> PHYSIONET_USERNAME=<username> PHYSIONET_PASSWORD=<password> 
mimic-cardio <cases> <prefix> <model> <tpm>
```
where:
- token - OpenAI API key
- prefix - experiment identifier (i.e. `e2`)
- cases - name of the JSONL file containing cases to be process, the file must be located in `/asssets` (i.e. `sample.jsonl`)
- model - LLM to be queried (i.e. `gpt-4.1-nano`)
- tpm - tokens per limit respective for current OpenAI tier (i.e. `30000`)

To calculate performance metrics:
```shell
mimic-stats <prefix> <cases>
```
where:
- prefix - experiment identifier (i.e. `e2`), suffix with `c` to calculate aggregated metrics (i.e. `e2c`)
- cases - name of the JSONL file containing cases to be processed, the file must be located in `/asssets` (i.e. `sample.jsonl`)

To perform statistical tests:
```shell
mimic-test <alpha> <prefix1> <prefix2> <cluster>
```
where:
- alpha - significance level (i.e. `0.05`)
- prefix1 - first experiment identifier (i.e. `e2`)
- prefix2 - second experiment identifier (i.e. `e3`)
- cluster - (optional) whether the tests are evaluated on aggregated data; use `c` if needed, omit otherwise 

## Documentation
For further details see:
- [OpenAI API docs](https://platform.openai.com/docs/overview)
- [PhysioNet](https://physionet.org/)
