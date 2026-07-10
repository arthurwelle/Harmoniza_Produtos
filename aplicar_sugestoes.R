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
SUGESTOES_CSV <- "<PREENCHER: export CSV da planilha de respostas do Form Sugestões>"
EXECUCOES_CSV <- "<PREENCHER: export CSV da planilha de respostas do Form Execuções>"

OUT_XLSX <- "HarmonizacaoProdutos_novo.xlsx"

# ------------------------------------------------------------------ helpers
baixar <- function(url, destfile, mode = "wb") {
  download.file(url, destfile, mode = mode, quiet = TRUE)
  destfile
}

# parse do timestamp do Google Forms (coluna "Carimbo de data/hora"), tenta formatos
parse_ts <- function(x) {
  x <- as.character(x)
  out <- suppressWarnings(parse_date_time(
    x, orders = c("Y-m-d H:M:S","d/m/Y H:M:S","m/d/Y H:M:S","Y-m-dTH:M:S"),
    tz = "America/Sao_Paulo", quiet = TRUE))
  out
}

# gera próximo cod_final livre dentro de um prefixo N1N2 (ex. "091" -> 09199 livre)
proximo_cod <- function(final_df, n1, n2) {
  # deduz prefixo dos códigos já existentes no mesmo (n1,n2)
  irmaos <- final_df$Codigo_final[final_df$Nivel1 == n1 & final_df$Nivel2 == n2]
  irmaos <- irmaos[!is.na(irmaos)]
  if (length(irmaos)) {
    prefixo <- substr(irmaos[1], 1, 3)             # NN + N
    nums <- as.integer(substr(irmaos, 4, 5))
    novo <- sprintf("%s%02d", prefixo, max(nums, na.rm = TRUE) + 1L)
  } else {
    stop("Sem folhas irmãs em N1=", n1, " N2=", n2, " — informe um código base manualmente.")
  }
  novo
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
tj_df$Cod_harmo <- as.character(tj_df$Cod_harmo)
tj_df$Codigo    <- as.character(tj_df$Codigo)
tj_df$Ano       <- as.character(tj_df$Ano)

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
log <- character(0)
for (i in seq_len(nrow(novas))) {
  r <- novas[i, ]
  acao  <- tolower(trimws(r[[c_acao]]))
  itens <- tryCatch(fromJSON(r[[c_itens]], simplifyVector = FALSE), error = function(e) NULL)

  match_linhas <- function(itens) {
    # itens: lista de [ano, codigo]
    idx <- rep(FALSE, nrow(tj_df))
    for (it in itens) {
      ano <- as.character(it[[1]]); cod <- as.character(it[[2]])
      idx <- idx | (tj_df$Ano == ano & tj_df$Codigo == cod)
    }
    idx
  }

  if (acao == "mover") {
    idx <- match_linhas(itens)
    tj_df$Cod_harmo[idx] <<- as.character(r[[c_alvo]])
    log <- c(log, sprintf("[mover] %d linhas -> %s", sum(idx), r[[c_alvo]]))

  } else if (acao == "criar") {
    novo <- proximo_cod(final_df, r[[c_n1]], r[[c_n2]])
    final_df <- bind_rows(final_df, tibble(
      Nivel1 = r[[c_n1]], Nivel2 = r[[c_n2]],
      Descrição = r[[c_nome]], Codigo_final = novo))
    idx <- match_linhas(itens)
    tj_df$Cod_harmo[idx] <<- novo
    log <- c(log, sprintf("[criar] %s '%s' <- %d linhas", novo, r[[c_nome]], sum(idx)))

  } else if (acao == "renomear") {
    alvo <- as.character(r[[c_alvo]])
    final_df$Descrição[final_df$Codigo_final == alvo] <- r[[c_nome]]
    log <- c(log, sprintf("[renomear] %s -> '%s'", alvo, r[[c_nome]]))

  } else if (acao == "fundir") {
    # funde a(s) folha(s) dos itens NA folha alvo: reaponta Cod_harmo e remove folhas vazias
    idx <- match_linhas(itens)
    origem <- unique(tj_df$Cod_harmo[idx])
    tj_df$Cod_harmo[idx] <<- as.character(r[[c_alvo]])
    vazias <- setdiff(origem, unique(tj_df$Cod_harmo))
    final_df <- final_df[!final_df$Codigo_final %in% vazias, ]
    log <- c(log, sprintf("[fundir] %d linhas -> %s (removidas: %s)",
                          sum(idx), r[[c_alvo]], paste(vazias, collapse = ",")))

  } else if (acao == "dividir") {
    # cria nova folha (nome/n1/n2 informados) e move os itens selecionados p/ ela
    novo <- proximo_cod(final_df, r[[c_n1]], r[[c_n2]])
    final_df <- bind_rows(final_df, tibble(
      Nivel1 = r[[c_n1]], Nivel2 = r[[c_n2]],
      Descrição = r[[c_nome]], Codigo_final = novo))
    idx <- match_linhas(itens)
    tj_df$Cod_harmo[idx] <<- novo
    log <- c(log, sprintf("[dividir] %s '%s' <- %d linhas", novo, r[[c_nome]], sum(idx)))

  } else {
    log <- c(log, sprintf("[ignorado] ação desconhecida: %s", acao))
  }
}

# ------------------------------------------------------------------ 5) grava
message("Gravando ", OUT_XLSX, " …")
wb <- loadWorkbook(tmp_xlsx)                 # preserva as demais abas
writeData(wb, "FINAL", final_df)             # sobrescreve com o df atualizado
writeData(wb, "TodosJuntos", tj_df)
saveWorkbook(wb, OUT_XLSX, overwrite = TRUE)

cat("\n===== RESUMO =====\n"); cat(log, sep = "\n"); cat("\n")
cat("Gerado:", OUT_XLSX, "\n")
cat("PRÓXIMO PASSO: conferir, subir ao Drive (Gerenciar versões, mesmo ID),\n")
cat("               e clicar 'Registrei execução' no site (t_leitura =", format(t_leitura), ").\n")
