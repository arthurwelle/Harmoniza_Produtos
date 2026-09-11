# Partição R1 — quadros ['42'] · grupos todos

264 células · 55 conceitos · 26 componentes · 0 células com `excecao_r1`

## Itens sem regra de conceito (1) — completar `conceitos_regras.csv`

- `ultrasonografia`

## Componentes (menores grupos compatíveis com a R1)

| comp | células | 1987 1995 2002 2008 2017 | grupos atuais | conceitos (itens) |  |
|---|---|---|---|---|---|
| C01 | 140 | 10 13 27 20 70 | 36004 Consulta medica (59), 36008 Exames diversos (52), 36005 Tratamento ambulat (18), 36006 Servicos de cirurg (4), 36010 Outras assistencia (4), 36009 Material de tratam (3) | exames (114), consulta_medica (99), cirurgia (22), exame_ginecologico (12) | **VIOLA R1** |
| C02 | 13 | 1 3 3 2 4 | 36009 Material de tratam (9), 36010 Outras assistencia (3), 36005 Tratamento ambulat (1) | oculos_lentes (21) | **VIOLA R1** |
| C03 | 11 | 1 2 2 1 5 | 36009 Material de tratam (10), 36010 Outras assistencia (1) | artigos_ortopedicos (53), aparelho_auditivo (8), lente_intraocular (7), dental_get (4) | **VIOLA R1** |
| C04 | 11 | 2 2 3 2 2 | 36003 Consulta e tratame (10), 36004 Consulta medica (1) | odontologia (50) | **VIOLA R1** |
| C05 | 10 | 2 3 3 1 1 | 36010 Outras assistencia (10) | aluguel_conserto_aparelho (22), oxigenio (7) |  |
| C06 | 8 | 1 2 1 2 2 | 36002 Plano Seguro saude (8) | plano_saude (20) |  |
| C07 | 7 | 2 2 1 1 1 | 36010 Outras assistencia (7) | agregado (7) |  |
| C08 | 7 | 1 1 1 2 2 | 36005 Tratamento ambulat (7) | ambulatorial (20), vacinacao (4) |  |
| C09 | 6 | 0 1 1 2 2 | 36002 Plano Seguro saude (6) | plano_odonto (15) |  |
| C10 | 5 | 1 1 1 1 1 | 36010 Outras assistencia (5) | acompanhante (6) |  |
| C11 | 5 | 1 1 1 1 1 | 36010 Outras assistencia (4), 36005 Tratamento ambulat (1) | ambulancia (7) | **VIOLA R1** |
| C12 | 5 | 1 1 1 1 1 | 36010 Outras assistencia (4), 36005 Tratamento ambulat (1) | curandeiro_parteira (13) | **VIOLA R1** |
| C13 | 5 | 1 1 1 1 1 | 36010 Outras assistencia (3), 36005 Tratamento ambulat (2) | hemoterapia (6) | **VIOLA R1** |
| C14 | 5 | 1 1 1 1 1 | 36007 Hospitalizacao (5) | hospitalizacao (17) |  |
| C15 | 4 | 0 1 1 1 1 | 36002 Plano Seguro saude (3), 36010 Outras assistencia (1) | mensalidade_clinica (4) | **VIOLA R1** |
| C16 | 3 | 0 0 0 2 1 | 36010 Outras assistencia (3) | clinica_residencial (3) |  |
| C17 | 3 | 0 0 1 1 1 | 36005 Tratamento ambulat (2), 36008 Exames diversos (1) | dialise (4) | **VIOLA R1** |
| C18 | 3 | 0 0 1 1 1 | 36005 Tratamento ambulat (2), 36004 Consulta medica (1) | fonoaudiologia (5) | **VIOLA R1** |
| C19 | 3 | 0 0 1 1 1 | 36005 Tratamento ambulat (3) | quimioterapia (5) |  |
| C20 | 2 | 0 0 0 1 1 | 36010 Outras assistencia (2) | clinica_psiquiatrica (2) |  |
| C21 | 2 | 0 0 0 1 1 | 36010 Outras assistencia (2) | home_care (2) |  |
| C22 | 2 | 0 0 0 1 1 | 36005 Tratamento ambulat (2) | podologo (2) |  |
| C23 | 1 | 0 0 0 0 1 | 36008 Exames diversos (1) | fertilizacao (1) |  |
| C24 | 1 | 0 0 0 1 0 | 36005 Tratamento ambulat (1) | nutricao_enteral (1) |  |
| C25 | 1 | 0 0 0 0 1 | 36004 Consulta medica (1) | plano_descontos (2) |  |
| C26 | 1 | 0 0 0 0 1 | 36005 Tratamento ambulat (1) | radioterapia (1) |  |


## C01: células em 6 grupos — pontes candidatas a exceção

| célula | grupo | conceitos | partes sem ela | grupos por parte | itens |
|---|---|---|---|---|---|
| 2002:42046 | 36004 | consulta_medica (14), nutricionista (1) | 2 | {36004,36008} ⟂ {36004,36005,36006,36009,36010} | CONSULTA MEDICA (ALERGISTA) / CONSULTA MEDICA GASTROENTEROLOGICA / CONSULTA MEDICA GERAL / CONSULTA MEDICA GERIATRICA / CONSULTA MEDICA HOMEOPATICA / CONSULTA M |
| 2008:42005 | 36006 | cirurgia (6), laser (2), implante_cabelo (2), fotografia_cirurgia (1), instrumentador (1) | 2 | {36004,36005,36006,36008,36010} ⟂ {36009} | ANESTESISTA PARA CIRURGIA E PARTO / APLICACAO DE RAIO LASER / CIRURGIA (QUALQUER TIPO) / CIRURGIAO PARA OPERACAO E PARTO / FOTOGRAFIA RELATIVA A CIRURGIA / IMPL |
| 1987:4215 | 36005 | acupuntura (2), psicologo (2), nutricionista (1), massagem (1), enfermagem (1), fisioterapia (1) | 3 | {36004,36005,36006,36008,36009,36010} ⟂ {36004,36005} ⟂ {36004,36005} | ACUPUNTURA (TRATAMENTO) / OUTROS TRATAMENTOS (PSICOLOGICO, FISIOTERAPICO, MASSAGEM, ETC.) / TRATAMENTO COM ACUPUNTURA / TRATAMENTO COM DIETISTA / TRATAMENTO COM |
| 2002:42008 | 36008 | exames (8), exame_ginecologico (3), exame_oftalmologico (1) | 2 | {36004,36005,36006,36008,36009,36010} ⟂ {36008} | BIOPSIA (EM GERAL) / EXAME DE BACILO / EXAME DE FEZES / EXAME DE LABORATORIO / EXAME DE SANGUE / EXAME DE URINA / EXAME GINECOLOGICO / EXAME OFTALMOLOGICO / EXA |
| 2017:42043 | 36004 | exame_orl (2), consulta_medica (1) | 2 | {36004,36005,36006,36008,36009,36010} ⟂ {36004} | CONSULTA MEDICA COM OTORRINOLARINGOLOGISTA / EXAME DE NASOFIBROSCOPIA / EXAME DE VIDEOLARINGOSCOPIA |

Células que ligam conceitos:

| célula | grupo | conceitos |
|---|---|---|
| 1987:4207 | 36008 | exames (7), ?ultrasonografia (1) |
| 1987:4215 | 36005 | acupuntura (2), psicologo (2), nutricionista (1), massagem (1) |
| 1987:4221 | 36008 | pressao_arterial (2), exames (1) |
| 2002:42007 | 36008 | exames (13), ?ultrasonografia (1) |
| 2002:42008 | 36008 | exames (8), exame_ginecologico (3), exame_oftalmologico (1) |
| 2002:42015 | 36005 | acupuntura (2), hidroterapia (2), implante_cabelo (2), outros_tratamentos (1) |
| 2002:42016 | 36010 | enfermagem (1), instrumentador (1) |
| 2002:42021 | 36008 | pressao_arterial (2), pesagem (2), exames (1) |
| 2002:42046 | 36004 | consulta_medica (14), nutricionista (1) |
| 2008:42005 | 36006 | cirurgia (6), laser (2), implante_cabelo (2), fotografia_cirurgia (1) |
| 2008:42011 | 36004 | exame_ginecologico (4), consulta_medica (3) |
| 2008:42033 | 36005 | hidroterapia (2), massagem (2) |
| 2008:42043 | 36008 | pressao_arterial (2), pesagem (2), exames (1) |
| 2017:42008 | 36004 | consulta_medica (2), exame_ginecologico (2) |
| 2017:42010 | 36004 | consulta_medica (1), exame_oftalmologico (1) |
| 2017:42026 | 36005 | cirurgia (5), laser (2), instrumentador (1) |
| 2017:42043 | 36004 | exame_orl (2), consulta_medica (1) |
| 2017:42048 | 36004 | consulta_medica (1), exame_prostata (1) |


## C02: células em 3 grupos — pontes candidatas a exceção

_nenhuma célula isolada desfaz a junção; seria preciso excetuar mais de uma_

Células que ligam conceitos:

| célula | grupo | conceitos |
|---|---|---|


## C03: células em 2 grupos — pontes candidatas a exceção

| célula | grupo | conceitos | partes sem ela | grupos por parte | itens |
|---|---|---|---|---|---|
| 2008:42041 | 36009 | artigos_ortopedicos (16), aparelho_auditivo (2), lente_intraocular (2) | 2 | {36009,36010} ⟂ {36009} | APARELHO DE SURDEZ / ARTIGOS ORTOPEDICOS E OUTROS / ARTIGOS ORTOPEDICOS E PROTESES DIVERSAS / BOTA ORTOPEDICA / CADEIRA DE RODAS / CAMA HOSPITALAR / CARRINHO PA |

Células que ligam conceitos:

| célula | grupo | conceitos |
|---|---|---|
| 1987:4212 | 36009 | artigos_ortopedicos (10), dental_get (2), aparelho_auditivo (2), equip_massagem (1) |
| 2002:42012 | 36009 | artigos_ortopedicos (14), aparelho_auditivo (2), dental_get (2), glicosimetro (1) |
| 2008:42041 | 36009 | artigos_ortopedicos (16), aparelho_auditivo (2), lente_intraocular (2) |


## C04: células em 2 grupos — pontes candidatas a exceção

_nenhuma célula isolada desfaz a junção; seria preciso excetuar mais de uma_

Células que ligam conceitos:

| célula | grupo | conceitos |
|---|---|---|


## C11: células em 2 grupos — pontes candidatas a exceção

_nenhuma célula isolada desfaz a junção; seria preciso excetuar mais de uma_

Células que ligam conceitos:

| célula | grupo | conceitos |
|---|---|---|


## C12: células em 2 grupos — pontes candidatas a exceção

_nenhuma célula isolada desfaz a junção; seria preciso excetuar mais de uma_

Células que ligam conceitos:

| célula | grupo | conceitos |
|---|---|---|


## C13: células em 2 grupos — pontes candidatas a exceção

_nenhuma célula isolada desfaz a junção; seria preciso excetuar mais de uma_

Células que ligam conceitos:

| célula | grupo | conceitos |
|---|---|---|


## C15: células em 2 grupos — pontes candidatas a exceção

_nenhuma célula isolada desfaz a junção; seria preciso excetuar mais de uma_

Células que ligam conceitos:

| célula | grupo | conceitos |
|---|---|---|


## C17: células em 2 grupos — pontes candidatas a exceção

_nenhuma célula isolada desfaz a junção; seria preciso excetuar mais de uma_

Células que ligam conceitos:

| célula | grupo | conceitos |
|---|---|---|


## C18: células em 2 grupos — pontes candidatas a exceção

_nenhuma célula isolada desfaz a junção; seria preciso excetuar mais de uma_

Células que ligam conceitos:

| célula | grupo | conceitos |
|---|---|---|

## Grupos atuais com mais de um componente (divisão possível se R3 permitir)

| grupo | nome | componentes (células) |
|---|---|---|
| 36002 | Plano Seguro saude | C06 (8), C09 (6), C15 (3) |
| 36004 | Consulta medica | C01 (59), C04 (1), C18 (1), C25 (1) |
| 36005 | Tratamento ambulatorial | C01 (18), C08 (7), C19 (3), C17 (2), C18 (2), C13 (2), C22 (2), C24 (1), C11 (1), C12 (1), C02 (1), C26 (1) |
| 36008 | Exames diversos | C01 (52), C17 (1), C23 (1) |
| 36009 | Material de tratamento | C03 (10), C02 (9), C01 (3) |
| 36010 | Outras assistencia saude | C05 (10), C07 (7), C10 (5), C12 (4), C01 (4), C11 (4), C13 (3), C16 (3), C02 (3), C21 (2), C20 (2), C03 (1), C15 (1) |
