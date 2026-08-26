# Runbook: Phase 1 Virtual Infrastructure

## Purpose and boundary

This runbook records the repeatable steps used to build and verify the Phase 1
Ubuntu Server lab on Windows 11 with Microsoft Hyper-V.

| VM | Role | IP | CPU | Memory | Disk |
|---|---|---|---|---|---|
| drl-ops-01 | Operations | 192.168.50.10/24 | 2 vCPU | 4 GB fixed | C:\Hyper-V\VHDX\drl-ops-01.vhdx |
| drl-k8s-cp-01 | Control plane | 192.168.50.20/24 | 2 vCPU | 4 GB fixed | C:\Hyper-V\VHDX\drl-k8s-cp-01.vhdx |
| drl-k8s-wk-01 | Worker 1 | 192.168.50.21/24 | 2 vCPU | 4 GB fixed | C:\Hyper-V\VHDX\drl-k8s-wk-01.vhdx |
| drl-k8s-wk-02 | Worker 2 | 192.168.50.22/24 | 2 vCPU | 4 GB fixed | C:\Hyper-V\VHDX\drl-k8s-wk-02.vhdx |

Network: Internal switch drl-lab; Windows adapter vEthernet (drl-lab);
Windows address 192.168.50.1/24; subnet 192.168.50.0/24; user opsadmin;
static hosts files; UFW default-deny incoming with TCP 22 allowed from
192.168.50.1.

Hyper-V configuration, hosts-file edits, guest configuration, and verification
are repeat-safe. Ubuntu ISO installation remains manual: its UI, credentials,
and installer prompts are deliberately not automated. Existing VMs are never
deleted or replaced. A conflicting VM generation, disk, address, or switch is
a stop-and-inspect condition.

## 1. Verify Windows and Hyper-V

Run as Administrator:

```powershell
$ErrorActionPreference = 'Stop'
Get-ComputerInfo -Property WindowsProductName, WindowsVersion, OsArchitecture
Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All | Select-Object FeatureName, State
Get-Service vmms | Select-Object Name, Status, StartType
Get-VMSwitch | Select-Object Name, SwitchType, NetAdapterName
```

Expected: Windows 11 x64; Microsoft-Hyper-V-All Enabled; vmms Running,
normally Automatic.

## 2. Create or verify the Internal switch

```powershell
$SwitchName = 'drl-lab'
$Switch = Get-VMSwitch -Name $SwitchName -ErrorAction SilentlyContinue
if (-not $Switch) {
    New-VMSwitch -Name $SwitchName -SwitchType Internal | Out-Null
    'Created Internal switch: drl-lab'
} elseif ($Switch.SwitchType -ne 'Internal') {
    throw "Existing drl-lab switch is not Internal."
} else {
    'Switch already exists: drl-lab'
}
Get-VMSwitch -Name $SwitchName | Select-Object Name, SwitchType, NetAdapterName
```

Expected values: Name drl-lab, SwitchType Internal, NetAdapterName
vEthernet (drl-lab).

## 3. Configure or verify the Windows host adapter

This adds the address only when absent and refuses to overwrite a different
non-link-local address.

```powershell
$AdapterName = 'vEthernet (drl-lab)'
$HostAddress = '192.168.50.1'
$Adapter = Get-NetAdapter -Name $AdapterName -ErrorAction Stop
Set-NetIPInterface -InterfaceIndex $Adapter.ifIndex -Dhcp Disabled
$Current = Get-NetIPAddress -InterfaceIndex $Adapter.ifIndex -AddressFamily IPv4 -ErrorAction SilentlyContinue
$Conflict = $Current | Where-Object { $_.IPAddress -notlike '169.254.*' -and $_.IPAddress -ne $HostAddress }
if ($Conflict) { throw "Conflicting IPv4 address: $($Conflict.IPAddress -join ', ')" }
if (-not ($Current | Where-Object IPAddress -eq $HostAddress)) {
    New-NetIPAddress -InterfaceIndex $Adapter.ifIndex -IPAddress $HostAddress -PrefixLength 24 | Out-Null
    'Added 192.168.50.1/24'
} else { '192.168.50.1/24 already present' }
Get-NetIPAddress -InterfaceIndex $Adapter.ifIndex -AddressFamily IPv4 |
    Select-Object IPAddress, PrefixLength, InterfaceAlias
```

Expected: 192.168.50.1, prefix 24, on vEthernet (drl-lab). No gateway is
required for this internal-only network.

## 4. Create or verify the four VM definitions

Run with the VMs Off. This creates missing VMs and reapplies approved hardware
settings without deleting anything.

```powershell
$ErrorActionPreference = 'Stop'
$SwitchName = 'drl-lab'
$VmRoot = 'C:\Hyper-V\VMs'
$VhdRoot = 'C:\Hyper-V\VHDX'
$Specs = @(
  @{ Name='drl-ops-01'; Vhd='C:\Hyper-V\VHDX\drl-ops-01.vhdx' },
  @{ Name='drl-k8s-cp-01'; Vhd='C:\Hyper-V\VHDX\drl-k8s-cp-01.vhdx' },
  @{ Name='drl-k8s-wk-01'; Vhd='C:\Hyper-V\VHDX\drl-k8s-wk-01.vhdx' },
  @{ Name='drl-k8s-wk-02'; Vhd='C:\Hyper-V\VHDX\drl-k8s-wk-02.vhdx' }
)
New-Item -ItemType Directory -Force -Path $VmRoot, $VhdRoot | Out-Null
foreach ($Spec in $Specs) {
  $Vm = Get-VM -Name $Spec.Name -ErrorAction SilentlyContinue
  if (-not $Vm) {
    New-VM -Name $Spec.Name -Generation 2 -MemoryStartupBytes 4GB -Path $VmRoot -NewVHDPath $Spec.Vhd -NewVHDSizeBytes 40GB -SwitchName $SwitchName | Out-Null
    $Vm = Get-VM -Name $Spec.Name
    "Created $($Spec.Name)"
  } elseif ($Vm.Generation -ne 2) { throw "$($Spec.Name) is not Generation 2." }
  if ($Vm.State -ne 'Off') { throw "$($Spec.Name) must be Off; state is $($Vm.State)." }
  Set-VMProcessor -VMName $Spec.Name -Count 2
  Set-VMMemory -VMName $Spec.Name -DynamicMemoryEnabled $false -StartupBytes 4GB
  $Nic = Get-VMNetworkAdapter -VMName $Spec.Name | Select-Object -First 1
  if (-not $Nic) { Add-VMNetworkAdapter -VMName $Spec.Name -SwitchName $SwitchName }
  elseif ($Nic.SwitchName -ne $SwitchName) { Connect-VMNetworkAdapter -VMName $Spec.Name -SwitchName $SwitchName }
  [pscustomobject]@{
    Name=$Spec.Name; State=(Get-VM $Spec.Name).State; Generation=(Get-VM $Spec.Name).Generation
    CPU=(Get-VMProcessor $Spec.Name).Count; MemoryGB=((Get-VMMemory $Spec.Name).Startup/1GB)
    DynamicMemory=(Get-VMMemory $Spec.Name).DynamicMemoryEnabled
    Switch=(Get-VMNetworkAdapter $Spec.Name | Select-Object -First 1).SwitchName
    VHD=(Get-VMHardDiskDrive $Spec.Name).Path
  }
}
```

Expected: four objects with Generation 2, CPU 2, MemoryGB 4,
DynamicMemory False, switch drl-lab, and matching VHDX paths. If a disk path
conflicts, inspect it with Get-VMHardDiskDrive -VMName <name> and stop.

## 5. Install Ubuntu Server manually

For each VM, in Hyper-V Manager:

1. Confirm one network adapter is connected to drl-lab.
2. In Firmware, put DVD Drive before Hard Drive for the first boot.
3. Attach Ubuntu Server 24.04.3 ISO and start the VM.
4. Use the normal guided install and default Ubuntu LVM layout.
5. Create opsadmin, select Install OpenSSH server, finish, and reboot.
6. Enter the password interactively; never save it in this repository.

After installation, eject the ISO. This guarded command is safe if absent:

```powershell
$VmName = 'drl-ops-01' # Change for the VM being installed.
$Dvd = Get-VMDvdDrive -VMName $VmName | Select-Object -First 1
if ($Dvd -and $Dvd.Path) {
    Set-VMDvdDrive -VMName $VmName -ControllerNumber $Dvd.ControllerNumber -ControllerLocation $Dvd.ControllerLocation -Path $null
    "Ejected installation media from $VmName"
} else { "No ISO is mounted on $VmName" }
```

Expected: either Ejected installation media... or No ISO is mounted....

## 6. Start or verify the VM

```powershell
$VmName = 'drl-ops-01' # Change for the VM being configured.
$Vm = Get-VM -Name $VmName -ErrorAction Stop
if ($Vm.State -ne 'Running') { Start-VM -Name $VmName | Out-Null; "Started $VmName" }
else { "$VmName is already Running" }
Get-VM -Name $VmName | Select-Object Name, State, Status
```

Expected: State Running and status Operating normally. Use the Hyper-V console
for the first guest login.

## 7. Configure hostname and static guest IP

Inside each guest, discover its interface:

```bash
ip -br link
ip -br addr
```

Expected resembles:

```text
lo       UNKNOWN  127.0.0.1/8 ::1/128
ens160   UP       192.168.x.x/24
```

Use the actual non-loopback interface and the matching values:

| VM | Hostname | Address |
|---|---|---|
| Operations | drl-ops-01 | 192.168.50.10/24 |
| Control plane | drl-k8s-cp-01 | 192.168.50.20/24 |
| Worker 1 | drl-k8s-wk-01 | 192.168.50.21/24 |
| Worker 2 | drl-k8s-wk-02 | 192.168.50.22/24 |

```bash
set -euo pipefail
GUEST_HOSTNAME='drl-ops-01'       # Change for this VM.
GUEST_ADDRESS='192.168.50.10/24'  # Change for this VM.
INTERFACE='ens160'                # Change to the discovered interface.
sudo hostnamectl set-hostname "$GUEST_HOSTNAME"
sudo tee /etc/netplan/99-drl-lab.yaml >/dev/null <<EOF
network:
  version: 2
  ethernets:
    $INTERFACE:
      dhcp4: false
      addresses:
        - $GUEST_ADDRESS
EOF
sudo netplan generate
sudo netplan apply
hostnamectl --static
ip -br addr show "$INTERFACE"
```

Expected: the selected hostname, an UP interface, the selected
192.168.50.x/24 address, and no netplan error. There is no default route
because NAT is out of scope. Repeating overwrites the same managed file.

## 8. Install and verify SSH

```bash
sudo apt-get update
sudo apt-get install -y openssh-server
sudo systemctl enable --now ssh
systemctl is-enabled ssh
systemctl is-active ssh
ss -lntp | grep ':22'
```

Expected:

```text
enabled
active
LISTEN ... 0.0.0.0:22 ...
LISTEN ... [::]:22 ...
```

## 9. Configure and verify guest name resolution

The marked section is the only section managed, so this is repeat-safe:

```bash
set -euo pipefail
sudo sed -i '/^# BEGIN DRL LAB HOSTS$/,/^# END DRL LAB HOSTS$/d' /etc/hosts
sudo tee -a /etc/hosts >/dev/null <<'EOF'
# BEGIN DRL LAB HOSTS
192.168.50.10 drl-ops-01
192.168.50.20 drl-k8s-cp-01
192.168.50.21 drl-k8s-wk-01
192.168.50.22 drl-k8s-wk-02
# END DRL LAB HOSTS
EOF
getent hosts drl-ops-01 drl-k8s-cp-01 drl-k8s-wk-01 drl-k8s-wk-02
```

Expected: four lines map all four names to their 192.168.50.x addresses.

## 10. Configure and verify UFW

Add the SSH rule before enabling UFW:

```bash
sudo apt-get install -y ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow from 192.168.50.1 to any port 22 proto tcp
sudo ufw --force enable
sudo systemctl enable ufw
sudo ufw status verbose
```

Expected:

```text
Status: active
Default: deny (incoming), allow (outgoing), deny (routed)
192.168.50.1 22/tcp  ALLOW IN
```

If a broad 22/tcp ALLOW IN Anywhere rule exists, remove it only after
confirming it is not needed. The intended boundary is the Windows host only.

## 11. Verify each guest locally

```bash
set -euo pipefail
EXPECTED_HOSTNAME='drl-ops-01'      # Change for this VM.
EXPECTED_ADDRESS='192.168.50.10/24' # Change for this VM.
INTERFACE='ens160'                  # Change if needed.
test "$(hostnamectl --static)" = "$EXPECTED_HOSTNAME"
ip -o -4 addr show dev "$INTERFACE" | grep -F "$EXPECTED_ADDRESS"
systemctl is-active --quiet ssh
systemctl is-enabled --quiet ssh
sudo ufw status | grep -F '192.168.50.1' | grep -F '22/tcp'
getent hosts drl-ops-01 drl-k8s-cp-01 drl-k8s-wk-01 drl-k8s-wk-02
echo "PASS: local identity, address, SSH, UFW, and host resolution"
```

Expected final line: PASS: local identity, address, SSH, UFW, and host
resolution. Any failed check stops the block.

## 12. Configure the Windows hosts file

Run as Administrator. The managed block is replaced; unrelated entries stay.

```powershell
$ErrorActionPreference = 'Stop'
$HostsPath = Join-Path $env:SystemRoot 'System32\drivers\etc\hosts'
$Begin = '# BEGIN DRL LAB HOSTS'
$End = '# END DRL LAB HOSTS'
$Entries = @(
  '192.168.50.10 drl-ops-01',
  '192.168.50.20 drl-k8s-cp-01',
  '192.168.50.21 drl-k8s-wk-01',
  '192.168.50.22 drl-k8s-wk-02'
)
$Content = Get-Content $HostsPath -Raw
$Pattern = '(?ms)^' + [regex]::Escape($Begin) + '\r?\n.*?^' + [regex]::Escape($End) + '\r?\n?'
$Content = [regex]::Replace($Content, $Pattern, '')
$Block = $Begin + [Environment]::NewLine + ($Entries -join [Environment]::NewLine) + [Environment]::NewLine + $End
Set-Content $HostsPath ($Content.TrimEnd() + [Environment]::NewLine + $Block + [Environment]::NewLine) -Encoding ascii
Select-String $HostsPath -Pattern 'drl-ops-01|drl-k8s-cp-01|drl-k8s-wk-01|drl-k8s-wk-02'
```

Expected: one line per hostname and matching address. Access denied means
PowerShell was not opened as Administrator.

## 13. Verify Windows-to-guest TCP and SSH

```powershell
$Targets = @(
  @{ Name='drl-ops-01'; IP='192.168.50.10' },
  @{ Name='drl-k8s-cp-01'; IP='192.168.50.20' },
  @{ Name='drl-k8s-wk-01'; IP='192.168.50.21' },
  @{ Name='drl-k8s-wk-02'; IP='192.168.50.22' }
)
foreach ($Target in $Targets) {
  $ByIP = Test-NetConnection $Target.IP -Port 22 -WarningAction SilentlyContinue
  $ByName = Test-NetConnection $Target.Name -Port 22 -WarningAction SilentlyContinue
  [pscustomobject]@{ Name=$Target.Name; IPPort22=$ByIP.TcpTestSucceeded; HostnamePort22=$ByName.TcpTestSucceeded }
}
```

Expected: True for both checks for all four VMs.

```powershell
ssh opsadmin@drl-ops-01 'hostname; hostname -I; sudo ufw status | head -n 8'
ssh opsadmin@drl-k8s-cp-01 'hostname; hostname -I; sudo ufw status | head -n 8'
ssh opsadmin@drl-k8s-wk-01 'hostname; hostname -I; sudo ufw status | head -n 8'
ssh opsadmin@drl-k8s-wk-02 'hostname; hostname -I; sudo ufw status | head -n 8'
```

Enter the password interactively. Expected: matching hostname, 192.168.50.x
address, and Status: active for each.

## 14. Reboot-verify each guest

Reboot one guest at a time after its configuration passes the local and
Windows SSH checks. Run inside the guest:

```bash
sudo reboot
```

Expected: the SSH session closes. After the guest returns, rerun the local
checkpoint from section 11 and the Windows TCP check from section 13. Both
must pass again, proving that the hostname, static address, SSH service, UFW
policy, and hosts-file configuration survive a reboot.

## 15. Verify the Hyper-V inventory

```powershell
$VmNames = 'drl-ops-01','drl-k8s-cp-01','drl-k8s-wk-01','drl-k8s-wk-02'
Get-VM -Name $VmNames | Select-Object Name, State, Status, Generation,
  @{Name='MemoryGB';Expression={(Get-VMMemory -VMName $_.Name).Startup/1GB}},
  @{Name='CPU';Expression={(Get-VMProcessor -VMName $_.Name).Count}}
foreach ($VmName in $VmNames) {
  Get-VMNetworkAdapter -VMName $VmName | Select-Object VMName, SwitchName, Status
  Get-VMHardDiskDrive -VMName $VmName | Select-Object VMName, Path
}
```

Expected: four VMs; Generation 2; CPU 2; memory 4 GB; switch drl-lab; and
matching VHDX paths under C:\Hyper-V\VHDX.

## 16. Verify the guest-to-guest firewall boundary

From drl-ops-01, test the other three guests:

```bash
for target in 192.168.50.20 192.168.50.21 192.168.50.22; do
  if timeout 5 bash -c "cat < /dev/null > /dev/tcp/$target/22" 2>/dev/null; then
    echo "UNEXPECTED: $target:22 is reachable"
  else
    echo "EXPECTED BLOCK: $target:22 is not reachable"
  fi
done
```

Expected: EXPECTED BLOCK for all three. From the control plane and each
worker, run the same test against 192.168.50.10:

```bash
if timeout 5 bash -c 'cat < /dev/null > /dev/tcp/192.168.50.10/22' 2>/dev/null; then
  echo "UNEXPECTED: 192.168.50.10:22 is reachable"
else
  echo "EXPECTED BLOCK: 192.168.50.10:22 is not reachable"
fi
```

Expected: EXPECTED BLOCK. Timeout or refusal is acceptable; a successful TCP
connection is not.

## 17. Final handoff checklist

- [ ] Hyper-V and vmms are healthy.
- [ ] drl-lab is Internal and vEthernet (drl-lab) is 192.168.50.1/24.
- [ ] All four VMs have approved generation, CPU, memory, switch, and VHDX.
- [ ] Each VM boots from its installed VHDX after reboot.
- [ ] Each guest reports the approved hostname and static address.
- [ ] SSH works from Windows by IP and hostname for opsadmin.
- [ ] Windows and guest hosts files contain all four mappings.
- [ ] Each guest resolves all four names with getent hosts.
- [ ] UFW is active with default-deny incoming on every guest.
- [ ] UFW allows TCP 22 from 192.168.50.1.
- [ ] Guest-to-guest TCP 22 tests fail as expected.
- [ ] No Kubernetes, NAT, guest Internet access, or DNS server was added.

Known limitations: Ubuntu installation and credentials remain manual; there is
no automatic DNS or DHCP; NAT and guest Internet access are not configured;
SSH key hardening and Kubernetes traffic rules are future work; WSL2 and other
administrative origins have not been validated.

See [docs/environment.md](../docs/environment.md) for the implemented record and
[architecture/adr/001-hyper-v-lab-network.md](../architecture/adr/001-hyper-v-lab-network.md)
for the approved network design.




