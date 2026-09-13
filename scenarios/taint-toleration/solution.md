Export audit-agent, add this toleration, then recreate the Pod under the same name while preserving its nodeSelector:

    tolerations:
    - key: training
      operator: Equal
      value: dedicated
      effect: NoSchedule
