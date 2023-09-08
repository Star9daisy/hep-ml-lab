# Generate events via HML MG5 API

This example shows how to generate events via the HEP ML Lab (**HML**) Madgraph5
(**MG5**) application programming interface (**API**). It also shows how to check the
information of each run and manage all the runs.

## Launch the first run

Unlike the MG5 command line interface (**CLI**) which requires users to modify
configurations interactively, the HML MG5 API specify them when users create a
`Madgraph5` object:

``` py title="notebook.ipynb"
g = Madgraph5(
    executable="mg5_aMC",
    processes=["p p > z z, z > j j, z > vl vl~"],
    output="data/pp2zz_z2jj_z2vlvl",
    shower="Pythia8",
    detector="Delphes",
    n_events=1000,
)
```

!!! note
    1. Try to use `g.commands` before `g.launch()` to see the commands that will
        be executed by inner MG5.
    2. `n_events`, `seed` and `tags` are and are only settings over the
        `nevents`, `seed` and `run_tag` in `settings`. Remember to set their
        value directly in `g.n_events`, `g.seed` and `g.tags` if you want to
        change them.

Similar to the MG5, HML MG5 API uses the `launch` method to generate events: 

``` py title="notebook.ipynb"
g.launch()
```

<div class="result" markdown>

```
Generating events...
Running Pythia8...
Running Delphes...
Storing files...
Done
```

</div>

The `summary` method shows the information of all the runs:
    
``` py title="notebook.ipynb"
g.summary()
```

<div class="result" markdown>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">                  p p &gt; z z, z &gt; j j, z &gt; vl vl~                   </span>
┏━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃<span style="font-weight: bold"> # </span>┃<span style="font-weight: bold"> Name     </span>┃<span style="font-weight: bold"> Tag   </span>┃<span style="font-weight: bold">   Cross section (pb)   </span>┃<span style="font-weight: bold"> N events </span>┃<span style="font-weight: bold"> Seed </span>┃
┡━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 0 │ run_1[1] │ tag_1 │ 1.989e+00 +- 1.324e-02 │    1,000 │   42 │
└───┴──────────┴───────┴────────────────────────┴──────────┴──────┘
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f; font-style: italic">                  Output: data/pp2zz_z2jj_z2vlvl                   </span>
</pre>

</div>

## Change parameters

Users can assign new values to parameters of the `Madgraph5` object to change
the configurations for the next run::

``` py title="notebook.ipynb"
g.seed = 123
g.tag = "ptj=10,etaj=2.4"
g.settings["ptj"] = 10
g.settings["etaj"] = 2.4

g.launch(show_status=False)
g.summary()
```

<div class="result" markdown>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">                       p p &gt; z z, z &gt; j j, z &gt; vl vl~                        </span>
┏━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃<span style="font-weight: bold"> # </span>┃<span style="font-weight: bold"> Name     </span>┃<span style="font-weight: bold"> Tag             </span>┃<span style="font-weight: bold">   Cross section (pb)   </span>┃<span style="font-weight: bold"> N events </span>┃<span style="font-weight: bold"> Seed </span>┃
┡━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 0 │ run_1[1] │ tag_1           │ 1.989e+00 +- 1.324e-02 │    1,000 │   42 │
│ 1 │ run_2[1] │ ptj=10,etaj=2.4 │ 1.956e+00 +- 1.537e-02 │    1,000 │  123 │
└───┴──────────┴─────────────────┴────────────────────────┴──────────┴──────┘
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f; font-style: italic">                       Output: data/pp2zz_z2jj_z2vlvl                        </span>
</pre>

</div>

!!! note
    The value in `[]` is the number of subruns, which is calculated by the
    `n_events` and `n_events_per_subrun` of the generator.

## Check the run information

The values in the `summary` table are accessible via the `runs` attribute. Take
the second one as an example:

``` py title="notebook.ipynb"
run = g.runs[1]
print("Name:", run.name)
print("N Subruns:", run.n_subruns)
print("Tag:", run.tag)
print("Cross section:", run.cross_section)
print("Error:", run.error)
print("N events:", run.n_events)
print("Seed:", run.seed)
```

<div class="result" markdown>

```
Name: run_2
N Subruns: 1
Tag: ptj=10,etaj=2.4
Cross section: 1.95604
Error: 0.015374662254501723
N events: 1000
Seed: 123
```

</div>

To read the events from Delphes output, use the `events` method of a run:

``` py title="notebook.ipynb"
for event in run.events:
    print(f"n_jets: {event.Jet_size}")
    print(f"n_fat_jets: {event.FatJet_size}")
    break
```

<div class="result" markdown>

```
n_jets: 3
n_fat_jets: 0
```

</div>

!!! note
    1. Behind the scenes, the `events` method uses `PyROOT` as the backend to
    read the events.
    2. Right inside this event loop, users can apply cuts to filter events.

## Remove and clean runs

HML MG5 API also provides `remove` and `clean` methods to manage runs:

``` py title="notebook.ipynb"
g.remove("run_1") # remove the first run
g.summary()
```

<div class="result" markdown>

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">                       p p &gt; z z, z &gt; j j, z &gt; vl vl~                        </span>
┏━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃<span style="font-weight: bold"> # </span>┃<span style="font-weight: bold"> Name     </span>┃<span style="font-weight: bold"> Tag             </span>┃<span style="font-weight: bold">   Cross section (pb)   </span>┃<span style="font-weight: bold"> N events </span>┃<span style="font-weight: bold"> Seed </span>┃
┡━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 0 │ run_2[1] │ ptj=10,etaj=2.4 │ 1.956e+00 +- 1.537e-02 │    1,000 │  123 │
└───┴──────────┴─────────────────┴────────────────────────┴──────────┴──────┘
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f; font-style: italic">                       Output: data/pp2zz_z2jj_z2vlvl                        </span>
</pre>

</div>

The `clean` method removes all the runs and the output directory itself:

``` py title="notebook.ipynb"
g.clean()
```

---

Check [Madgraph5](../../api-reference/hml.generators#hml.generators.Madgraph5)
for more details.
