# basyx-setup

Local Eclipse BaSyx Java V2 Digital Twin server for the AAS V3 exercise.

## 1. Run the project

Install Docker with the Compose plugin (Docker Desktop on Windows/macOS).
From this directory run:

```sh
docker compose up
```

- AAS Editor: http://localhost:3000/aaseditor
- REST API / Swagger: http://localhost:8081/swagger-ui/index.html
- List shells: http://localhost:8081/shells

The default configuration imports `changed-shell.aasx` (two demo shells) and `new-shell.aasx` (one personal shell) on startup. It does not import the original simultaneously because it has the same IDs as the changed package. In-memory storage resets on restart; saved AASX files are the durable deliverables. Both ports are bound to localhost. No authentication is configured; this is a local learning setup only.

## 2. Repeat the original exercise in the server

Stop the default setup (`docker compose down`). Start with no preloaded shells:

```sh
BASYX_ENVIRONMENT='' docker compose up
```

In PowerShell, use `$env:BASYX_ENVIRONMENT=''` only if your version preserves empty environment variables; alternatively set it to `file:/application/aas/ExampleV3.aasx` to start with the original already imported. You can also set `BASYX_ENVIRONMENT` in an `.env` file to an empty value before starting Compose.

Open the AAS Editor. Use its import/upload action to select `ExampleV3.aasx` if not already loaded. Select Demo AAS V3 > Demo Submodel V3 > Demo List (`DemoSMLV3`). Add a Property with these fields:

| Field | Value |
|---|---|
| ID short | Element3 |
| Display name (en) | Third Element |
| Value type | xs:string |
| Value | third |

Save the edit and use the shell download/export action to export an AASX file named `changed-shell.aasx`. The supplied example contains two shells; exporting only Demo AAS V3 may omit the second one. The included offline-generated package preserves both.

Create a new shell with a unique ID, asset kind Instance and your actual name as its English display name. Export it as `new-shell.aasx`. The included personal shell uses the repository username `ashirzad313` as a placeholder; replace it with your actual name if different. The original demo already uses ID shorts on list entries, and the exercise explicitly requires Element3. Strict AAS validators may reject ID shorts on list children (AASd-120); do not silently remove the requested field.

The included packages were generated offline, not downloaded from a live server. Complete the live import/edit/export sequence above to demonstrate the assignment. If the UI refuses the requested ID short, show the assignment requirement and original file to your evaluator.

## 3. Bonus Python script

No third-party Python packages needed (Python 3.9+).

```sh
python transfer.py list
python transfer.py upload ExampleV3.aasx
```

Use the upload command on an empty server to avoid duplicate IDs. The script sends a multipart POST to `/upload` and prints the HTTP response. `list` sends GET `/shells`.

## 4. Reproduce the supplied packages offline

```sh
python prepare_shells.py --name "Your actual name"
python verify_shells.py
```

`prepare_shells.py` preserves the original and supplementary files; it replaces the output packages. `verify_shells.py` checks ZIP integrity, the requested property, the personal shell and preserved attachments. This is not full AAS schema validation.

## 5. Submit

```sh
git add .
git commit -m "Complete AAS server exercise"
git push origin main
```

`repo.txt` contains the GitHub link. Docker startup and browser interactions must be verified locally; this project was prepared in an environment without Docker.

## References

- [AAS Environment](https://wiki.basyx.org/en/latest/content/user_documentation/basyx_components/v2/aas_environment/index.html)
- [Web UI Docker configuration](https://wiki.basyx.org/en/latest/content/user_documentation/basyx_components/web_ui/features/docker_config.html)
- [AAS Editor](https://wiki.basyx.org/en/latest/content/user_documentation/basyx_components/web_ui/features/aas_editor.html)
- [Original example](https://github.com/eclipse-basyx/basyx-java-server-sdk/tree/main/examples/BaSyxMinimal/aas) (identical to the supplied input).
