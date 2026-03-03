# 📡 Last30Days — Contexto Brain OS

## Casos de Uso Académicos

Esta skill investiga cualquier tema en Reddit + X + Web de los **últimos 30 días**. En Brain OS, se usa principalmente para trabajos que requieren contexto de actualidad.

### Por materia

| Materia | Uso típico |
|---------|-----------|
| Economía Internacional | `"last30days: aranceles Trump proteccionismo 2026"` |
| Economía Ambiental | `"last30days: COP30 política climática Perú"` |
| Macroeconomía | `"last30days: política monetaria BCRP inflación"` |
| Microeconomía | `"last30days: regulación antimonopolio tech"` |
| Economía Pública | `"last30days: reforma tributaria Perú"` |

## Modo de Operación (sin API keys)

Brain OS funciona en modo **Web-Only** por defecto (sin OPENAI_API_KEY ni XAI_API_KEY):

```
✅ Fuentes: blogs, tutoriales, noticias, papers, GitHub
❌ Sin métricas de Reddit (upvotes) ni X (likes)
```

Esto es suficiente para trabajos académicos: los journals y news son más relevantes que Reddit para economía.

## Flujo de trabajo recomendado en Brain OS

```
1. last30days → [tema académico]    # Obtener panorama actual
2. research-engineer → [tema]       # Rigor académico + fuentes primarias
3. doc-coauthoring → [documento]    # Redactar el trabajo con ambas fuentes
4. docx-official / pptx-official    # Generar el archivo final
```

## Limitación importante

> ⚠️ Esta skill requiere acceso a internet en tiempo real. No funciona offline. Usar solo cuando se necesite información de las últimas 4 semanas.

Para temas atemporales o históricos, `research-engineer` es más apropiado y riguroso.

## Complementa

- `research-engineer` → rigor académico posterior a la investigación de actualidad
- `doc-coauthoring` → estructura el documento con los hallazgos
- `prompt-library` → guardar los mejores prompts de investigación por materia
