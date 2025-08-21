name: Bug report
description: File a bug report
labels: [bug]
body:
  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: Describe the bug
      placeholder: A clear and concise description
    validations:
      required: true
  - type: input
    id: steps
    attributes:
      label: Steps to reproduce
      placeholder: 1. Go to '...'
  - type: input
    id: env
    attributes:
      label: Environment
      placeholder: OS, Python version
