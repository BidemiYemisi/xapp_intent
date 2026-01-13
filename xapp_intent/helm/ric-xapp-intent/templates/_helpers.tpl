{{- define "xapp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end}}
{{- define "xapp.fullname" -}}
{{ include "xapp.name" . }}
{{- end}}
