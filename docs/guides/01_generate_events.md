# Generate events

This guide shows how to use the Madgraph5 class of HML to generate events from Z boson and QCD to dijets processes. To get started, let’s import some necessary classes from `generators` module:

```python
from hml.generators import Madgraph5, Madgraph5MultiRun, Madgraph5Run
```

<div class="result" markdown>

```
Welcome to JupyROOT 6.24/02
```

</div>

## Initialization

The Madgraph5 API (application programming interface) provided by HML works similarly to the Madgraph5 CLI (command line interface): initialization corresponds to the classic workflow of `generate, output, launch`.

```python
zjj = Madgraph5(
    executable="mg5_aMC",
    model="sm",
    definitions={},
    processes=["p p > z z, z > j j, z > vl vl~"],
    output="data/pp2zz_z2jj_z2vlvl",
)
```

- `executable` refers to the path of the `mg5_aMC` executable file.
- `model` is managed by Madgraph5 itself.
- `definitions` are used for the `define` command in Madgraph5.
- Usually in Madgraph5, you need to use `generate` and `add process` to create multiple processes. In HML, processes are represented as a list of strings.
- If `output` already exists, this class will not generate processes again.

## Launch the first run

After initializing the class (or `output` in Madgraph5 CLI), you can now launch a new run:

```python
zjj.launch(
    shower="pythia8",
    detector="delphes",
    settings={"iseed": 42, "nevents": 1000, "htjmin": 400},
)
```

<div class="result" markdown>

```
Running Survey
Running Pythia8
Running Delphes
Storing files

Done
```

</div>

- `shower` and `detector` are options for parton shower and detector simulation tools. Currently, `pythia8` and `delphes` are available.
- In Madgraph5, you can use the `set` command to change configurations in different cards without opening them. The `settings` attribute contains these configurations as a Python dictionary.
- To generate a large number of events, set the `multi_run` parameter.

## Check the information

After the generation is finished, you can use `.summary()` to check all the information of runs:

```python
zjj.summary()
```

<div class="result" markdown>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">                 p p &gt; z z, z &gt; j j, z &gt; vl vl~                 </span>
┏━━━┳━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃<span style="font-weight: bold"> # </span>┃<span style="font-weight: bold"> Name      </span>┃<span style="font-weight: bold"> Tag   </span>┃<span style="font-weight: bold"> Cross section (pb) </span>┃<span style="font-weight: bold"> N events </span>┃<span style="font-weight: bold"> Seed </span>┃
┡━━━╇━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 0 │ run_01[1] │ tag_1 │     2.273e-03      │    1,000 │   42 │
└───┴───────────┴───────┴────────────────────┴──────────┴──────┘
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f; font-style: italic">                            Output:                             </span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f; font-style: italic">/root/workspace_ssd/projects/hep-ml-lab/examples/data/pp2zz_z2jj</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f; font-style: italic">                            _z2vlvl                             </span>
</pre>

</div>

- The number in the square bracket after “run_01” represents the value of `multi_run`.
- A random seed is crucial to reproduce the results, which is why `Seed` is also displayed.

The data in the summary table are properties of a run:

```python
run_01 = zjj.runs[0]
print("Name:", run_01.name)
print("N Subruns:", len(run_01.runs))
print("Tag:", run_01.tag)
print("Cross section:", run_01.cross_section)
print("N events:", run_01.n_events)
print("Seed:", run_01.seed)
```

<div class="result" markdown>

```
Name: run_01
N Subruns: 1
Tag: tag_1
Cross section: 0.0022735
N events: 1000
Seed: 42
```

</div>

You can access the `events` attribute to read the root file from Delphes:

```python
for event in run.events:
    print(f"n_jets: {event.Jet_size}")
    print(f"n_fat_jets: {event.FatJet_size}")
    break
```

<div class="result" markdown>

```
n_jets: 2
n_fat_jets: 1
```

</div>

## Launch the second run similarly

To build a signal vs background binary classification task, we need to generate QCD events without the intermediate Z boson.

```python
qcd = Madgraph5(
    processes=['p p > j j / z'],
    output="./data/qcd"
)
qcd.launch(
    shower="pythia8",
    detector="delphes",
    settings={"iseed": 42, "nevents": 1000, "htjmin": 400},
)
qcd.summary()
```

<div class="result" markdown>

```
Running Survey
Running Pythia8
Running Delphes
Storing files

Done
```

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">                         p p &gt; j j / z                          </span>
┏━━━┳━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃<span style="font-weight: bold"> # </span>┃<span style="font-weight: bold"> Name      </span>┃<span style="font-weight: bold"> Tag   </span>┃<span style="font-weight: bold"> Cross section (pb) </span>┃<span style="font-weight: bold"> N events </span>┃<span style="font-weight: bold"> Seed </span>┃
┡━━━╇━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 0 │ run_01[1] │ tag_1 │     5.611e+04      │    1,000 │   42 │
└───┴───────────┴───────┴────────────────────┴──────────┴──────┘
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f; font-style: italic">                            Output:                             </span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f; font-style: italic">   /root/workspace_ssd/projects/hep-ml-lab/examples/data/qcd    </span>
</pre>

</div>

## Read the existing output

HML can handle three cases:

1. Events are generated by HML:
    
    ```python
    Madgraph5.from_output("./data/qcd")
    ```
    
2. Events are generated by the `multi_run` command from MadEvent:
    
    ```python
    Madgraph5MultiRun.from_name("run_01", "./data/qcd")
    ```
    
3. Events are generated normally by the `launch` command from Madgraph5:
    
    ```python
    Madgraph5Run.from_directory("./data/qcd/Events/run_01_0")
    ```

Check the [doc](../api/hml.generators.md) to learn more about `Madgraph5, Madgraph5MultiRun, Madgraph5Run`.
