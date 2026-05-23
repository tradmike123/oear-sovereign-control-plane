# OEAR — Gobernanza Cognitiva Verificable con Certificación Mecánica y Telemetría Longitudinal

**Whitepaper Técnico — Versión v1**

**Autor**: Miguel Garay  
**Sistema**: OEAR Sovereign Control Plane  
**Estado**: Certificación Mecánica v1 + Telemetría Diferencial Activa  

## Resumen (Abstract)

Este documento presenta OEAR, una arquitectura de gobernanza cognitiva verificable diseñada para controlar sistemas de inferencia probabilística mediante un plano de control determinista, validación mecánica de invariantes y certificación reproducible. El sistema separa explícitamente la generación de salidas (LLM) de la gobernanza, aplicando gates de riesgo, validadores contractuales, bitácora forense y métricas persistentes. Se implementa un arnés sintético de pruebas con vectores versionados y congelados criptográficamente, junto con validación automática de equivalencia y quality gates integrados en el flujo de Git. Sobre esta base se añade telemetría longitudinal por commit y diagnóstico diferencial de drift por familia de prueba, permitiendo detectar degradación progresiva de la gobernanza antes de fallos críticos. El enfoque sustituye la confianza subjetiva por evidencia mecánica reproducible, ofreciendo un marco de ingeniería responsable para sistemas cognitivos asistidos.

## 1. Problema

Los modelos de lenguaje y sistemas cognitivos probabilísticos producen salidas plausibles pero no garantizadas. La mayoría de integraciones dependen de filtros heurísticos o validaciones ad-hoc, lo que introduce:
- **Deriva silenciosa**
- **Pérdida de control de invariantes**
- **Cambios no detectados tras refactorización**
- **Confianza no verificable**

El problema no es la potencia del modelo, sino la ausencia de gobernanza verificable.

## 2. Principio de Diseño

OEAR adopta un principio central: **La confianza no se deposita en el modelo, sino en artefactos verificables.**

Separación estricta de capas:
1. **Capa probabilística**: LLM / generador
2. **Capa determinista**: Control Plane OEAR
3. **Capa forense**: Journal + Metrics
4. **Capa de prueba**: Harness sintético
5. **Capa de certificación**: Validator de invariantes
6. **Capa de tendencia**: Telemetría longitudinal

## 3. Arquitectura del Sistema

**Pipeline de interacción:**
Input → State Reducer → Integrity Gate (PS3) → Risk Scoring (PS2) → Gate A/B/C → Route Select → Prompt Wrapper → LLM Call → Output Validator → Commit o Block → Journal Append → MetricsHook

**Propiedades:**
- Determinismo en gobernanza
- Bloqueo fail-closed
- Trazabilidad completa
- Registro append-only

## 4. Sistema de Gates de Riesgo

Clasificación por métricas sintéticas:
- **Gate A — Seguro**: flujo normal.
- **Gate B — Riesgo medio**: wrapper endurecido + auditoría.
- **Gate C — Riesgo alto o invariantes violados**: bloqueo inmediato.

Gate C genera un evento `gate_block`, el hash SHA-256 del disparador y un registro forense obligatorio.

## 5. Output Validator Contractual

El validador clasifica salidas en:
- **SOFT_FAIL**: permite reintento con wrapper endurecido programáticamente.
- **HARD_FAIL**: bloqueo definitivo con respuesta segura y métrica crítica.

Ninguna salida se emite sin validación.

## 6. Journal Forense

Bitácora append-only estructurada que verifica:
- Monotonicidad temporal
- Presencia de `input_hash` en bloqueos
- Correlación causal con métricas
- Secuencia válida de fases (`gate_block`, `validator_fail`, `commit_ok`)

## 7. Arnés Sintético de Certificación

Harness determinista sin LLM real con 23 vectores (v1) cubriendo Gate A/B/C, freeze, invariantes y bordes. La línea base se congela con SHA-256.

## 8. Certificación Mecánica

El validador automático certifica la integridad del vector set, la monotonicidad temporal, la correlación causal y la secuencia de fases. El resultado es binario: `CERTIFICATION PASSED / FAILED`.

## 9. Quality Gates en Control de Versiones

Integración con Git:
- **Pre-commit**: validación de equivalencia y chequeo de invariantes.
- **Pre-push**: harness completo y certificación mecánica.

## 10. Telemetría Longitudinal

Rastrea `block_rate`, `soft_fail_rate`, `freeze_rate` y `drift` promedio por commit, indexado por commit hash para detectar degradación lenta.

## 11. Diagnóstico Diferencial de Grip

Cálculo de drift promedio por familia (`SAFE`, `HIGH`, `BORDER`, `INVARIANT`). Permite detectar erosión de frontera de gobernanza (grip weakening) antes de la ruptura.

## 12. Propiedades Científicas del Enfoque

Cumple con principios de falsabilidad, reproducibilidad, trazabilidad, inmutabilidad de baseline y verificación criptográfica. No es confianza declarada; es evidencia mecánica.

## 13. Estado Actual

**Estado: Publicable — Certificado — Instrumentado**
Implementado con control plane gobernado, validator endurecido, journal forense, harness sintético y telemetría longitudinal activa.
