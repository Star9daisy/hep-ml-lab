# Generate events via HML MG5 API

This example shows how to generate events via the HEP ML Lab (**HML**) Madgraph5
(**MG5**) application programming interface (**API**). It also shows how to check the
information of each run and manage all the runs.

## Launch the first run

Unlike the MG5 command line interface (**CLI**) which requires users to modify
configurations interactively, the HML MG5 API specify them as uses create the
`Madgraph5` object:

``` py title="notebook.ipynb"
g = Madgraph5(
    executable="mg5_aMC",
    processes=["p p > z z, z > j j, z > vl vl~"],
    output="data/pp2zz_z2jj_z2vvlv",
    settings={
        "ptj": 10,
        "etaj": 2.4,
    },
    n_events=1000,
    seed=42,
    tag="ptj=10,etaj=2.4",
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
Storing files...
Done
```

</div>

The `summary` method shows the information of all the runs:
    
``` py title="notebook.ipynb"
g.summary()
```

<div class="result" markdown>

```
                       p p > z z, z > j j, z > vl vl~                        
┏━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃ # ┃ Name     ┃ Tag             ┃   Cross section (pb)   ┃ N events ┃ Seed ┃
┡━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 0 │ run_1[1] │ ptj=10,etaj=2.4 │ 1.989e+00 +- 1.324e-02 │    1,000 │   42 │
└───┴──────────┴─────────────────┴────────────────────────┴──────────┴──────┘
                       Output: data/pp2zz_z2jj_z2vvlv                        
```

</div>

## Change parameters and launch the second run

Users can assign new values to parameters of the `Madgraph5` object to change
the configurations for the next run::

``` py title="notebook.ipynb"
g.seed = 123
g.tag = "no_cuts"

del g.settings["ptj"] # remove this setting
del g.settings["etaj"] # remove this setting

g.launch(show_status=False)
g.summary()
```

<div class="result" markdown>

```
                       p p > z z, z > j j, z > vl vl~                        
┏━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃ # ┃ Name     ┃ Tag             ┃   Cross section (pb)   ┃ N events ┃ Seed ┃
┡━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 0 │ run_1[1] │ ptj=10,etaj=2.4 │ 1.989e+00 +- 1.324e-02 │    1,000 │   42 │
│ 1 │ run_2[1] │ no_cuts         │ 1.956e+00 +- 1.537e-02 │    1,000 │  123 │
└───┴──────────┴─────────────────┴────────────────────────┴──────────┴──────┘
                       Output: data/pp2zz_z2jj_z2vvlv                        
```

</div>

## Check the information of any run

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
Tag: no_cuts
Cross section: 1.95604
Error: 0.015374662254501723
N events: 1000
Seed: 123
```

</div>

## Remove and clean runs

HML MG5 API also provides `remove` and `clean` methods to manage runs:

``` py title="notebook.ipynb"
g.remove("run_1") # remove the first run
g.summary()
```

<div class="result" markdown>

```
                   p p > z z, z > j j, z > vl vl~                    
┏━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┓
┃ # ┃ Name     ┃ Tag     ┃   Cross section (pb)   ┃ N events ┃ Seed ┃
┡━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━┩
│ 0 │ run_2[1] │ no_cuts │ 1.956e+00 +- 1.537e-02 │    1,000 │  123 │
└───┴──────────┴─────────┴────────────────────────┴──────────┴──────┘
                   Output: data/pp2zz_z2jj_z2vvlv                    
```

</div>

``` py title="notebook.ipynb"
g.clean() # remove the output directory
```

---

Check more in [API documentation](../../api-reference/hml.generators#hml.generators.Madgraph5).
