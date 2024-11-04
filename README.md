# Virtual Box UUID Changer
The script should generate 2 UUIDS using `vboxmanage internalcommands sethduuid` and then replace the 3 UUIDs inside the .vbox file.
1. <Machine uuid="{uuid_1}"
2. <HardDisk uuid="{uuid_2}"
3. <Image uuid="{uuid_2}"

Changing the UUID avoids the error in VirtualBox:
```
Failed to open virtual machine located in /home/.../path_to_new_VM.vbox
Trying to open a VM config '/home/.../path_to_VM_with_same_UUID.vbox' which has the same UUID as an existing virtual machine.Result Code:NS_ERROR_FAILURE
Result Code:NS_ERROR_FAILURE (0x80004005)
Component:MachineWrap
...
```
This python script allow you to quickly change clone of a VM without having to change it manually.
## Use
`python3 gen_uuid_for_vb.py <path_to_VM_dir>`

or

Place script in directory with *.vdi/ *.vbox and run without arguments:

`python3 gen_uuid_for_vb.py`

## ISSUE
It works <ins>sometimes</ins>. But i have no idea how to fix RegEx formatting error, here is an [issue](https://github.com/Gnomee1337/vb_uuid_changer/issues/1#issue-2633553470)
