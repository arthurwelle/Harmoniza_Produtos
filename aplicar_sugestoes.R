# =============================================================================
# aplicar_sugestoes.R
# Aplica as sugestões de recategorização (enviadas pelo site) ao xlsx mestre.
#
# Fluxo:
#   1. Baixa o xlsx atual do Drive (abas FINAL e TodosJuntos).
#   2. Lê as respostas do Form Sugestões (CSV público) e do Form Execuções (CSV).
#   3. Corte = maior timestamp de Execuções. Aplica só sugestões posteriores ao corte
#      e anteriores ao instante de leitura (t_leitura).
#   4. Aplica: mover / criar / renomear / fundir / dividir.
#   5. Grava HarmonizacaoProdutos_novo.xlsx.  (NÃO sobe ao Drive — fazer manual)
#   6. Depois de conferir e subir ao Drive, clicar "Registrei execução" no site
#      (registra t_leitura como novo corte).
#
# Dependências: readxl, openxlsx, jsonlite, dplyr, lubridate
#   install.packages(c("readxl","openxlsx","jsonlite","dplyr","lubridate"))
# =============================================================================

suppressMessages({
  library(readxl); library(openxlsx); library(jsonlite)
  library(dplyr);  library(lubridate)
})

# ------------------------------------------------------------------ CONFIG
DRIVE_XLSX <- "https://docs.google.com/spreadsheets/d/1keMjsrEDLgCWheWCSjgXRoLPwYA8x1-a/export?format=xlsx"

# URLs de export CSV das planilhas de respostas dos 2 Forms.
# COMO OBTER: abra a planilha de respostas do Form -> Arquivo > Compartilhar
# ("qualquer um com o link", Leitor) -> copie o ID da URL
# (docs.google.com/spreadsheets/d/<ID>/...) e monte:
#   https://docs.google.com/spreadsheets/d/<ID>/export?format=csv
SUGESTOES_CSV <- "https://docs.google.com/spreadsheets/d/1JDqb5SYAwx3oB4rfB3hVBRKxrWwNtb1tCkBGYddRE10/export?format=csv"
EXECUCOES_CSV <- "https://docs.google.com/spreadsheets/d/11FhuDDvhE33E7E-c_qsdmAD7AeCGkMo8duxG2My4WnE/export?format=csv"

OUT_XLSX <- "HarmonizacaoProdutos_novo.xlsx"

# ------------------------------------------------------------------ helpers
baixar <- function(url, destfile, mode = "wb") {
  download.file(url, destfile, mode = mode, quiet = TRUE)
  destfile
}

# parse do timestamp do Google Forms (coluna "Carimbo de data/hora"), tenta formatos
parse_ts <- function(x) {
  # Carimbo do Google Forms (locale pt-BR) = "DD/MM/YYYY HH:MM:SS".
  # Um formato por vez p/ evitar bug de regex do parse_date_time com muitos orders.
  x <- as.character(x)
  out <- suppressWarnings(parse_date_time(x, "d/m/Y H:M:S",
                                          tz = "America/Sao_Paulo", quiet = TRUE))
  if (any(is.na(out)))
    out[is.na(out)] <- suppressWarnings(parse_date_time(
      x[is.na(out)], "Y-m-d H:M:S", tz = "America/Sao_Paulo", quiet = TRUE))
  out
}

match_n2 <- function(col, val) {
  val <- trimws(as.character(val))
  colt <- trimws(col)
  ex <- which(colt == val)
  if (length(ex)) return(ex)                       # match exato (dropdown do site)
  # prefixo só vale se o restante começa por espaço (ex. "1.2" casa "1.2 Leguminosas",
  # mas "1" NÃO casa "1.1 Cereais" — evita ambiguidade entre subníveis).
  hit <- which(startsWith(colt, paste0(val, " ")))
  n2s <- unique(colt[hit])
  if (length(n2s) > 1)
    stop("Nível 2 ambíguo: '", val, "' casa ", length(n2s),
         " subcategorias (", paste(n2s, collapse = "; "),
         "). Use o rótulo completo (ex. '1.2 Leguminosas').")
  hit
}

# Retorna list(cod, pos): código 5-díg novo para o N2 e a POSIÇÃO de inserção
# (antes da folha "Outros"=xx99, para manter a ordem por código dentro do N2).
proximo_cod <- function(final_df, n1, n2) {
  i2 <- match_n2(final_df$Nivel2, n2)
  cods <- final_df$Codigo_final[i2]
  ok <- !is.na(cods) & nchar(cods) == 5
  i2  <- i2[ok]; cods <- cods[ok]
  if (!length(cods))
    stop("Não achei folhas irmãs p/ Nível 2='", n2,
         "'. Use o rótulo exato da aba FINAL (ex. '1.1 Cereais').")
  prefixo <- substr(cods[1], 1, 3)                 # NN + N
  nums    <- as.integer(substr(cods, 4, 5))
  # novo número = maior que NÃO seja 99 (Outros), +1
  base <- nums[nums < 99]
  prox <- if (length(base)) max(base) + 1L else 1L
  if (prox >= 99L) stop("N2 '", n2, "' já cheio (chegou ao código 99).")
  novo <- sprintf("%s%02d", prefixo, prox)
  # posição: linha da folha "99" (Outros) desse N2; se não houver, após a última irmã
  is99 <- nums == 99
  pos  <- if (any(is99)) i2[which(is99)[1]] else max(i2) + 1L
  list(cod = novo, pos = pos)
}

# insere a nova folha no data.frame na posição 'pos' (empurra o resto p/ baixo)
inserir_folha <- function(fin, pos, n1, n2, nome, cod_txt) {
  nova <- fin[1, ][NA, ]                       # linha vazia com o mesmo schema
  nova[[1]] <- as.character(n1)                # Nivel1
  nova[[2]] <- as.character(n2)                # Nivel2
  nova[[6]] <- as.character(nome)              # Descrição
  nova[[7]] <- cod_txt                         # 'Codigo final' (coluna real, col7)
  nova$Codigo_final <- cod_txt                 # cópia auxiliar
  nova$cod_int <- as_codeint(cod_txt)
  if (pos <= 1)            rbind(nova, fin)
  else if (pos > nrow(fin)) rbind(fin, nova)
  else rbind(fin[1:(pos - 1), ], nova, fin[pos:nrow(fin), ])
}

# ------------------------------------------------------------------ 1) dados
message("Baixando xlsx do Drive…")
tmp_xlsx <- baixar(DRIVE_XLSX, tempfile(fileext = ".xlsx"))
final_df <- read_excel(tmp_xlsx, sheet = "FINAL")
tj_df    <- read_excel(tmp_xlsx, sheet = "TodosJuntos")

# normaliza nomes de colunas da FINAL que o script usa
# (ajuste os índices/nomes se o cabeçalho real diferir)
names(final_df)[1:2] <- c("Nivel1", "Nivel2")
if (!"Codigo_final" %in% names(final_df)) {
  # 'Codigo final' costuma ser a 7ª coluna
  final_df$Codigo_final <- as.character(final_df[[7]])
}
# força character nas colunas que o script escreve (evita erro de tipo no bind_rows)
final_df$Nivel1      <- as.character(final_df$Nivel1)
final_df$Nivel2      <- as.character(final_df$Nivel2)
final_df$Descrição   <- as.character(final_df$Descrição)
final_df$Codigo_final<- as.character(final_df$Codigo_final)
# Normalização de códigos:
# No xlsx, Cod_harmo vem como "31007.0" (inteiro, zero à esq. perdido) e o
# 'Codigo final' da FINAL como "01101" (5 díg). Comparo tudo por INTEIRO.
as_codeint <- function(x) suppressWarnings(as.integer(round(as.numeric(as.character(x)))))
tj_df$Cod_harmo_int <- as_codeint(tj_df$Cod_harmo)   # chave harmonizada (inteiro)
tj_df$Codigo    <- sub("\\.0$", "", as.character(tj_df$Codigo))  # código original do ano
tj_df$Ano       <- sub("\\.0$", "", as.character(tj_df$Ano))
final_df$cod_int <- as_codeint(final_df$Codigo_final)

# ------------------------------------------------------------------ 2) respostas
message("Lendo sugestões e execuções…")
sug <- read.csv(SUGESTOES_CSV, stringsAsFactors = FALSE, check.names = FALSE)
exe <- read.csv(EXECUCOES_CSV, stringsAsFactors = FALSE, check.names = FALSE)

# 1ª coluna de cada = carimbo de data/hora do Google
sug$ts <- parse_ts(sug[[1]])
exe$ts <- parse_ts(exe[[1]])

t_leitura <- now(tzone = "America/Sao_Paulo")
corte <- if (nrow(exe)) max(exe$ts, na.rm = TRUE) else as.POSIXct("2000-01-01", tz = "America/Sao_Paulo")
message("Corte anterior: ", corte, " | leitura: ", t_leitura)

# ------------------------------------------------------------------ 3) filtro
novas <- sug %>%
  filter(!is.na(ts), ts > corte, ts <= t_leitura) %>%
  arrange(ts)
message(nrow(novas), " sugestões novas a aplicar.")

# mapeia nomes das colunas do form (por título das perguntas)
col <- function(df, nome) {
  hit <- names(df)[tolower(names(df)) == tolower(nome)]
  if (length(hit)) hit[1] else NA_character_
}
c_acao  <- col(novas, "Acao");        c_alvo <- col(novas, "Codigo-alvo")
c_nome  <- col(novas, "Nome novo");   c_n1   <- col(novas, "Nivel 1")
c_n2    <- col(novas, "Nivel 2");     c_itens<- col(novas, "Itens JSON")

# ------------------------------------------------------------------ 4) aplica
match_linhas <- function(tj, itens) {
  idx <- rep(FALSE, nrow(tj))
  for (it in itens) {
    ano <- as.character(it[[1]]); cod <- as.character(it[[2]])
    idx <- idx | (tj$Ano == ano & tj$Codigo == cod)
  }
  idx
}
# aplica UMA sugestão; recebe e devolve list(tj, fin, msg)
aplicar_uma <- function(tj, fin, r) {
  acao  <- tolower(trimws(r[[c_acao]]))
  itens <- tryCatch(fromJSON(r[[c_itens]], simplifyVector = FALSE),
                    error = function(e) NULL)
  msg <- ""
  if (acao == "mover") {
    idx <- match_linhas(tj, itens)
    tj$Cod_harmo_int[idx] <- as_codeint(r[[c_alvo]])
    msg <- sprintf("[mover] %d linhas -> %s", sum(idx), r[[c_alvo]])
  } else if (acao == "criar") {
    nc <- proximo_cod(fin, r[[c_n1]], r[[c_n2]])
    fin <- inserir_folha(fin, nc$pos, r[[c_n1]], r[[c_n2]], r[[c_nome]], nc$cod)
    idx <- match_linhas(tj, itens)
    tj$Cod_harmo_int[idx] <- as_codeint(nc$cod)
    msg <- sprintf("[criar] %s '%s' <- %d linhas", nc$cod, r[[c_nome]], sum(idx))
  } else if (acao == "renomear") {
    alvo <- as_codeint(r[[c_alvo]])
    fin$Descrição[fin$cod_int == alvo] <- as.character(r[[c_nome]])
    msg <- sprintf("[renomear] %s -> '%s'", r[[c_alvo]], r[[c_nome]])
  } else if (acao == "fundir") {
    idx <- match_linhas(tj, itens)
    origem <- unique(tj$Cod_harmo_int[idx])
    tj$Cod_harmo_int[idx] <- as_codeint(r[[c_alvo]])
    vazias <- setdiff(origem, unique(tj$Cod_harmo_int))
    fin <- fin[!fin$cod_int %in% vazias, ]
    msg <- sprintf("[fundir] %d linhas -> %s (folhas removidas: %s)",
                   sum(idx), r[[c_alvo]], paste(vazias, collapse = ","))
  } else if (acao == "dividir") {
    nc <- proximo_cod(fin, r[[c_n1]], r[[c_n2]])
    fin <- inserir_folha(fin, nc$pos, r[[c_n1]], r[[c_n2]], r[[c_nome]], nc$cod)
    idx <- match_linhas(tj, itens)
    tj$Cod_harmo_int[idx] <- as_codeint(nc$cod)
    msg <- sprintf("[dividir] %s '%s' <- %d linhas", nc$cod, r[[c_nome]], sum(idx))
  } else {
    msg <- sprintf("[ignorado] ação desconhecida: %s", acao)
  }
  list(tj = tj, fin = fin, msg = msg)
}

log <- character(0)
for (i in seq_len(nrow(novas))) {
  res <- tryCatch(aplicar_uma(tj_df, final_df, novas[i, ]),
                  error = function(e)
                    list(tj = tj_df, fin = final_df,
                         msg = sprintf("[ERRO sugestão %d] %s", i, conditionMessage(e))))
  tj_df <- res$tj; final_df <- res$fin
  log <- c(log, res$msg)
}

# ------------------------------------------------------------------ 5) grava
message("Gravando ", OUT_XLSX, " …")
# reconstitui Cod_harmo (mesmo formato inteiro do original) e remove auxiliares
tj_df$Cod_harmo <- as.character(tj_df$Cod_harmo_int)
tj_df$Cod_harmo_int <- NULL
final_df$cod_int <- NULL
final_df$Codigo_final <- NULL   # col auxiliar (o original só tem 'Codigo final' col7)
wb <- loadWorkbook(tmp_xlsx)                 # preserva as demais abas
writeData(wb, "FINAL", final_df)             # sobrescreve com o df atualizado
writeData(wb, "TodosJuntos", tj_df)
saveWorkbook(wb, OUT_XLSX, overwrite = TRUE)

cat("\n===== RESUMO =====\n"); cat(log, sep = "\n"); cat("\n")
cat("Gerado:", OUT_XLSX, "\n")
cat("PRÓXIMO PASSO: conferir, subir ao Drive (Gerenciar versões, mesmo ID),\n")
cat("               e clicar 'Registrei execução' no site (t_leitura =", format(t_leitura), ").\n")
