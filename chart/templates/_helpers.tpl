{{- define "rate-my-guinness.fullname" -}}
{{- printf "%s" .Release.Name -}}
{{- end -}}

{{- define "rate-my-guinness.name" -}}
rate-my-guinness
{{- end -}}
