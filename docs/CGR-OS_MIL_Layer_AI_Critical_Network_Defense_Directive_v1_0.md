# CGR-OS / MIL Layer
## AI Critical Network Defense Directive
### Directiva de Defensa en Profundidad para Infraestructuras Críticas de IA en Redes Aisladas, Multihomed y DNS Seguro

**Autor / Arquitecto Principal:** Miguel Garay Gracia  
**Rol:** Ingeniero Informático / Arquitecto de Sistemas de IA y Seguridad Crítica  
**Afiliación operativa:** Antigua Orden Dominicana  
**Página oficial:** www.eldominicanoespanol.com  
**Clasificación operativa:** Directiva técnica defensiva  
**Dominio:** IA crítica, redes corporativas, air-gap, BGP, DNS seguro, Zero Trust, DFIR  
**Versión:** CGR-OS / MIL Layer v1.0 — Public Release  
**Fecha:** 13 de mayo de 2026

---

## Resumen Ejecutivo

La integración de sistemas de Inteligencia Artificial en infraestructuras críticas obliga a redefinir el perímetro de seguridad. Un entorno air-gap reduce exposición, pero no elimina riesgo. Bajo una arquitectura de Confianza Cero, ninguna red debe considerarse confiable por estar aislada; todo flujo, dispositivo, transferencia, resolución DNS, ruta BGP y operación de inferencia debe ser verificada.

Esta directiva adopta una postura MIL Layer: la infraestructura de IA no se conecta primero para luego protegerla; se valida, segmenta, firma, enruta, monitorea y solo entonces se expone bajo control.

---

## Principio Rector

Un núcleo de IA en infraestructura crítica no debe ser tratado como un servidor tradicional. Debe ser tratado como un activo estratégico compuesto por pesos del modelo, datos de entrenamiento, datasets sensibles, pipelines de inferencia, resolución DNS, rutas BGP, identidad de acceso, telemetría, emisiones físicas, medios removibles y superficie semántica de prompts, herramientas y agentes.

El fallo de una sola capa puede comprometer el sistema completo.

---

## Arquitectura CGR-OS / MIL Layer

| Capa | Función |
|---|---|
| MIL-0 Gobernanza | Define autoridad, clasificación, responsables y reglas de exposición |
| MIL-1 Red | BGP multihomed, RPKI/ROV, filtrado, rutas resilientes |
| MIL-2 DNS | DNSSEC, ZONEMD, TSIG, PDNS, RPZ, DoH/DoT/DoQ corporativo |
| MIL-3 Zero Trust | PDP/PEP, mTLS, SPA, identidad continua |
| MIL-4 IA segura | Control de prompts, herramientas, RAG, datos, modelos y agentes |
| MIL-5 Red-Black | Separación física/lógica, control de medios, transferencia validada |
| MIL-6 DFIR/SOC | SIEM, EDR, NDR, DNSTAP, BGP logs, detección de anomalías |

---

## Directiva BGP Multihomed

La infraestructura de IA crítica debe usar conectividad multihomed con dos o más proveedores cuando exista exposición operativa o dependencia de red externa.

Controles obligatorios:

- ASN propio cuando el caso de uso lo justifique.
- eBGP con múltiples ISPs.
- RPKI.
- ROA.
- Route Origin Validation.
- Prefix filtering.
- Max-prefix.
- uRPF / Source Address Validation.
- Monitoreo de route leaks.
- Control de comunidades BGP.
- Alertas ante anuncios no autorizados.

El tráfico saliente se controlará mediante Local Preference, política de prefijos, comunidades BGP y multipath cuando aplique. El tráfico entrante se influirá mediante AS_PATH prepending, comunidades BGP con proveedores, anuncios selectivos de prefijos, desagregación controlada y políticas documentadas por región y criticidad.

---

## Directiva DNS Seguro según NIST SP 800-81r3

El DNS corporativo debe operar como punto de aplicación de políticas. Ningún workload de IA puede usar resolvers externos no autorizados.

Controles obligatorios:

- DNSSEC validation.
- Trust anchors actualizados.
- Protective DNS.
- RPZ.
- DNSTAP.
- QNAME minimization.
- Bloqueo de DoH/DoT/DoQ externo.
- Logging hacia SIEM.
- Detección de túneles DNS.
- Análisis de entropía de QNAME y TXT.

### DNSSEC, ZONEMD y TSIG

| Control | Función |
|---|---|
| TSIG | Autentica transferencias AXFR/IXFR entre servidores |
| DNSSEC | Autentica respuestas DNS y protege integridad de datos publicados |
| ZONEMD | Verifica el digest completo de una zona como objeto |

ZONEMD no reemplaza a TSIG ni a DNSSEC. Los tres controles son complementarios.

### Puertos y protocolos DNS cifrados

| Protocolo | Puerto |
|---|---|
| DoT | TCP/853 |
| DoQ | UDP/853 |
| DoH | HTTPS/443; TCP/443 para HTTP/2 y UDP/443 solo cuando se use HTTP/3/QUIC corporativo |

---

## Directiva Zero Trust / SDP

Los servicios críticos de IA deben operar bajo principio de invisibilidad selectiva. La Nube Negra aplica a consolas administrativas, nodos de entrenamiento, pesos del modelo, almacenamiento de checkpoints, RAG privado, orquestadores, pipelines internos, APIs internas y sistemas de evaluación.

Los endpoints públicos de inferencia no deben exponerse directamente. Deben pasar por API Gateway, WAF/API firewall, rate limiting, mTLS cuando aplique, autorización por identidad, DLP, logging completo y evaluación de abuso.

---

## Seguridad específica de IA

La seguridad del modelo no se resuelve solo con red.

Controles obligatorios:

- Validación de prompts.
- Clasificación de fuentes confiables/no confiables.
- Aislamiento de herramientas.
- Allowlist de acciones.
- Sandboxing.
- DLP en prompts y respuestas.
- Registro de tool-calls.
- Control de RAG.
- Evaluación de salidas.
- Protección contra data poisoning.
- Control de supply chain de modelos, datasets y dependencias.

---

## Air-Gap, Red-Black y canales encubiertos

| Dominio | Contenido |
|---|---|
| Red | Pesos, datasets, PII, biometría, datos médicos, secretos, llaves, entrenamiento |
| Black | API cifrada, inferencia controlada, telemetría sanitizada, respuestas autorizadas |

Regla: ningún dato Red cruza hacia Black sin PDP, sanitización, trazabilidad y autorización explícita.

Clasificación defensiva:

| Canal | Severidad | Frecuencia operacional esperada | Control |
|---|---:|---:|---|
| USB/removable media | Muy alta | Alta | Bloqueo, allowlist, estación de transferencia |
| Supply chain | Muy alta | Media | SBOM, firma, validación, cuarentena |
| Acústico | Alta | Baja | Control de audio, móviles, sensores |
| Electromagnético | Alta | Baja | TEMPEST, cableado blindado |
| Magnético | Alta | Baja | Zonas sin smartphones, sensores |
| Óptico | Media/Alta | Baja | Opacidad LED, control de cámaras |
| Térmico | Media | Baja | Monitoreo térmico y separación física |
| Vibratorio | Media | Baja | Aislamiento mecánico y control de dispositivos |

Exfiltrar pesos completos de modelos modernos por canales físicos de baja tasa suele ser impráctico por tamaño. El riesgo más realista por esos canales es fuga de llaves, tokens, fragmentos, hashes, credenciales, muestras críticas o metadatos.

---

## Control de medios removibles

Todo medio removible queda prohibido por defecto. Excepciones solo bajo inventario, cifrado, firma, allowlist, escaneo fuera de banda, estación de transferencia controlada, registro de custodia, doble autorización, cuarentena previa, bloqueo de autorun/LNK e inspección de particiones ocultas.

---

## DFIR, SOC y telemetría

Fuentes obligatorias:

- DNSTAP.
- BGP telemetry.
- SIEM.
- EDR.
- NDR.
- DHCP histórico.
- IAM logs.
- API Gateway logs.
- Model/tool logs.
- DLP.
- Sensores físicos cuando aplique.

Detecciones prioritarias:

- QNAME de alta entropía.
- TXT anómalos.
- DoH externo.
- Cambios inesperados de resolvedor.
- Rutas BGP no autorizadas.
- Cambios de ROA/ROV.
- USB no autorizado.
- Procesos accediendo a checkpoints.
- Copias masivas de pesos.
- Acceso inusual a llaves.
- Tool-calls fuera de política.
- Inferencias con extracción de datos.
- Actividad fuera de ventana operativa.

---

## Directivas finales MIL Layer

**Directiva 001 — Integridad absoluta**  
Todo dato autoritativo, zona DNS, transferencia, dataset, checkpoint, modelo y ruta crítica debe ser validado mediante firma, digest, control de origen y trazabilidad.

**Directiva 002 — Resiliencia determinista**  
La red debe sobrevivir a fallos de ISP, router, ruta, proveedor y ataque de enrutamiento mediante BGP multihomed, RPKI/ROV y política verificable.

**Directiva 003 — DNS como control de seguridad**  
El DNS corporativo será punto de aplicación de políticas. Todo DNS externo no autorizado queda prohibido.

**Directiva 004 — Zero Trust real**  
Ningún sistema de IA será confiable por ubicación, red o aislamiento. Todo acceso requiere identidad, contexto, autorización y monitoreo.

**Directiva 005 — Air-gap gestionado**  
El aislamiento físico no es una garantía; es una capa. Debe acompañarse de control de medios, cadena de suministro, monitoreo y auditoría.

**Directiva 006 — Vigilancia multidimensional**  
La defensa debe cubrir software, red, DNS, rutas, modelos, prompts, herramientas, medios físicos y emisiones no intencionadas.

**Directiva 007 — IA como activo estratégico**  
Los pesos del modelo, datasets, prompts internos, herramientas y checkpoints tienen valor equivalente a propiedad intelectual crítica.

---

## Nota de autoría

Este documento fue estructurado bajo la dirección conceptual y técnica de **Miguel Garay Gracia**, como parte del marco de análisis **CGR-OS / MIL Layer**, orientado a la defensa en profundidad de infraestructuras críticas de Inteligencia Artificial.

La arquitectura aquí presentada integra criterios de resiliencia BGP, DNS seguro, Zero Trust, separación Red-Black, mitigación de canales encubiertos, telemetría forense y protección de activos estratégicos de IA, incluyendo pesos de modelos, datasets sensibles, inferencias, pipelines y sistemas aislados.

---

## Firma técnica

**Miguel Garay Gracia**  
Ingeniero Informático  
Arquitecto conceptual de **CGR-OS / MIL Layer**  
Antigua Orden Dominicana  
www.eldominicanoespanol.com

---

## Frase doctrinal final

**No se protege una IA crítica conectándola a una red. Se la admite dentro de una arquitectura verificable, donde cada ruta, nombre, paquete, identidad, modelo, dato y señal física tiene una política, una evidencia y un responsable.**
