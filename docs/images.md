
the `image` 
```
# list images available locally
uenv image pull gromacs/2023
# pull directly from: requires credentials
uenv image pull --full <https://jfrog...> --name test/2023

# list images available locally
uenv image find
# list images available on JFrog
uenv image avail
uenv image avail --cluster=eiger
```

updates to other commands
```
# this should return information about the current cluster?
> uenv status
no uenv loaded
on cluster eiger
```


