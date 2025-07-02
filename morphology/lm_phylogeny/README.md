# Landmark based phylogenetics

You should use pvm to parallelize the computation.

```
pvmd3 hostlist
```

The hostlist file should look like this:

```holist
helix ep=/usr/bin/
```

`helix` is the host name of the Linux machine.

To obtain the results

```
tnt run tnt_search.tnt,
tnt run tnt_vis.tnt,
```
