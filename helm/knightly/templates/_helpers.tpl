{{/*
Expand the name of the chart.
*/}}
{{- define "knightly.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "knightly.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{- define "knightly.controllerFullname" -}}
{{- printf "%s-controller" (include "knightly.fullname" .) | trunc 63 }}
{{- end }}

{{- define "knightly.annotatorFullname" -}}
{{- printf "%s-annotator" (include "knightly.fullname" .) | trunc 63 }}
{{- end }}

{{- define "knightly.zeroScalerFullname" -}}
{{- printf "%s-zero-scaler" (include "knightly.fullname" .) | trunc 63 }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "knightly.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "knightly.commonLabels" -}}
helm.sh/chart: {{ include "knightly.chart" . }}
app.kubernetes.io/name: {{ include "knightly.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "knightly.controllerLabels" -}}
{{ include "knightly.commonLabels" . }}
{{ include "knightly.controllerSelectorLabels" . }}
{{- end }}

{{- define "knightly.annotatorLabels" -}}
{{ include "knightly.commonLabels" . }}
{{ include "knightly.annotatorSelectorLabels" . }}
{{- end }}

{{- define "knightly.zeroScalerLabels" -}}
{{ include "knightly.commonLabels" . }}
{{ include "knightly.zeroScalerSelectorLabels" . }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "knightly.controllerSelectorLabels" -}}
knightly.everc.com/service: controller
{{- end }}
{{- define "knightly.annotatorSelectorLabels" -}}
knightly.everc.com/service: annotator
{{- end }}
{{- define "knightly.zeroScalerSelectorLabels" -}}
knightly.everc.com/service: zero-scaler
{{- end }}

{{/*
Create the name of the service account to use for controller
*/}}
{{- define "knightly.controllerServiceAccountName" -}}
{{- if .Values.controller.serviceAccount.create }}
{{- default (include "knightly.controllerFullname" .) .Values.controller.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.controller.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the service account to use for annotator
*/}}
{{- define "knightly.annotatorServiceAccountName" -}}
{{- if .Values.annotator.serviceAccount.create }}
{{- default (include "knightly.annotatorFullname" .) .Values.annotator.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.annotator.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the service account to use for zero-scaler
*/}}
{{- define "knightly.zeroScalerServiceAccountName" -}}
{{- if .Values.zeroScaler.serviceAccount.create }}
{{- default (include "knightly.zeroScalerFullname" .) .Values.zeroScaler.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.zeroScaler.serviceAccount.name }}
{{- end }}
{{- end }}
