# Day 13 chat flow snapshots

Captured November 27, 2026, during Mission 1, Task 1 of the Neptune Insurance architect bootcamp.

| Export | Purpose |
| --- | --- |
| [Neptune-Inbound-Chat-before-Day13.json](Neptune-Inbound-Chat-before-Day13.json) | Baseline supplied before the Day 13 recovery drill. |
| [Neptune-Day13-Recovery-Chat.json](Neptune-Day13-Recovery-Chat.json) | Supplied recovery-copy export, archived under the owner's filename. |

Both supplied exports contain the same 20 executable actions and valid connected targets. Their designer-generated condition IDs differ. Both exports retain `Metadata.name = Neptune-Inbound-Chat`; the supplied filename alone does not establish a distinct deployed flow identity. The original internal name and graph are preserved. No version A marker is present in either snapshot. This archive does not mark Day 13, publication, rollback or runtime tests complete.

## Public resource placeholders

The public JSON follows the existing Connect template convention. AWS account, instance, queue, hours, follow-up flow, Agentic CX workspace, application and deployed-alias bindings are replaced consistently throughout the files. Prompts, attributes, block identifiers, connections and routing logic are retained. The uploaded originals are retained privately outside the Git checkout.

| Placeholder | Resource to select in the destination instance |
| --- | --- |
| `000000000000` | AWS account |
| `00000000-0000-0000-0000-000000000000` | Connect instance |
| `11111111-1111-1111-1111-111111111111` | Existing Neptune lab hours |
| `22222222-2222-2222-2222-222222222222` | Auto Claims queue |
| `33333333-3333-3333-3333-333333333333` | Neptune-Billing queue |
| `44444444-4444-4444-4444-444444444444` | Neptune Insurance Lab Agentic CX workspace |
| `55555555-5555-5555-5555-555555555555` | NeptuneInsurance application |
| `66666666-6666-6666-6666-666666666666` | Existing Claims follow-up task flow |
| `RESELECT_DEPLOYED_ALIAS` | Existing deployed application alias, shown as Production in the supplied export |

These public templates require rebinding before import/use. They do not include the application, queues, users, hours or task resources. Import only into the intended isolated lab flow, confirm its name and resource selections, then save/publish as appropriate. Importing an export is not proof of a successful customer interaction.
