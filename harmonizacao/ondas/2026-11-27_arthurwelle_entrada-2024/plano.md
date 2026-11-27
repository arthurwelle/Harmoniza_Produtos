# Plano — 2026-11-27_arthurwelle_entrada-2024

## Por que esta onda agora
A primeira divulgação dos microdados da POF 2024-2025 saiu em novembro de 2026. O pipeline de `POF2024/` (scripts 1-4)
já reproduz os totais do IBGE. Falta o `Cod_harmo` para pôr 2024 na mesma série de 1987-2017.

## Motivo humano
Arthur (2026-11-27): avaliar se dá para copiar os códigos harmonizados de 2017 para 2024 e fazer a harmonização; depois,
"acato a proposta ... leve para a harmonização, rode, faça upload na ferramenta".

## Método
Ver `fonte/2024/plano_original.md` e `fonte/2024/relatorio_original.md`. Em resumo:
- célula 2024 = código de 6 dígitos (ADR 0011);
- casamento com 2017 pela descrição (exata ou aproximada), restrito ao quadro equivalente (mapa derivado dos dados) e
  conferido com o nível do tradutor do IBGE;
- as células sem correspondência clara foram decididas uma a uma ou por regra explícita (passo 4).
