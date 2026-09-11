# Ondas: tipos, escolha e tamanho

Onda = unidade de trabalho com escopo, propostas, decisões humanas e relatório. Uma onda = uma branch = um PR.

## Tipos

| Tipo | Olha para | Típico | Gatilho |
|---|---|---|---|
| `base` | tudo | importar planilha | só uma vez |
| `familia` | 1–5 grupos vizinhos e suas células nos 5 anos | MOVER, MANTER, ausência estrutural | alerta de cobertura, balde suspeito |
| `pendencia` | células citadas por pendências (Form, Melhorias, NOTAS) | MOVER, REVISAR | pendência aberta |
| `balde` | 1 mega-balde (ex. 9109, 9201, 32003) | DIVIDIR respeitando R1/R3 | balde com >500 itens |
| `global` | todos os grupos, sem células | UNIR/RENOMEAR, regras gerais, contradições entre famílias | a cada ~3 ondas locais |
| `taxonomia` | níveis/nomes/códigos | RENOMEAR, conversão não-alimentos p/ NN S LL | decisão de grupo |

Ondas locais aprofundam; ondas globais evitam que 50 decisões locais produzam taxonomia incoerente
(mesma distinção aceita numa família e recusada noutra, regra que deveria generalizar, nomes inconsistentes).

## Fila de prioridade para sugerir a próxima onda

1. ERRO do `hp_validar.py` (sempre primeiro; bloqueia PR).
2. Pendências de origem `Form`/`Melhorias`/`humano` abertas há mais tempo.
3. Grupos com vazio não justificado (A01), agrupados por nível 1 (resolver família inteira).
4. Mega-baldes (ver `hp_cobertura.py --medida itens`).
5. Nomes/níveis ruins (nomes-lista das folhas de alimentos).
6. Contador: se as últimas 3 ondas mescladas foram locais ⇒ sugerir `global`.

Excluir escopos que já estão em branch `onda/*` remota aberta (`hp_onda.py abrir` avisa).
Apresentar ao humano 2–3 candidatas com o porquê de cada; a escolha e o motivo vão para `plano.md`.

## Tamanho

- Alvo: ≤ 40 propostas e ≤ ~300 células por onda. Maior ⇒ quebrar.
- Ondas `balde` podem ter muitas células mas poucas propostas (DIVIDIR por subconjunto).
- Onda que não termina no dia deve ficar pushada (reserva o escopo para o grupo).

## Célula heterogênea: calcular a cadeia da R1

Onda cujo escopo tenha célula com itens de conceitos diferentes (o IBGE junta serviços distintos num código de
5 dígitos) exige `hp_particao.py` antes das propostas: escrever `conceitos_regras.csv` na pasta da onda, rodar
por quadro, ler componentes/ligações/células-ponte e simular cada exceção (`--simular`) para medir o efeito.
Sem isso a cadeia passa despercebida: no quadro 42, quatro junções de 2002 uniriam 140 células de 6 grupos.

## Onda global: roteiro

1. `hp_onda.py consolidar` e ler `decisoes_todas.csv` + `regras.csv` inteiros.
2. Procurar: regras aplicadas numa família e ignoradas noutra análoga; UNIR/DIVIDIR incoerentes entre
   famílias irmãs (mesmo nível 1); ausências estruturais com justificativas contraditórias;
   MANTER com confiança BAIXA acumulados; nomes que não descrevem membros.
3. Propor: regras gerais (`REGRA`), revogações explícitas (`revoga`), RENOMEAR, abrir pendências para
   ondas locais onde a correção exige olhar células.
