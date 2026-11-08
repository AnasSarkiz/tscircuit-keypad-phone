# Preserved pre-migration source

These are unchanged snapshots of the three footprint providers and their former TypeScript tests/input gate before the 2026-11-08 JLC migration. They require historical JSON files absent from the recovery bundle and are retained for comparison, not used by the current build. Git commit1cdd7ca also preserves the complete prior tree.

Active sources now use the six exact normal JLC imports. Existing historical Python tests remain in tests/ and still require their original data/routed outputs; they are not represented as passing tests. New placement and source-net checks do not replace routed-board DRC or manufacturing validation.
