# X-Plane 12 Flight Planner

This Python package aims at recreating the experience of the free and useful
[onlineflightplanner.org](https://onlineflightplanner.org). As the original web site is
not well maintained anymore, I wanted to have a CLI tool which provides me the same
functionality without being dependent on the maintenance state.

In terms of defaults and file locations, this code is currently heavily opinionated.
Just raise an issue if you find this project useful and I will add a proper
configuration system.

Also in terms of file types and available planes, this project is currently limited to
my needs. The only current file output is a PDF and an FMS v11 file. You can choose from
these planes:

- A319
- A320
- A321
- A330
- A340
- B737 (-800X, the Zibo Mod)

## Usage

Just execute the program without parameters and you will the help text:

```bash
$ uv run xplane12-flightplanner

 Usage: xplane12-flightplanner [OPTIONS] COMMAND [ARGS]...

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                                                                                                   │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                                                                                            │
│ --help                        Show this message and exit.                                                                                                                                                                                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ create  Create flightplan files for desired departure and arrival in the download dir.                                                                                                                                                                    │
│ delete  Delete a potentially existing flightplan tuple of FMS and PDF.                                                                                                                                                                                    │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Create

Read the help text:

```bash
$ uv run xplane12-flightplanner create --help

 Usage: xplane12-flightplanner create [OPTIONS] {plane} {departure} {arrival}

 Create flightplan files for desired departure and arrival in the download dir.

 Args:
 plane: The desired plane type. One of A319, A320, A321, A330, A340, B737
 departure: The departure airport's ICAO code (e.g. EDDW)
 arrival: The arrival airport's ICAO code (e.g. EDDM)
 min_level: Minimum flight level for the given plan
 max_level: Maximum flight level for the given plan
 airac_cycle: Your AIRAC data's release date. This is updated eventually with
              X-Plane versions. You can find it in your plane's FMS computer or
              e.g. in your installation directory in the file
              "X-Plane 12/Resources/default data/earth_awy.dat"

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    plane          <str>  [required]                                                                                                                                                                                                                     │
│ *    departure      <str>  [required]                                                                                                                                                                                                                     │
│ *    arrival        <str>  [required]                                                                                                                                                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --min-level          <int>  [default: 300]                                                                                                                                                                                                                │
│ --max-level          <int>  [default: 400]                                                                                                                                                                                                                │
│ --airac-cycle        <str>  [default: 2406]                                                                                                                                                                                                               │
│ --help                      Show this message and exit.                                                                                                                                                                                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

In the easiest use case, just choose your plane, departure ICAO and arrival ICAO:

```bash
$ uv run xplane12-flightplanner create A320 KJFK KBOS
Flight Plan Obtained
Fuel Plan Obtained
FMS file written to <xplane12_location>/Output/FMS plans/KJFKKBOS.fms
PDF file written to <pdf_file_location>/A320/A320-KJFK-KBOS.pdf
```

### Delete

You can easily remove existing file tuples via `delete`.

Read the help text:

```bash
$ uv run xplane12-flightplanner delete --help

 Usage: xplane12-flightplanner delete [OPTIONS] {plane} {departure} {arrival}

 Delete a potentially existing flightplan tuple of FMS and PDF.

 Args:
 plane: The desired plane type. One of A319, A320, A321, A330, A340, B737
 departure: The departure airport's ICAO code (e.g. EDDW)
 arrival: The arrival airport's ICAO code (e.g. EDDM)

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    plane          <str>  [required]                                                                                                                                                                                                                     │
│ *    departure      <str>  [required]                                                                                                                                                                                                                     │
│ *    arrival        <str>  [required]                                                                                                                                                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                                                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

In the easiest use case, just choose your plane, departure ICAO and arrival ICAO and
confirm the deletion:

```bash
$ uv run xplane12-flightplanner delete A320 KJFK KBOS
Do you want to delete the currently existing flight plan files? [y/n] (y):
File(s) Deleted
```
