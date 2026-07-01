# CLAUDE.md — aiocomfoconnect (m7les fork)

Asyncio Python library for the Zehnder ComfoConnect LAN C protocol (PDO stream +
RMI request/response over the unit's CANbus). This is the **m7les fork**, ahead of
upstream `michaelarnauts/aiocomfoconnect`.

## Repo / release
- Working branch: `feat/full-pdo-and-rmi-coverage`. `origin` = m7les fork.
- Consumed by the HA integration via a **git tag pin** (`aiocomfoconnect @ git+...@vX.Y.Z`).
  When you add/change a public method the HA side uses, you MUST: bump `pyproject.toml`,
  commit, **create a new tag**, push branch + tag, then re-pin the HA `manifest.json`.
  An untagged push does nothing for HA.
- Tests: `.venv/bin/python -m pytest` (poetry env). Keep new getters/setters covered by
  asserting the exact RMI wire bytes (see `tests/test_properties.py`).

## Core design principle
The library exposes **all data raw**. It does NOT decode/label mode enums — all
enum→text mapping and presentation lives in the HA integration. Don't add enum
string maps here; keep `value_fn` limited to numeric scaling (e.g. INT16 temps ÷10).

## PDOs (`sensors.py`)
- 158 PDOs defined. `SENSORS_STANDARD` (72 named) vs `SENSORS_DEBUG` (86 unknown,
  named `sensor_<id>`). Unknown PDOs stream but their meaning isn't mapped yet.
- PDO 212 is intentionally `INT16` though the doc says `UINT8` (backward-compat).
  Tests whitelist it via `TYPE_EXCEPTIONS = {212}` in `tests/test_sensors.py`.
- Sentinel values seen on absent features: `-40.0`, `-25344` = "not present/available".

## RMI (`comfoconnect.py`, `properties.py`, `const.py`)
- Primitives: `get_property(Property)`, `get_single_property(unit,sub,prop,type)`,
  `set_property_typed(...)`. `Property` dataclass holds unit/subunit/property_id/type.
- Registration: use `ComfoConnect.register()` (one-shot low-level connect). The normal
  `connect()` reconnect-loop tears down the socket on `ComfoConnectNotAllowed`, which
  breaks a register-then-connect flow.

### Protocol gotchas (important — these are non-obvious)
- **Boost is a schedule TIMER entry, not a boolean.** SCHEDULE unit `0x15`, subunit `0x01`:
  - `0x06` = app-boost (`get_boost`/`set_boost`)
  - `0x08` = BOOSTSWITCH = the physical wall button (`get_bathroom_boost`/`cancel_bathroom_boost`)
  - `0x0b` = away
  These are **independent timers**. `set_boost(False)` only clears `0x06`; a wall-button
  boost must be cleared via `0x08` (`cancel_bathroom_boost`).
- **Auto/manual mode is a DIFFERENT timer** — subunit `0x08`, property `0x01`
  (`get_mode`/`set_mode`). Selecting "auto" does NOT cancel a boost.
- **Timeout `-1`** (0xFFFFFFFF) = indefinite / "until cancelled" sentinel (used by
  comfocool and by the HA boost latch). Timeout field is signed int32 seconds.
- **Bathroom-switch installer config** (VENTILATIONCONFIG `0x1e`, sub `0x01`):
  `0x0b` activation delay (INT16 s, **writable**), `0x0c` deactivation/boost duration
  (UINT8 min, **writable**), `0x0d` mode (UINT8 0=fixed/1=mirrored — accepts a write but
  the unit ignores it, so treat as **read-only**). Writability was verified on real HW;
  the protocol doc's blank `rw` column is unreliable.

## Live hardware & probing
- Reference unit: ComfoAir Q350, bridge `comfoconnect_lan_c.jtt.lfnt.xyz` (reachable via
  Tailscale). Test app `aiocc-claude-test` is registered on the bridge.
- Reusable RE tool (kept in the parent working dir, **not committed** — it writes to
  hardware and hardcodes the bridge): `../probe_property.py`. Reads any unit/subunit/
  property; `--write` does a non-destructive write-then-restore to test writability.

## Known unknowns (RE backlog)
- 86 unknown PDOs → observational RE (stimulus/response on the live stream), not RMI.
- 47 `??` RMI property rows in `docs/PROTOCOL-RMI.md`.
- 5 undocumented sensor units: temp `0x21`, humidity `0x22`, pressure `0x23`,
  analog input `0x25`, CO2 `0x2b` — property layouts unknown; need an ID sweep
  (many may be absent on any given unit and just error out).
