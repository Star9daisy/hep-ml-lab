# Generate events

This guide shows how to use the `Madgraph5` class to generate events WW and QCD to dijet processes. To get started, let’s import some necessary classes from `generators` module:

```python
from hml.generators import Madgraph5, Madgraph5Run
```

API is designed to be as much similar as the CLI. The following table shows the correspondence between the CLI commands and the API methods:

| CLI command                                    | API method                               |
|------------------------------------------------|------------------------------------------|
| `import model sm`                              | `g.import_model("sm")`                   |
| `define l = e+ e-`                             | `g.define("l = e+ e-")`                  |
| `generate p p > j j` `add process p p > j j j` | `g.generate("p p > j j", "p p > j j j")` |
| `display diagrams Diagrams`                    | `g.display_diagrams("Diagrams")`         |
| `output ./test`                                | `g.output("./test")`                     |
| `launch`                                       | `g.launch(...)`                          |


## Initialization

The Madgraph5 API (application programming interface) works similarly to the Madgraph5 CLI (command line interface). It uses CLI commands to generate events, so the very first step is to connect to the Madgraph5 executable file:

```python
g = Madgraph5(executable="mg5_aMC", verbose=1)
```

<div class="result" markdown>

```
************************************************************
*                                                          *
*                     W E L C O M E to                     *
*              M A D G R A P H 5 _ a M C @ N L O           *
*                                                          *
*                                                          *
*                 *                       *                *
*                   *        * *        *                  *
*                     * * * * 5 * * * *                    *
*                   *        * *        *                  *
*                 *                       *                *
*                                                          *
*         VERSION 3.5.3                 2023-12-23         *
*                                                          *
*    The MadGraph5_aMC@NLO Development Team - Find us at   *
*              http://madgraph.phys.ucl.ac.be/             *
*                            and                           *
*            http://amcatnlo.web.cern.ch/amcatnlo/         *
*                                                          *
*               Type 'help' for in-line help.              *
*           Type 'tutorial' to learn how MG5 works         *
*    Type 'tutorial aMCatNLO' to learn how aMC@NLO works   *
*    Type 'tutorial MadLoop' to learn how MadLoop works    *
*                                                          *
************************************************************
load MG5 configuration from ../../../../softwares/madgraph5/input/mg5_configuration.txt 
fastjet-config does not seem to correspond to a valid fastjet-config executable (v3+). We will use fjcore instead.
 Please set the 'fastjet'variable to the full (absolute) /PATH/TO/fastjet-config (including fastjet-config).
 MG5_aMC> set fastjet /PATH/TO/fastjet-config

eMELA-config does not seem to correspond to a valid eMELA-config executable.
 Please set the 'fastjet'variable to the full (absolute) /PATH/TO/eMELA-config (including eMELA-config).
 MG5_aMC> set eMELA /PATH/TO/eMELA-config

set lhapdf to lhapdf-config
set lhapdf to lhapdf-config
Using default text editor "vi". Set another one in ./input/mg5_configuration.txt
No valid eps viewer found. Please set in ./input/mg5_configuration.txt
No valid web browser found. Please set in ./input/mg5_configuration.txt
Loading default model: sm
INFO: Restrict model sm with file ../../../../softwares/madgraph5/models/sm/restrict_default.dat . 
INFO: Run "set stdout_level DEBUG" before import for more information. 
INFO: Change particles name to pass to MG5 convention 
Defined multiparticle p = g u c d s u~ c~ d~ s~
Defined multiparticle j = g u c d s u~ c~ d~ s~
Defined multiparticle l+ = e+ mu+
Defined multiparticle l- = e- mu-
Defined multiparticle vl = ve vm vt
Defined multiparticle vl~ = ve~ vm~ vt~
Defined multiparticle all = g u c d s u~ c~ d~ s~ a ve vm vt e- mu- ve~ vm~ vt~ e+ mu+ t b t~ b~ z w+ h w- ta- ta+
MG5_aMC>
```

</div>

- `executable` refers to the path of the `mg5_aMC` executable file.
- `verbose` is used to control the output level. The default value is 1 showing all the information as the CLI does. If it is set to 0, no information will be displayed.

## Generate the process

We take "p p > w+ z" as the first example. We want to give the W boson a boost to simulate there is a heavy intermediate particles from new physics. So no decay chain is specified here. In the launch part, W boson decays to two jets and Z boson decays invisibly to ensure the fatjet is consistent with the W boson.

```python
g.generate("p p > w+ z")
```
<div class="result" markdown>

```
generate p p > w+ z
INFO: Checking for minimal orders which gives processes. 
INFO: Please specify coupling orders to bypass this step. 
INFO: Trying process: u d~ > w+ z WEIGHTED<=4 @1  
INFO: Process has 3 diagrams 
INFO: Trying process: u s~ > w+ z WEIGHTED<=4 @1  
INFO: Trying process: c d~ > w+ z WEIGHTED<=4 @1  
INFO: Trying process: c s~ > w+ z WEIGHTED<=4 @1  
INFO: Process has 3 diagrams 
INFO: Process d~ u > w+ z added to mirror process u d~ > w+ z 
INFO: Process s~ c > w+ z added to mirror process c s~ > w+ z 
2 processes with 6 diagrams generated in 0.025 s
Total: 2 processes with 6 diagrams
```

</div>

!!! note
    The `add process` and `generate` commands from CLI are combined into `generate` in the API. So you can directly add processes one by one. For example: `g.generate("p p > w+ j", "p p > w- j")`

After generating the process, it is crutial to check the feynman diagram before moving on:

```python
g.display_diagrams()
```

<div class="result" markdown>

```
display diagrams Diagrams
Drawing Process: u d~ > w+ z WEIGHTED<=4 @1
Wrote file Diagrams/diagrams_1_udx_wpz.eps
open Diagrams/diagrams_1_udx_wpz.eps
Not able to open file Diagrams/diagrams_1_udx_wpz.eps since no program configured.Please set one in ./input/mg5_configuration.txt
Drawing Process: c s~ > w+ z WEIGHTED<=4 @1
Wrote file Diagrams/diagrams_1_csx_wpz.eps
open Diagrams/diagrams_1_csx_wpz.eps
Not able to open file Diagrams/diagrams_1_csx_wpz.eps since no program configured.Please set one in ./input/mg5_configuration.txt
time to draw 0.012159109115600586
```

</div>

```python
!tree Diagrams
```

<div class="result" markdown>

```
Diagrams/
├── diagrams_1_csx_wpz.eps
├── diagrams_1_csx_wpz.pdf
├── diagrams_1_udx_wpz.eps
└── diagrams_1_udx_wpz.pdf

0 directories, 4 files
```

</div>

- By default, the diagram is stored in the `Diagrams` folder in the current directory. You can change the path by setting the parameter `diagram_dir`.
- The `.eps` file is converted in `.pdf` format for convenience.

Finally, we can save the process to a directory:

```python
g.output("data/pp2wz")
```

<div class="result" markdown>

```
output /root/workspace_ssd/projects/hep-ml-lab/examples/data/pp2wz
INFO: initialize a new directory: pp2wz 
INFO: remove old information in pp2wz 
INFO: Organizing processes into subprocess groups 
INFO: Generating Helas calls for process: u d~ > w+ z WEIGHTED<=4 @1 
INFO: Processing color information for process: u d~ > w+ z @1 
INFO: Combined process c s~ > w+ z WEIGHTED<=4 @1 with process u d~ > w+ z WEIGHTED<=4 @1 
INFO: Creating files in directory P1_qq_wpz 
INFO: Generating Feynman diagrams for Process: u d~ > w+ z WEIGHTED<=4 @1 
INFO: Finding symmetric diagrams for subprocess group qq_wpz 
Generated helas calls for 1 subprocesses (3 diagrams) in 0.007 s
Wrote files for 10 helas calls in 0.033 s
ALOHA: aloha starts to compute helicity amplitudes
ALOHA: aloha creates 4 routines in  1.021 s
The option auto_update is modified [7] but will not be written in the configuration files.
If you want to make this value the default for future session, you can run 'save options --all'
save configuration file to /root/workspace_ssd/projects/hep-ml-lab/examples/data/pp2wz/Cards/me5_configuration.txt
INFO: Use Fortran compiler gfortran 
INFO: Use c++ compiler g++ 
INFO: Generate jpeg diagrams 
INFO: Generate web pages 
Output to directory /root/workspace_ssd/projects/hep-ml-lab/examples/data/pp2wz done.
Type "launch" to generate events from this process, or see
/root/workspace_ssd/projects/hep-ml-lab/examples/data/pp2wz/README
Run "open index.html" to see more information about this process.
display diagrams /root/workspace_ssd/projects/hep-ml-lab/examples/data/pp2wz/Diagrams
Drawing Process: u d~ > w+ z WEIGHTED<=4 @1
Wrote file /root/workspace_ssd/projects/hep-ml-lab/examples/data/pp2wz/Diagrams/diagrams_1_udx_wpz.eps
open /root/workspace_ssd/projects/hep-ml-lab/examples/data/pp2wz/Diagrams/diagrams_1_udx_wpz.eps
Not able to open file /root/workspace_ssd/projects/hep-ml-lab/examples/data/pp2wz/Diagrams/diagrams_1_udx_wpz.eps since no program configured.Please set one in ./input/mg5_configuration.txt
time to draw 0.007663726806640625
Process log saved to data/pp2wz/Logs/process.log
```

</div>

!!! note
    Even if you don't `display_diagram` before, the diagram will be saved in the `Diagrams` folder of the output directory.

## Launch the first run
It's time to launch the first run. In the CLI, two prompts will show up: one for the tools and the other for the configurations. In the API, they are combined into one method:

```python
g.launch(
    shower="pythia8",
    detector="delphes",
    madspin="none",
    settings={
        "nevents": 1000,
        "run_tag": "250-300",
        "pt_min_pdg": {24: 250},
        "pt_max_pdg": {24: 300},
    },
    decays=[
        "w+ > j j",
        "z > vl vl~",
    ],
    seed=42,
)
```

- `shower` and `detector` are options for parton shower and detector simulation tools. Currently, `pythia8` and `delphes` are available.
- In Madgraph5, you can use the `set` command to change configurations in different cards without opening them. The `settings` attribute contains these configurations as a Python dictionary.
- To generate a large number of events, set the `multi_run` parameter.

## Check the information

After the generation is finished, you can use `.summary()` to check all the information of runs:

```python
g.summary()
```

<div class="result" markdown>

<style>
    pre.small-text {
        font-size: 12px; /* Adjust this value to increase or decrease the font size */
        font-family: Menlo, 'DejaVu Sans Mono', consolas, 'Courier New', monospace;
        line-height: normal;
        overflow-x: auto;
        white-space: pre;
    }
</style>
<pre class="small-text">
                                       p p > w+ z                                        
┏━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃ # ┃ Name      ┃ Collider         ┃ Tag     ┃   Cross section (pb)   ┃ N events ┃ Seed ┃
┡━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 0 │ run_01[1] │ pp:6500.0x6500.0 │ 250-300 │ 4.371e-02 +- 4.200e-04 │    1,000 │   42 │
└───┴───────────┴──────────────────┴─────────┴────────────────────────┴──────────┴──────┘
                                   Output: data/pp2wz                                    
</pre>

</div>

- The number in the square bracket after “run_01” represents the value of `multi_run`.
- A random seed is crucial to reproduce the results, which is why `Seed` is also displayed.

The data in the summary table are properties of a run:

```python
run_01 = g.runs[0]
print(f"Processes: {g.processes}")
print(f"Name: {run_01.name}")
print(f"N subruns: {len(run_01.sub_runs)}")
print(f"Collider: {run_01.collider}")
print(f"Tag: {run_01.tag}")
print(f"Cross section: {run_01.cross}")
print(f"Error: {run_01.error}")
print(f"N events: {run_01.n_events}")
print(f"Seed: {run_01.seed}")
```

<div class="result" markdown>

```
Processes: ['p p > w+ z']
Name: run_01
N subruns: 1
Collider: pp:6500.0x6500.0
Tag: 250-300
Cross section: 0.04371
Error: 0.00042
N events: 1000
Seed: 42

```

</div>

Use `events()` to retrieve the event files:

```python
run_01.events()
```

<div class="result" markdown>

```
['data/pp2wz/Events/run_01_decayed_1/250-300_delphes_events.root:Delphes']
```

</div>

This string could be used directly in the `uproot`:

```python
import uproot

events = uproot.open(run_01.events()[0])
events
```

<div class="result" markdown>

```
<TTree 'Delphes' (34 branches) at 0x7fc181a77310>
```

</div>


## Launch more runs

Under the same process, we can adjust the configurations and launch multiple runs to "scan":

```python
low_limits = [300, 350, 400, 450]
high_limits = [350, 400, 450, 500]

g.verbose = 0

for low, high in zip(low_limits, high_limits):
    print(f"Generating events between {low} and {high} GeV")
    g.launch(
        shower="pythia8",
        detector="delphes",
        madspin="none",
        settings={
            "nevents": 1000,
            "run_tag": f"{low}-{high}",
            "pt_min_pdg": {24: low},
            "pt_max_pdg": {24: high},
        },
        decays=[
            "w+ > j j",
            "z > vl vl~",
        ],
        seed=42,
    )

g.summary()
```

<div class="result" markdown>

```
Generating events between 300 and 350 GeV
Generating events between 350 and 400 GeV
Generating events between 400 and 450 GeV
Generating events between 450 and 500 GeV
```

<style>
    pre.small-text {
        font-size: 12px; /* Adjust this value to increase or decrease the font size */
        font-family: Menlo, 'DejaVu Sans Mono', consolas, 'Courier New', monospace;
        line-height: normal;
        overflow-x: auto;
        white-space: pre;
    }
</style>
<pre class="small-text">
                                       p p > w+ z                                        
┏━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃ # ┃ Name      ┃ Collider         ┃ Tag     ┃   Cross section (pb)   ┃ N events ┃ Seed ┃
┡━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 0 │ run_01[1] │ pp:6500.0x6500.0 │ 250-300 │ 4.371e-02 +- 4.200e-04 │    1,000 │   42 │
│ 1 │ run_02[1] │ pp:6500.0x6500.0 │ 300-350 │ 2.021e-02 +- 1.900e-04 │    1,000 │   42 │
│ 2 │ run_03[1] │ pp:6500.0x6500.0 │ 350-400 │ 9.985e-03 +- 9.400e-05 │    1,000 │   42 │
│ 3 │ run_04[1] │ pp:6500.0x6500.0 │ 400-450 │ 5.322e-03 +- 8.100e-05 │    1,000 │   42 │
│ 4 │ run_05[1] │ pp:6500.0x6500.0 │ 450-500 │ 2.972e-03 +- 3.500e-05 │    1,000 │   42 │
└───┴───────────┴──────────────────┴─────────┴────────────────────────┴──────────┴──────┘
                                   Output: data/pp2wz                                    
</pre>

</div>

## Build a binary classification task

We take QCD to dijet as the background and WZ to dijet as the signal. Both have 10,000 events.

```python
wz = Madgraph5(executable="mg5_aMC", verbose=0)

wz.generate("p p > w+ z")
wz.output("data/pp2wz@10k")
wz.launch(
    shower="pythia8",
    detector="delphes",
    madspin="none",
    settings={
        "nevents": 10000,
        "pt_min_pdg": {24: 250},
        "pt_max_pdg": {24: 300},
    },
    decays=[
        "w+ > j j",
        "z > vl vl~",
    ],
    seed=42,
)

wz.summary()
```

<div class="result" markdown>

<style>
    pre.small-text {
        font-size: 12px; /* Adjust this value to increase or decrease the font size */
        font-family: Menlo, 'DejaVu Sans Mono', consolas, 'Courier New', monospace;
        line-height: normal;
        overflow-x: auto;
        white-space: pre;
    }
</style>
<pre class="small-text">
                                      p p > w+ z                                       
┏━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃ # ┃ Name      ┃ Collider         ┃ Tag   ┃   Cross section (pb)   ┃ N events ┃ Seed ┃
┡━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 0 │ run_01[1] │ pp:6500.0x6500.0 │ tag_1 │ 4.375e-02 +- 1.400e-04 │   10,000 │   42 │
└───┴───────────┴──────────────────┴───────┴────────────────────────┴──────────┴──────┘
                                Output: data/pp2wz@10k                                 
</pre>
</div>

```python
qcd = Madgraph5(executable="mg5_aMC", verbose=0)

qcd.generate("p p > j j")
qcd.output("data/pp2jj@10k")
qcd.launch(
    shower="pythia8",
    detector="delphes",
    settings={
        "nevents": 10000,
        "ptj": 250,
        "ptjmax": 300,
    },
    seed=42,
)

qcd.summary()
```

<div class="result" markdown>

<style>
    pre.small-text {
        font-size: 12px; /* Adjust this value to increase or decrease the font size */
        font-family: Menlo, 'DejaVu Sans Mono', consolas, 'Courier New', monospace;
        line-height: normal;
        overflow-x: auto;
        white-space: pre;
    }
</style>
<pre class="small-text">
                                       p p > j j                                       
┏━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃ # ┃ Name      ┃ Collider         ┃ Tag   ┃   Cross section (pb)   ┃ N events ┃ Seed ┃
┡━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 0 │ run_01[0] │ pp:6500.0x6500.0 │ tag_1 │ 1.161e+04 +- 4.000e+01 │   10,000 │   42 │
└───┴───────────┴──────────────────┴───────┴────────────────────────┴──────────┴──────┘
                                Output: data/pp2jj@10k                                 

</pre>
</div>

## Read the existing output

Here we take the "pp2wz" as the exising output directory:

- If you want to check all information of runs inside this output, use `Madgraph5.from_output`:

```python
g = Madgraph5.from_output("data/pp2wz", executable="mg5_aMC")
g.summary()
```

<div class="result" markdown>

<style>
    pre.small-text {
        font-size: 12px; /* Adjust this value to increase or decrease the font size */
        font-family: Menlo, 'DejaVu Sans Mono', consolas, 'Courier New', monospace;
        line-height: normal;
        overflow-x: auto;
        white-space: pre;
    }
</style>
<pre class="small-text">
                                       p p > w+ z                                        
┏━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃ # ┃ Name      ┃ Collider         ┃ Tag     ┃   Cross section (pb)   ┃ N events ┃ Seed ┃
┡━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 0 │ run_01[1] │ pp:6500.0x6500.0 │ 250-300 │ 4.371e-02 +- 4.200e-04 │    1,000 │   42 │
│ 1 │ run_02[1] │ pp:6500.0x6500.0 │ 300-350 │ 2.021e-02 +- 1.900e-04 │    1,000 │   42 │
│ 2 │ run_03[1] │ pp:6500.0x6500.0 │ 350-400 │ 9.985e-03 +- 9.400e-05 │    1,000 │   42 │
│ 3 │ run_04[1] │ pp:6500.0x6500.0 │ 400-450 │ 5.322e-03 +- 8.100e-05 │    1,000 │   42 │
│ 4 │ run_05[1] │ pp:6500.0x6500.0 │ 450-500 │ 2.972e-03 +- 3.500e-05 │    1,000 │   42 │
└───┴───────────┴──────────────────┴─────────┴────────────────────────┴──────────┴──────┘
                                   Output: data/pp2wz                            
</pre>
</div>

- Or you only want to retrieve a single run:

```python
run = Madgraph5Run("data/pp2wz", name="run_02")
run
```

<div class="result" markdown>

```
Madgraph5Run run_02 (1 sub runs):
- collider: pp:6500.0x6500.0
- tag: 300-350
- seed: 42
- cross: 0.02021
- error: 0.00019
- n_events: 1000
```

</div>

Check the [doc](../api_reference/hml.generators.md) to learn more about `Madgraph5`, `Madgraph5Run`.
