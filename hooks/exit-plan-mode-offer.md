# Optional ExitPlanMode Hook

This is an opt-in Claude Code hook for users who want a reminder at plan
finalization. It does not run `temp-agency-plan` automatically; it only prints a
reminder when `ExitPlanMode` is about to run.

Install by adapting this snippet into your personal Claude Code hook settings:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "printf '%s\\n' 'Optional: run /temp-agency-plan on this draft before it hardens.'"
          }
        ]
      }
    ]
  }
}
```

Remove the snippet to uninstall. Keep this separate from repository defaults; the
hook is never wired globally by Temp Agency.
