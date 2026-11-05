# SLI, SLO and alerting design

## Initial objectives (learning targets)
- Availability SLI: successful eligible requests (HTTP 2xx/3xx) divided by all eligible requests.
- Initial availability SLO: 99.5% over a rolling 30-day window.
- Latency SLI: proportion of eligible requests completed in under 500ms.
- Initial latency objective: 95% of eligible requests under 500ms over 30 days.

These are teaching examples, not universal production recommendations. Real targets should reflect user expectations, business impact, traffic profile and dependencies.

## Error budget
A 99.5% availability objective permits 0.5% unsuccessful requests. For a time-based 30-day window, 0.5% is 3.6 hours. For request-based SLIs, calculate the budget from eligible request volume.

## Alert philosophy
Page on sustained user-visible symptoms and meaningful error-budget burn. Use warning notifications for slower degradation. Avoid paging on every exception or transient spike. The included Prometheus rules are starter rules; a mature implementation should add multi-window, multi-burn-rate SLO alerts and test thresholds against observed traffic.
