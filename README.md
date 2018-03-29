# SPA112Ctl: SPA112 Controller

## Dependencies

```
aptitude install python3-docopt python3-termcolor python3-requests
```
## Examples

```
./spa112-ctl.py reboot --ip-address 10.72.0.10
[FAIL] Could not connect to SPA112 ... failed!
```

```
./spa112-ctl.py reboot -i 10.72.0.10
[FAIL] Timeout from SPA112 ... failed!
```

```
./spa112-ctl.py reboot --ip-address 10.72.0.10
[ ok ] Successfully reboot SPA112.
```

```
./spa112-ctl.py reboot -i 10.72.0.10 -l admin -p admin
[ ok ] Successfully reboot SPA112.
```

```
./spa112-ctl.py reset -i 10.72.0.10
[ ok ] Successfully reset SPA112.
```
